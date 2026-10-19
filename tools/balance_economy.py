"""Generate an ATM10 price catalogue from DynEco's recipe report.

Run against the baseline report, never against this rebalance's output.
All values are base credits; buy/sell spreads and demand apply in game.
"""
import argparse, collections, csv, hashlib, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = {
 'cobblestone':.01,'cobbled_deepslate':.01,'stone':.01,'deepslate':.01,
 'dirt':.02,'sand':.02,'red_sand':.02,'gravel':.02,'netherrack':.02,
 'andesite':.02,'diorite':.02,'granite':.02,'basalt':.02,'blackstone':.02,
 'end_stone':.04,'obsidian':.25,'clay_ball':.04,'clay':.16,'glass':.03,
 'snowball':.01,'snow_block':.04,'ice':.02,'packed_ice':.18,'blue_ice':1.62,
 'oak_log':.08,'oak_planks':.02,'stick':.01,'bamboo':.01,'sugar_cane':.03,
 'cactus':.02,'kelp':.01,'moss_block':.02,'wheat':.10,'wheat_seeds':.02,
 'carrot':.10,'potato':.10,'beetroot':.10,'pumpkin':.15,'melon_slice':.03,
 'sugar':.03,'paper':.03,'bone':.20,'bone_meal':.066667,'rotten_flesh':.05,
 'string':.15,'spider_eye':.20,'gunpowder':.30,'slime_ball':.20,'leather':.30,
 'feather':.10,'egg':.10,'ink_sac':.15,'glow_ink_sac':.25,'ender_pearl':2,
 'blaze_rod':3,'blaze_powder':1.5,'ghast_tear':5,'magma_cream':.50,
 'prismarine_shard':.30,'prismarine_crystals':.50,'phantom_membrane':3,
 'shulker_shell':15,'nether_star':250,'wither_skeleton_skull':30,
 'coal':1,'charcoal':.50,'iron_ingot':8,'copper_ingot':4,'gold_ingot':12,
 'redstone':1,'lapis_lazuli':2,'quartz':2,'diamond':100,'emerald':30,
 'netherite_scrap':240,'netherite_ingot':1000,'ancient_debris':240,
 'amethyst_shard':1,'glowstone_dust':1,'flint':.05,'honeycomb':.20,
 'apple':.15,'sweet_berries':.08,'glow_berries':.10,'cocoa_beans':.10,
 'beef':.25,'porkchop':.25,'chicken':.20,'mutton':.25,'rabbit':.30,
 'cod':.15,'salmon':.20,'tropical_fish':.20,'pufferfish':.30,
 'totem_of_undying':100,'nautilus_shell':10,'sponge':5,'wet_sponge':5,
}
METALS = {'iron':8,'copper':4,'gold':12,'tin':6,'lead':6,'zinc':5,'silver':10,
 'nickel':8,'aluminum':5,'aluminium':5,'osmium':12,'uranium':20,'platinum':30,
 'steel':16,'bronze':10,'brass':10,'electrum':12,'invar':14,'constantan':10,
 'allthemodium':1500,'vibranium':4000,'unobtainium':10000,'netherite':1000}
SPECIAL = {'allthetweaks:atm_star':2500000,'allthetweaks:atm_star_block':22500000,
 'allthetweaks:atm_star_shard':10000,
 'allthetweaks:greg_star':25000000,'allthetweaks:greg_star_block':225000000,
 'quarryplus:adv_quarry':15000,
 'allthemodium:piglich_heart':250,'allthemodium:piglich_heart_block':2250,
 'mekanism:pellet_antimatter':10000,'allthecompressed:antimatter_block':90000,
 'allthemodium:vibranium_allthemodium_alloy_ingot':12500,
 'allthemodium:unobtainium_allthemodium_alloy_ingot':25000,
 'allthemodium:unobtainium_vibranium_alloy_ingot':40000}
GEMS = {'diamond':100,'emerald':30,'quartz':2,'lapis':2,'redstone':1,'coal':1,
 'amethyst':1,'ruby':15,'sapphire':15,'peridot':10,'apatite':2,'fluorite':4,
 'sulfur':2,'sulphur':2,'saltpeter':2,'niter':2,'certus_quartz':4,'fluix':8}
