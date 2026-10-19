#requires -Version 5.1
$ErrorActionPreference='Stop'
. "$PSScriptRoot/../client/Update-Pack.ps1" -LibraryOnly
$testRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot ('../.work/tests/'+[Guid]::NewGuid().ToString('N'))))
[IO.Directory]::CreateDirectory($testRoot) | Out-Null
$script:passed=0
function Assert($Condition,[string]$Message) { if (!$Condition) { throw "FAIL: $Message" };$script:passed++;Write-Host "PASS: $Message" }
function Expect-Failure([scriptblock]$Body,[string]$Message) { $failed=$false;try { &$Body | Out-Null }catch{$failed=$true};Assert $failed $Message }
function Make-File([string]$Root,[string]$Rel,[string]$Text) { $p=Safe-Path $Root $Rel;Write-Utf8 $p $Text;return $p }
function Fixture([string]$Name) {
 $r=Join-Path $testRoot $Name;[IO.Directory]::CreateDirectory($r) | Out-Null
 $null=Make-File $r 'mods/base.jar' 'base';$null=Make-File $r 'mods/old.jar' 'old'
 $null=Make-File $r 'config/example.toml' 'before';$null=Make-File $r 'saves/MyWorld/level.dat' 'precious world'
 $null=Make-File $r 'options.txt' 'personal options';$null=Make-File $r 'journeymap/map.dat' 'personal map'
 return $r
}
function Entry([string]$Rel,[string]$Text) {
 $src=Make-File $testRoot ('inputs/'+$Rel) $Text
 return [pscustomobject]@{path=$Rel;sha256=(Hash-File $src);size=(Get-Item -LiteralPath $src).Length;source='payload'}
}
$root=Fixture 'success'
$manifest=[pscustomobject]@{schema=1;repository='PuzzleOP/CustomATM';client_version=1;version='1.0.0';quest_group='28D38D1EC21B4002';files=@((Entry 'mods/base.jar' 'base'),(Entry 'mods/new.jar' 'new'),(Entry 'config/example.toml' 'after'));obsolete=@([pscustomobject]@{path='mods/old.jar';sha256=(Hash-File (Join-Path $root 'mods/old.jar'))})}
Assert-Manifest $manifest $root
Assert $true 'valid manifest accepted'
$plan=@(Get-Plan $root $manifest $null)
Assert ($plan.Count -eq 3) 'first update plans one addition, one replacement and one known removal'
$payloadDir=Join-Path $testRoot 'inputs';$payload=Join-Path $testRoot 'payload.zip'
$archive=[IO.Compression.ZipFile]::Open($payload,[IO.Compression.ZipArchiveMode]::Create)
try { foreach($file in Get-ChildItem -LiteralPath $payloadDir -Recurse -File) {
 $rel=$file.FullName.Substring($payloadDir.Length+1).Replace('\','/')
 [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive,$file.FullName,$rel) | Out-Null
} } finally {$archive.Dispose()}
$stage=Join-Path $testRoot 'stage';Stage-Files $root $stage $plan $payload
$txn=Join-Path $root '.customatm/transactions/success';Apply-Transaction $root $txn $stage $plan
Assert ((Hash-File (Join-Path $root 'mods/new.jar')) -eq $manifest.files[1].sha256) 'new mod installed with verified bytes'
Assert ([IO.File]::ReadAllText((Join-Path $root 'config/example.toml')) -eq 'after') 'managed config updated'
Assert (!(Test-Path -LiteralPath (Join-Path $root 'mods/old.jar'))) 'known obsolete mod removed'
Assert ([IO.File]::ReadAllText((Join-Path $txn 'backup/mods/old.jar')) -eq 'old') 'removed mod preserved in backup'
Assert ([IO.File]::ReadAllText((Join-Path $root 'saves/MyWorld/level.dat')) -eq 'precious world') 'world preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'options.txt')) -eq 'personal options') 'personal settings preserved'
Assert ([IO.File]::ReadAllText((Join-Path $root 'journeymap/map.dat')) -eq 'personal map') 'map preserved'
$previous=[pscustomobject]@{repository='PuzzleOP/CustomATM';version='1.0.0';files=$manifest.files}
Assert (@(Get-Plan $root $manifest $previous).Count -eq 0) 'repeat update is idempotent'
$null=Make-File $root 'config/example.toml' 'local change'
Assert (@(Get-Plan $root $manifest $previous).Count -eq 0) 'unchanged published configs preserve local/runtime changes'
$changed=$manifest | ConvertTo-Json -Depth 20 | ConvertFrom-Json
$changed.files[2].sha256='1'*64
Expect-Failure {Get-Plan $root $changed $previous} 'new config updates do not overwrite conflicting local edits'
$root2=Fixture 'extra';$null=Make-File $root2 'mods/unknown.jar' 'unknown'
Expect-Failure {Get-Plan $root2 $manifest $null} 'unknown extra mods are not deleted'
$root3=Fixture 'obsolete-modified';$null=Make-File $root3 'mods/old.jar' 'modified old'
Expect-Failure {Get-Plan $root3 $manifest $null} 'modified obsolete mod is protected'
foreach($path in @('../saves/a','mods/../../outside','C:/outside','mods/a:stream','mods/CON.jar','mods/a/../b','mods/test.','mods\test.jar')) {
 Expect-Failure {Safe-Path $root $path} "unsafe path rejected: $path"
}
Expect-Failure {Assert-ManagedPath 'saves/world/level.dat'} 'manifest cannot manage saves'
Expect-Failure {Assert-DownloadUrl 'http://cdn.modrinth.com/a'} 'HTTP rejected'
Expect-Failure {Assert-DownloadUrl 'https://example.com/a'} 'unknown download host rejected'
Expect-Failure {Assert-DownloadUrl 'https://github.com/Other/Repo/releases/download/x/a'} 'wrong GitHub repository rejected'
$bad=[pscustomobject]@{schema=1;repository='PuzzleOP/CustomATM';client_version=1;version='1.0.0';quest_group=$manifest.quest_group;files=@($manifest.files[0],$manifest.files[0]);obsolete=@()}
Expect-Failure {Assert-Manifest $bad $root} 'duplicate manifest paths rejected'
$root4=Fixture 'corrupt';$badPlan=@(Get-Plan $root4 $manifest $null)
$badPlan[0].newHash='0'*64
Expect-Failure {Stage-Files $root4 (Join-Path $testRoot 'bad-stage') $badPlan $payload} 'bad payload checksum fails before installation'
Assert ([IO.File]::ReadAllText((Join-Path $root4 'config/example.toml')) -eq 'before') 'failed download/stage leaves original intact'
$root5=Fixture 'rollback';$plan5=@(Get-Plan $root5 $manifest $null)
$stage5=Join-Path $testRoot 'stage5';Stage-Files $root5 $stage5 $plan5 $payload
$originalCopy=(Get-Item Function:Atomic-Copy).ScriptBlock
$script:copyCalls=0
function Atomic-Copy([string]$Source,[string]$Destination) { $script:copyCalls++;if($script:copyCalls -eq 2){throw 'simulated disk write failure'};&$originalCopy $Source $Destination }
Expect-Failure {Apply-Transaction $root5 (Join-Path $root5 '.customatm/transactions/failure') $stage5 $plan5} 'mid-apply failure triggers rollback'
Set-Item Function:Atomic-Copy $originalCopy
Assert ([IO.File]::ReadAllText((Join-Path $root5 'config/example.toml')) -eq 'before') 'rollback restores replaced config'
Assert (!(Test-Path -LiteralPath (Join-Path $root5 'mods/new.jar'))) 'rollback removes newly created mod'
Assert ([IO.File]::ReadAllText((Join-Path $root5 'mods/old.jar')) -eq 'old') 'rollback preserves old mod'
$root6=Fixture 'interrupt';$tx6=Join-Path $root6 '.customatm/transactions/interrupted'
$oldHash=Hash-File (Join-Path $root6 'config/example.toml')
$null=Make-File $tx6 'backup/config/example.toml' 'before'
$newFile=Make-File $root6 'config/example.toml' 'after'
$null=Make-File $root6 'config/example.toml.customatm-tmp' 'interrupted partial write'
Save-Json (Join-Path $tx6 'journal.json') ([pscustomobject]@{status='applying';entries=@([pscustomobject]@{path='config/example.toml';oldHash=$oldHash;newHash=(Hash-File $newFile);action='write'})})
Recover-Pending $root6
Assert ([IO.File]::ReadAllText($newFile) -eq 'before') 'next-run recovery restores an interrupted transaction'
Assert ((Read-Json (Join-Path $tx6 'journal.json')).status -eq 'rolled-back') 'recovery journal records completion'
Assert (!(Test-Path -LiteralPath (Join-Path $root6 'config/example.toml.customatm-tmp'))) 'hard-interruption temporary file is recovered'
$base=[pscustomobject]@{version='8.3';minecraft='1.21.1';loader='neoforge-21.1.259';curseforge_file_id=9190157}
$mBase=[pscustomobject]@{base=$base}
Save-Json (Join-Path $root6 'minecraftinstance.json') @{projectID=925200;fileID=9190157;gameVersion='1.21.1';baseModLoader=@{name='neoforge-21.1.259'}}
Assert-Base $root6 $mBase;Assert $true 'matching CurseForge base accepted'
$base.curseforge_file_id=1;Expect-Failure {Assert-Base $root6 $mBase} 'wrong base pack version rejected'
# Exercise the complete entry point with local release bytes and a fake profile.
# A running game is irrelevant to these isolated fixtures; never permit a real profile here.
function Assert-GameClosed {
 $fixturePath=[IO.Path]::GetFullPath($Profile)
 if (!$fixturePath.StartsWith($testRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Test updater may only touch its isolated fixture directory' }
}
$full=Fixture 'full-flow'
Save-Json (Join-Path $full 'minecraftinstance.json') @{projectID=925200;fileID=9190157;gameVersion='1.21.1';baseModLoader=@{name='neoforge-21.1.259'}}
$null=Make-File $full 'config/ftbquests/quests/chapter_groups.snbt' "{ chapter_groups: [ { id: `"1111111111111111`" } ] }"
$base.curseforge_file_id=9190157
$manifest | Add-Member -NotePropertyName base -NotePropertyValue $base
$manifest | Add-Member -NotePropertyName payload -NotePropertyValue ([pscustomobject]@{name='customatm-payload.zip';sha256=(Hash-File $payload)})
$mf=Join-Path $testRoot 'pack-manifest.json';Save-Json $mf $manifest
$script:fakeRelease=[pscustomobject]@{tag_name='v1.0.0';draft=$false;prerelease=$false;assets=@(
 [pscustomobject]@{name='pack-manifest.json';browser_download_url='https://github.com/PuzzleOP/CustomATM/releases/download/v1.0.0/pack-manifest.json';digest=('sha256:'+(Hash-File $mf))},
 [pscustomobject]@{name='customatm-payload.zip';browser_download_url='https://github.com/PuzzleOP/CustomATM/releases/download/v1.0.0/customatm-payload.zip';digest=('sha256:'+(Hash-File $payload))})}
function Invoke-RestMethod { return $script:fakeRelease }
$script:testPayloadPath=$payload
$script:testManifestPath=$mf
function Download-File([string]$Url,[string]$Destination,[string]$Hash) {
 $source=if($Url.EndsWith('pack-manifest.json')){$script:testManifestPath}else{$script:testPayloadPath}
 Copy-Item -LiteralPath $source -Destination $Destination
 if((Hash-File $Destination) -ne $Hash){throw 'Mock download hash mismatch'}
}
$Profile=$full
Invoke-Update
Assert ((Read-Json (Join-Path $full '.customatm/state.json')).version -eq '1.0.0') 'full update writes a version receipt'
Assert (Test-Path -LiteralPath (Join-Path $full 'Update Pack.cmd')) 'full update installs permanent shortcut'
Assert ([IO.File]::ReadAllText((Join-Path $full 'config/ftbquests/quests/chapter_groups.snbt')).Contains($manifest.quest_group)) 'full update registers the quest group'
Assert ([IO.File]::ReadAllText((Join-Path $full 'options.txt')).Contains('key_key.casinomod.open_casino:key.keyboard.f8')) 'full update adds casino key without copying someone else\s options'
Invoke-Update
Assert ((Read-Json (Join-Path $full '.customatm/state.json')).version -eq '1.0.0') 'complete updater can run again successfully'
Assert ((Get-CasinoOptions '') -eq "key_key.casinomod.open_casino:key.keyboard.f8`n") 'fresh profiles get F8 before their first launch'
$oldOptions="soundCategory_master:0.7`r`nkey_key.casinomod.open_casino:key.keyboard.h`r`n"
$newOptions=Get-CasinoOptions $oldOptions
Assert ($newOptions.Contains('key_key.casinomod.open_casino:key.keyboard.f8')) 'conflicting default H migrates to F8'
Assert ($newOptions.Contains('soundCategory_master:0.7')) 'casino migration preserves unrelated options'
Assert ((Get-CasinoOptions $newOptions) -eq $newOptions) 'casino migration is idempotent'
$customOptions="key_key.casinomod.open_casino:key.keyboard.j`n"
Assert ((Get-CasinoOptions $customOptions) -eq $customOptions) 'explicit custom casino key is preserved'
# Accept only verified FTB rewrites tied to the previous published hash.
$questRoot=Join-Path $testRoot 'quest-rewrite';[IO.Directory]::CreateDirectory($questRoot) | Out-Null
$questRel='config/ftbquests/quests/chapters/local_guide_01_test.snbt'
$publishedQuest=Make-File $testRoot 'published-quest.snbt' 'published quest'
$runtimeQuest=Make-File $questRoot $questRel 'verified FTB rewrite'
$questEntry=Entry $questRel 'new quest'
$questEntry | Add-Member -NotePropertyName previous_forms -NotePropertyValue @([pscustomobject]@{published_sha256=(Hash-File $publishedQuest);runtime_sha256=(Hash-File $runtimeQuest)})
$questManifest=[pscustomobject]@{schema=1;repository=$script:Repo;client_version=4;version='1.3.0';quest_group=$manifest.quest_group;files=@($questEntry);obsolete=@()}
$questPrevious=[pscustomobject]@{repository=$script:Repo;files=@([pscustomobject]@{path=$questRel;sha256=(Hash-File $publishedQuest)})}
Assert-Manifest $questManifest $questRoot
$questPlan=@(Get-Plan $questRoot $questManifest $questPrevious)
Assert ($questPlan.Count -eq 1) 'verified FTB rewrite can upgrade'
Assert ($questPlan[0].oldHash -eq (Hash-File $runtimeQuest)) 'rollback uses the actual prior quest bytes'
$questPrevious.files[0].sha256='a'*64
Expect-Failure {Get-Plan $questRoot $questManifest $questPrevious} 'rewrite allowance requires the matching previous published hash'
$questPrevious.files[0].sha256=Hash-File $publishedQuest
$null=Make-File $questRoot $questRel 'personal quest changes'
Expect-Failure {Get-Plan $questRoot $questManifest $questPrevious} 'unknown personal quest edits remain protected'
$questEntry.path='config/personal.toml'
Expect-Failure {Assert-Manifest $questManifest $questRoot} 'rewrite allowances cannot relax protection for other configs'
Assert (!(Test-KnownQuestRewrite $questEntry $questPrevious.files[0].sha256 $questEntry.previous_forms[0].runtime_sha256)) 'planning independently restricts rewrite allowances to custom quest chapters'
$questEntry.path=$questRel;$questEntry.previous_forms[0].runtime_sha256='invalid'
Expect-Failure {Assert-Manifest $questManifest $questRoot} 'invalid rewrite checksums are rejected'
Write-Host "ALL $script:passed CHECKS PASSED. Fixtures: $testRoot"
