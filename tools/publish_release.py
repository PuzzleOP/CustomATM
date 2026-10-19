"""Publish verified release assets to the user-selected repository using Git Credential Manager."""
import argparse,hashlib,json,os,pathlib,subprocess,urllib.request,urllib.error,urllib.parse
ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO='PuzzleOP/CustomATM'
def credentials():
    env=os.environ.copy();env.update(GIT_TERMINAL_PROMPT='0',GCM_INTERACTIVE='never')
    p=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',capture_output=True,text=True,env=env,check=True,timeout=30)
    fields=dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line)
    if not fields.get('password'):raise RuntimeError('Sign in to GitHub using Git Credential Manager first.')
    return fields['password']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--version',required=True);parser.add_argument('--notes',type=pathlib.Path,required=True)
    a=parser.parse_args();folder=ROOT/'dist'/a.version
    manifest=json.loads((folder/'pack-manifest.json').read_text())
    assert manifest['version']==a.version and manifest['repository']==REPO
    assert hashlib.sha256((folder/'customatm-payload.zip').read_bytes()).hexdigest()==manifest['payload']['sha256']
    token=credentials()
    def api(path,method='GET',value=None,raw=None,ctype='application/json'):
        url=path if path.startswith('https://') else 'https://api.github.com/'+path
        assert urllib.parse.urlparse(url).hostname in ('api.github.com','uploads.github.com')
        data=raw if raw is not None else (json.dumps(value).encode() if value is not None else None)
        req=urllib.request.Request(url,data=data,method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','User-Agent':'CustomATM-release-publisher','Content-Type':ctype})
        # Do not follow a redirect carrying an Authorization header to another host.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args,**kwargs):return None
        with urllib.request.build_opener(NoRedirect).open(req,timeout=120) as response:return json.load(response)
    assert api('user')['login'].lower()=='puzzleop'
    repo=api('repos/'+REPO);assert repo['permissions']['push']
    sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    remote=api('repos/'+REPO+'/commits/'+sha);assert remote['sha']==sha
    tag='v'+a.version
    existing=next((r for r in api('repos/'+REPO+'/releases?per_page=100') if r['tag_name']==tag),None)
    if existing and not existing['draft']:raise RuntimeError('This version is already published. Use a new version.')
    release=existing or api('repos/'+REPO+'/releases','POST',{'tag_name':tag,'target_commitish':sha,'name':'CustomATM '+a.version,'body':a.notes.read_text(encoding='utf-8'),'draft':True,'prerelease':False})
    expected={}
    for name in ['pack-manifest.json','customatm-payload.zip','CustomATM-Setup.zip']:
        data=(folder/name).read_bytes();digest='sha256:'+hashlib.sha256(data).hexdigest();expected[name]=digest
        prior=next((x for x in release.get('assets',[]) if x['name']==name),None)
        if prior:
            if prior.get('digest')!=digest:raise RuntimeError('Draft contains different bytes: '+name)
            continue
        endpoint=release['upload_url'].split('{')[0]+'?name='+urllib.parse.quote(name)
        asset=api(endpoint,'POST',raw=data,ctype='application/zip' if name.endswith('.zip') else 'application/json')
        if asset.get('digest')!=digest:raise RuntimeError('GitHub checksum mismatch: '+name)
        print('Uploaded and verified:',name,len(data),'bytes')
    verified=api('repos/'+REPO+'/releases/'+str(release['id']))
    assert all(any(x['name']==name and x.get('digest')==digest for x in verified['assets']) for name,digest in expected.items())
    result=api('repos/'+REPO+'/releases/'+str(release['id']),'PATCH',{'draft':False,'make_latest':'true'})
    print('Published:',result['html_url'])
    (folder/'published.json').write_text(json.dumps({'url':result['html_url'],'id':result['id'],'tag':tag,'commit':sha,'asset_hashes':expected},indent=2))
if __name__=='__main__':main()
