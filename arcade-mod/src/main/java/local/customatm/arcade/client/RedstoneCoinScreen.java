package local.customatm.arcade.client;

import com.togascasino.casinomod.CasinoConfig;
import com.togascasino.casinomod.client.CasinoSounds;
import com.togascasino.casinomod.client.ClientPayloadHandler;
import com.togascasino.casinomod.menu.game.CoinFlipMenu;
import com.togascasino.casinomod.network.payload.*;
import com.togascasino.casinomod.util.CasinoGame;
import java.util.LinkedHashMap;
import java.util.Map;
import local.customatm.arcade.*;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.components.AbstractWidget;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.neoforged.neoforge.network.PacketDistributor;
import org.lwjgl.glfw.GLFW;

public final class RedstoneCoinScreen extends AbstractContainerScreen<CoinFlipMenu> {
    private final CoinModel model=GameRuntime.coin();
    private final Map<String,AbstractWidget> controls=new LinkedHashMap<>();
    private ArcadeLayout.Fit fit;
    private EditBox entry;
    private boolean firstInit=true;
    private boolean announced;
    private boolean activateHeld;

    public RedstoneCoinScreen(CoinFlipMenu menu,Inventory inventory,Component title) { super(menu,inventory,title); }
    private static long now() { return System.nanoTime()/1_000_000L; }
    private int sx(int v) { return (int)Math.round(fit.x()+v*fit.scale()); }
    private int sy(int v) { return (int)Math.round(fit.y()+v*fit.scale()); }
    private int span(int v) { return Math.max(1,(int)Math.round(v*fit.scale())); }