BULK = set('cobblestone cobbled_deepslate stone deepslate dirt sand red_sand gravel netherrack andesite diorite granite basalt blackstone end_stone obsidian clay glass snow ice calcite tuff mud terracotta concrete moss sandstone soul_sand soul_soil'.split())
INPUT = re.compile(r'([0-9.]+)x ((?:[if]:)?[a-z0-9_.-]+:[a-z0-9_./-]+) @ ([0-9.Ee+-]+)')

def key(s): return s if s.startswith(('i:','f:')) else 'i:'+s
def classify(id, source):
 ns,path=id[2:].split(':',1)
 if ns=='allthecompressed': path=re.sub(r'_\d+x$','',path)
 if ns=='kubejs' and (path.endswith('_cell') or path.startswith('atm_star_shard_')): return 'manufactured'
 if path in ('piglich_heart','piglich_heart_block','nether_star_block'): return 'resources'
 if id.startswith('f:'): return 'bulk' if path in ('water','flowing_water','lava','flowing_lava') else 'resources'
 if any(path==x or path.startswith(x+'_') for x in BULK): return 'bulk'
 if ns in ('chipped','rechiseled','chisel','xtonesreworked'): return 'bulk'
 if re.search(r'(^|_)(log|wood|planks|leaves|sapling|bamboo|cactus|kelp|crop|seeds|berries|wheat|carrot|potato|beetroot|pumpkin|melon|mushroom|flower|dye|wool)(_|$)',path): return 'farming'
 if ns in ('productivetrees','pamhc2crops','pamhc2trees','pamhc2foodcore','pamhc2foodextended','farmersdelight','herbsandharvest','merrymaking'): return 'farming'
 if ns=='bibliocraft' or ns.startswith('mcw') or ns in ('handcrafted','refurbished_furniture'): return 'farming'
 if path in BASE and path not in ('nether_star','netherite_ingot','diamond','emerald') and BASE[path] <= 5: return 'farming'
 if re.search(r'(^|_)(ingot|nugget|ore|raw|dust|gem|essence|comb|honeycomb|chunk|crystal|plate|rod|wire|gear|clump|shard)(_|$)',path): return 'resources'
 if path in BASE or any(path==m+'_block' or path=='block_of_'+m for m in METALS|GEMS): return 'resources'
 if ns=='hostilenetworks' and ('prediction' in path or 'matter' in path): return 'resources'
 return 'manufactured'

