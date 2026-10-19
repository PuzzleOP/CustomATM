import local.customatm.arcade.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.nio.file.*;
import java.util.*;
import javax.imageio.ImageIO;

public final class RenderAllPreview {
    static GameModel sample(GameKind kind,String state){
        GameModel m=new GameModel(kind);m.balance=12450;
        if(state.equals("rules")){m.rules=true;return m;}
        if(state.equals("insufficient")){m.balance=10;return m;}
        if(state.equals("ready")||kind==GameKind.HUB)return m;
        if(kind==GameKind.ROULETTE){m.addWager(1000);m.selectedType=0;m.selectedNumber=17;m.addWager(1000);}
        m.start(1000);
        if(state.equals("pending"))return m;
        switch(kind){
            case SLOTS->m.receive("spin",new int[]{1,3,3,3,1500},"",1200);
            case MINES->{m.receive("start",new int[]{1},"",1200);m.action("reveal",0,1500);m.receive("reveal",new int[]{1,0,0,121,121,0},"",1600);m.action("reveal",6,1800);m.receive("reveal",new int[]{1,6,0,153,153,0},"",1900);}
            case BLACKJACK->m.receive("start",new int[]{1,2,9,32,2,11,-1,0,0,100},"",1200);
            case ROULETTE->m.receive("spin",new int[]{1,17,2,0,0,1,3600},"",1200);
            case PLINKO->{m.risk=1;m.receive("drop",new int[]{1,6,0b10101010101,30,30},"",1200);}
            case SCRATCH->{m.receive("buy",new int[]{1,3,0,3,2,1,5,3,0,2,3,1000},"",1200);Arrays.fill(m.scratched,true);}
            case CRASH->{m.receive("start",new int[]{1},"",1200);for(int i=0;i<25;i++)m.receive("poll",new int[]{1,100+i*i/2,1},"",1300+i*300);}
            default->{}
        }
        if(state.equals("loss")){
            if(kind==GameKind.MINES){m.action("reveal",4,4000);int[] d=new int[28];d[0]=1;d[1]=4;d[2]=1;for(int i:new int[]{4,8,12,15,22})d[3+i]=1;m.receive("reveal",d,"",4200);}
            else if(kind==GameKind.BLACKJACK){m.action("hit",0,4000);m.receive("resolve",new int[]{1,3,9,32,8,2,11,3,1,1,100,0},"",4200);}
            else if(kind==GameKind.CRASH)m.receive("crashed",new int[]{1,388,0},"",4200);
            else {m.returned=0;if(kind==GameKind.SLOTS)m.symbols=new int[]{0,2,4};if(kind==GameKind.SCRATCH){m.winningSymbol=-1;m.ticket=new int[]{0,0,1,1,2,2,3,3,4};}}
        }
        return m;
    }
    static void draw(Graphics2D g,Path r,Path b,GameKind kind,String state,int w,int h)throws Exception{
        g.setRenderingHint(RenderingHints.KEY_INTERPOLATION,RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);g.setColor(new Color(0x101513));g.fillRect(0,0,w,h);
        var fit=ArcadeLayout.fit(w,h);g.translate(fit.x(),fit.y());g.scale(fit.scale(),fit.scale());
        var c=new RenderPreview(g,r,b.resolve("ascii.png"),b.resolve("ascii-chars.txt"));
        if(kind==GameKind.COIN_FLIP){var coin=new CoinModel();coin.balance=12450;ArcadeView.render(c,coin,5000,ArcadeView.Input.idle());}
        else GameView.render(c,sample(kind,state),state.equals("pending")?1800:10000,ArcadeView.Input.idle());
    }
    public static void main(String[] args)throws Exception{
        Path r=Path.of(args[0]),b=Path.of(args[1]),out=Path.of(args[2]);int count=0;
        for(GameKind kind:GameKind.values())if(kind!=GameKind.COIN_FLIP)for(String state:new String[]{"ready","playing","pending","loss","rules","insufficient","small"}){
            if(kind==GameKind.HUB&&!state.equals("ready")&&!state.equals("small"))continue;
            int w=state.equals("small")?854:1536,h=state.equals("small")?480:1024;
            var image=new BufferedImage(w,h,BufferedImage.TYPE_INT_RGB);Graphics2D g=image.createGraphics();draw(g,r,b,kind,state.equals("small")?"playing":state,w,h);g.dispose();ImageIO.write(image,"png",out.resolve(kind.target()+"-"+state+".png").toFile());count++;
        }
        var sheet=new BufferedImage(2304,1536,BufferedImage.TYPE_INT_RGB);int n=0;
        for(GameKind kind:GameKind.values()){
            Graphics2D g=sheet.createGraphics();g.translate(n%3*768,n/3*512);g.clipRect(0,0,768,512);draw(g,r,b,kind,kind==GameKind.ROULETTE?"ready":"playing",768,512);g.dispose();n++;
        }
        ImageIO.write(sheet,"png",out.resolve("all-games-overview.png").toFile());
        System.out.println("PASS: "+count+" additional game-state renders and nine-screen overview; production renderers, no game launched.");
    }
}