    @Override protected void init() {
        fit=ArcadeLayout.fit(width,height);
        imageWidth=span(1364); imageHeight=span(954);
        super.init();controls.clear();
        if(firstInit) { model.rules=false;firstInit=false; }
        model.minBet=CasinoConfig.MIN_BET.get();model.maxBet=CasinoConfig.MAX_BET.get();
        for(var b:ArcadeLayout.CONTROLS) {
            AbstractWidget widget;
            if(b.id().equals("bet")) {
                entry=new EditBox(font,sx(b.x()),sy(b.y()),span(b.w()),span(b.h()),Component.literal(b.label())) {
                    @Override public void renderWidget(GuiGraphics g,int x,int y,float t) { }
                    @Override public void onClick(double x,double y) { moveCursorToEnd(false); }
                };
                entry.setMaxLength(10);entry.setBordered(false);
                entry.setFilter(s->s.matches("[0-9]{0,10}"));entry.setValue(model.input);
                entry.setResponder(s->{model.input=s;});widget=entry;
            } else {
                widget=new AbstractButton(sx(b.x()),sy(b.y()),span(b.w()),span(b.h()),Component.literal(b.label())) {
                    @Override public void onPress() { press(b.id()); }
                    @Override protected void renderWidget(GuiGraphics g,int x,int y,float t) { }
                    @Override protected void updateWidgetNarration(NarrationElementOutput out) { defaultButtonNarrationText(out); }
                };
            }
            controls.put(b.id(),widget);addRenderableWidget(widget);
        }
        refreshControls();
    }
    private void refreshControls() {
        long time=now();model.balance=ClientPayloadHandler.getBalance();
        for(var e:controls.entrySet()) {
            e.getValue().active=ArcadeView.enabled(e.getKey(),model,time);
            e.getValue().visible=e.getKey().equals("dismiss")==model.rules || (!e.getKey().equals("dismiss") && !model.rules) || e.getKey().equals("close");
        }
        entry.setEditable(!model.locked(time) && !model.rules);
        controls.get("flip").setMessage(Component.literal("Flip "+CoinModel.money(model.bet())+". 50 percent chance. Total return "+CoinModel.money(CoinModel.payout(model.bet()))));
    }
    private void setBet(long n) { entry.setValue(Long.toString(Math.max(model.minBet,Math.min(model.limit(),n)))); }
    private void press(String id) {
        if(!ArcadeView.enabled(id,model,now()))return;
        if(id.equals("close")) { onClose();return; }
        if(id.equals("rules")) { model.rules=true;setFocused(controls.get("dismiss"));refreshControls();return; }
        if(id.equals("dismiss")) { model.rules=false;setFocused(controls.get("rules"));refreshControls();return; }
        if(id.startsWith("game")) {
            int index=Integer.parseInt(id.substring(4));CasinoSounds.click();
            PacketDistributor.sendToServer(new OpenGamePayload(ArcadeLayout.TARGETS[index]));return;
        }
        switch(id) {
            case "heads" -> model.side=0;
            case "tails" -> model.side=1;
            case "minus" -> setBet(model.bet()-25);
            case "plus" -> setBet(model.bet()+25);
            case "flip" -> {
                int[] args=model.begin(now());
                if(args!=null) {
                    announced=false;
                    CasinoSounds.click();
                    PacketDistributor.sendToServer(new CasinoActionPayload(CasinoGame.COIN_FLIP,"bet",args));
                }
            }
            default -> { if(id.startsWith("preset")) setBet(Long.parseLong(id.substring(6))); }
        }
        refreshControls();
    }
    @Override protected void containerTick() {
        super.containerTick();
        // Results are routed globally, including while a casino screen is closed.
        refreshControls();
        if(model.resultReady && !model.locked(now()) && !announced) {
            announced=true;
            if(model.won)CasinoSounds.win();else CasinoSounds.lose();
        }
    }
    @Override public void render(GuiGraphics g,int mouseX,int mouseY,float partialTick) {
        refreshControls();
        String hover="",focus="";
        for(var e:controls.entrySet()) {
            if(e.getValue().visible && e.getValue().isMouseOver(mouseX,mouseY))hover=e.getKey();
            if(e.getValue().isFocused())focus=e.getKey();
        }
        g.fill(0,0,width,height,0xB0101513);
        g.pose().pushPose();g.pose().translate((float)fit.x(),(float)fit.y(),0);g.pose().scale((float)fit.scale(),(float)fit.scale(),1);
        ArcadeView.render(new MinecraftCanvas(g,font),model,now(),new ArcadeView.Input(hover,focus,entry.isFocused(),entry.getCursorPosition(),entry.getHighlighted(),now()%1000<500));
        g.pose().popPose();
        // Native widgets own hit testing, keyboard navigation and narration; shared view owns their pixels.
        for(var widget:controls.values())widget.render(g,mouseX,mouseY,partialTick);
    }
    @Override public boolean keyPressed(int key,int scan,int mods) {
        if(key==GLFW.GLFW_KEY_ESCAPE && model.rules) { press("dismiss");return true; }
        if(entry.isFocused() && !model.rules) {
            if(key==GLFW.GLFW_KEY_ENTER || key==GLFW.GLFW_KEY_KP_ENTER) { activateHeld=true;setFocused(controls.get("flip"));return true; }
            if(key!=GLFW.GLFW_KEY_TAB && key!=GLFW.GLFW_KEY_ESCAPE) return entry.keyPressed(key,scan,mods);
        }
        if(controls.get("flip").isFocused() && (key==GLFW.GLFW_KEY_ENTER || key==GLFW.GLFW_KEY_KP_ENTER || key==GLFW.GLFW_KEY_SPACE)) {
            if(!activateHeld) { activateHeld=true;press("flip"); }
            return true;
        }
        return super.keyPressed(key,scan,mods);
    }
    @Override public boolean keyReleased(int key,int scan,int mods) {
        if(key==GLFW.GLFW_KEY_ENTER || key==GLFW.GLFW_KEY_KP_ENTER || key==GLFW.GLFW_KEY_SPACE)activateHeld=false;
        return super.keyReleased(key,scan,mods);
    }
    @Override public boolean mouseClicked(double x,double y,int button) {
        refreshControls();boolean wasRules=model.rules;
        for(var widget:controls.values())if(widget.mouseClicked(x,y,button)){setFocused(widget);break;}
        // ContainerEventHandler focuses the clicked button after its callback, so
        // restore modal focus once that dispatch has finished.
        if(wasRules!=model.rules)setFocused(controls.get(model.rules?"dismiss":"rules"));
        return true;
    }
    @Override protected void renderBg(GuiGraphics g,float t,int x,int y) { }
    @Override protected void renderLabels(GuiGraphics g,int x,int y) { }
    @Override public boolean isPauseScreen() { return false; }
}
