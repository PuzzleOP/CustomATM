# CurseForge Standalone bootstrap. Loaded by Update-Pack.ps1; no extra runtime required.
$script:BaseArchiveUrl='https://edge.forgecdn.net/files/9190/157/All%20the%20Mods%2010-8.3.zip'
$script:BaseArchiveHash='24440fb355de69b28af6ff18556b5d0598bb93570b2b745552cdb1bcb5448c8f'

function Connect-CurseForge {
    $agent=Get-CimInstance Win32_Process -Filter "Name='Curse.Agent.Host.exe'" | Select-Object -First 1
    if (!$agent) {
        $exe=Join-Path $env:LOCALAPPDATA 'Programs/CurseForge Windows/CurseForge.exe'
        if (!(Test-Path -LiteralPath $exe)) { throw 'Install CurseForge Standalone for Windows, open Minecraft in it once, then run this Setup again.' }
        Start-Process -FilePath $exe -WindowStyle Hidden
        Write-Host 'Starting CurseForge. Complete its Minecraft setup if prompted.'
        $deadline=(Get-Date).AddMinutes(3)
        do {
            Start-Sleep -Seconds 2
            $agent=Get-CimInstance Win32_Process -Filter "Name='Curse.Agent.Host.exe'" | Select-Object -First 1
        } while (!$agent -and (Get-Date) -lt $deadline)
    }
    if (!$agent) { throw 'CurseForge is not ready. Open its Minecraft page and run Setup again.' }
    # This is the running local agent's temporary connection key, never saved or logged.
    $key=[regex]::Match($agent.CommandLine,'--api-key=([^"\s]+)').Groups[1].Value
    if (!$key) { throw 'This CurseForge version does not expose the compatible local agent connection. Update CurseForge Standalone and retry.' }
    $ports=@(Get-NetTCPConnection -OwningProcess $agent.ProcessId -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty LocalPort -Unique)
    foreach($port in $ports) {
        $ws=New-Object Net.WebSockets.ClientWebSocket
        $ws.Options.SetRequestHeader('Origin','cfapp')
        $cts=New-Object Threading.CancellationTokenSource(5000)
        try {
            $null=$ws.ConnectAsync([uri]"ws://127.0.0.1:$port/CurseForge",$cts.Token).GetAwaiter().GetResult()
            return [pscustomobject]@{socket=$ws;key=$key;nextId=900000}
        } catch { $ws.Dispose() } finally { $cts.Dispose() }
    }
    throw 'Could not connect to CurseForge. Open its Minecraft page and retry.'
}
function Invoke-CurseForge($Connection,[string]$Method,[object[]]$Arguments=@(),[int]$TimeoutSeconds=600) {
    $Connection.nextId++
    $id=$Connection.nextId
    $cts=New-Object Threading.CancellationTokenSource($TimeoutSeconds*1000)
    $data=New-Object IO.MemoryStream
    try {
        $request=@{id=$id;type='method';apiKey=$Connection.key;name=$Method;args=@($Arguments)} | ConvertTo-Json -Depth 30 -Compress
        $bytes=[Text.Encoding]::UTF8.GetBytes($request)
        $null=$Connection.socket.SendAsync([ArraySegment[byte]]::new($bytes),[Net.WebSockets.WebSocketMessageType]::Text,$true,$cts.Token).GetAwaiter().GetResult()
        $buffer=New-Object byte[] 65536
        $lastStatus=Get-Date
        while ($true) {
            $data.SetLength(0)
            do {
                $receive=$Connection.socket.ReceiveAsync([ArraySegment[byte]]::new($buffer),$cts.Token)
                while (!$receive.IsCompleted) {
                    Start-Sleep -Milliseconds 100
                    if (((Get-Date)-$lastStatus).TotalSeconds -ge 30) { Write-Host 'CurseForge is still preparing the profile...';$lastStatus=Get-Date }
                }
                $r=$receive.GetAwaiter().GetResult()
                if ($r.MessageType -eq [Net.WebSockets.WebSocketMessageType]::Close) { throw 'CurseForge disconnected. Reopen it and run Setup again.' }
                $data.Write($buffer,0,$r.Count)
                if ($data.Length -gt 67108864) { throw 'Unexpectedly large CurseForge response.' }
            } while (!$r.EndOfMessage)
            $reply=[Text.Encoding]::UTF8.GetString($data.ToArray()) | ConvertFrom-Json
            if ($reply.type -eq 'callback' -and $reply.id -eq $id) {
                if (!$reply.result.success) { throw "CurseForge $Method failed: $($reply.result.error)" }
                return $reply.result.data
            }
        }
    } finally { $cts.Dispose();$data.Dispose() }
}
function Get-OwnedProfile($Instances) {
    $owned=@()
    foreach($instance in $Instances) {
        if (!$instance.installPath) { continue }
        $receipt=Join-Path $instance.installPath '.customatm/bootstrap.json'
        if (Test-Path -LiteralPath $receipt) {
            $b=Read-Json $receipt
            if ($b.repository -eq $script:Repo -and $b.instance_id -eq $instance.guid -and $b.archive_sha256 -eq $script:BaseArchiveHash) { $owned+=$instance }
        }
    }
    if ($owned.Count -gt 1) { throw 'Multiple CustomATM profiles found. Run Update Pack.cmd inside the profile you want to use.' }
    if ($owned.Count) { return $owned[0] }
    return $null
}
function Install-BaseOverrides([string]$Root,[string]$Archive) {
    if ((Hash-File $Archive) -ne $script:BaseArchiveHash) { throw 'ATM10 archive checksum mismatch.' }
    $zip=[IO.Compression.ZipFile]::OpenRead($Archive)
    try {
        $entry=$zip.GetEntry('manifest.json');if (!$entry) { throw 'Base manifest is missing.' }
        $reader=New-Object IO.StreamReader($entry.Open())
        try {$manifest=$reader.ReadToEnd() | ConvertFrom-Json} finally {$reader.Dispose()}
        if ($manifest.version -ne '8.3' -or $manifest.minecraft.version -ne '1.21.1' -or $manifest.minecraft.modLoaders[0].id -ne 'neoforge-21.1.259') { throw 'Unexpected ATM10 archive version.' }
        $seen=@{}
        foreach($e in $zip.Entries) {
            if (!$e.FullName.StartsWith('overrides/') -or $e.FullName.EndsWith('/')) {continue}
            $relative=$e.FullName.Substring(10)
            if ($relative -notmatch '^(config|defaultconfigs|kubejs|local|datapacks)/') {throw "Unexpected base override: $relative"}
            $target=Safe-Path $Root $relative
            if ($seen.ContainsKey($relative)) {throw 'Duplicate base override'};$seen[$relative]=$true
            [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
            [IO.Compression.ZipFileExtensions]::ExtractToFile($e,$target,$true)
        }
        if (!$seen.Count) {throw 'Base archive contains no recognized overrides.'}
    } finally {$zip.Dispose()}
}
function Initialize-CustomATM {
    Assert-GameClosed
    $setupLock=[IO.File]::Open((Join-Path ([IO.Path]::GetTempPath()) 'CustomATM-profile-setup.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
    $connection=$null
    try {
        $connection=Connect-CurseForge
        $instances=@(Invoke-CurseForge $connection 'minecraftGetInstances')
        $owned=Get-OwnedProfile $instances
        if (!$owned) {
            if ($CheckOnly) { throw 'CustomATM is not installed. Run Setup without -CheckOnly to create it.' }
            Write-Host 'Creating a separate CustomATM profile in CurseForge (Minecraft 1.21.1 / NeoForge 21.1.259)...'
            $request=@{GameId=432;Name='CustomATM';Author='PuzzleOP';GameVersion='1.21.1';ModloaderVersionString='neoforge-21.1.259';ProfileImagePath=$null;InstallSource=0;ModsToInstall=@();GroupId=$null}
            $id=Invoke-CurseForge $connection 'createModpack' @($request) 1800
            $instances=@(Invoke-CurseForge $connection 'minecraftGetInstances')
            $owned=@($instances | Where-Object guid -eq $id) | Select-Object -First 1
            if (!$owned -or !$owned.installPath) { throw 'CurseForge created a profile but did not return its folder. Inspect CustomATM in CurseForge before retrying.' }
            $receipt=Safe-Path $owned.installPath '.customatm/bootstrap.json'
            Save-Json $receipt @{schema=1;repository=$script:Repo;instance_id=$id;archive_sha256=$script:BaseArchiveHash;version='8.3';complete=$false}
        }
        $root=[IO.Path]::GetFullPath($owned.installPath).TrimEnd('\')
        $receipt=Safe-Path $root '.customatm/bootstrap.json'
        $b=Read-Json $receipt
        if (!$b.complete) {
            if ($CheckOnly) {throw 'CustomATM base setup is incomplete. Run Setup without -CheckOnly.'}
            $archive=Safe-Path $root '.customatm/base/ATM10-8.3.zip'
            if ((Hash-File $archive) -ne $script:BaseArchiveHash) {
                Write-Host 'Downloading the official ATM10 8.3 base...'
                Download-File $script:BaseArchiveUrl $archive $script:BaseArchiveHash
            }
            Write-Host 'Installing the original ATM10 configs, quests and recipes...'
            Install-BaseOverrides $root $archive
            $extras=Read-Json (Join-Path $PSScriptRoot 'base-extras.json')
            foreach($extra in $extras) {
                if ($extra.path -notmatch '^shaderpacks/[^/]+\.zip$') {throw 'Invalid base resource path.'}
                $target=Safe-Path $root $extra.path
                if ((Hash-File $target) -ne $extra.sha256) {Download-File $extra.url $target $extra.sha256}
            }
            # ATM10 8.3's official manifest recommends 8196 MB. Set once, preserve later user changes.
            $null=Invoke-CurseForge $connection 'changeModpackProperties' @($owned.guid,@{Name='CustomATM';IsMemoryOverride=$true;MemoryAllocatedType=1;AllocatedMemory=8196})
            $b.complete=$true;Save-Json $receipt $b
        }
        # Rename through CurseForge so both its in-memory tile and on-disk metadata agree.
        if (!$CheckOnly) { $null=Invoke-CurseForge $connection 'changeModpackProperties' @($owned.guid,@{Name='CustomATM';IsUnlocked=$true}) }
        $script:ReuseProfiles=@($instances | Where-Object { $_.installPath -ne $owned.installPath -and $_.gameVersion -eq '1.21.1' } | ForEach-Object installPath)
        return $root
    } finally { if ($connection) {$connection.socket.Dispose();$connection.key=$null};$setupLock.Dispose() }
}

function Install-DesktopShortcut([string]$Root) {
    if (!(Test-Path -LiteralPath (Join-Path $Root '.customatm/bootstrap.json'))) { return }
    try {
        $desktop=[Environment]::GetFolderPath('Desktop')
        $shell=New-Object -ComObject WScript.Shell
        $linkPath=Join-Path $desktop 'Update CustomATM.lnk'
        $link=$shell.CreateShortcut($linkPath)
        if (Test-Path -LiteralPath $linkPath) {
            $oldState=Join-Path ([IO.Path]::GetDirectoryName($link.TargetPath)) '.customatm/state.json'
            if (!(Test-Path -LiteralPath $oldState) -or (Read-Json $oldState).repository -ne $script:Repo) {
                Write-Host 'Existing desktop shortcut was kept. Use Update Pack.cmd inside CustomATM to update.';return
            }
        }
        $link.TargetPath=Join-Path $Root 'Update Pack.cmd'
        $link.WorkingDirectory=$Root
        $link.Description='Update the CustomATM CurseForge profile from GitHub releases'
        $link.Save()
    } catch {Write-Host 'Desktop shortcut could not be created. Use Update Pack.cmd inside the profile.'}
}
