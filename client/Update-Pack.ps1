#requires -Version 5.1
[CmdletBinding()]
param([string]$Profile, [switch]$CheckOnly, [switch]$LibraryOnly)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$script:Repo = 'PuzzleOP/CustomATM'
$script:ClientVersion = 3
$script:Headers = @{ 'User-Agent'='CustomATM-Updater/1'; 'Accept'='application/vnd.github+json' }
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

function Hash-File([string]$Path) {
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Write-Utf8([string]$Path,[string]$Text) {
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Path)) | Out-Null
    [IO.File]::WriteAllText($Path,$Text,(New-Object Text.UTF8Encoding($false)))
}
function Save-Json([string]$Path,$Value) {
    $pending=$Path+'.pending-'+[Guid]::NewGuid().ToString('N')
    try {
        Write-Utf8 $pending ($Value | ConvertTo-Json -Depth 30)
        if ([IO.File]::Exists($Path)) { [IO.File]::Replace($pending,$Path,[NullString]::Value) }
        else { [IO.File]::Move($pending,$Path) }
    } finally { if ([IO.File]::Exists($pending)) { [IO.File]::Delete($pending) } }
}
function Read-Json([string]$Path) { return (Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json) }
function Safe-Path([string]$Root,[string]$Relative) {
    if (!$Relative -or $Relative.Contains('\') -or $Relative.Contains(':') -or $Relative.StartsWith('/') -or $Relative -match '[\x00-\x1f]') { throw "Unsafe path: $Relative" }
    foreach($part in $Relative.Split('/')) {
        if (!$part -or $part -in @('.','..') -or $part -match '[. ]$' -or $part -match '^(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])(\.|$)' -or $part -match '[<>"|?*]') { throw "Unsafe path: $Relative" }
    }
    $rootFull=[IO.Path]::GetFullPath($Root).TrimEnd('\','/')
    $full=[IO.Path]::GetFullPath((Join-Path $rootFull $Relative))
    if (!$full.StartsWith($rootFull+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Path escapes profile.' }
    $walk=$rootFull
    foreach($part in @('') + $Relative.Split('/')) {
        if ($part) { $walk=Join-Path $walk $part }
        if (Test-Path -LiteralPath $walk) {
            if ((Get-Item -LiteralPath $walk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked paths are not supported: $walk" }
        }
    }
    return $full
}
function Assert-ManagedPath([string]$Path) {
    if ($Path -notmatch '^(mods/[^/]+\.jar|config/|defaultconfigs/|kubejs/|resourcepacks/)') { throw "Not a managed pack path: $Path" }
}
function Assert-DownloadUrl([string]$Url) {
    $u=[Uri]$Url
    if ($u.Scheme -ne 'https' -or $u.UserInfo -or !$u.IsDefaultPort) { throw 'Downloads must use ordinary HTTPS URLs.' }
    $allowed=@('cdn.modrinth.com','edge.forgecdn.net','mediafilez.forgecdn.net','media.forgecdn.net','api.github.com','github.com','release-assets.githubusercontent.com')
    if ($u.Host -notin $allowed) { throw "Unapproved download host: $($u.Host)" }
    if ($u.Host -eq 'github.com' -and !$u.AbsolutePath.StartsWith('/'+$script:Repo+'/releases/')) { throw 'Unexpected GitHub download repository.' }
    if ($u.Host -eq 'api.github.com' -and !$u.AbsolutePath.StartsWith('/repos/'+$script:Repo+'/')) { throw 'Unexpected GitHub API repository.' }
}
function Download-File([string]$Url,[string]$Destination,[string]$Hash) {
    Assert-DownloadUrl $Url
    if ($Hash -notmatch '^[0-9a-f]{64}$') { throw 'Missing SHA256.' }
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Destination)) | Out-Null
    Invoke-WebRequest -UseBasicParsing -Uri $Url -OutFile $Destination -Headers @{ 'User-Agent'='CustomATM-Updater/1' } -TimeoutSec 300
    if ((Hash-File $Destination) -ne $Hash) { throw "Download checksum failed: $([IO.Path]::GetFileName($Destination))" }
}
function Assert-Manifest($Manifest,[string]$Root) {
    if ($Manifest.schema -ne 1 -or $Manifest.repository -ne $script:Repo -or $Manifest.client_version -gt $script:ClientVersion) { throw 'Unsupported update format. Download the latest Setup ZIP from the repository releases.' }
    if ($Manifest.version -notmatch '^\d+\.\d+\.\d+$') { throw 'Invalid release version.' }
    if (@($Manifest.files).Count -lt 1) { throw 'Empty pack manifest.' }
    $seen=@{}
    foreach($f in @($Manifest.files)) {
        Assert-ManagedPath $f.path
        $null=Safe-Path $Root $f.path
        if ($seen.ContainsKey($f.path)) { throw "Duplicate update path: $($f.path)" };$seen[$f.path]=$true
        if ($f.sha256 -notmatch '^[0-9a-f]{64}$' -or $f.size -lt 0) { throw "Invalid file metadata: $($f.path)" }
        if ($f.source -eq 'url') { Assert-DownloadUrl $f.url }
        elseif ($f.source -ne 'payload') { throw 'Unknown download type.' }
    }
    foreach($f in @($Manifest.obsolete)) {
        Assert-ManagedPath $f.path;$null=Safe-Path $Root $f.path
        if ($seen.ContainsKey($f.path) -or $f.sha256 -notmatch '^[0-9a-f]{64}$') { throw 'Invalid obsolete file entry.' }
        $seen[$f.path]=$true
    }
    if ($Manifest.quest_group -notmatch '^[0-7][0-9A-F]{15}$') { throw 'Invalid chapter group ID.' }
}
function Assert-Base([string]$Root,$Manifest) {
    $file=Safe-Path $Root 'minecraftinstance.json'
    if (!(Test-Path -LiteralPath $file)) { throw 'Select an existing CurseForge ATM10 8.3 profile folder (the one containing minecraftinstance.json).' }
    $instance=Read-Json $file
    $baseMatch=($instance.projectID -eq 925200 -and $instance.fileID -eq $Manifest.base.curseforge_file_id)
    $receipt=Safe-Path $Root '.customatm/bootstrap.json'
    if (Test-Path -LiteralPath $receipt) {
        $b=Read-Json $receipt
        $baseMatch=($b.repository -eq $script:Repo -and $b.instance_id -eq $instance.guid -and $b.archive_sha256 -eq $script:BaseArchiveHash -and $b.complete -and $b.version -eq $Manifest.base.version)
    }
    if (!$baseMatch -or $instance.gameVersion -ne $Manifest.base.minecraft -or $instance.baseModLoader.name -ne $Manifest.base.loader) {
        throw "This update requires ATM10 $($Manifest.base.version), Minecraft $($Manifest.base.minecraft), $($Manifest.base.loader). Install that exact version with CurseForge first."
    }
}
function Assert-GameClosed {
    # Conservative: prevents changes under an active game, even when its command line is unavailable.
    if (@(Get-Process -Name java,javaw -ErrorAction SilentlyContinue).Count) { throw 'Close Minecraft (and any other Java program) before updating, then try again.' }
}
function Get-Plan([string]$Root,$Manifest,$Previous) {
    $desired=@{};$old=@{};$removed=@{};$plan=New-Object Collections.Generic.List[object]
    foreach($f in @($Manifest.files)) { $desired[$f.path]=$f }
    if ($Previous) {
        if ($Previous.repository -ne $script:Repo) { throw 'Unexpected previous updater state.' }
        foreach($f in @($Previous.files)) { Assert-ManagedPath $f.path;$null=Safe-Path $Root $f.path;$old[$f.path]=$f.sha256 }
    }
    foreach($f in @($Manifest.obsolete)) { $removed[$f.path]=$f.sha256 }
    foreach($path in $old.Keys) { if (!$desired.ContainsKey($path)) { $removed[$path]=$old[$path] } }
    foreach($f in @($Manifest.files)) {
        $dest=Safe-Path $Root $f.path;$actual=Hash-File $dest
        if ($actual -ne $f.sha256) {
            # Mods commonly expand/reformat configs on launch. Preserve those changes when
            # the published config itself has not changed; still pin every mod jar exactly.
            if ($actual -and !$f.path.StartsWith('mods/') -and $old.ContainsKey($f.path) -and $old[$f.path] -eq $f.sha256) { continue }
            if ($actual -and $old.ContainsKey($f.path) -and $actual -ne $old[$f.path]) { throw "Local edits detected in $($f.path). Keep a copy of your edits, then restore the previous published version or ask the pack maintainer to include your change." }
            if ($actual -and !$old.ContainsKey($f.path) -and $f.path.StartsWith('mods/')) { throw "Unexpected contents in $($f.path). Repair that mod through CurseForge before updating." }
            $plan.Add([pscustomobject]@{path=$f.path;oldHash=$actual;newHash=$f.sha256;action='write';source=$f})
        }
    }
    foreach($path in $removed.Keys) {
        $actual=Hash-File (Safe-Path $Root $path)
        if ($actual) {
            if ($actual -ne $removed[$path]) { throw "Refusing to remove modified file: $path" }
            $plan.Add([pscustomobject]@{path=$path;oldHash=$actual;newHash=$null;action='remove';source=$null})
        }
    }
    foreach($jar in @(if(Test-Path -LiteralPath (Join-Path $Root 'mods')) { Get-ChildItem -LiteralPath (Join-Path $Root 'mods') -File -Filter '*.jar' })) {
        $rel='mods/'+$jar.Name
        if (!$desired.ContainsKey($rel) -and !$removed.ContainsKey($rel)) { throw "Extra mod found: $($jar.Name). Move it outside mods before syncing so both players have the same pack." }
    }
    return $plan.ToArray()
}
function Stage-Files([string]$Root,[string]$Stage,$Plan,[string]$Payload) {
    $zip=$null
    try {
        if ($Payload) {
            $zip=[IO.Compression.ZipFile]::OpenRead($Payload)
            $names=@{}
            foreach($e in $zip.Entries) {
                if ($e.FullName.EndsWith('/')) { continue }
                $null=Safe-Path $Stage $e.FullName
                if ($names.ContainsKey($e.FullName)) { throw 'Duplicate payload entry.' };$names[$e.FullName]=$true
            }
        }
        foreach($item in @($Plan)) {
            if ($item.action -ne 'write') { continue }
            $dest=Safe-Path $Stage $item.path
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest)) | Out-Null
            if ($item.source.source -eq 'url') {
                $reused=$false
                foreach($cacheRoot in @($script:ReuseProfiles)) {
                    if (!$cacheRoot) {continue}
                    $cached=Safe-Path $cacheRoot $item.path
                    if ((Hash-File $cached) -eq $item.newHash) { [IO.File]::Copy($cached,$dest,$true);$reused=$true;break }
                }
                if (!$reused) { Write-Host ('Downloading '+[IO.Path]::GetFileName($item.path));Download-File $item.source.url $dest $item.newHash }
            }
            else {
                if (!$zip) { throw 'Missing payload archive.' }
                $entry=$zip.GetEntry($item.path)
                if (!$entry -or $entry.Length -ne $item.source.size) { throw "Missing/wrong-sized payload file: $($item.path)" }
                [IO.Compression.ZipFileExtensions]::ExtractToFile($entry,$dest,$true)
            }
            if ((Hash-File $dest) -ne $item.newHash -or (Get-Item -LiteralPath $dest).Length -ne $item.source.size) { throw "Staged file validation failed: $($item.path)" }
        }
    } finally { if ($zip) { $zip.Dispose() } }
}
function Atomic-Copy([string]$Source,[string]$Destination) {
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Destination)) | Out-Null
    $temporary=$Destination+'.customatm-tmp'
    if (Test-Path -LiteralPath $temporary) { throw "Temporary update file already exists: $temporary" }
    try {
        [IO.File]::Copy($Source,$temporary,$false)
        if ([IO.File]::Exists($Destination)) { [IO.File]::Replace($temporary,$Destination,[NullString]::Value) }
        else { [IO.File]::Move($temporary,$Destination) }
    } finally { if ([IO.File]::Exists($temporary)) { [IO.File]::Delete($temporary) } }
}
function Restore-Transaction([string]$Root,[string]$Txn) {
    $j=Read-Json (Join-Path $Txn 'journal.json')
    foreach($entry in @($j.entries)) {
        $dest=Safe-Path $Root $entry.path;$current=Hash-File $dest
        if ($current -and $current -ne $entry.newHash -and $current -ne $entry.oldHash) { throw "Recovery stopped: $($entry.path) changed outside the updater. Backup: $Txn" }
        $stale=Safe-Path $Root ($entry.path+'.customatm-tmp')
        if ([IO.File]::Exists($stale)) { [IO.File]::Delete($stale) }
        if ($entry.oldHash) {
            $backup=Safe-Path (Join-Path $Txn 'backup') $entry.path
            if ((Hash-File $backup) -ne $entry.oldHash) { throw "Recovery backup failed verification: $($entry.path)" }
            Atomic-Copy $backup $dest
        } elseif ($current) { [IO.File]::Delete($dest) }
    }
    $j.status='rolled-back';Save-Json (Join-Path $Txn 'journal.json') $j
}
function Recover-Pending([string]$Root) {
    $dir=Safe-Path $Root '.customatm/transactions'
    if (Test-Path -LiteralPath $dir) {
        foreach($folder in Get-ChildItem -LiteralPath $dir -Directory) {
            $jp=Join-Path $folder.FullName 'journal.json'
            if ((Test-Path -LiteralPath $jp) -and (Read-Json $jp).status -eq 'applying') {
                Write-Host 'Recovering an interrupted update...';Restore-Transaction $Root $folder.FullName
            }
        }
    }
}
function Apply-Transaction([string]$Root,[string]$Txn,[string]$Stage,$Plan) {
    $entries=@($Plan | ForEach-Object { [pscustomobject]@{path=$_.path;oldHash=$_.oldHash;newHash=$_.newHash;action=$_.action} })
    foreach($item in $entries) {
        $dest=Safe-Path $Root $item.path
        if ((Hash-File $dest) -ne $item.oldHash) { throw "File changed while preparing update: $($item.path)" }
        if ($item.oldHash) {
            $backup=Safe-Path (Join-Path $Txn 'backup') $item.path
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($backup)) | Out-Null
            Copy-Item -LiteralPath $dest -Destination $backup
            if ((Hash-File $backup) -ne $item.oldHash) { throw 'Backup checksum mismatch.' }
        }
    }
    $journal=[pscustomobject]@{status='applying';entries=$entries;started=(Get-Date).ToString('o')}
    Save-Json (Join-Path $Txn 'journal.json') $journal
    try {
        foreach($item in $entries) {
            $dest=Safe-Path $Root $item.path
            if ($item.action -eq 'remove') { [IO.File]::Delete($dest) }
            else { Atomic-Copy (Safe-Path $Stage $item.path) $dest }
            if ((Hash-File $dest) -ne $item.newHash) { throw 'Applied file checksum mismatch.' }
        }
        $journal.status='complete';Save-Json (Join-Path $Txn 'journal.json') $journal
    } catch {
        $failure=$_
        Restore-Transaction $Root $Txn
        throw "Update rolled back: $failure"
    }
}
function Add-GeneratedFile($Plan,[string]$Root,[string]$Stage,[string]$Path,[string]$Text) {
    $dest=Safe-Path $Stage $Path;Write-Utf8 $dest $Text
    $new=Hash-File $dest;$old=Hash-File (Safe-Path $Root $Path)
    if ($new -ne $old) { $Plan.Add([pscustomobject]@{path=$Path;oldHash=$old;newHash=$new;action='write';source=$null}) }
}
function Find-Profile {
    # A shortcut installed inside a profile always targets that specific profile.
    $candidate=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
    if ((Split-Path $PSScriptRoot -Leaf) -eq 'client' -and (Split-Path (Split-Path $PSScriptRoot -Parent) -Leaf) -eq '.customatm' -and (Test-Path -LiteralPath (Join-Path $candidate 'minecraftinstance.json'))) { return $candidate }
    return (Initialize-CustomATM)
}
function Invoke-Update {
    if (!$Profile) { $Profile=Find-Profile }
    $Profile=[IO.Path]::GetFullPath($Profile)
    Write-Host "CustomATM - $Profile"
    Assert-GameClosed
    $control=Safe-Path $Profile '.customatm'
    [IO.Directory]::CreateDirectory($control) | Out-Null
    $lock=$null
    try {
        $lock=[IO.File]::Open((Join-Path $control 'update.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
        Recover-Pending $Profile
        $release=Invoke-RestMethod -Uri "https://api.github.com/repos/$script:Repo/releases/latest" -Headers $script:Headers -TimeoutSec 60
        if ($release.draft -or $release.prerelease) { throw 'No published stable release is available.' }
        $asset=@($release.assets | Where-Object name -eq 'pack-manifest.json')
        if ($asset.Count -ne 1) { throw 'Release does not contain exactly one pack manifest.' }
        $txn=Safe-Path $Profile ('.customatm/transactions/'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,8))
        [IO.Directory]::CreateDirectory($txn) | Out-Null
        $manifestPath=Join-Path $txn 'pack-manifest.json'
        $digest=$asset[0].digest
        if (!$digest -or !$digest.StartsWith('sha256:')) { throw 'GitHub did not provide an asset checksum.' }
        Download-File $asset[0].browser_download_url $manifestPath $digest.Substring(7)
        $m=Read-Json $manifestPath
        Assert-Manifest $m $Profile;Assert-Base $Profile $m
        if ($release.tag_name -ne 'v'+$m.version) { throw 'Release tag does not match manifest version.' }
        $statePath=Join-Path $control 'state.json';$previous=$null
        if (Test-Path -LiteralPath $statePath) { $previous=Read-Json $statePath }
        if ($previous -and [Version]$previous.version -gt [Version]$m.version) { throw 'Refusing an automatic downgrade. Ask the maintainer for a rollback release.' }
        $plan=New-Object Collections.Generic.List[object]
        foreach($entry in @(Get-Plan $Profile $m $previous)) { $plan.Add($entry) }
        Write-Host "Release $($m.version): $($plan.Count) pack file changes."
        if ($CheckOnly) { Write-Host 'Check complete; no pack files changed.';return }
        $stage=Join-Path $txn 'stage';[IO.Directory]::CreateDirectory($stage) | Out-Null
        $payload=$null
        if (@($plan | Where-Object { $_.action -eq 'write' -and $_.source.source -eq 'payload' }).Count) {
            $pa=@($release.assets | Where-Object name -eq $m.payload.name)
            if ($pa.Count -ne 1 -or $pa[0].digest -ne 'sha256:'+$m.payload.sha256) { throw 'Payload asset does not match manifest.' }
            $payload=Join-Path $txn 'payload.zip';Download-File $pa[0].browser_download_url $payload $m.payload.sha256
        }
        Stage-Files $Profile $stage $plan.ToArray() $payload
        # Add the new group without replacing the base questbook or its translation aggregate.
        $groupRel='config/ftbquests/quests/chapter_groups.snbt'
        $groups=[IO.File]::ReadAllText((Safe-Path $Profile $groupRel))
        if ($groups -notmatch [regex]::Escape($m.quest_group)) {
            $at=$groups.LastIndexOf(']');if ($at -lt 0) { throw 'Unrecognized FTB chapter group file.' }
            $groups=$groups.Insert($at,"`n`t`t{ id: `"$($m.quest_group)`" }`n`t")
            Add-GeneratedFile $plan $Profile $stage $groupRel $groups
        }
        # Preserve personal options, including any explicitly selected casino key.
        $optionsRel='options.txt';$optionsPath=Safe-Path $Profile $optionsRel
        if (Test-Path -LiteralPath $optionsPath) {
            $options=[IO.File]::ReadAllText($optionsPath)
            $key='key_key.casinomod.open_casino:'
            if ($options -notmatch '(?m)^key_key\.casinomod\.open_casino:') { $options=$options.TrimEnd()+"`n"+$key+"key.keyboard.f8`n" }
            else { $options=[regex]::Replace($options,'(?m)^key_key\.casinomod\.open_casino:key\.keyboard\.h\r?$',$key+'key.keyboard.f8') }
            Add-GeneratedFile $plan $Profile $stage $optionsRel $options
        }
        $state=[ordered]@{schema=1;repository=$script:Repo;version=$m.version;files=@($m.files | ForEach-Object { @{path=$_.path;sha256=$_.sha256} })}
        Add-GeneratedFile $plan $Profile $stage '.customatm/state.json' ($state | ConvertTo-Json -Depth 10)
        # The downloaded Setup program installs a local copy of itself; no remote code is executed.
        foreach($name in @('Update-Pack.ps1','Update Pack.cmd','Setup-Profile.ps1','base-extras.json')) {
            $source=Join-Path $PSScriptRoot $name
            $target='.customatm/client/'+$name
            Add-GeneratedFile $plan $Profile $stage $target ([IO.File]::ReadAllText($source))
        }
        $shortcut="@echo off`r`npowershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File `"%~dp0.customatm\client\Update-Pack.ps1`" -Profile `"%~dp0.`" %*`r`nif errorlevel 1 (echo Update failed. Read the message above.) else (echo Update complete. Launch through CurseForge.)`r`npause`r`n"
        Add-GeneratedFile $plan $Profile $stage 'Update Pack.cmd' $shortcut
        Assert-GameClosed
        if ($plan.Count) { Apply-Transaction $Profile $txn $stage $plan.ToArray() }
        Install-DesktopShortcut $Profile
        Write-Host "Ready: CustomATM $($m.version). Launch this profile through CurseForge." -ForegroundColor Green
        Write-Host "Recovery files: $txn"
    } finally { if ($lock) { $lock.Dispose() } }
}
. (Join-Path $PSScriptRoot 'Setup-Profile.ps1')
if (!$LibraryOnly) {
    try { Invoke-Update;exit 0 }
    catch { Write-Host ('UPDATE STOPPED: '+$_.Exception.Message) -ForegroundColor Red;exit 1 }
}
