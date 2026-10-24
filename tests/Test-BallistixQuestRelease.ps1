#requires -Version 5.1
# Real old/new payloads, private fixture only. Does not run Minecraft.
$ErrorActionPreference='Stop'
. "$PSScriptRoot/../client/Update-Pack.ps1" -LibraryOnly
$repoRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$testRoot=Join-Path $repoRoot ('.work/ballistix-quest-release-tests/'+[Guid]::NewGuid().ToString('N'))
$root=Join-Path $testRoot 'profile'
[IO.Directory]::CreateDirectory($root) | Out-Null
function Assert($Value,[string]$Message) {if(!$Value){throw "FAIL: $Message"};Write-Host "PASS: $Message"}
$old=Read-Json (Join-Path $repoRoot 'dist/1.5.0/pack-manifest.json')
$new=Read-Json (Join-Path $repoRoot 'dist/1.6.0/pack-manifest.json')
Assert-Manifest $new $root
Assert ($new.version -eq '1.6.0' -and $new.client_version -eq 4) 'existing updater accepts 1.6.0'
$byPath=@{};foreach($f in $new.files){$byPath[$f.path]=$f}
foreach($f in $old.files){
 if(!$byPath.ContainsKey($f.path) -or (($f | ConvertTo-Json -Depth 20 -Compress) -cne ($byPath[$f.path] | ConvertTo-Json -Depth 20 -Compress))){throw "Changed old entry: $($f.path)"}
}
Assert ($old.files.Count -eq 582 -and $new.files.Count -eq 593) 'all 582 old entries preserved; 11 files added'
Assert (($old.obsolete | ConvertTo-Json -Depth 20 -Compress) -ceq ($new.obsolete | ConvertTo-Json -Depth 20 -Compress)) 'no new removals'
Assert ((Hash-File (Join-Path $repoRoot 'dist/1.6.0/customatm-payload.zip')) -eq $new.payload.sha256) 'payload checksum matches'
$zip=[IO.Compression.ZipFile]::OpenRead((Join-Path $repoRoot 'dist/1.5.0/customatm-payload.zip'))
try {foreach($e in $zip.Entries){
 $dest=Safe-Path $root $e.FullName
 [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest)) | Out-Null
 [IO.Compression.ZipFileExtensions]::ExtractToFile($e,$dest,$false)
}} finally {$zip.Dispose()}
$old.files=@($old.files | Where-Object source -eq 'payload')
$new.files=@($new.files | Where-Object source -eq 'payload')
Write-Utf8 (Join-Path $root 'saves/Example/level.dat') 'world untouched'
Write-Utf8 (Join-Path $root 'saves/Example/ftbquests/progress.snbt') 'quest progress untouched'
Write-Utf8 (Join-Path $root 'options.txt') 'personal settings'
# FTB may rewrite existing chapter files at runtime; this addition must leave them alone.
$priorChapter=Join-Path $root 'config/ftbquests/quests/chapters/local_guide_01_minecolonies.snbt'
Add-Content -LiteralPath $priorChapter -Value '// runtime rewrite simulation'
$priorHash=Hash-File $priorChapter
$plan=@(Get-Plan $root $new $old)
Assert ($plan.Count -eq 11 -and @($plan | Where-Object action -ne 'write').Count -eq 0) 'plans only new Ballistix chapter, language and images'
$stage=Join-Path $testRoot 'stage'
Stage-Files $root $stage $plan (Join-Path $repoRoot 'dist/1.6.0/customatm-payload.zip')
Apply-Transaction $root (Join-Path $root '.customatm/transactions/ballistix-quests') $stage $plan
foreach($p in $plan){Assert ((Hash-File (Safe-Path $root $p.path)) -eq $p.newHash) ('installed bytes verified: '+$p.path)}
Assert (@(Get-Plan $root $new $new).Count -eq 0) 'repeat update is idempotent'
Assert ((Hash-File $priorChapter) -eq $priorHash) 'existing runtime-rewritten chapter preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'saves/Example/level.dat')) -eq 'world untouched') 'world preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'saves/Example/ftbquests/progress.snbt')) -eq 'quest progress untouched') 'quest progress preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'options.txt')) -eq 'personal settings') 'personal settings preserved'
Write-Host 'PASS: isolated 1.5.0 -> 1.6.0 quest addition; no live profile touched.'
