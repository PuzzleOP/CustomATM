"""Build only the new Ballistix chapter and original diagrams; no live-profile access."""
import collections
import hashlib
import json
import pathlib
import runpy
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
SNAP = ROOT / 'pack/snapshot'
ASSETS = SNAP / 'kubejs/assets/customatm/textures/quests'
DATA = runpy.run_path(str(ROOT / 'quest-source/ballistix.py'))
NAME = 'local_guide_11_ballistix'

def uid(key):
    return f'{int(hashlib.sha256(("customatm-ballistix-quests/v1/"+key).encode()).hexdigest()[:16],16)&0x7fffffffffffffff:016X}'

def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'), size)

def canvas(title, subtitle):
    im = Image.new('RGB', (1100, 520), '#20252b')
    d = ImageDraw.Draw(im)
    d.rectangle((10,10,1090,510), outline='#ac9564', width=3)
    d.text((35,27), title, font=font(30, True), fill='#f1d49b')
    d.text((35,74), subtitle, font=font(18), fill='#c2cbd3')
    return im,d

def box(d, rect, title, lines):
    x,y,r,b = rect
    d.rectangle(rect, fill='#34414d', outline='#75c6d3', width=2)
    d.text((x+14,y+12), title, font=font(23,True), fill='#fff4db')
    for i,line in enumerate(lines):
        d.text((x+14,y+51+i*27),line,font=font(18),fill='#dde5eb')

def arrow(d,a,b):
    d.line((*a,*b),fill='#edbf62',width=4)
    x,y=b
    if a[0] == b[0]:
        s=1 if b[1]>a[1] else -1
        d.polygon([(x,y),(x-7,y-12*s),(x+7,y-12*s)],fill='#edbf62')
    else:
        s=1 if b[0]>a[0] else -1
        d.polygon([(x,y),(x-12*s,y-7),(x-12*s,y+7)],fill='#edbf62')

def diagrams():
    ASSETS.mkdir(parents=True,exist_ok=True)
    im,d=canvas('OUTPOST SYSTEMS','Three separate jobs: deliver energy, identify threats, and act on them.')
    for i,(t,lines) in enumerate([
        ('POWER',['Generator + buffer','FE cables to inputs']),
        ('LAUNCH',['Panel + platform','Missile + payload']),
        ('DETECT',['Search: alarm','Fire Control: targets']),
        ('DEFEND',['Linked SAM + CIWS','Power and ammunition'])]):
        x=35+i*265;box(d,(x,145,x+235,285),t,lines)
    d.text((40,330),'Build order: power → one launch → warning drill → interception drill',font=font(23,True),fill='#f1d49b')
    d.text((40,381),'Search Radar is not a substitute for Fire Control Radar.',font=font(22),fill='#dde5eb')
    d.text((40,425),'Keep the target range separate from factories and colonies.',font=font(22),fill='#dde5eb')
    im.save(ASSETS/'ballistix_overview.png')
    im,d=canvas('FE POWER: CONNECT TO THE INPUT','CustomATM has no Electrodynamics requirement. Existing FE generation works.')
    box(d,(35,150,285,290),'GENERATOR',['Existing FE supply','Output enabled'])
    box(d,(340,150,615,290),'ENERGY CUBE',['Input from generator','Output toward cables'])
    box(d,(675,125,1065,315),'MACHINE INPUTS',['Panel / VLS: any side','Radars / turrets: bottom','ESM Tower: bottom'])
    arrow(d,(286,220),(335,220));arrow(d,(617,220),(670,220))
    d.text((40,355),'Turret or radar base',font=font(22,True),fill='#dde5eb')
    arrow(d,(345,438),(345,370))
    d.text((375,396),'Cable underneath the base block',font=font(23),fill='#75c6d3')
    d.text((40,465),'Verify the machine energy reading; watch the reserve while defenses fire.',font=font(21),fill='#f1d49b')
    im.save(ASSETS/'ballistix_power.png')
    im,d=canvas('MISSILE SILO: BASE POSITIONS','Top-down schematic. Three adjacent positions at the same ground level.')
    box(d,(50,150,350,300),'CONTROL PANEL',['Display faces outward','Power the panel'])
    box(d,(395,150,695,300),'LAUNCH PLATFORM',['Directly behind panel','Missile + explosive slots'])
    box(d,(740,150,1040,300),'SUPPORT FRAME',['Opposite the panel','Reduces launch scatter'])
    d.line((350,225,395,225),fill='#edbf62',width=4);d.line((695,225,740,225),fill='#edbf62',width=4)
    d.text((50,340),'Leave the full machine shapes and launch path above the bases clear.',font=font(22),fill='#dde5eb')
    d.text((50,388),'First load: 1 × Tier 1 Missile + 1 × Condensive Explosive',font=font(24,True),fill='#f1d49b')
    d.text((50,440),'Check orientation, target coordinates and energy before a single launch.',font=font(22),fill='#dde5eb')
    im.save(ASSETS/'ballistix_silo.png')
    im,d=canvas('LAYERED DEFENSE: TWO DISTINCT RADARS','Feed FE into the bottom of each radar and turret base. Give them sky light.')
    box(d,(35,130,335,255),'SEARCH RADAR',['Early warning','Normal redstone → siren'])
    box(d,(395,130,720,255),'FIRE CONTROL',['Missile guidance','Radar Gun → bind turrets'])
    box(d,(785,130,1065,255),'LINK DISTANCE',['Within 32 blocks','Sample radar base first'])
    box(d,(135,325,485,440),'SAM: OUTER LAYER',['Surface-to-Air Missiles','100–300 block base band'])
    box(d,(615,325,965,440),'CIWS: INNER LAYER',['Ballistix Bullets','100 block base range'])
    d.line((555,257,555,285,310,285),fill='#edbf62',width=3);arrow(d,(310,285),(310,320))
    d.line((555,285,790,285),fill='#edbf62',width=3);arrow(d,(790,285),(790,320))
    d.text((100,468),'Missile range and radar-link distance are different measurements.',font=font(23,True),fill='#f1d49b')
    im.save(ASSETS/'ballistix_defense.png')

