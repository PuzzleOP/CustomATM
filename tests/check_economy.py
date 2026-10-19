"""Fast catalogue/packaging checks. Does not launch Minecraft or read worlds."""
import csv
import json
import math
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / 'pack/snapshot/config/customatm_economy/catalog.json').read_text())
ITEMS = CATALOG['items']


class CatalogueChecks(unittest.TestCase):
    def test_coverage_and_validity(self):
        with (ROOT / 'economy/price-audit.csv').open(newline='') as file:
            audit = {row['commodity']: row for row in csv.DictReader(file)}
        self.assertEqual(set(ITEMS), set(audit))
        self.assertGreater(len(ITEMS), 64000)
        for item, value in ITEMS.items():
            self.assertTrue(math.isfinite(value['value']) and value['value'] >= .01, item)
            self.assertIn(value['group'], ('bulk', 'farming', 'resources', 'manufactured'))
            self.assertEqual(value['value'], float(audit[item]['new_base']), item)
            self.assertEqual(value['group'], audit[item]['income_group'], item)

    def test_progression_regressions(self):
        self.assertEqual(ITEMS['i:minecraft:cobblestone'], {'value': .01, 'group': 'bulk'})
        self.assertEqual(ITEMS['i:minecraft:wheat']['group'], 'farming')
        self.assertEqual(ITEMS['i:minecraft:diamond']['group'], 'resources')
        self.assertLess(ITEMS['i:minecraft:diamond_pickaxe']['value'], 500)
        self.assertGreater(ITEMS['i:minecraft:diamond_pickaxe']['value'], 300)
        self.assertGreaterEqual(ITEMS['i:allthetweaks:atm_star_shard']['value'], 10000)
        self.assertEqual(ITEMS['i:allthetweaks:atm_star_block']['value'], 9 * ITEMS['i:allthetweaks:atm_star']['value'])
        self.assertEqual(ITEMS['i:kubejs:dirt_cell']['group'], 'manufactured')
        self.assertEqual(ITEMS['i:allthecompressed:nether_star_block_3x']['group'], 'resources')

    def test_compression_conservation(self):
        bases = json.loads((ROOT / 'economy/compression-bases.json').read_text())
        tested = 0
        for item, value in ITEMS.items():
            match = re.fullmatch(r'i:allthecompressed:(.+)_(\d+)x', item)
            if not match:
                continue
            self.assertIn(match[1], bases, 'No verified recipe base: ' + item)
            base = bases[match[1]]
            level = int(match[2])
            if base not in ITEMS:
                base = 'i:allthecompressed:' + match[1] + '_1x'
                level -= 1
            expected = ITEMS[base]['value'] * 9 ** level
            self.assertTrue(math.isclose(value['value'], expected, rel_tol=2e-5, abs_tol=1e-6), item)
            self.assertEqual(value['group'], ITEMS[base]['group'], item)
            tested += 1
        self.assertGreater(tested, 1500)

    def test_release_allowlist(self):
        paths = json.loads((ROOT / 'pack/managed-paths.json').read_text())['files']
        self.assertIn('config/customatm_economy/catalog.json', paths)
        self.assertNotIn('config/*', paths)
        self.assertEqual(CATALOG['schema'], 1)


if __name__ == '__main__':
    unittest.main()
