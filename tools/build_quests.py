"""Build original guided chapters in the public snapshot; never touch a live profile."""
import hashlib
import collections
import json
import pathlib
import runpy
import textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCE=ROOT/'quest-source'
SNAP=ROOT/'pack/snapshot'
CH=SNAP/'config/ftbquests/quests/chapters'
LANG=SNAP/'config/ftbquests/quests/lang/en_us/chapters'
ASSETS=SNAP/'kubejs/assets/customatm/textures/quests'
LEGACY=json.loads((SOURCE/'legacy-ids.json').read_text())
CONTENT=runpy.run_path(str(SOURCE/'content.py'))['CHAPTERS']
DATA=runpy.run_path(str(SOURCE/'rework.py'))

def uid(value):
    # Positive 64-bit IDs, stable across rebuilds and distinct from legacy IDs.
    return f'{int(hashlib.sha256(("customatm-guides-v2/"+value).encode()).hexdigest()[:16],16)&0x7fffffffffffffff:016X}'

def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'),size)

def diagram(slug,data):
    title,boxes,notes=data
    img=Image.new('RGB',(1100,500),'#101c2b');d=ImageDraw.Draw(img)
    d.rounded_rectangle((12,12,1088,488),18,outline='#32637c',width=3)
    d.text((42,35),title,font=font(32,True),fill='#f3cb72')
    d.text((42,82),'CustomATM | workshop reference',font=font(17),fill='#9bb7c9')
    if slug=='astral':
        for i,label in enumerate(boxes[:3]):
            x=42+i*350
            d.rounded_rectangle((x,126,x+300,215),12,fill='#203a50',outline='#5bc8cd',width=2)
            d.text((x+15,154),label,font=font(23,True),fill='#f1f6fa')
            d.line((x+150,216,x+150,245,550,245,550,270),fill='#f3cb72',width=3)
        d.rounded_rectangle((380,271,720,333),12,fill='#203a50',outline='#5bc8cd',width=2)
        d.text((410,286),boxes[3],font=font(23,True),fill='#f1f6fa')
        for i,note in enumerate(notes):d.text((42,355+36*i),note,font=font(18),fill='#d8e4ee')
        ASSETS.mkdir(parents=True,exist_ok=True);img.save(ASSETS/(slug+'.png'),optimize=True)
        return
    for i,label in enumerate(boxes):
        x=42+i*263
        d.rounded_rectangle((x,135,x+225,245),12,fill='#203a50',outline='#5bc8cd',width=2)
        for j,line in enumerate(textwrap.wrap(label,17)):
            d.text((x+15,158+j*29),line,font=font(22,True),fill='#f1f6fa')
        if i<3:
            d.line((x+229,190,x+255,190),fill='#f3cb72',width=3)
            d.polygon([(x+255,190),(x+246,183),(x+246,197)],fill='#f3cb72')
    for i,note in enumerate(notes):
        d.text((45,286+53*i),f'{i+1:02d}',font=font(20,True),fill='#5bc8cd')
        d.text((90,284+53*i),note,font=font(20),fill='#d8e4ee')
    ASSETS.mkdir(parents=True,exist_ok=True);img.save(ASSETS/(slug+'.png'),optimize=True)

def lane_header(slug,row,label):
    image=Image.new('RGBA',(900,70),(0,0,0,0));draw=ImageDraw.Draw(image)
    draw.text((0,6),label,font=font(36,True),fill='#69d4db')
    image.save(ASSETS/f'{slug}_lane_{row}.png')

def stack(spec):
    name,_,count=spec.partition('*')
    return {'id':name,'count':1},int(count or 1)

def texts(q,slug,index=None):
    desc=[q['why'],'','&b&lGet it working&r',q['action']]
    extra=DATA['DETAILS'].get((slug,index),[])
    if extra:desc += ['','&6&lWorkshop notes&r',*sum(([p,''] for p in extra),[])]
    if q.get('code'):
        desc += ['','&b&lExample program&r',*q['code']]
    desc += ['','&e&lTip&r',q['tip']]
    return desc

