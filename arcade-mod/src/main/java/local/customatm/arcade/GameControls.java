package local.customatm.arcade;

import java.util.*;
import local.customatm.arcade.ArcadeLayout.Box;

/** Shared hit targets for native input, drawing and offline layout checks. */
public final class GameControls {
    private static final Map<GameKind,List<Box>> ALL=new EnumMap<>(GameKind.class);
    static {for(GameKind kind:GameKind.values())ALL.put(kind,build(kind));}
    public static List<Box> boxes(GameKind kind){return ALL.get(kind);}
    private static List<Box> build(GameKind kind) {
        List<Box> b=new ArrayList<>();
        for(int i=0;i<8;i++)b.add(new Box("game"+i,130,139+i*95,310,83,ArcadeLayout.GAMES[i]));
        b.add(new Box("home",510,60,520,50,"Arcade home"));
        b.add(new Box("close",1246,920,151,37,"Close casino"));
        b.add(new Box("dismiss",674,784,250,58,"Back to game"));
        if(kind==GameKind.HUB) {
            for(int i=0;i<8;i++)b.add(new Box("tile"+i,515+(i%2)*438,280+(i/2)*143,412,124,ArcadeLayout.GAMES[i]));
            return List.copyOf(b);
        }
        b.add(new Box("rules",1190,161,180,42,"Rules and payouts"));
        b.add(new Box("minus",520,782,48,54,"Decrease bet"));
        b.add(new Box("bet",576,782,224,54,"Bet amount in credits"));
        b.add(new Box("plus",808,782,48,54,"Increase bet"));
        for(int i=0;i<4;i++){int n=new int[]{25,50,100,250}[i];b.add(new Box("preset"+n,520+i*86,845,78,39,"Bet $"+n));}
        b.add(new Box("start",1010,798,360,80,switch(kind){case SLOTS->"Spin reels";case MINES->"Start round";case BLACKJACK->"Deal hand";case ROULETTE->"Spin wheel";case PLINKO->"Drop ball";case SCRATCH->"Buy ticket";case CRASH->"Start round";default->"Play";}));
        switch(kind) {
            case MINES -> {
                for(int i=0;i<25;i++)b.add(new Box("cell"+i,520+i%5*94,280+i/5*82,84,72,"Reveal tile "+(i+1)));
                b.add(new Box("minesLess",1040,346,58,50,"Fewer mines"));b.add(new Box("minesMore",1298,346,58,50,"More mines"));
                b.add(new Box("cashout",1040,604,316,72,"Cash out current return"));
            }
            case BLACKJACK -> {String[] ids={"hit","stand","double"};for(int i=0;i<3;i++)b.add(new Box(ids[i],520+i*282,691,265,57,ids[i].equals("double")?"Double stake and draw one card":ids[i]));}
            case ROULETTE -> {
                b.add(new Box("number0",520,346,58,177,"Straight bet on zero"));
                for(int n=1;n<=36;n++)b.add(new Box("number"+n,586+(n-1)/3*64,346+(2-(n-1)%3)*61,58,55,"Straight bet on "+n));
                String[] labels={"Red","Black","Even","Odd","1 - 18","19 - 36","1st dozen","2nd dozen","3rd dozen"};
                for(int i=0;i<9;i++)b.add(new Box("outside"+(i+1),520+i%3*282,537+i/3*49,270,42,labels[i]));
                b.add(new Box("add",520,698,270,50,"Place selected bet"));b.add(new Box("undo",802,698,270,50,"Undo last bet"));b.add(new Box("clear",1084,698,270,50,"Clear all bets"));
            }
            case PLINKO -> {for(int i=0;i<3;i++)b.add(new Box("risk"+i,520+i*282,704,270,47,new String[]{"Low risk","Medium risk","High risk"}[i]));}
            case SCRATCH -> {
                for(int i=0;i<9;i++)b.add(new Box("scratch"+i,520+i%3*143,280+i/3*136,133,126,"Reveal ticket square "+(i+1)));
                b.add(new Box("revealAll",520,704,419,47,"Reveal whole ticket"));
            }
            case CRASH -> b.add(new Box("cashout",1010,704,360,60,"Cash out at the server multiplier"));
            default -> {}
        }
        return List.copyOf(b);
    }
    public static Box box(GameKind kind,String id){return boxes(kind).stream().filter(b->b.id().equals(id)).findFirst().orElseThrow();}
    public static boolean enabled(String id,GameModel m,long now){
        if(m.rules)return id.equals("dismiss")||id.equals("close");
        if(id.equals("dismiss"))return false;
        if(id.equals("close")||id.equals("rules"))return true;
        if(id.equals("home")||id.startsWith("game")||id.startsWith("tile"))return !m.busy(now)&&!id.equals("game"+m.kind.nav);
        if(id.equals("start"))return m.canStart(now);
        if(m.locked(now))return false;
        if(id.equals("cashout"))return m.active;
        if(id.startsWith("cell"))return m.active&&m.cells[Integer.parseInt(id.substring(4))]==0&&m.nextMineReturn()<=Integer.MAX_VALUE;
        if(id.equals("hit")||id.equals("stand"))return m.active;
        if(id.equals("double"))return m.active&&m.player.size()==2&&m.invalid(m.submitted).isEmpty();
        if(id.startsWith("scratch"))return m.hasResult&&!m.scratched[Integer.parseInt(id.substring(7))];
        if(id.equals("revealAll"))return m.hasResult&&!m.allScratched();
        if(m.active)return false;
        if(id.equals("add"))return m.wagers.size()<64&&m.invalid(m.bet()).isEmpty()&&m.invalid(m.totalWager()+m.bet()).isEmpty();
        if(id.equals("undo")||id.equals("clear"))return !m.wagers.isEmpty();
        if(id.equals("minesLess"))return m.mines>1;
        if(id.equals("minesMore"))return m.mines<24;
        return true;
    }
}
