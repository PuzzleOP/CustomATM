"""Run only bounded compilation, pure Java checks and a headless image renderer."""
import argparse, hashlib, json, pathlib, subprocess, zipfile
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parent
ap=argparse.ArgumentParser();ap.add_argument('--profile',type=pathlib.Path,required=True);a=ap.parse_args()
profile=a.profile.resolve();build=ROOT/'.work/arcade-build';classes=pathlib.Path((build/'classes-path.txt').read_text())
subprocess.run(['javac','-J-Xmx128m','--release','21','-cp',str(classes),'-d',str(classes),*[str(p) for p in (HERE/'tests').glob('*.java')]],check=True)
subprocess.run(['java','-Xmx64m','-Djava.awt.headless=true','-cp',str(classes),'ArcadeChecks'],check=True)
subprocess.run(['java','-Xmx64m','-Djava.awt.headless=true','-cp',str(classes),'GameChecks'],check=True)
# Vanilla's bitmap font is used locally to compare type. It is never packaged.
vanilla=profile.parent.parent/'Install/versions/1.21.1/1.21.1.jar'
with zipfile.ZipFile(vanilla) as z:
 provider=next(p for p in json.loads(z.read('assets/minecraft/font/include/default.json'))['providers'] if p.get('file')=='minecraft:font/ascii.png')
 (build/'ascii.png').write_bytes(z.read('assets/minecraft/textures/font/ascii.png'))
 (build/'ascii-chars.txt').write_text(''.join(provider['chars']),encoding='utf-8')
 for item in ['coal','iron_ingot','gold_ingot','emerald','diamond','netherite_ingot','nether_star','gold_nugget','iron_nugget','redstone']:
  (build/('item-'+item+'.png')).write_bytes(z.read('assets/minecraft/textures/item/'+item+'.png'))
subprocess.run(['java','-Xmx128m','-Djava.awt.headless=true','-cp',str(classes),'RenderPreview',str(HERE/'src/main/resources/assets/customatm_arcade/textures/gui'),str(build),str(HERE/'design/preview')],check=True)
subprocess.run(['java','-Xmx128m','-Djava.awt.headless=true','-cp',str(classes),'RenderAllPreview',str(HERE/'src/main/resources/assets/customatm_arcade/textures/gui'),str(build),str(HERE/'design/preview')],check=True)
jar=build/'customatm-arcade-0.2.0.jar'
with zipfile.ZipFile(jar) as z:
 names=z.namelist()
 assert 'META-INF/neoforge.mods.toml' in names
 assert 'local/customatm/arcade/client/ArcadeClient.class' in names
 assert 'local/customatm/arcade/client/RedstoneCoinScreen.class' in names
 assert 'local/customatm/arcade/client/RedstoneGameScreen.class' in names
 assert 'local/customatm/arcade/client/mixin/ResultDeliveryMixin.class' in names
 assert json.loads(z.read('customatm_arcade.mixins.json'))['injectors']['defaultRequire']==1
 assert len([n for n in names if n.endswith('.png')])==7
 assert not any(n.startswith(('com/togascasino','net/minecraft')) or 'RenderPreview' in n or 'ArcadeChecks' in n for n in names)
 for name,(width,height) in {'skin':(1536,1024),'heads':(1254,1254),'tails':(1254,1254),'shell':(1536,1024),'slot_frame':(1875,839),'card_face':(1024,1536),'card_back':(1024,1536)}.items():
  import struct
  png=z.read('assets/customatm_arcade/textures/gui/'+name+'.png')
  assert struct.unpack('>II',png[16:24])==(width,height)
source=profile/'mods/casinomod-1.0.0.jar'
with zipfile.ZipFile(source) as z:
 for screen in ['CasinoScreen','game/CoinFlipScreen','game/SlotsScreen','game/MinesScreen','game/BlackjackScreen','game/RouletteScreen','game/PlinkoScreen','game/ScratchScreen','game/CrashScreen']:
  assert 'com/togascasino/casinomod/client/screen/'+screen+'.class' in z.namelist()
handler=subprocess.check_output(['javap','-classpath',str(source),'-p','com.togascasino.casinomod.client.ClientPayloadHandler'],text=True)
assert 'public static void handleGameResult(com.togascasino.casinomod.network.payload.GameResultPayload);' in handler
mixin=subprocess.check_output(['javap','-classpath',str(jar),'-p','-v','local.customatm.arcade.client.mixin.ResultDeliveryMixin'],text=True)
assert 'handleGameResult' in mixin and 'remap=false' in mixin and 'cancellable=true' in mixin
server=subprocess.check_output(['javap','-classpath',str(source),'-c','-p','com.togascasino.casinomod.network.ServerPayloadHandler'],text=True)
coin=server.split('private static void coinFlip(')[1].split('private static java.lang.String side(')[0]
for signature in ['double 1.96d','java/lang/Math.round:(D)J','java/util/Random.nextInt:(I)I','String bet']:
 assert signature in coin,signature
screen=subprocess.check_output(['javap','-classpath',str(source),'-c','-p','com.togascasino.casinomod.client.screen.game.CoinFlipScreen'],text=True)
assert 'Method flip:(I)V' in screen and 'String Heads' in screen and 'String Tails' in screen
receipt={'artifact':jar.name,'sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'bytes':jar.stat().st_size,'casino_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'minecraft_launched':False,'installed':False,'runtime_validation':'pending','offline_checks':'passed','preview_states':59,'overview_screens':9}
(build/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
