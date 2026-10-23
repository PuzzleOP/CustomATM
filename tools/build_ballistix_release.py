"""Build the fixed 1.4.0 -> 1.5.0 Ballistix overlay without accessing a live profile."""
import copy
import hashlib
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / 'dist/1.4.0'
OUT = ROOT / 'dist/1.5.0'
POLICY = 'kubejs/server_scripts/local_customizations/ballistix_survival.js'
CONFIG = 'config/ballistix-common.toml'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert not (OUT / 'published.json').exists(), 'Never overwrite a published release'
    receipt = json.loads((BASE / 'published.json').read_text())
    assert receipt['tag'] == 'v1.4.0'
    for name in ('pack-manifest.json', 'customatm-payload.zip'):
        assert receipt['asset_hashes'][name] == 'sha256:' + sha((BASE / name).read_bytes())
    old = json.loads((BASE / 'pack-manifest.json').read_text())
    assert old['version'] == '1.4.0' and old['repository'] == 'PuzzleOP/CustomATM'
    assert sha((BASE / 'customatm-payload.zip').read_bytes()) == old['payload']['sha256']
    current = json.loads((ROOT / 'pack/current-manifest.json').read_text())
    assert current == old or current['version'] == '1.5.0', 'Review unrelated changes first'
    expected = {f['path']: f for f in old['files'] if f['source'] == 'payload'}
    payload = {}
    with zipfile.ZipFile(BASE / 'customatm-payload.zip') as z:
        assert len(z.namelist()) == len(set(z.namelist()))
        assert set(z.namelist()) == set(expected)
        for path, entry in expected.items():
            data = z.read(path)
            assert sha(data) == entry['sha256'] and len(data) == entry['size'], path
            payload[path] = data
    additions = json.loads((ROOT / 'pack/ballistix-additions.json').read_text())
    assert {f['path'] for f in additions} == {
        'mods/ballistix-1.21.1-1.2.3.jar', 'mods/voltaic-1.21.1-1.2.0.jar'}
    sources = json.loads((ROOT / 'pack/extra-sources.json').read_text())
    for entry in additions:
        name = pathlib.PurePosixPath(entry['path']).name
        data = (ROOT / '.work/ballistix' / name).read_bytes()
        assert sha(data) == entry['sha256'] and len(data) == entry['size'], name
        assert entry['source'] == 'url' and entry['url'] == sources[name]
        assert not any(f['path'] == entry['path'] for f in old['files'])
    for path in (POLICY, CONFIG):
        assert path not in expected
        payload[path] = (ROOT / 'pack/snapshot' / path).read_bytes()
        additions.append({'path': path, 'source': 'payload',
                          'sha256': sha(payload[path]), 'size': len(payload[path])})
    manifest = copy.deepcopy(old)
    manifest['version'] = '1.5.0'
    manifest['files'] = sorted(manifest['files'] + additions, key=lambda f: f['path'])
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT / 'customatm-payload.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for path, data in sorted(payload.items()):
            info = zipfile.ZipInfo(path, (2026, 10, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    manifest['payload']['sha256'] = sha((OUT / 'customatm-payload.zip').read_bytes())
    (OUT / 'pack-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(OUT / 'CustomATM-Setup.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted((ROOT / 'client').iterdir()):
            if path.is_file():
                z.write(path, path.name)
        z.write(ROOT / 'FRIEND-SETUP.md', 'READ-ME-FIRST.md')
    (ROOT / 'pack/current-manifest.json').write_bytes((OUT / 'pack-manifest.json').read_bytes())
    print(json.dumps({'version': '1.5.0', 'unchanged_files': len(old['files']),
                      'added': [f['path'] for f in additions], 'live_profile_modified': False}, indent=2))


if __name__ == '__main__':
    main()