def task_list(slug,key,legacy,items,practice,lang):
    result=[]
    for spec in items:
        item,count=stack(spec)
        # Preserve existing item task IDs when the objective still uses the item.
        old=next((t for t in legacy if t['type']=='item' and t['item']['id']==item['id']),None)
        tid=old['id'] if old else uid(slug+'/'+str(key)+'/item/'+item['id'])
        if item['id']=='enderio:conduit':item['components']={'enderio:conduit':'enderio:item'}
        result.append({'id':tid,'type':'item','item':item,'count':count,'consume_items':False})
    if practice or not result:
        old=next((t for t in legacy if t['type']=='checkmark'),None)
        tid=old['id'] if old else uid(slug+'/'+str(key)+'/practice')
        result.append({'id':tid,'type':'checkmark'})
        lang[f'task.{tid}.title']='I completed the setup and observed the result' if practice else 'I understand this reference'
    return result

def build():
    summary=[]
    for number,c in enumerate(CONTENT,1):
        slug=c['slug'];name=f'local_guide_{number:02d}_{slug}'
        old=LEGACY[slug];ids=[q['id'] for q in old['quests']]
        lang={f'chapter.{old["chapter"]}.title':f'{number:02d} • '+c['title']}
        lanes=DATA['LANES'][slug];positions={0:(-3,0),1:(-3,3)};dependencies={0:[],1:[0]};lane_names={0:'START HERE',1:'REFERENCE'}
        for row,(label,indexes) in enumerate(lanes):
            for col,index in enumerate(indexes):
                positions[index]=(col*3.0,row*4.0);lane_names[index]=label
                dependencies[index]=[indexes[col-1]] if col else [0]
        dependencies.update(DATA['DEPS'].get(slug,{}))
        assert set(positions)==set(range(len(c['quests'])))
        quests=[]
        for index,q in enumerate(c['quests']):
            q=dict(q)
            q.update(DATA['OVERRIDES'].get((slug,index),{}))
            if slug=='sfm' and index==10:
                q['code']=[s.replace('OUTPUT RETAIN 1 TO EACH furnace BOTTOM SIDE','OUTPUT RETAIN 1 TO EACH furnace NORTH SIDE') for s in q['code']]
            if slug=='economy' and index==13:
                q['action']='Press F8 with the default CustomATM key binding while in a world with menus closed. If reassigned, search Open Casino under Casino Mod in Controls. Open the interface, identify the shared DynEco balance, and close it without placing a bet.'
            if index==1:
                q.update(title='Map legend & completion rules',why='Follow a branch that solves your next problem. Equipment icons lead to concrete inventory milestones; the book card is a reference, and a large diamond marks a workshop project.',action='Read the setup before crafting. Item milestones detect your inventory without consuming items. Their practical checkmarks are optional reminders; final workshop projects require a practical confirmation. An item in your bag does not prove that a machine is configured. Existing equipment counts: do not rebuild a working system just for this map.',tip='JEI shows this pack\'s current recipes. Branches explain how the systems connect. Optional side projects are independent of the main route; no casino win is required.')
            items=DATA['ITEMS'].get(slug,{}).get(index,[q['item']] if q['item'] else [])
            practice=q['practice'] or (index>1 and bool(items) and not q['item'])
            entry={'id':ids[index],'dependencies':[ids[i] for i in dependencies[index]],'tasks':task_list(slug,index,old['quests'][index]['tasks'],items,practice,lang),'x':positions[index][0],'y':positions[index][1],'shape':'hexagon' if items else 'square'}
            if index in (0,1):entry['icon']={'id':c['icon'] if index==0 else 'minecraft:book','count':1}
            elif items:entry['icon']=entry['tasks'][0]['item']
            else:entry['icon']={'id':'minecraft:book','count':1}
            project=q['title'].startswith('Project:')
            if items and not project:
                for task in entry['tasks']:
                    if task['type']=='checkmark':task['optional_task']=True
            if index==0 or project:entry.update(shape='diamond',size=1.5)
            if index==1 or (slug=='economy' and 13<=index<=16):entry['optional']=True
            if items and index>1 and not entry.get('optional'):
                entry['rewards']=[{'id':uid(slug+'/'+str(index)+'/xp'),'type':'xp','xp':75 if project else 15}]
            if slug=='ad_astra' and index in (12,16,20):
                dimension={12:'moon',16:'mars',20:'glacio'}[index]
                entry['tasks'].append({'id':uid(slug+'/'+dimension+'/visit'),'type':'dimension','dimension':'ad_astra:'+dimension})
            desc=texts(q,slug,index)
            if index==0:
                desc=[q['why'],'',f'{{image:customatm:textures/quests/{slug}.png width:330 height:150 align:center}}','','&b&lChoose a branch&r',*('• '+label.title() for label,_ in lanes),'',q['action'],'','&eStart with the first equipment milestone, then follow the branch you need.']
            # Put a working diagram beside the relevant setup, not just on the map intro.
            if index=={'minecolonies':11,'ad_astra':11,'advanced_rs':6,'economy':9,'enderio':8,'astral':19,'sfm':4,'xnet':6,'computercraft':7,'rftools':8}[slug]:
                desc += ['',f'{{image:customatm:textures/quests/{slug}.png width:330 height:150 align:center}}']
            lang[f'quest.{ids[index]}.title']=q['title']
            lang[f'quest.{ids[index]}.quest_subtitle']=lane_names[index].title()
            lang[f'quest.{ids[index]}.quest_desc']=desc
            quests.append(entry)
        # Practical side branches sit directly below their parent lesson.
        counts=collections.Counter(q['after'] for q in DATA['EXTRAS'][slug]);placed=collections.Counter()
        for col,q in enumerate(DATA['EXTRAS'][slug]):
            qid=uid(slug+'/'+q['key']);key=q['key'];parent=q['after']
            x,y=positions[parent];x+=(placed[parent]-(counts[parent]-1)/2)*1.5;placed[parent]+=1
            tasks=task_list(slug,key,[],[q['item']],True,lang)
            for task in tasks:
                if task['type']=='checkmark':task['optional_task']=True
            quests.append({'id':qid,'dependencies':[ids[parent]],'tasks':tasks,'x':x,'y':y+1.7,'shape':'hexagon','icon':tasks[0]['item'],'optional':True,'rewards':[{'id':uid(slug+'/'+key+'/xp'),'type':'xp','xp':25}]})
            lang[f'quest.{qid}.title']=q['title'];lang[f'quest.{qid}.quest_subtitle']='Workshop • '+lane_names[q['after']].title();lang[f'quest.{qid}.quest_desc']=texts(q,slug)
        out={'default_hide_dependency_lines':False,'default_quest_shape':'hexagon','filename':name,'group':'28D38D1EC21B4002','icon':{'id':c['icon'],'count':1},'id':old['chapter'],'order_index':number-1,'progression_mode':'flexible','quest_links':[],'quests':quests}
        out['images']=[]
        for row,(label,_) in enumerate(lanes):
            lane_header(slug,row,label)
            out['images'].append({'id':uid(slug+'/lane/'+str(row)),'image':f'customatm:textures/quests/{slug}_lane_{row}.png','x':5.0,'y':row*4.0-1.15,'width':11.0,'height':.85,'rotation':0.0})
        (CH/(name+'.snbt')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (LANG/(name+'.snbt')).write_text(json.dumps(lang,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        diagram(slug,DATA['DIAGRAMS'][slug])
        summary.append({'chapter':slug,'quests':len(quests),'item_quests':sum(any(t['type']=='item' for t in q['tasks']) for q in quests),'branches':len(lanes),'new_workshops':len(DATA['EXTRAS'][slug])})
    (SOURCE/'build-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':build()
