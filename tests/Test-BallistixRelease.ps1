#requires -Version 5.1
# Tests a real update in a private fixture, using already verified downloads.
$ErrorActionPreference='Stop'
. "$PSScriptRoot/../client/Update-Pack.ps1" -LibraryOnly
$repoRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$testRoot=Join-Path $repoRoot ('.work/ballistix-release-tests/'+[Guid]::NewGuid().ToString('N'))
$root=Join-Path $testRoot 'profile'
[IO.Directory]::CreateDirectory($root) | Out-Null
function Assert($Value,[string]$Message) {if(!$Value){throw "FAIL: $Message"};Write-Host "PASS: $Message"}
$old=Read-Json (Join-Path $repoRoot 'dist/1.4.0/pack-manifest.json')
$new=Read-Json (Join-Path $repoRoot 'dist/1.5.0/pack-manifest.json')
Assert-Manifest $new $root
Assert ($new.version -eq '1.5.0' -and $new.client_version -eq 4) 'existing updater accepts release 1.5.0'
$byPath=@{};foreach($f in $new.files){$byPath[$f.path]=$f}
foreach($f in $old.files){
 if(!$byPath.ContainsKey($f.path) -or (($f | ConvertTo-Json -Depth 20 -Compress) -cne ($byPath[$f.path] | ConvertTo-Json -Depth 20 -Compress))){throw "Changed old entry: $($f.path)"}
}
Assert ($new.files.Count -eq $old.files.Count+4) 'all 578 existing entries unchanged; exactly four additions'
Assert (($old.obsolete | ConvertTo-Json -Depth 20 -Compress) -ceq ($new.obsolete | ConvertTo-Json -Depth 20 -Compress)) 'no new removals'
Assert ((Hash-File (Join-Path $repoRoot 'dist/1.5.0/customatm-payload.zip')) -eq $new.payload.sha256) 'archive checksum matches'
$zip=[IO.Compression.ZipFile]::OpenRead((Join-Path $repoRoot 'dist/1.4.0/customatm-payload.zip'))
try {foreach($e in $zip.Entries){
 $dest=Safe-Path $root $e.FullName
 [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest)) | Out-Null
 [IO.Compression.ZipFileExtensions]::ExtractToFile($e,$dest,$false)
}} finally {$zip.Dispose()}
# Omit unchanged base jars from the fixture; compare their exact manifest entries above.
$old.files=@($old.files | Where-Object source -eq 'payload')
$additions=Read-Json (Join-Path $repoRoot 'pack/ballistix-additions.json')
$new.files=@($new.files | Where-Object { $_.source -eq 'payload' -or $_.path -in $additions.path })
$cache=Join-Path $testRoot 'download-cache'
[IO.Directory]::CreateDirectory((Join-Path $cache 'mods')) | Out-Null
foreach($f in $additions){
 $source=Join-Path $repoRoot ('.work/ballistix/'+[IO.Path]::GetFileName($f.path))
 Assert ((Hash-File $source) -eq $f.sha256) ('author download verified: '+$f.path)
 [IO.File]::Copy($source,(Safe-Path $cache $f.path))
}
$script:ReuseProfiles=@($cache)
Write-Utf8 (Join-Path $root 'saves/Example/level.dat') 'world untouched'
Write-Utf8 (Join-Path $root 'options.txt') 'personal settings'
$plan=@(Get-Plan $root $new $old)
Assert ($plan.Count -eq 4 -and @($plan | Where-Object action -ne 'write').Count -eq 0) 'plans four additions only'
$stage=Join-Path $testRoot 'stage'
Stage-Files $root $stage $plan (Join-Path $repoRoot 'dist/1.5.0/customatm-payload.zip')
Apply-Transaction $root (Join-Path $root '.customatm/transactions/ballistix') $stage $plan
foreach($f in $new.files){if((Hash-File (Safe-Path $root $f.path)) -ne $f.sha256){throw "Wrong installed bytes: $($f.path)"}}
Assert (@(Get-Plan $root $new $new).Count -eq 0) 'installed hashes match; repeat update is idempotent'
Add-Content -LiteralPath (Safe-Path $root 'config/ballistix-common.toml') -Value '# simulated NeoForge config expansion'
Assert (@(Get-Plan $root $new $new).Count -eq 0) 'first-launch config expansion is preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'saves/Example/level.dat')) -eq 'world untouched') 'world preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'options.txt')) -eq 'personal settings') 'personal settings preserved'
Write-Host 'PASS: isolated 1.4.0 -> 1.5.0 update. No live profile or Minecraft process touched.'
