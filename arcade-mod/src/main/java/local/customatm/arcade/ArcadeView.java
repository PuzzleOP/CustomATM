package local.customatm.arcade;

/** The native screen and headless preview execute this exact drawing routine. */
public final class ArcadeView {
    public interface Canvas {
        void image(String name, double x, double y, double w, double h, int u, int v, int sw, int sh);
        void fill(double x, double y, double w, double h, int argb);
        void text(String value, double x, double y, double size, int color, double maxWidth, boolean centered);
    }
    public record Input(String hover, String focus, boolean editing, int cursor, String selected, boolean blink) {
        public static Input idle() { return new Input("","",false,0,"",false); }
    }
    private static final int WHITE=0xFFF1ECD9, GRAY=0xFFADAFAE, GREEN=0xFF49F9A5, GOLD=0xFFFFE7A0;
    private static void texture(Canvas c,String n,double x,double y,double w,double h) { c.image(n,x,y,w,h,0,0,1254,1254); }
    private static void border(Canvas c,ArcadeLayout.Box b,int color) {
        c.fill(b.x(),b.y(),b.w(),2,color);c.fill(b.x(),b.y()+b.h()-2,b.w(),2,color);
        c.fill(b.x(),b.y(),2,b.h(),color);c.fill(b.x()+b.w()-2,b.y(),2,b.h(),color);
    }
    public static boolean enabled(String id,CoinModel m,long now) {
        if (m.rules) return id.equals("dismiss") || id.equals("close");
        if (id.equals("dismiss")) return false;
        if (id.equals("close") || id.equals("rules")) return true;
        if (m.locked(now)) return false;
        if (id.equals("flip")) return m.canFlip(now);
        return !id.equals("game1");
    }
    public static void render(Canvas c,CoinModel m,long now,Input in) {
        // Sample only the designed frame; no generated scenery becomes the live world background.
        c.image("skin",88,32,1364,954,88,32,1364,954);
        c.text("REDSTONE ARCADE",285,78,17,GRAY,270,true);
        c.text("CustomATM Arcade",782,68,40,WHITE,415,true);
        c.text("DynEco wallet",1151,81,17,GRAY,154,false);
        c.text(CoinModel.money(m.balance),1354,81,23,GREEN,112,true);
        c.text("Coin Flip",830,158,66,GOLD,560,true);
        c.text("Pick a side. One coin, one result.",830,233,25,GRAY,655,true);
        for (int i=0;i<8;i++) c.text(ArcadeLayout.GAMES[i],242,171+i*95,28,WHITE,191,false);
        c.text("Win chance",1113,318,23,WHITE,180,false);c.text("50%",1336,316,25,GREEN,70,true);
        long bet = m.bet(), payout = CoinModel.payout(bet);
        c.text("Total return",1113,385,22,WHITE,180,false);c.text(bet>0?CoinModel.money(payout):"--",1335,383,25,GREEN,83,true);
        c.text("Net win",1113,445,23,WHITE,150,false);c.text(bet>0?"+"+CoinModel.money(payout-bet):"--",1333,444,25,GREEN,87,true);
        c.fill(1112,358,250,1,0xFF424747);c.fill(1112,482,250,1,0xFF424747);
        c.text("A loss costs "+CoinModel.money(bet)+".",1113,499,18,GRAY,247,false);
        c.text("Return includes your bet.",1113,526,18,GRAY,247,false);
        c.text("Rules & payouts",1113,559,20,GREEN,246,false);
        boolean spin=m.locked(now);
        double phase=(now-m.started)/180.0;
        boolean heads=spin?Math.cos(phase)>=0:(m.resultReady?m.landed==0:m.side==0);
        double coinW=spin?Math.max(24,300*Math.abs(Math.cos(phase))):300;
        double lift=spin?Math.sin(Math.min(1,(now-m.started)/1200.0)*Math.PI)*35:0;
        texture(c,heads?"heads":"tails",831-coinW/2,251-lift,coinW,285);
        for(int side=0;side<2;side++) {
            var b=ArcadeLayout.box(side==0?"heads":"tails");
            boolean selected=m.side==side;
            c.image("skin",b.x(),b.y(),b.w(),b.h(),selected?548:814,566,selected?255:252,65);
            texture(c,side==0?"heads":"tails",b.x()+38,b.y()+10,47,47);
            c.text(side==0?"Heads":"Tails",b.x()+105,b.y()+21,27,selected?WHITE:GRAY,139,false);
        }
        c.text("Bet amount",580,688,25,GRAY,174,false);
        c.text("-",791,683,34,WHITE,40,true);c.text("+",1164,683,34,WHITE,40,true);
        String amount=in.editing?m.input:CoinModel.money(bet);
        if(in.editing && in.blink) {
            int pos=Math.min(in.cursor,amount.length());amount=amount.substring(0,pos)+"|"+amount.substring(pos);
        }
        if(in.editing && !in.selected.isEmpty()) c.fill(841,676,273,39,0x6634D895);
        c.text(amount,976,683,30,WHITE,280,true);
        for(int n:new int[]{25,50,100,250}) {
            var b=ArcadeLayout.box("preset"+n);
            c.image("skin",b.x(),b.y(),b.w(),b.h(),bet==n?982:756,744,98,45);
            c.text("$"+n,b.x()+b.w()/2.0,b.y()+14,20,WHITE,b.w()-12,true);
        }
        c.text(spin?"Flipping...":"Flip - "+CoinModel.money(bet),969,837,34,WHITE,391,true);
        if(!enabled("flip",m,now)) {var b=ArcadeLayout.box("flip");c.fill(b.x(),b.y(),b.w(),b.h(),0x77232323);}
        String status=m.status(now);
        if(!status.isEmpty()) c.text(status,938,634,18,m.resultReady&&!spin?(m.won?GREEN:0xFFFFC187):GRAY,820,true);
        c.text("DynEco connected  |  Server-settled bets",162,931,17,GRAY,780,false);
        c.text("Esc  Close",1320,931,19,WHITE,145,true);
        for(var b:ArcadeLayout.CONTROLS) {
            if(enabled(b.id(),m,now) && (b.id().equals(in.hover) || b.id().equals(in.focus))) {
                c.fill(b.x()+3,b.y()+3,b.w()-6,b.h()-6,0x153CFFA3);
                border(c,b,GREEN);
            }
        }
        if(m.rules) {
            c.fill(88,32,1364,954,0xD00A0D0C);
            c.image("skin",437,220,700,598,1085,286,299,312);
            c.text("Coin Flip rules",787,264,38,GOLD,620,true);
            String[] lines={"Choose Heads or Tails, then place one bet.","Each side has a 50% chance to win.","A win returns 1.96x your bet, rounded to", "whole credits. That includes your stake.","Example: $100 bet -> $196 back (+$96).", "A loss returns $0 and costs your bet.","The server decides the result and pays", "your DynEco wallet. No automatic re-bets."};
            for(int i=0;i<lines.length;i++)c.text(lines[i],479,339+i*40,22,WHITE,610,false);
            c.text("Current rules; other games are unchanged.",787,680,18,GRAY,615,true);
            var b=ArcadeLayout.box("dismiss");c.image("skin",b.x(),b.y(),b.w(),b.h(),548,566,255,65);
            c.text("Back to game",799,751,24,WHITE,224,true);
        }
    }
}