def root_price(id, old, source):
 ns,path=id[2:].split(':',1)
 if id[2:] in SPECIAL:return SPECIAL[id[2:]]
 if ns=='kubejs' and re.fullmatch('atm_star_shard_[1-5]',path):return 500000
 if 'alloy_block' in path and id[2:].replace('_alloy_block','_alloy_ingot') in SPECIAL:return 9*SPECIAL[id[2:].replace('_alloy_block','_alloy_ingot')]
 if id.startswith('f:'):
  if path in ('water','flowing_water','lava','flowing_lava'): return .01
  # Fluids are per bucket. Renewable fuel and chemicals are commodity inputs.
  return max(.01,min(100,old*.05)) if source in ('anchor','heuristic','fallback') else None
 if ns=='minecraft' and path in BASE: return BASE[path]
 for material,value in METALS.items():
  for form,mult in [('ingot',1),('nugget',1/9),('block',9),('dust',1),('plate',1.05),('rod',.5),('gear',4),('wire',.5)]:
   if path in (material+'_'+form,form+'_'+material): return value*mult
 for material,value in GEMS.items():
  if path in (material,material+'_gem','gem_'+material,material+'_dust'): return value
  if path==material+'_block': return value*9
 if re.search(r'(^|_)(log|wood)$',path): return .08
 if path.endswith('_planks'): return .02
 if path.endswith(('_leaves','_sapling')): return .03
 if path.endswith('_wool'): return .20
 if path.endswith('_dye'): return .10
 if ns=='mysticalagriculture' and path.endswith('_essence'):
  return {'inferium':.05,'prudentium':.20,'tertium':.80,'imperium':3.20,'supremium':12.80,'insanium':51.20}.get(path[:-8],max(.05,min(25,old*.03)))
 if source in ('anchor','heuristic','fallback'):
  group=classify(id,source)
  ceiling={'bulk':.25,'farming':2,'resources':250,'manufactured':100000}[group]
  return max(.01,min(ceiling,old*.10))
 return None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=pathlib.Path,required=True);a=ap.parse_args()
 raw=a.report.read_bytes();rows=list(csv.DictReader(line for line in raw.decode('utf-8-sig').splitlines() if not line.startswith('#')))
 data={r['commodity']:r for r in rows};assert len(data)>50000
 prices={id:max(.01,float(r['value'])*.1) for id,r in data.items()};fixed={};edges={};groups={}
 for id,r in data.items():
  groups[id]=classify(id,r['source'])
  v=root_price(id,float(r['value']),r['source'])
  if v is not None: fixed[id]=v
  deps=[(float(q),key(dep),float(old)) for q,dep,old in INPUT.findall(r['inputs']) if float(q)>0 and key(dep) in data]
  if deps: edges[id]=deps
 suffix=re.compile(r'^i:allthecompressed:(.+)_(\d+)x$')
 compression={}
 compression_bases=json.loads((ROOT/'economy/compression-bases.json').read_text())
 for id in data:
  m=suffix.match(id)
  if m:
   base=compression_bases.get(m[1]);level=int(m[2])
   if base in data:compression[id]=(base,9**level)
   elif level>1:
    # Compatibility blocks whose source mod is absent still have registered
    # compressed items. Preserve the ratios between their available tiers.
    compression[id]=('i:allthecompressed:'+m[1]+'_1x',9**(level-1))
 # Reprice the cheapest known recipe chain, preserving its original per-output
 # work ratio. Cycles are bounded and no free machine recipe gets an invented profit.
 for _ in range(120):
  new={}
  for id,r in data.items():
   if id in fixed: v=fixed[id]
   elif id in compression:
    base,mult=compression[id];v=prices[base]*mult
   elif id in edges:
    deps=edges[id];oldcost=sum(q*old for q,dep,old in deps)
    ratio=sum(q*prices[dep] for q,dep,old in deps)/oldcost if oldcost>0 else .1
    v=float(r['value'])*ratio
   else:v=float(r['value'])*.1
   if id not in fixed:
    # The report contains cheapest-path packing cycles, not the full recipe
    # graph. Never repeatedly discount a cycle down to a 1-cent endgame item.
    v=max(v,float(r['value'])*.02)
   new[id]=max(.01,v if id in compression else min(500000000,v))
  prices=new
 # Explicit compression conservation avoids variant premiums and 1-cent rounding
 # being multiplied into free profit. Underlying resource group also follows it.
 for id,(base,mult) in compression.items():
  prices[id]=prices[base]*mult;groups[id]=groups[base]
 # Basic crafting is not a way to turn a tree/cobble farm into factory income.
 # Preserve the cheap-input group through furniture, buttons and similar chains.
 for _ in range(20):
  for id,deps in edges.items():
   if groups[id]=='bulk' and all(groups[d]=='resources' for q,d,old in deps):groups[id]='resources'
   if groups[id]=='manufactured' and all(groups[d] in ('bulk','farming') for q,d,old in deps):
    groups[id]='farming' if any(groups[d]=='farming' for q,d,old in deps) else 'bulk'
 for id,(base,mult) in compression.items():groups[id]=groups[base]
 out=ROOT/'pack/snapshot/config/customatm_economy';out.mkdir(parents=True,exist_ok=True)
 catalog={id:{'value':round(prices[id],6),'group':groups[id]} for id in sorted(data)}
 (out/'catalog.json').write_text(json.dumps({'schema':1,'baseline_sha256':hashlib.sha256(raw).hexdigest(),'items':catalog},separators=(',',':'))+'\n')
 # A compact audit is kept beside source, not written over player's DynEco anchors.
 audit=ROOT/'economy';audit.mkdir(exist_ok=True)
 with (audit/'price-audit.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['commodity','old_base','new_base','income_group','source'])
  for id in sorted(data):w.writerow([id,data[id]['value'],catalog[id]['value'],groups[id],data[id]['source']])
 print(json.dumps({'commodities':len(catalog),'groups':dict(collections.Counter(groups.values()))},indent=2))
 for id in ['i:minecraft:cobblestone','i:minecraft:iron_ingot','i:minecraft:diamond','i:minecraft:diamond_pickaxe','i:mekanism:steel_casing','i:allthecompressed:cobblestone_9x']:print(id,catalog.get(id))
if __name__=='__main__':main()
