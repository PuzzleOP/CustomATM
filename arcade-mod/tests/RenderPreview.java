import local.customatm.arcade.*;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.nio.file.*;
import java.util.*;
import javax.imageio.ImageIO;

/** Java2D renderer of the production draw routine. No Minecraft classes or game bootstrap. */
public final class RenderPreview implements ArcadeView.Canvas {
    private final Graphics2D g;
    private final Map<String,BufferedImage> art=new HashMap<>();
    private final BufferedImage atlas;
    private final String characters;
    RenderPreview(Graphics2D g,Path resources,Path font,Path chars) throws Exception {
        this.g=g;atlas=ImageIO.read(font.toFile());characters=Files.readString(chars);
        for(String name:new String[]{"skin","heads","tails","shell","slot_frame","card_face","card_back"})art.put(name,ImageIO.read(resources.resolve(name+".png").toFile()));
        for(String name:new String[]{"coal","iron_ingot","gold_ingot","emerald","diamond","netherite_ingot","nether_star","gold_nugget","iron_nugget","redstone"})art.put("item:"+name,ImageIO.read(font.getParent().resolve("item-"+name+".png").toFile()));
    }
    public void image(String name,double x,double y,double w,double h,int u,int v,int sw,int sh) {
        g.drawImage(art.get(name),(int)x,(int)y,(int)(x+w),(int)(y+h),u,v,u+sw,v+sh,null);
    }
    public void fill(double x,double y,double w,double h,int argb) {
        g.setColor(new Color(argb,true));g.fillRect((int)x,(int)y,(int)w,(int)h);
    }
    private int index(char c) { return Math.max(0,characters.indexOf(c)); }
    private int advance(char c) {
        if(c==' ')return 4;
        int i=index(c),cx=(i%16)*8,cy=(i/16)*8;
        for(int x=7;x>=0;x--)for(int y=0;y<8;y++)if((atlas.getRGB(cx+x,cy+y)>>>24)!=0)return x+2;
        return 1;
    }
    private int width(String s) { int n=0;for(char c:s.toCharArray())n+=advance(c);return n; }
    private void draw(String s,int color,int dx,int dy) {
        int px=0;
        for(char c:s.toCharArray()) {
            int i=index(c),cx=(i%16)*8,cy=(i/16)*8;
            if(c!=' ')for(int y=0;y<8;y++)for(int x=0;x<8;x++) {
                int alpha=atlas.getRGB(cx+x,cy+y)>>>24;
                if(alpha!=0) {g.setColor(new Color((color&0xFFFFFF)|(alpha<<24),true));g.fillRect(px+x+dx,y+dy,1,1);}
            }
            px+=advance(c);
        }
    }
    public void text(String value,double x,double y,double size,int color,double maxWidth,boolean centered) {
        if(value.isEmpty())return;
        double scale=Math.min(size/9,maxWidth/Math.max(1,width(value)));
        if(centered)x-=width(value)*scale/2;
        AffineTransform old=g.getTransform();g.translate(x,y);g.scale(scale,scale);
        draw(value,0xFF000000|((color&0xFCFCFC)>>2),1,1);draw(value,color,0,0);g.setTransform(old);
    }
    public static void main(String[] args) throws Exception {
        Path r=Path.of(args[0]),b=Path.of(args[1]),out=Path.of(args[2]);Files.createDirectories(out);
        for(String state:new String[]{"ready","tails","pending","win","loss","insufficient","rules","small"}) {
            int w=state.equals("small")?854:1536,h=state.equals("small")?480:1024;
            BufferedImage image=new BufferedImage(w,h,BufferedImage.TYPE_INT_ARGB);Graphics2D g=image.createGraphics();
            g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);
            g.setColor(new Color(0x101513));g.fillRect(0,0,w,h);
            var fit=ArcadeLayout.fit(w,h);g.translate(fit.x(),fit.y());g.scale(fit.scale(),fit.scale());
            var model=new CoinModel();model.balance=12450;long time=5000;
            switch(state) {
                case "tails" -> model.side=1;
                case "pending" -> {model.begin(4600);}
                case "win" -> {model.begin(2000);model.receive(new int[]{1,0,1,196},"",2200);model.balance=12546;}
                case "loss" -> {model.begin(2000);model.receive(new int[]{1,1,0,0},"",2200);model.balance=12350;}
                case "insufficient" -> model.balance=50;
                case "rules" -> model.rules=true;
            }
            var canvas=new RenderPreview(g,r,b.resolve("ascii.png"),b.resolve("ascii-chars.txt"));
            ArcadeView.render(canvas,model,time,ArcadeView.Input.idle());g.dispose();
            ImageIO.write(image,"png",out.resolve("coin-flip-"+state+".png").toFile());
        }
        System.out.println("PASS: rendered 8 states with the production ArcadeView and local Minecraft bitmap font; no game launched.");
    }
}
