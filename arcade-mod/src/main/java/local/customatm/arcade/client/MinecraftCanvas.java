package local.customatm.arcade.client;

import local.customatm.arcade.ArcadeView;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.resources.ResourceLocation;

final class MinecraftCanvas implements ArcadeView.Canvas {
    private final GuiGraphics g;
    private final Font font;
    MinecraftCanvas(GuiGraphics g, Font font) { this.g=g; this.font=font; }
    public void image(String name,double x,double y,double w,double h,int u,int v,int sw,int sh) {
        int tw=switch(name){case "skin","shell"->1536;case "slot_frame"->1875;case "card_face","card_back"->1024;default->name.startsWith("item:")?16:1254;};
        int th=switch(name){case "skin","shell"->1024;case "slot_frame"->839;case "card_face","card_back"->1536;default->name.startsWith("item:")?16:1254;};
        var texture=name.startsWith("item:")?ResourceLocation.fromNamespaceAndPath("minecraft","textures/item/"+name.substring(5)+".png"):ResourceLocation.fromNamespaceAndPath("customatm_arcade","textures/gui/"+name+".png");
        RenderSystem.enableBlend();RenderSystem.defaultBlendFunc();
        g.blit(texture,
            (int)x,(int)y,(int)w,(int)h,(float)u,(float)v,sw,sh,tw,th);
    }
    public void fill(double x,double y,double w,double h,int color) { g.fill((int)x,(int)y,(int)(x+w),(int)(y+h),color); }
    public void text(String value,double x,double y,double size,int color,double maxWidth,boolean centered) {
        if(value.isEmpty())return;
        double scale=Math.min(size/9, maxWidth/Math.max(1,font.width(value)));
        if(centered)x-=font.width(value)*scale/2;
        g.pose().pushPose();g.pose().translate((float)x,(float)y,0);g.pose().scale((float)scale,(float)scale,1);
        g.drawString(font,value,0,0,color,true);g.pose().popPose();
    }
}