def build():
    diagrams()
    rows=collections.Counter();lang={f'chapter.{uid("chapter")}.title':'11 • Ballistix: Missile Outposts'};quests=[]
    bykey={q['key']:q for q in DATA['QUESTS']}
    for q in DATA['QUESTS']:
        key=q['key'];qid=uid('quest/'+key);lane=q['lane']
        if key=='start':x,y=-3,0
        elif key=='legend':x,y=-3,3
        elif key=='graduation':x,y=9,20
        else:x,y=rows[lane]*3,lane*4;rows[lane]+=1
        tasks=[]
        for spec in q['items']:
            item,_,count=spec.partition('*')
            tasks.append({'id':uid(key+'/item/'+item),'type':'item','item':{'id':item,'count':1},'count':int(count or 1),'consume_items':False})
        if not tasks or q['project']:
            tid=uid(key+'/practice');tasks.append({'id':tid,'type':'checkmark'})
            lang[f'task.{tid}.title']='I performed the described drill' if q['project'] else 'I have read and followed this lesson'
        icon=tasks[0]['item'] if tasks[0]['type']=='item' else {'id':'ballistix:launcherplatformtier1' if key=='start' else 'minecraft:book','count':1}
        entry={'id':qid,'dependencies':[uid('quest/'+k) for k in q['deps']], 'tasks':tasks,'x':float(x),'y':float(y),'icon':icon,
               'shape':'diamond' if q['project'] or key=='start' else ('hexagon' if q['items'] else 'square')}
        if q['project'] or key=='start':entry['size']=1.5
        if q['optional']:entry['optional']=True
        if key != 'legend' and any(bykey[k]['lane'] != lane for k in q['deps']):
            entry['hide_dependency_lines']=True
        if q['items'] or q['project']:entry['rewards']=[{'id':uid(key+'/reward'),'type':'xp','xp':75 if q['project'] else 15}]
        desc=[q['why'],'']
        if q['deps']:desc.extend(['&7Before this lesson: '+', '.join(bykey[k]['title'] for k in q['deps'])+'&r',''])
        desc.append('&b&lBuild & configure&r')
        for i,step in enumerate(q['steps'],1):desc.extend([f'{i}. {step}',''])
        if q['image']:desc.extend([f'{{image:customatm:textures/quests/ballistix_{q["image"]}.png width:330 height:156 align:center}}',''])
        desc.extend(['&e&lWorkshop tip&r',q['tip']])
        if q['project']:desc.extend(['','&7Completion is a manual confirmation of the practical test. Items are not consumed.&r'])
        lang[f'quest.{qid}.title']=q['title'];lang[f'quest.{qid}.quest_subtitle']=DATA['LANES'][lane].title() if 0<=lane<5 else ('Final workshop' if key=='graduation' else 'Start here')
        lang[f'quest.{qid}.quest_desc']=desc;quests.append(entry)
    images=[]
    for row,label in enumerate(DATA['LANES']):
        im=Image.new('RGBA',(1100,72),(0,0,0,0));d=ImageDraw.Draw(im)
        d.text((0,8),f'{row+1:02d}  {label}',font=font(34,True),fill='#e9ca89')
        im.save(ASSETS/f'ballistix_lane_{row}.png')
        images.append({'id':uid('lane/'+str(row)),'image':f'customatm:textures/quests/ballistix_lane_{row}.png','x':8.0,'y':row*4-1.15,'width':19.0,'height':1.0,'rotation':0.0})
    chapter={'default_hide_dependency_lines':False,'default_quest_shape':'hexagon','filename':NAME,'group':'28D38D1EC21B4002',
             'icon':{'id':'ballistix:launcherplatformtier3','count':1},'id':uid('chapter'),'order_index':10,'progression_mode':'flexible','quest_links':[],'quests':quests,'images':images}
    for folder,data in [('chapters',chapter),('lang/en_us/chapters',lang)]:
        p=SNAP/'config/ftbquests/quests'/folder/(NAME+'.snbt');p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary={'chapter':'ballistix','quests':len(quests),'item_quests':sum(bool(q['items']) for q in DATA['QUESTS']),
             'projects':sum(q['project'] for q in DATA['QUESTS']),'branches':5,'diagrams':4}
    (ROOT/'quest-source/ballistix-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    # A review-only map, not part of the distributed resource pack.
    im=Image.new('RGB',(1750,1400),'#20252b');d=ImageDraw.Draw(im)
    d.text((30,18),'BALLISTIX • QUEST MAP',font=font(30,True),fill='#f1d49b')
    points={q['id']:(int(330+q['x']*65),int(150+q['y']*52)) for q in quests}
    for q in quests:
        if q.get('hide_dependency_lines'):continue
        for dep in q['dependencies']:d.line((*points[dep],*points[q['id']]),fill='#4e636e',width=2)
    for row,label in enumerate(DATA['LANES']):d.text((320,90+row*208),label,font=font(23,True),fill='#75c6d3')
    for q in quests:
        x,y=points[q['id']];d.ellipse((x-16,y-16,x+16,y+16),fill='#edbf62' if q['shape']=='diamond' else '#75c6d3')
        for i,line in enumerate(textwrap.wrap(lang[f'quest.{q["id"]}.title'],23)):
            d.text((x-72,y+25+i*21),line,font=font(15),fill='#eef3f6')
    p=ROOT/'.work/ballistix/quest-map.png';im.save(p)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':build()
