package local.customatm.arcade.client;

import java.util.*;
import local.customatm.arcade.*;
import com.togascasino.casinomod.client.CasinoSounds;
import com.togascasino.casinomod.network.payload.OpenGamePayload;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.*;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.neoforged.neoforge.network.PacketDistributor;
import org.lwjgl.glfw.GLFW;

public final class RedstoneGameScreen<T extends AbstractContainerMenu> extends AbstractContainerScreen<T> {
    private final GameModel model;
    private final Map<String,AbstractWidget> controls=new LinkedHashMap<>();
    private ArcadeLayout.Fit fit;private EditBox entry;private boolean activateHeld;private int announced;
    public RedstoneGameScreen(T menu,Inventory inv,Component title,GameKind kind){super(menu,inv,title);model=GameRuntime.model(kind);model.rules=false;announced=model.resultSerial;}
    private int sx(int v){return (int)Math.round(fit.x()+v*fit.scale());}
    private int sy(int v){return (int)Math.round(fit.y()+v*fit.scale());}
    private int span(int v){return Math.max(1,(int)Math.round(v*fit.scale()));}
    @Override protected void init(){
        fit=ArcadeLayout.fit(width,height);imageWidth=span(1364);imageHeight=span(954);super.init();controls.clear();
        for(var b:GameControls.boxes(model.kind)){
            AbstractWidget widget;
            if(b.id().equals("bet")){
                entry=new EditBox(font,sx(b.x()),sy(b.y()),span(b.w()),span(b.h()),Component.literal(b.label())){
                    @Override public void renderWidget(GuiGraphics g,int x,int y,float t){}
                    @Override public void onClick(double x,double y){moveCursorToEnd(false);}
                };
                entry.setMaxLength(10);entry.setBordered(false);entry.setFilter(s->s.matches("[0-9]{0,10}"));entry.setValue(model.input);entry.setResponder(s->model.input=s);widget=entry;
            }else widget=new AbstractButton(sx(b.x()),sy(b.y()),span(b.w()),span(b.h()),Component.literal(b.label())){
                @Override public void onPress(){press(b.id());}
                @Override protected void renderWidget(GuiGraphics g,int x,int y,float t){}
                @Override protected void updateWidgetNarration(NarrationElementOutput out){defaultButtonNarrationText(out);}
            };
            controls.put(b.id(),widget);addRenderableWidget(widget);
        }
        refresh();
    }
    private void refresh(){
        GameRuntime.refresh(model);long time=GameRuntime.now();
        for(var e:controls.entrySet()){
            String id=e.getKey();e.getValue().active=GameControls.enabled(id,model,time);
            e.getValue().visible=model.rules?(id.equals("dismiss")||id.equals("close")):!id.equals("dismiss");
        }
        if(entry!=null)entry.setEditable(GameControls.enabled("bet",model,time));
        if(controls.containsKey("cashout"))controls.get("cashout").setMessage(Component.literal("Cash out. Current return "+CoinModel.money(model.kind==GameKind.CRASH?Math.round(model.submitted*model.multiplier):model.returned)));
        if(model.kind==GameKind.ROULETTE)controls.get("start").setMessage(Component.literal("Spin wheel. Total stake "+CoinModel.money(model.totalWager())));
    }
    private void setBet(long value){model.setBet(value);entry.setValue(model.input);}
    private void press(String id){
        long time=GameRuntime.now();if(!GameControls.enabled(id,model,time))return;
        if(id.equals("close")){onClose();return;}
        if(id.equals("rules")||id.equals("dismiss")){model.rules=id.equals("rules");refresh();setFocused(controls.get(model.rules?"dismiss":"rules"));return;}
        if(id.equals("home")||id.startsWith("game")||id.startsWith("tile")){
            String target=id.equals("home")?"hub":ArcadeLayout.TARGETS[Integer.parseInt(id.substring(4))];CasinoSounds.click();PacketDistributor.sendToServer(new OpenGamePayload(target));return;
        }
        GameModel.Request request=null;
        if(id.startsWith("preset"))setBet(Long.parseLong(id.substring(6)));
        else if(id.startsWith("cell"))request=model.action("reveal",Integer.parseInt(id.substring(4)),time);
        else if(id.startsWith("scratch"))model.scratched[Integer.parseInt(id.substring(7))]=true;
        else if(id.startsWith("number")){model.selectedType=0;model.selectedNumber=Integer.parseInt(id.substring(6));}
        else if(id.startsWith("outside"))model.selectedType=Integer.parseInt(id.substring(7));
        else if(id.startsWith("risk")){model.risk=Integer.parseInt(id.substring(4));model.hasResult=false;}
        else switch(id){
            case "minus"->setBet(model.bet()-25);case "plus"->setBet(model.bet()+25);
            case "minesLess"->{model.mines--;model.safe=0;Arrays.fill(model.cells,0);}case "minesMore"->{model.mines++;model.safe=0;Arrays.fill(model.cells,0);}
            case "start"->request=model.start(time);
            case "hit","stand","double","cashout"->request=model.action(id,-1,time);
            case "add"->model.addWager(time);
            case "undo"->model.wagers.removeLast();case "clear"->model.wagers.clear();
            case "revealAll"->Arrays.fill(model.scratched,true);
            default->{}
        }
        if(request!=null){CasinoSounds.click();GameRuntime.send(model,request);}refresh();
    }
    @Override protected void containerTick(){super.containerTick();refresh();if(model.resultSerial!=announced&&!model.locked(GameRuntime.now())&&(model.kind!=GameKind.SCRATCH||model.allScratched())){announced=model.resultSerial;if(model.returned>model.submitted)CasinoSounds.win();else CasinoSounds.lose();}}
    @Override public void render(GuiGraphics g,int mx,int my,float partial){
        refresh();String hover="",focus="";for(var e:controls.entrySet()){if(e.getValue().visible&&e.getValue().isMouseOver(mx,my))hover=e.getKey();if(e.getValue().isFocused())focus=e.getKey();}
        g.fill(0,0,width,height,0xB0101513);g.pose().pushPose();g.pose().translate((float)fit.x(),(float)fit.y(),0);g.pose().scale((float)fit.scale(),(float)fit.scale(),1);
        GameView.render(new MinecraftCanvas(g,font),model,GameRuntime.now(),new ArcadeView.Input(hover,focus,entry!=null&&entry.isFocused(),entry==null?0:entry.getCursorPosition(),entry==null?"":entry.getHighlighted(),GameRuntime.now()%1000<500));g.pose().popPose();
        for(var widget:controls.values())widget.render(g,mx,my,partial);
    }
    @Override public boolean keyPressed(int key,int scan,int mods){
        if(key==GLFW.GLFW_KEY_ESCAPE&&model.rules){press("dismiss");return true;}
        boolean activation=key==GLFW.GLFW_KEY_ENTER||key==GLFW.GLFW_KEY_KP_ENTER||key==GLFW.GLFW_KEY_SPACE;
        if(entry!=null&&entry.isFocused()&&!model.rules){
            if(key==GLFW.GLFW_KEY_ENTER||key==GLFW.GLFW_KEY_KP_ENTER){activateHeld=true;setFocused(controls.get("start"));return true;}
            if(key!=GLFW.GLFW_KEY_TAB&&key!=GLFW.GLFW_KEY_ESCAPE)return entry.keyPressed(key,scan,mods);
        }
        if(activation){if(activateHeld)return true;activateHeld=true;}
        return super.keyPressed(key,scan,mods);
    }
    @Override public boolean keyReleased(int key,int scan,int mods){if(key==GLFW.GLFW_KEY_ENTER||key==GLFW.GLFW_KEY_KP_ENTER||key==GLFW.GLFW_KEY_SPACE)activateHeld=false;return super.keyReleased(key,scan,mods);}
    @Override public boolean mouseClicked(double x,double y,int button){
        refresh();boolean old=model.rules;
        // Consume blank-space clicks too: the retained stock menu has invisible item slots.
        for(var widget:controls.values())if(widget.mouseClicked(x,y,button)){setFocused(widget);break;}
        if(old!=model.rules)setFocused(controls.get(model.rules?"dismiss":"rules"));return true;
    }
    @Override public boolean mouseDragged(double x,double y,int button,double dx,double dy){
        if(button==0&&model.kind==GameKind.SCRATCH&&!model.rules)for(var b:GameControls.boxes(model.kind))if(b.id().startsWith("scratch")&&b.contains(fit.localX(x),fit.localY(y)))press(b.id());
        return true;
    }
    @Override protected void renderBg(GuiGraphics g,float t,int x,int y){}
    @Override protected void renderLabels(GuiGraphics g,int x,int y){}
    @Override public boolean isPauseScreen(){return false;}
}
