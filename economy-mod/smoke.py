"""Launch an isolated, minimal client solely to validate real Mixin application.
Uses a local test identity and stops during common setup, before opening a world.
No account credentials, user saves, or active profile configuration are used.
"""
import tempfile
import json
import pathlib
import shutil
import subprocess
import zipfile
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--game-closed', action='store_true', help='Required: confirm Minecraft is closed before launching a second client')
if not parser.parse_args().game_closed:
    parser.error('This launches Minecraft/NeoForge. Close the game first, then explicitly pass --game-closed.')
# Never launch a second JVM beside an existing game. Do not print process
# command lines: launcher arguments can contain authentication information.
guard = subprocess.run(['powershell', '-NoProfile', '-Command',
    "$p = Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object { $_.Name -match '^javaw?\\.exe$' }; if ($p) { exit 9 }"],
    capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
if guard.returncode:
    raise SystemExit('Java is already running or the process check failed. No test client was started.')

HERE = pathlib.Path(__file__).resolve().parent
PROFILE = HERE.parent.parent / 'CustomATM (1)'
INSTALL = PROFILE.parent.parent / 'Install'
BUILD = HERE.parent / '.work/economy-build'
SMOKE = pathlib.Path(tempfile.mkdtemp(prefix='customatm-economy-probe-'))
print('Probe directory:', SMOKE, flush=True)
(SMOKE / 'mods').mkdir(parents=True, exist_ok=True)
(SMOKE / 'natives').mkdir(exist_ok=True)
cp = (BUILD / 'compile-classpath.txt').read_text()
cp += ';' + (BUILD / 'classes').as_posix()
testclasses = BUILD / 'probe-classes'
testclasses.mkdir(exist_ok=True)
args = ['--release', '21', '-proc:none', '-classpath', cp, '-d', testclasses.as_posix()]
args += [p.as_posix() for p in (HERE / 'src/smoke/java').rglob('*.java')]
argfile = BUILD / 'probe-javac.args'
argfile.write_text('\n'.join('"' + a + '"' for a in args))
subprocess.run([shutil.which('javac'), '@' + str(argfile)], check=True)
with zipfile.ZipFile(SMOKE / 'mods/customatm-economy-probe.jar', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in testclasses.rglob('*.class'): z.write(p, p.relative_to(testclasses).as_posix())
    z.writestr('META-INF/neoforge.mods.toml', '''modLoader="javafml"
loaderVersion="[4,)"
license="MIT"
[[mods]]
modId="customatm_economy_probe"
version="1.0.0"
displayName="Isolated bridge validation"
[[dependencies.customatm_economy_probe]]
modId="customatm_economy"
type="required"
versionRange="[1.0.0]"
ordering="AFTER"
side="BOTH"
''')
for p in [PROFILE / 'mods/dyneco-1.2.0.jar', BUILD / 'customatm-economy-1.0.0.jar']:
    shutil.copy2(p, SMOKE / 'mods' / p.name)

shutil.copytree(HERE.parent / 'pack/snapshot/config/customatm_economy', SMOKE / 'config/customatm_economy')

neo = json.loads((INSTALL / 'versions/neoforge-21.1.259/neoforge-21.1.259.json').read_text(encoding='utf-8-sig'))
vanilla = json.loads((INSTALL / 'versions/1.21.1/1.21.1.json').read_text(encoding='utf-8-sig'))
def allowed(entry):
    if not entry.get('rules'): return True
    result = False
    for rule in entry['rules']:
        os = rule.get('os', {})
        matches = os.get('name', 'windows') == 'windows' and os.get('arch', 'amd64') in ('amd64', 'x86_64') and not rule.get('features')
        if matches: result = rule['action'] == 'allow'
    return result

libraries = {}
for version in (neo, vanilla):
    for lib in version['libraries']:
        if not allowed(lib): continue
        if 'natives-' in lib['name'] and not lib['name'].endswith(':natives-windows'): continue
        parts = lib['name'].split(':')
        key = ':'.join(parts[:2] + parts[3:])
        a = (lib.get('downloads') or {}).get('artifact')
        if a and key not in libraries:
            p = INSTALL / 'libraries' / a['path']
            if not p.exists(): raise FileNotFoundError(p)
            libraries[key] = p
launcher_cp = ';'.join(p.as_posix() for p in [*libraries.values(), INSTALL / 'versions/neoforge-21.1.259/neoforge-21.1.259.jar'])
substitutions = {
    'version_name': 'neoforge-21.1.259', 'library_directory': (INSTALL / 'libraries').as_posix(),
    'classpath_separator': ';', 'natives_directory': (SMOKE / 'natives').as_posix(),
    'launcher_name': 'local-integration-test', 'launcher_version': '1', 'classpath': launcher_cp
}
def expand(s):
    for key, value in substitutions.items(): s = s.replace('${' + key + '}', value)
    if '${' in s: raise ValueError('Unresolved JVM argument: ' + s)
    return s
jvm = ['-Xmx2G', '-Dfml.earlyprogresswindow=false', '-Dmixin.debug.export=true']
for version in (vanilla, neo):
    for a in version['arguments']['jvm']:
        if isinstance(a, str): jvm.append(expand(a))
        elif allowed(a):
            val = a['value']
            jvm.extend(expand(s) for s in (val if isinstance(val, list) else [val]))
game = ['--username', 'IntegrationTest', '--version', 'neoforge-21.1.259', '--gameDir', SMOKE.as_posix(),
        '--assetsDir', (INSTALL / 'assets').as_posix(), '--assetIndex', vanilla['assetIndex']['id'],
        '--uuid', '00000000000000000000000000000001', '--accessToken', '0', '--userType', 'legacy',
        '--versionType', 'release', '--width', '854', '--height', '480', *neo['arguments']['game']]
launch = jvm + [neo['mainClass']] + game
launchfile = BUILD / 'smoke-java.args'
launchfile.write_text('\n'.join('"' + a.replace('"', '\\"') + '"' for a in launch), encoding='utf-8')
java = INSTALL / 'java/java-runtime-delta/bin/java.exe'
with (SMOKE / 'launcher.log').open('w', encoding='utf-8') as out:
    try:
        result = subprocess.run([str(java), '@' + str(launchfile)], cwd=SMOKE, stdout=out, stderr=subprocess.STDOUT,
                                timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        print('Runtime exit code:', result.returncode)
    except subprocess.TimeoutExpired:
        print('Runtime probe timed out; see launcher.log')
        raise
report = SMOKE / 'probe-result.txt'
if report.exists(): print(report.read_text())
else: print((SMOKE / 'launcher.log').read_text(encoding='utf-8', errors='replace')[-6500:])
if not report.exists() or not report.read_text().startswith('PASS:'):
    raise SystemExit(1)
