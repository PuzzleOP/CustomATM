#requires -Version 5.1
# Exercise real release payloads only inside an isolated fixture; never start Minecraft.
$ErrorActionPreference='Stop'
. "$PSScriptRoot/../client/Update-Pack.ps1" -LibraryOnly
$repoRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$testRoot=Join-Path $repoRoot ('.work/arcade-release-tests/'+[Guid]::NewGuid().ToString('N'))
$root=Join-Path $testRoot 'profile'
[IO.Directory]::CreateDirectory($root) | Out-Null
$old=Read-Json (Join-Path $repoRoot 'dist/1.3.0/pack-manifest.json')
$new=Read-Json (Join-Path $repoRoot 'dist/1.4.0/pack-manifest.json')
function Assert($Value,[string]$Message) {if(!$Value){throw "FAIL: $Message"};Write-Host "PASS: $Message"}
Assert-Manifest $new $root
Assert ($new.version -eq '1.4.0' -and $new.client_version -eq 4) 'existing updater accepts release 1.4.0'
$byPath=@{};foreach($f in $new.files){$byPath[$f.path]=$f}
foreach($f in $old.files){
 Assert ($byPath.ContainsKey($f.path) -and (($f | ConvertTo-Json -Depth 20 -Compress) -ceq ($byPath[$f.path] | ConvertTo-Json -Depth 20 -Compress))) ('unchanged release entry: '+$f.path)
}
Assert ($new.files.Count -eq $old.files.Count+1) 'exactly one managed file added'
$addon=$byPath['mods/customatm-arcade-0.2.0.jar']
Assert ($null -ne $addon -and $addon.source -eq 'payload') 'arcade addon comes from verified payload'
Assert (($old.obsolete | ConvertTo-Json -Depth 20 -Compress) -ceq ($new.obsolete | ConvertTo-Json -Depth 20 -Compress)) 'no new removals'
Assert ((Hash-File (Join-Path $repoRoot 'dist/1.4.0/customatm-payload.zip')) -eq $new.payload.sha256) 'release archive checksum matches'
# URL-sourced third-party jars are unchanged above. Test all actual overlay bytes without downloading the base pack.
$zip=[IO.Compression.ZipFile]::OpenRead((Join-Path $repoRoot 'dist/1.3.0/customatm-payload.zip'))
try {foreach($e in $zip.Entries){
 $dest=Safe-Path $root $e.FullName
 [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dest)) | Out-Null
 [IO.Compression.ZipFileExtensions]::ExtractToFile($e,$dest,$false)
}} finally {$zip.Dispose()}
$old.files=@($old.files | Where-Object source -eq 'payload')
$new.files=@($new.files | Where-Object source -eq 'payload')
Write-Utf8 (Join-Path $root 'saves/Example/level.dat') 'world untouched'
Write-Utf8 (Join-Path $root 'options.txt') 'personal settings'
$plan=@(Get-Plan $root $new $old)
Assert ($plan.Count -eq 1 -and $plan[0].path -eq $addon.path -and $plan[0].action -eq 'write') '1.3.0 overlay plans only the new addon'
$stage=Join-Path $testRoot 'stage'
Stage-Files $root $stage $plan (Join-Path $repoRoot 'dist/1.4.0/customatm-payload.zip')
Apply-Transaction $root (Join-Path $root '.customatm/transactions/arcade') $stage $plan
Assert ((Hash-File (Join-Path $root $addon.path)) -eq $addon.sha256) 'real addon installed with exact release bytes in fixture'
Assert (@(Get-Plan $root $new $new).Count -eq 0) 'repeat update is idempotent'
Assert ([IO.File]::ReadAllText((Join-Path $root 'saves/Example/level.dat')) -eq 'world untouched') 'world preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'options.txt')) -eq 'personal settings') 'personal settings preserved'
Write-Host 'PASS: isolated 1.3.0 -> 1.4.0 overlay migration. No live profile or Minecraft process touched.'
