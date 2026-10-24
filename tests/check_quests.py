"""Validate all original quest chapters without starting Minecraft."""
import collections
import json
import math
import pathlib
import re
import unittest
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
SNAP=ROOT/'pack/snapshot'
CH=SNAP/'config/ftbquests/quests/chapters'
LANG=SNAP/'config/ftbquests/quests/lang/en_us/chapters'
LEGACY=json.loads((ROOT/'quest-source/legacy-ids.json').read_text())
CHAPTERS=[(p,json.loads(p.read_text(encoding='utf-8'))) for p in sorted(CH.glob('local_guide_*.snbt'))]

class QuestChecks(unittest.TestCase):
    def test_unique_ids_and_references(self):
        seen=set();quests={}
        for path,c in CHAPTERS:
            for value in [c,*c['quests'],*c.get('images',[])]:
                self.assertRegex(value['id'],r'^[0-9A-F]{16}$')
                self.assertNotIn(value['id'],seen);seen.add(value['id'])
            for q in c['quests']:
                quests[q['id']]=q
                for task in q['tasks']+q.get('rewards',[]):
                    self.assertNotIn(task['id'],seen);seen.add(task['id'])
                    self.assertIn(task['type'],('item','checkmark','dimension','xp'))
        visiting=set();done=set()
        def visit(id):
            self.assertIn(id,quests)
            self.assertNotIn(id,visiting,'Dependency cycle at '+id)
            if id in done:return
            visiting.add(id)
            for dep in quests[id]['dependencies']:visit(dep)
            visiting.remove(id);done.add(id)
        for id in quests:visit(id)
        self.assertEqual(len(quests),302)

    def test_preserved_progress_ids(self):
        current={q['id']:q for _,c in CHAPTERS for q in c['quests']}
        for chapter in LEGACY.values():
            for old in chapter['quests']:
                self.assertIn(old['id'],current)
                # Existing item tasks retain their IDs when their item remains.
                for t in old['tasks']:
                    if t['type']=='item':
                        candidates=[x for x in current[old['id']]['tasks'] if x['type']=='item' and x['item']['id']==t['item']['id']]
                        if candidates:self.assertEqual(candidates[0]['id'],t['id'])

    def test_language_assets_and_layout(self):
        image_count=0
        for path,c in CHAPTERS:
            lang=json.loads((LANG/path.name).read_text(encoding='utf-8'))
            self.assertIn('chapter.'+c['id']+'.title',lang)
            for i,q in enumerate(c['quests']):
                prefix='quest.'+q['id']
                self.assertTrue(lang[prefix+'.title']);desc=lang[prefix+'.quest_desc']
                self.assertGreater(len(' '.join(desc)),300,prefix)
                for ref in re.findall(r'\{image:([^ ]+)', ' '.join(desc)):
                    namespace,asset=ref.split(':',1)
                    self.assertTrue((SNAP/'kubejs/assets'/namespace/asset).is_file(),ref);image_count+=1
                for other in c['quests'][i+1:]:self.assertGreaterEqual(math.hypot(q['x']-other['x'],q['y']-other['y']),1.25)
                for t in q['tasks']:
                    if t['type']=='item':
                        self.assertFalse(t.get('consume_items',False))
                        self.assertGreater(t['count'],0)
                self.assertTrue(all(r['type']=='xp' and r['xp']<=75 for r in q.get('rewards',[])))
            for img in c['images']:
                namespace,asset=img['image'].split(':',1)
                self.assertTrue((SNAP/'kubejs/assets'/namespace/asset).is_file())
        self.assertEqual(image_count,28)

    def test_items_exist_in_installed_pack(self):
        # Most IDs are evidenced by the pack's runtime DynEco registry report.
        known={x[2:] for x in json.loads((SNAP/'config/customatm_economy/catalog.json').read_text())['items'] if x.startswith('i:')}
        # The tablet is deliberately excluded from trading; corroborate its model.
        needed={t['item']['id'] for _,c in CHAPTERS for q in c['quests'] for t in q['tasks'] if t['type']=='item'}-known
        jars=list((ROOT.parent/'CustomATM (1)/mods').glob('*.jar'))
        # The new mod is staged while the host is playing; verify its pinned bytes
        # before using its resources as registry evidence.
        import hashlib
        for entry in json.loads((ROOT/'pack/ballistix-additions.json').read_text()):
            jar=ROOT/'.work/ballistix'/pathlib.PurePosixPath(entry['path']).name
            self.assertEqual(hashlib.sha256(jar.read_bytes()).hexdigest(),entry['sha256'])
            jars.append(jar)
        for jar in jars:
            if not needed:break
            with zipfile.ZipFile(jar) as z:
                for id in list(needed):
                    ns,name=id.split(':',1)
                    if f'assets/{ns}/models/item/{name}.json' in z.namelist():needed.remove(id)
        self.assertFalse(needed,needed)

    def test_progression_and_optional_paths(self):
        item_quests=0
        for path,c in CHAPTERS:
            byid={q['id']:q for q in c['quests']}
            for q in c['quests']:
                item_quests+=any(t['type']=='item' for t in q['tasks'])
                if not q.get('optional'):
                    for dep in q['dependencies']:self.assertFalse(byid[dep].get('optional'),(path.name,q['id'],dep))
        self.assertGreaterEqual(item_quests,220)
        economy=next(c for p,c in CHAPTERS if 'economy' in p.name)
        self.assertTrue(all(q.get('optional') for q in economy['quests'][13:17]))
        ad=next(c for p,c in CHAPTERS if 'ad_astra' in p.name)
        self.assertEqual({t['dimension'] for q in ad['quests'] for t in q['tasks'] if t['type']=='dimension'},{'ad_astra:moon','ad_astra:mars','ad_astra:glacio'})

    def test_ballistix_workshops(self):
        c=next(c for p,c in CHAPTERS if 'ballistix' in p.name)
        self.assertEqual(len(c['quests']),33)
        self.assertEqual(c['order_index'],10)
        self.assertEqual(c['group'],'28D38D1EC21B4002')
        self.assertEqual(len(c['images']),5)
        self.assertEqual(sum(any(t['type']=='item' for t in q['tasks']) for q in c['quests']),24)
        self.assertEqual(sum(q['shape']=='diamond' and q.get('rewards') is not None for q in c['quests']),5)
        forbidden={'ballistix:'+p+n for p in ('','minecart') for n in ('nuclear','antimatter','largeantimatter','darkmatter')}
        self.assertFalse(any(t['item']['id'] in forbidden for q in c['quests'] for t in q['tasks'] if t['type']=='item'))

if __name__=='__main__':unittest.main()
