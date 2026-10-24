"""Package the Ballistix chapter on top of verified 1.5.0; never read a live profile."""
import copy
import hashlib
import json
import pathlib
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'dist/1.5.0'
OUT=ROOT/'dist/1.6.0'

def sha(data):return hashlib.sha256(data).hexdigest()

def main():
    assert not (OUT/'published.json').exists(), 'Never overwrite a published release'
    receipt=json.loads((BASE/'published.json').read_text())
    assert receipt['tag']=='v1.5.0'
    for name in ('pack-manifest.json','customatm-payload.zip'):
        assert receipt['asset_hashes'][name]=='sha256:'+sha((BASE/name).read_bytes())
    old=json.loads((BASE/'pack-manifest.json').read_text())
    assert old['version']=='1.5.0' and old['repository']=='PuzzleOP/CustomATM'
    assert sha((BASE/'customatm-payload.zip').read_bytes())==old['payload']['sha256']
    current=json.loads((ROOT/'pack/current-manifest.json').read_text())
    assert current==old or current['version']=='1.6.0', 'Review unrelated changes first'
    expected={f['path']:f for f in old['files'] if f['source']=='payload'}
    payload={}
    with zipfile.ZipFile(BASE/'customatm-payload.zip') as z:
        assert len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(expected)
        for path,entry in expected.items():
            data=z.read(path)
            assert sha(data)==entry['sha256'] and len(data)==entry['size'],path
            payload[path]=data
    name='local_guide_11_ballistix.snbt'
    paths=['config/ftbquests/quests/'+folder+'/'+name for folder in ('chapters','lang/en_us/chapters')]
    assets='kubejs/assets/customatm/textures/quests/'
    paths += [assets+'ballistix_'+key+'.png' for key in ('overview','power','silo','defense')]
    paths += [assets+f'ballistix_lane_{n}.png' for n in range(5)]
    assert len(paths)==11 and not set(paths).intersection(f['path'] for f in old['files'])
    manifest=copy.deepcopy(old);manifest['version']='1.6.0'
    for path in paths:
        data=(ROOT/'pack/snapshot'/path).read_bytes();payload[path]=data
        manifest['files'].append({'path':path,'source':'payload','sha256':sha(data),'size':len(data)})
    manifest['files'].sort(key=lambda f:f['path'])
    OUT.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(OUT/'customatm-payload.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path,data in sorted(payload.items()):
            info=zipfile.ZipInfo(path,(2026,10,24,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    manifest['payload']['sha256']=sha((OUT/'customatm-payload.zip').read_bytes())
    (OUT/'pack-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(OUT/'CustomATM-Setup.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((ROOT/'client').iterdir()):
            if p.is_file():z.write(p,p.name)
        z.write(ROOT/'FRIEND-SETUP.md','READ-ME-FIRST.md')
    (ROOT/'pack/current-manifest.json').write_bytes((OUT/'pack-manifest.json').read_bytes())
    print(json.dumps({'version':'1.6.0','unchanged_entries':len(old['files']),'additions':paths,'live_profile_modified':False},indent=2))

if __name__=='__main__':main()
