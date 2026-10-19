"""Add the verified arcade addon to a published release without touching a live profile."""
import argparse, copy, hashlib, json, pathlib, re, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[1]
def digest(data): return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-version', required=True)
    ap.add_argument('--version', required=True)
    a = ap.parse_args()
    for version in (a.base_version, a.version): assert re.fullmatch(r'\d+\.\d+\.\d+', version)
    assert tuple(map(int, a.version.split('.'))) > tuple(map(int, a.base_version.split('.')))
    base = ROOT / 'dist' / a.base_version
    out = ROOT / 'dist' / a.version
    assert not (out / 'published.json').exists(), 'Never overwrite a published release'
    published = json.loads((base / 'published.json').read_text())
    manifest_bytes = (base / 'pack-manifest.json').read_bytes()
    payload_bytes = (base / 'customatm-payload.zip').read_bytes()
    assert published['tag'] == 'v' + a.base_version
    assert published['asset_hashes']['pack-manifest.json'] == 'sha256:' + digest(manifest_bytes)
    assert published['asset_hashes']['customatm-payload.zip'] == 'sha256:' + digest(payload_bytes)
    old = json.loads(manifest_bytes)
    assert old['repository'] == 'PuzzleOP/CustomATM' and old['version'] == a.base_version
    assert digest(payload_bytes) == old['payload']['sha256']
    current = json.loads((ROOT / 'pack/current-manifest.json').read_text())
    assert current == old or current['version'] == a.version, 'Unrelated pack changes must be reviewed first'
    build = ROOT / '.work/arcade-build'
    validation = json.loads((build / 'validation.json').read_text())
    assert validation['offline_checks'] == 'passed'
    assert validation['artifact'] == 'customatm-arcade-0.2.0.jar'
    addon = (build / validation['artifact']).read_bytes()
    assert digest(addon) == validation['sha256'] and len(addon) == validation['bytes']
    casino = next(f for f in old['files'] if f['path'] == 'mods/casinomod-1.0.0.jar')
    assert casino['sha256'] == validation['casino_sha256']
    with zipfile.ZipFile(build / validation['artifact']) as z:
        assert 'local/customatm/arcade/client/RedstoneGameScreen.class' in z.namelist()
        assert 'customatm_arcade.mixins.json' in z.namelist()
        assert not any(n.startswith(('net/minecraft/', 'com/togascasino/')) for n in z.namelist())
    payload = {}
    expected = {f['path']: f for f in old['files'] if f['source'] == 'payload'}
    with zipfile.ZipFile(base / 'customatm-payload.zip') as z:
        assert len(z.namelist()) == len(set(z.namelist()))
        assert set(z.namelist()) == set(expected)
        for name, entry in expected.items():
            data = z.read(name)
            assert digest(data) == entry['sha256'] and len(data) == entry['size'], name
            payload[name] = data
    name = 'mods/' + validation['artifact']
    assert not any(f['path'].startswith('mods/customatm-arcade-') for f in old['files'])
    payload[name] = addon
    manifest = copy.deepcopy(old)
    manifest['version'] = a.version
    manifest['files'].append({'path': name, 'sha256': digest(addon), 'size': len(addon), 'source': 'payload'})
    manifest['files'].sort(key=lambda f: f['path'])
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out / 'customatm-payload.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for path, data in sorted(payload.items()):
            info = zipfile.ZipInfo(path, (2026, 10, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    manifest['payload']['sha256'] = digest((out / 'customatm-payload.zip').read_bytes())
    (out / 'pack-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(out / 'CustomATM-Setup.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted((ROOT / 'client').iterdir()):
            if path.is_file(): z.write(path, path.name)
        z.write(ROOT / 'FRIEND-SETUP.md', 'READ-ME-FIRST.md')
    (ROOT / 'pack/current-manifest.json').write_bytes((out / 'pack-manifest.json').read_bytes())
    print(json.dumps({'version': a.version, 'base_release': a.base_version, 'added': name,
                      'unchanged_files': len(old['files']), 'client_version': manifest['client_version'],
                      'payload_bytes': (out / 'customatm-payload.zip').stat().st_size,
                      'live_profile_modified': False}, indent=2))

if __name__ == '__main__': main()
