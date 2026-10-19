"""Compile/package the native addon only. Never starts Minecraft or edits a profile."""
import argparse, hashlib, json, pathlib, shutil, subprocess, tempfile, zipfile
HERE=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--profile',type=pathlib.Path,required=True);a=ap.parse_args()
profile=a.profile.resolve();install=profile.parent.parent/'Install';build=HERE.parent/'.work/arcade-build';build.mkdir(parents=True,exist_ok=True)
classes=pathlib.Path(tempfile.mkdtemp(prefix='classes-',dir=build))
instance=json.loads((profile/'minecraftinstance.json').read_text(encoding='utf-8-sig'))
neo=json.loads(instance['baseModLoader']['versionJson']);vanilla=json.loads((install/'versions/1.21.1/1.21.1.json').read_text(encoding='utf-8-sig'))
libs=[install/'libraries/net/neoforged/neoforge/21.1.259/neoforge-21.1.259-client.jar',install/'libraries/net/neoforged/neoforge/21.1.259/neoforge-21.1.259-universal.jar',install/'libraries/net/minecraft/client/1.21.1-20240808.144430/client-1.21.1-20240808.144430-srg.jar',profile/'mods/casinomod-1.0.0.jar']
for v in [neo,vanilla]:
 for lib in v['libraries']:
  art=(lib.get('downloads') or {}).get('artifact')
  if art:
   p=install/'libraries'/art['path']
   if p.exists() and p not in libs:libs.append(p)
cp=';'.join(p.as_posix() for p in libs);(build/'compile-classpath.txt').write_text(cp)
args=['--release','21','-proc:none','-encoding','UTF-8','-classpath',cp,'-d',classes.as_posix(),*[p.as_posix() for p in sorted((HERE/'src/main/java').rglob('*.java'))]]
argfile=build/'javac.args';argfile.write_text('\n'.join('"'+s+'"' for s in args))
subprocess.run([shutil.which('javac'),'-J-Xmx128m','@'+str(argfile)],check=True)
jar=build/'customatm-arcade-0.2.0.jar'
with zipfile.ZipFile(jar,'w',zipfile.ZIP_DEFLATED) as z:
 for root in [classes,HERE/'src/main/resources']:
  for p in sorted(root.rglob('*')):
   if p.is_file():
    info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,10,19,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,p.read_bytes())
print(jar);print('SHA256',hashlib.sha256(jar.read_bytes()).hexdigest())
(build/'classes-path.txt').write_text(str(classes))
