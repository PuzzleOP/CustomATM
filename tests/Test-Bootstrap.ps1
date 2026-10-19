$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot '../client/Update-Pack.ps1') -LibraryOnly
$script:passed=0
function Assert($Value,[string]$Message) {if(!$Value){throw "FAIL: $Message"};$script:passed++;Write-Host "PASS: $Message"}
function Expect-Failure([scriptblock]$Action,[string]$Message) {$failed=$false;try{&$Action}catch{$failed=$true};Assert $failed $Message}
$testRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot ('../.work/bootstrap-tests/'+[Guid]::NewGuid().ToString('N'))))
[IO.Directory]::CreateDirectory($testRoot) | Out-Null
$source=Join-Path $testRoot 'source'
Write-Utf8 (Join-Path $source 'manifest.json') '{"version":"8.3","minecraft":{"version":"1.21.1","modLoaders":[{"id":"neoforge-21.1.259"}]}}'
Write-Utf8 (Join-Path $source 'overrides/config/base.toml') 'official base'
$archive=Join-Path $testRoot 'base.zip'
$z=[IO.Compression.ZipFile]::Open($archive,[IO.Compression.ZipArchiveMode]::Create)
try {
 foreach($relative in @('manifest.json','overrides/config/base.toml')) {
  $null=[IO.Compression.ZipFileExtensions]::CreateEntryFromFile($z,(Join-Path $source $relative),$relative)
 }
} finally {$z.Dispose()}
$script:BaseArchiveHash=Hash-File $archive
$script:testArchive=$archive
$script:instances=@();$script:creates=0;$script:downloads=0;$script:calls=@()
$script:newRoot=Join-Path $testRoot 'new-profile'
function Assert-GameClosed {}
function Connect-CurseForge {return [pscustomobject]@{socket=(New-Object IO.MemoryStream);key='test-only'}}
function Invoke-CurseForge($Connection,[string]$Method,[object[]]$Arguments=@(),[int]$TimeoutSeconds=600) {
 $script:calls+=$Method
 switch($Method) {
  'minecraftGetInstances' {return $script:instances}
  'createModpack' {
   $script:creates++
   Assert ($Arguments[0].Name -eq 'CustomATM' -and $Arguments[0].ModloaderVersionString -eq 'neoforge-21.1.259') 'native creation pins name and loader'
   $instance=[pscustomobject]@{guid='test-guid';installPath=$script:newRoot;gameVersion='1.21.1';name='CustomATM';baseModLoader=@{name='neoforge-21.1.259'}}
   Save-Json (Join-Path $script:newRoot 'minecraftinstance.json') $instance
   $script:instances=@($instance)
   return $instance.guid
  }
  'changeModpackProperties' {Assert ($Arguments[0] -eq 'test-guid' -and $Arguments[1].Name -eq 'CustomATM') 'rename targets the created GUID'}
  default {throw "Unexpected API method: $Method"}
 }
}
$realRead=${function:Read-Json}
function Read-Json([string]$Path) {if([IO.Path]::GetFileName($Path) -eq 'base-extras.json'){return @()};return (&$realRead $Path)}
function Download-File([string]$Url,[string]$Destination,[string]$Hash) {
 $script:downloads++
 [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Destination)) | Out-Null
 [IO.File]::Copy($script:testArchive,$Destination,$true)
 if((Hash-File $Destination) -ne $Hash){throw 'Test download hash mismatch'}
}
$root=Initialize-CustomATM
Assert ($root -eq $script:newRoot) 'clean install works with no existing ATM10 profile'
Assert ((Read-Json (Join-Path $root '.customatm/bootstrap.json')).complete) 'base receipt marked complete only after installation'
Assert ([IO.File]::ReadAllText((Join-Path $root 'config/base.toml')) -eq 'official base') 'official overrides installed'
$m=[pscustomobject]@{base=@{version='8.3';curseforge_file_id=9190157;minecraft='1.21.1';loader='neoforge-21.1.259'}}
Assert-Base $root $m;Assert $true 'owned native custom profile accepted as verified base'
Write-Utf8 (Join-Path $root 'config/base.toml') 'personal adjustment'
$again=Initialize-CustomATM
Assert ($again -eq $root -and $script:creates -eq 1 -and $script:downloads -eq 1) 'repeat setup reuses tile and does not redownload base'
Assert ([IO.File]::ReadAllText((Join-Path $root 'config/base.toml')) -eq 'personal adjustment') 'repeat setup preserves base config edits'
$CheckOnly=$true;$count=$script:calls.Count
$null=Initialize-CustomATM
Assert (($script:calls[$count..($script:calls.Count-1)] -notcontains 'changeModpackProperties')) 'check-only does not mutate CurseForge properties'
$CheckOnly=$false
$receipt=Read-Json (Join-Path $root '.customatm/bootstrap.json');$receipt.instance_id='wrong-guid';Save-Json (Join-Path $root '.customatm/bootstrap.json') $receipt
Expect-Failure {Assert-Base $root $m} 'base receipt cannot be transferred to another profile'
Assert ($null -eq (Get-OwnedProfile $script:instances)) 'unowned profiles are not adopted by name'
$receipt.instance_id='test-guid';$receipt.complete=$false;Save-Json (Join-Path $root '.customatm/bootstrap.json') $receipt
$null=Initialize-CustomATM
Assert ($script:creates -eq 1 -and (Read-Json (Join-Path $root '.customatm/bootstrap.json')).complete) 'interrupted base installation resumes on the same tile'
$badArchive=Join-Path $testRoot 'bad.zip';Write-Utf8 $badArchive 'corrupt'
Expect-Failure {Install-BaseOverrides (Join-Path $testRoot 'rejected') $badArchive} 'bad archive rejected before extraction'
Assert (!(Test-Path -LiteralPath (Join-Path $testRoot 'rejected'))) 'checksum failure creates no base files'
$cache=Join-Path $testRoot 'cache';Write-Utf8 (Join-Path $cache 'mods/test.jar') 'verified mod'
$script:ReuseProfiles=@($cache)
$jar=Get-Item -LiteralPath (Join-Path $cache 'mods/test.jar')
$plan=@([pscustomobject]@{action='write';path='mods/test.jar';newHash=(Hash-File $jar.FullName);source=@{source='url';url='https://edge.forgecdn.net/test.jar';size=$jar.Length}})
$stage=Join-Path $testRoot 'stage';$before=$script:downloads
Stage-Files $root $stage $plan $null
Assert ((Hash-File (Join-Path $stage 'mods/test.jar')) -eq $plan[0].newHash -and $before -eq $script:downloads) 'identical existing mod reused without network download'
$malicious=Join-Path $testRoot 'traversal.zip'
$z=[IO.Compression.ZipFile]::Open($malicious,[IO.Compression.ZipArchiveMode]::Create)
try {
 foreach($pair in @(@('manifest.json',[IO.File]::ReadAllText((Join-Path $source 'manifest.json'))),@('overrides/config/../../escape.txt','bad'))) {
  $writer=New-Object IO.StreamWriter($z.CreateEntry($pair[0]).Open());try{$writer.Write($pair[1])}finally{$writer.Dispose()}
 }
} finally {$z.Dispose()}
$script:BaseArchiveHash=Hash-File $malicious
Expect-Failure {Install-BaseOverrides (Join-Path $testRoot 'safe') $malicious} 'base extraction rejects path traversal'
Assert (!(Test-Path -LiteralPath (Join-Path $testRoot 'escape.txt'))) 'base extraction cannot write outside profile'
Write-Host "ALL $script:passed BOOTSTRAP CHECKS PASSED"
