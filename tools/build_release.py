"""Build a versioned overlay for the fixed ATM10 8.3 base. No credentials or saves are packaged."""
import argparse,hashlib,json,pathlib,re,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
def digest(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--profile',type=pathlib.Path,required=True);ap.add_argument('--version',required=True)
    a=ap.parse_args();p=a.profile.resolve();version=a.version
    assert re.fullmatch(r'\d+\.\d+\.\d+',version)
    out=ROOT/'dist'/version;out.mkdir(parents=True,exist_ok=True)
    instance=json.loads((p/'minecraftinstance.json').read_text(encoding='utf-8-sig'))
    receipt_path=p/'.customatm/bootstrap.json'
    receipt=json.loads(receipt_path.read_text()) if receipt_path.exists() else {}
    assert (instance['projectID']==925200 and instance['fileID']==9190157) or (receipt.get('repository')=='PuzzleOP/CustomATM' and receipt.get('complete') and receipt.get('instance_id')==instance['guid'] and receipt.get('archive_sha256')=='24440fb355de69b28af6ff18556b5d0598bb93570b2b745552cdb1bcb5448c8f')
    assert instance['baseModLoader']['name']=='neoforge-21.1.259'
    previous=ROOT/'pack/current-manifest.json'
    urls={pathlib.PurePosixPath(f['path']).name:f['url'] for f in json.loads(previous.read_text())['files'] if f.get('url')} if previous.exists() else {}
    urls.update({x['installedFile']['fileName']:x['installedFile']['downloadUrl'] for x in instance['installedAddons'] if x['installedFile'].get('downloadUrl')})
    source_info=json.loads((ROOT/'pack/extra-sources.json').read_text())
    urls.update(source_info)
    files=[];payload={}
    for jar in sorted((p/'mods').glob('*.jar')):
        rel='mods/'+jar.name
        entry={'path':rel,'sha256':digest(jar),'size':jar.stat().st_size}
        if jar.name=='atm10-casino-dyneco-1.0.0.jar':entry['source']='payload';payload[rel]=jar
        else:
            url=urls.get(jar.name);assert url and url.startswith('https://'),('Missing original download URL',jar.name)
            entry.update(source='url',url=url)
        files.append(entry)
    # Deliberate allowlist: never recursively publish the live profile's config directory.
    policy=json.loads((ROOT/'pack/managed-paths.json').read_text())
    for pattern in policy['files']:
        matches=sorted(p.glob(pattern));assert matches,('No files for',pattern)
        for src in matches:
            assert src.is_file() and not src.is_symlink(),src
            rel=src.relative_to(p).as_posix()
            assert rel not in payload
            assert '/saves/' not in rel and not src.name.endswith('_merged.snbt')
            payload[rel]=src
            files.append({'path':rel,'sha256':digest(src),'size':src.stat().st_size,'source':'payload'})
    with zipfile.ZipFile(out/'customatm-payload.zip','w',zipfile.ZIP_DEFLATED) as z:
        for rel,src in sorted(payload.items()):
            info=zipfile.ZipInfo(rel,(2026,10,19,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,src.read_bytes())
    manifest={'schema':1,'repository':'PuzzleOP/CustomATM','client_version':3,'version':version,
              'base':{'name':'All the Mods 10 - ATM10','version':'8.3','minecraft':'1.21.1','loader':'neoforge-21.1.259','curseforge_project_id':925200,'curseforge_file_id':9190157},
              'quest_group':'28D38D1EC21B4002','files':sorted(files,key=lambda f:f['path']),
              'obsolete':json.loads((ROOT/'pack/obsolete.json').read_text()),
              'payload':{'name':'customatm-payload.zip','sha256':digest(out/'customatm-payload.zip')}}
    # Keep removals cumulative so a new friend starting from the original base also
    # removes jars retired by earlier CustomATM releases.
    previous=ROOT/'pack/current-manifest.json'
    removals={x['path']:x for x in manifest['obsolete']}
    current_paths={x['path'] for x in files}
    if previous.exists():
        for old in json.loads(previous.read_text())['files']:
            if old['path'] not in current_paths:removals[old['path']]={'path':old['path'],'sha256':old['sha256']}
    manifest['obsolete']=[v for k,v in sorted(removals.items()) if k not in current_paths]
    (ROOT/'pack/obsolete.json').write_text(json.dumps(manifest['obsolete'],indent=2)+'\n')
    (out/'pack-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    with zipfile.ZipFile(out/'CustomATM-Setup.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted((ROOT/'client').iterdir()):
            if f.is_file():z.write(f,f.name)
        z.write(ROOT/'FRIEND-SETUP.md','READ-ME-FIRST.md')
    # Sanitized public snapshot: exact inputs used to build this version, without the base pack's proprietary files.
    snapshots=ROOT/'pack/snapshot';snapshots.mkdir(exist_ok=True)
    for rel,src in payload.items():
        if rel.startswith('mods/'):continue
        dest=snapshots/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes())
    (ROOT/'pack/current-manifest.json').write_bytes((out/'pack-manifest.json').read_bytes())
    print(json.dumps({'version':version,'mods':len(list((p/'mods').glob('*.jar'))),'managed_files':len(files),'payload_files':len(payload),
                      'payload_bytes':(out/'customatm-payload.zip').stat().st_size,'setup_bytes':(out/'CustomATM-Setup.zip').stat().st_size},indent=2))
if __name__=='__main__':main()
