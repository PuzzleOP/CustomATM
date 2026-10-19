package local.customatm.arcade;

import java.util.*;
import local.customatm.arcade.ArcadeLayout.Box;
import local.customatm.arcade.ArcadeView.Canvas;
import local.customatm.arcade.ArcadeView.Input;

/** The production native GUI and offline previews share this renderer. */
public final class GameView {
    static final int WHITE=0xFFF1ECD9,GRAY=0xFFADB4AD,GREEN=0xFF49F9A5,GOLD=0xFFFFD98C,RED=0xFFFF8C79;
    public static final String[] ITEMS={"coal","iron_ingot","gold_ingot","emerald","diamond","netherite_ingot","nether_star"};
    public static final double[][] PLINKO={{8,3,1.5,1.2,1,.8,.6,.4,.3,.4,.6,.8,1,1.2,1.5,3,8},{15,6,3,1.5,.8,.5,.3,.2,.1,.2,.3,.5,.8,1.5,3,6,15},{30,10,5,2,.5,.3,.1,.1,.05,.1,.1,.3,.5,2,5,10,30}};
    public static String money(long n){return CoinModel.money(n);}
    static String mult(double n){return String.format(Locale.ROOT,"%.2fx",n);}
    static void text(Canvas c,String s,double x,double y,double size,int color,double width){c.text(s,x,y,size,color,width,false);}
    static void center(Canvas c,String s,double x,double y,double size,int color,double width){c.text(s,x,y,size,color,width,true);}
    static void panel(Canvas c,double x,double y,double w,double h){c.image("skin",x,y,w,h,1085,286,299,312);}
    static void item(Canvas c,String n,double x,double y,double size){c.image("item:"+n,x,y,size,size,0,0,16,16);}
    static void icon(Canvas c,int n,double x,double y,double size){c.image("shell",x,y,size,size,140,145+95*n,88,78);}
    static void outline(Canvas c,Box b,int color){c.fill(b.x(),b.y(),b.w(),2,color);c.fill(b.x(),b.y()+b.h()-2,b.w(),2,color);c.fill(b.x(),b.y(),2,b.h(),color);c.fill(b.x()+b.w()-2,b.y(),2,b.h(),color);}
    static void button(Canvas c,GameModel m,String id,String label,boolean selected,long now){
        Box b=GameControls.box(m.kind,id);boolean enabled=GameControls.enabled(id,m,now);
        c.image("skin",b.x(),b.y(),b.w(),b.h(),selected?548:814,566,selected?255:252,65);
        if(!enabled)c.fill(b.x()+3,b.y()+3,b.w()-6,b.h()-6,0x88202523);
        center(c,label,b.x()+b.w()/2.0,b.y()+b.h()/2.0-10,Math.min(27,b.h()*.39),enabled?WHITE:GRAY,b.w()-22);
    }
    public static void render(Canvas c,GameModel m,long now,Input in){
        c.image("shell",88,32,1364,954,88,32,1364,954);
        text(c,"REDSTONE ARCADE",158,78,17,GRAY,275);center(c,"CustomATM Arcade",782,68,40,WHITE,415);
        text(c,"DynEco wallet",1151,81,17,GRAY,154);center(c,money(m.balance),1354,81,23,GREEN,112);
        for(int i=0;i<8;i++){
            if(i==m.kind.nav){Box b=GameControls.box(m.kind,"game"+i);c.fill(b.x()+4,b.y()+4,b.w()-8,b.h()-8,0x3034DB8F);outline(c,b,0xFF5BBE89);}
            text(c,ArcadeLayout.GAMES[i],242,171+i*95,28,i==m.kind.nav?GREEN:WHITE,191);
        }
        text(c,m.kind==GameKind.HUB?"Welcome to the Arcade":m.kind.title,520,159,m.kind==GameKind.HUB?46:52,GOLD,m.kind==GameKind.HUB?850:650);
        text(c,m.kind.description,520,231,22,GRAY,850);
        if(m.kind==GameKind.HUB)hub(c,m,now);
        else {
            button(c,m,"rules","Rules & payouts",false,now);
            switch(m.kind){case SLOTS->slots(c,m,now);case MINES->mines(c,m,now);case BLACKJACK->blackjack(c,m,now);case ROULETTE->roulette(c,m,now);case PLINKO->plinko(c,m,now);case SCRATCH->scratch(c,m,now);case CRASH->crash(c,m,now);default->{}}
            footer(c,m,now,in);
        }
        text(c,m.active?"Round continues while connected. Return here to resume.":"DynEco connected  |  Server-settled bets",162,931,17,GRAY,1030);
        center(c,"Esc  Close",1320,931,19,WHITE,145);
        for(Box b:GameControls.boxes(m.kind))if(GameControls.enabled(b.id(),m,now)&&(b.id().equals(in.hover())||b.id().equals(in.focus()))){c.fill(b.x()+3,b.y()+3,b.w()-6,b.h()-6,0x183CFFA3);outline(c,b,GREEN);}
        if(m.rules)rules(c,m,now);
    }
    private static void hub(Canvas c,GameModel m,long now){
        String[] hints={"Match symbols across three reels","Heads or tails. 50% chance","Find emeralds, avoid hidden mines","Hit, stand or double your hand","Straight numbers and outside bets","16 rows. Three risk levels","Reveal nine hidden symbols","Cash out before it crashes"};
        for(int i=0;i<8;i++){
            Box b=GameControls.box(m.kind,"tile"+i);panel(c,b.x(),b.y(),b.w(),b.h());icon(c,i,b.x()+14,b.y()+17,84);
            text(c,ArcadeLayout.GAMES[i],b.x()+114,b.y()+25,30,WHITE,275);
            text(c,hints[i],b.x()+114,b.y()+73,17,GRAY,274);
        }
        center(c,"Choose a game to see its rules and payouts before betting.",940,877,19,GRAY,850);
    }
    private static void footer(Canvas c,GameModel m,long now,Input in){
        text(c,m.kind==GameKind.ROULETTE?"Amount per position":"Bet amount",520,756,19,GRAY,335);
        button(c,m,"minus","-",false,now);button(c,m,"plus","+",false,now);
        Box entry=GameControls.box(m.kind,"bet");panel(c,entry.x(),entry.y(),entry.w(),entry.h());
        String value=in.editing()?m.input:money(m.bet());
        if(in.editing()&&in.blink()){int p=Math.min(in.cursor(),value.length());value=value.substring(0,p)+"|"+value.substring(p);}
        if(in.editing()&&!in.selected().isEmpty())c.fill(582,790,210,36,0x6634D895);
        center(c,value,688,798,27,WHITE,203);
        for(int n:new int[]{25,50,100,250})button(c,m,"preset"+n,"$"+n,m.bet()==n,now);
        String label=switch(m.kind){case SLOTS->"Spin";case MINES,CRASH->"Start round";case BLACKJACK->"Deal hand";case ROULETTE->"Spin wheel";case PLINKO->"Drop ball";case SCRATCH->"Buy ticket";default->"Play";};
        long cost=m.kind==GameKind.ROULETTE?m.totalWager():m.bet();
        button(c,m,"start",m.pending?"Waiting...":m.active?"Round in progress":label+" - "+money(cost),true,now);
        text(c,m.status(now),520,891,16,m.hasResult&&!m.locked(now)?(m.returned>=m.submitted?GREEN:RED):GRAY,850);
    }
    private static void slots(Canvas c,GameModel m,long now){
        c.image("slot_frame",510,278,870,389,0,0,1875,839);
        for(int i=0;i<3;i++){
            boolean spin=m.pending||now<m.animationEnd-(2-i)*220;
            int symbol=spin?(int)((now/95+i*3)%7):m.symbols[i];
            item(c,ITEMS[symbol],585+i*264,400,148);
        }
        center(c,m.locked(now)?"REELS IN MOTION":"THREE OF A KIND",943,289,18,GOLD,680);
        center(c,"Pair: 1.2x  |  Triples pay 3x to 200x",940,676,23,WHITE,850);
        center(c,"Return includes the stake. See the full paytable in Rules.",940,715,18,GRAY,850);
    }
    private static void mines(Canvas c,GameModel m,long now){
        for(int i=0;i<25;i++){
            Box b=GameControls.box(m.kind,"cell"+i);
            c.image("skin",b.x(),b.y(),b.w(),b.h(),m.cells[i]==1?548:814,566,m.cells[i]==1?255:252,65);
            if(m.cells[i]!=0)item(c,m.cells[i]==1?"emerald":"redstone",b.x()+18,b.y()+12,48);
            else center(c,"?",b.x()+42,b.y()+23,28,m.active?GOLD:GRAY,60);
        }
        panel(c,1018,280,360,407);text(c,"Mines on the board",1040,305,23,WHITE,316);
        button(c,m,"minesLess","-",false,now);button(c,m,"minesMore","+",false,now);center(c,m.mines+" / 25",1198,360,25,GOLD,180);
        text(c,"Next safe tile",1040,425,20,GRAY,210);text(c,String.format(Locale.ROOT,"%.1f%%",m.nextSafeChance()*100),1270,423,23,GREEN,89);
        text(c,"Safe tiles found",1040,468,20,GRAY,240);text(c,""+m.safe,1314,466,23,WHITE,44);
        text(c,"Cash-out return",1040,517,20,GRAY,316);center(c,money(m.active?m.returned:0),1198,552,32,GREEN,300);
        button(c,m,"cashout","Cash out",true,now);
        text(c,m.active?"Next safe return: "+money(m.nextMineReturn()):"Choose 1-24 mines before starting.",520,712,21,GRAY,850);
    }
    private static void cards(Canvas c,List<Integer> cards,int y){
        int count=cards.size();double step=count<=6?130:Math.min(118,714.0/Math.max(1,count-1));
        if(count==0){c.image("card_back",530,y,113,157,66,69,890,1397);return;}
        for(int i=0;i<count;i++){
            int card=cards.get(i);double x=945-(113+(count-1)*step)/2+i*step;
            c.image(card<0?"card_back":"card_face",x,y,113,157,66,69,890,1397);
            if(card>=0){String rank=new String[]{"A","2","3","4","5","6","7","8","9","10","J","Q","K"}[card%13];String suit=new String[]{"CLUB","DIAMOND","HEART","SPADE"}[card/13];int color=(card/13==1||card/13==2)?0xFF9D302B:0xFF26352D;
                text(c,rank,x+12,y+14,24,color,82);center(c,suit,x+56,y+68,14,color,86);center(c,rank,x+56,y+100,33,color,75);
            }
        }
    }
    private static void blackjack(Canvas c,GameModel m,long now){
        text(c,"DEALER",520,271,20,GRAY,360);text(c,m.dealer.contains(-1)?"One card hidden":"Total: "+GameModel.total(m.dealer),1110,271,21,WHITE,260);
        cards(c,m.dealer,306);text(c,"YOUR HAND",520,480,20,GOLD,360);text(c,"Total: "+GameModel.total(m.player),1110,480,25,GREEN,260);cards(c,m.player,516);
        button(c,m,"hit","Hit",false,now);button(c,m,"stand","Stand",true,now);button(c,m,"double","Double +"+money(m.submitted>0?m.submitted:m.bet()),false,now);
        text(c,"Dealer hits soft 17. Blackjack pays 2.5x total.",882,766,16,GRAY,485);
    }
    public static boolean red(int n){return Set.of(1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36).contains(n);}
    private static void roulette(Canvas c,GameModel m,long now){
        String selected=m.selectedType==0?"Number "+m.selectedNumber:GameControls.box(m.kind,"outside"+m.selectedType).label();
        text(c,"Selected: "+selected,520,280,24,GOLD,490);
        int shown=m.locked(now)?(int)(now/60%37):m.winning;
        text(c,shown<0?"Total stake: "+money(m.totalWager()):"Winning number: "+shown,1040,280,24,shown>=0&&red(shown)?RED:GREEN,330);
        for(int n=0;n<=36;n++){
            Box b=GameControls.box(m.kind,"number"+n);c.fill(b.x(),b.y(),b.w(),b.h(),n==0?0xFF205F42:red(n)?0xFF793D36:0xFF242C29);outline(c,b,0xFF7D8276);
            if(m.selectedType==0&&m.selectedNumber==n)outline(c,b,GREEN);
            center(c,""+n,b.x()+b.w()/2.0,b.y()+b.h()/2.0-11,23,WHITE,b.w()-10);
            final int number=n;if(m.wagers.stream().anyMatch(w->w.type()==0&&w.number()==number))item(c,"gold_nugget",b.x()+b.w()-16,b.y()+3,13);
        }
        for(int i=1;i<=9;i++){String id="outside"+i;final int type=i;long stake=m.wagers.stream().filter(w->w.type()==type).mapToLong(GameModel.Wager::amount).sum();button(c,m,id,GameControls.box(m.kind,id).label()+(stake>0?" "+money(stake):""),m.selectedType==i,now);}
        button(c,m,"add","Place "+money(m.bet()),true,now);button(c,m,"undo","Undo last",false,now);button(c,m,"clear","Clear bets",false,now);
        text(c,m.wagers.size()+" positions  |  Total "+money(m.totalWager()),886,766,16,GRAY,482);
    }
    private static void plinko(Canvas c,GameModel m,long now){
        panel(c,510,272,870,421);
        for(int row=0;row<16;row++)for(int col=0;col<=row;col++)c.image("item:iron_nugget",936+(col-row/2.0)*47,294+row*21,10,8,4,5,8,6);
        double progress=m.hasResult?Math.min(16,Math.max(0,(now-m.started)/145.0)):0;
        int step=(int)progress,rights=0;for(int i=0;i<step;i++)rights+=(m.pathMask>>>i)&1;
        double fraction=progress-step;int next=step<16?(m.pathMask>>>step)&1:0;
        double offset=(rights-step/2.0+(next-.5)*fraction)*47;
        c.image("item:gold_nugget",931+offset,282+progress*21,20,23,5,4,6,8);
        for(int i=0;i<17;i++){
            double x=529+i*49;double payout=PLINKO[m.risk][i];boolean landed=m.hasResult&&!m.locked(now)&&m.bucket==i;
            c.fill(x,646,45,35,landed?0xFF267849:payout>=1?0xFF805A32:0xFF353F39);
            center(c,Double.toString(payout).replaceAll("\\.0$","")+"x",x+22,658,15,landed?GREEN:WHITE,42);
        }
        for(int i=0;i<3;i++)button(c,m,"risk"+i,new String[]{"Low risk","Medium risk","High risk"}[i],m.risk==i,now);
        text(c,"Center buckets are more likely. 16 fair left/right steps.",885,766,15,GRAY,480);
    }
    private static void scratch(Canvas c,GameModel m,long now){
        int[] pay={2,3,5,10,25,50,150};
        for(int i=0;i<9;i++){
            Box b=GameControls.box(m.kind,"scratch"+i);
            if(m.hasResult&&m.scratched[i]){
                panel(c,b.x(),b.y(),b.w(),b.h());item(c,ITEMS[m.ticket[i]],b.x()+26,b.y()+22,80);
                if(m.allScratched()&&m.ticket[i]==m.winningSymbol)outline(c,b,GREEN);
            }else {c.image("card_back",b.x(),b.y(),b.w(),b.h(),66,69,890,1397);if(!m.hasResult)c.fill(b.x(),b.y(),b.w(),b.h(),0x66303931);}
        }
        panel(c,978,280,400,406);text(c,"MATCH 3 OR MORE",1001,302,24,GOLD,352);
        for(int i=0;i<7;i++){item(c,ITEMS[i],1005,345+i*44,30);text(c,ITEMS[i].replace('_',' '),1050,353+i*44,18,WHITE,220);text(c,pay[i]+"x",1285,353+i*44,19,GREEN,68);}
        button(c,m,"revealAll","Reveal whole ticket",true,now);text(c,"Highest qualifying symbol pays once.",979,711,18,GRAY,397);text(c,"Settled when bought; reveal is visual.",979,738,16,GRAY,397);
    }
    private static void crash(Canvas c,GameModel m,long now){
        panel(c,510,277,870,410);
        for(int i=0;i<5;i++)c.fill(550,350+i*63,790,1,0xFF3B4640);
        for(int i=0;i<7;i++)c.fill(550+i*130,343,1,264,0xFF303B35);
        c.fill(550,616,790,3,0xFF6F8373);
        if(m.trail.size()>1){double max=Math.max(2,m.multiplier);for(int i=1;i<m.trail.size();i++){
            double x1=554+(i-1)*772.0/Math.max(30,m.trail.size()-1),x2=554+i*772.0/Math.max(30,m.trail.size()-1);
            double y1=610-(m.trail.get(i-1)-1)/max*225,y2=610-(m.trail.get(i)-1)/max*225;
            int steps=(int)Math.max(Math.abs(x2-x1),Math.abs(y2-y1));for(int s=0;s<=steps;s++){double f=s/(double)Math.max(1,steps);c.fill(x1+(x2-x1)*f,y1+(y2-y1)*f,5,5,m.hasResult&&m.returned==0?RED:GREEN);}
        }}
        center(c,mult(m.multiplier),945,372,88,m.hasResult&&m.returned==0?RED:GREEN,650);
        center(c,m.active?"LIVE SERVER MULTIPLIER":m.hasResult?(m.returned==0?"CRASHED":"CASHED OUT"):"READY WHEN YOU ARE",945,490,24,WHITE,700);
        center(c,"A crash returns $0. Closing the menu does not pause the round.",945,645,17,GRAY,790);
        text(c,"Current return: "+money(Math.round(m.submitted*m.multiplier)),520,717,27,GREEN,460);
        button(c,m,"cashout",m.pending&&m.pendingAction.equals("cashout")?"Cash-out requested...":"Cash out",true,now);
    }
    public static String[] ruleLines(GameKind kind){return switch(kind){
        case SLOTS->new String[]{"Each reel independently selects one of seven symbols.","Weights: coal 30%, iron 25%, gold 20%, emerald 12%,", "diamond 8%, netherite 4%, nether star 1%.","Triples return 3x / 5x / 8x / 15x / 30x / 60x / 200x", "in that order. An exact pair returns 1.2x.","Other combinations return $0. Returns are rounded.","Returns include your stake; these are current server rules."};
        case MINES->new String[]{"Choose 1-24 mines on a 25-tile board, then start.","Reveal safe emeralds to increase your cash-out return.","A mine ends the round and returns $0.","Cash out before revealing another tile to keep the return.","Next-safe odds are shown for the remaining hidden tiles.","Return = stake x 0.97 / probability of your safe sequence.","Clearing all safe tiles pays automatically. Returns round.","Cash-out before the first reveal returns 0.97x your bet."};
        case BLACKJACK->new String[]{"Get closer to 21 than the dealer without going over.","Aces count as 1 or 11; face cards count as 10.","Hit draws a card. Stand lets the dealer finish.","Double adds your original stake, draws once, then stands.","Double is available only on your first two cards.","Dealer hits soft 17. The server uses a four-deck shoe.","Win: 2x total. Natural blackjack: 2.5x. Push: stake back.","Busting or losing returns $0. All payouts include stake."};
        case ROULETTE->new String[]{"Select a number or outside position, then Place bet.","You may add several positions before pressing Spin.","The server checks your total stake against its bet limits.","Single-zero wheel: each number 0-36 has equal chance.","Straight number: 36x return. Red/black, even/odd and", "low/high: 2x. Each dozen: 3x. Zero loses outside bets.","Return includes stake. Undo removes the last placed bet.","Gold markers show straight bets; outside bets show totals."};
        case PLINKO->new String[]{"Choose Low, Medium or High risk, then drop one ball.","The server makes 16 independent 50/50 left/right steps.","Center buckets are much more common than edge buckets.","Bucket multiplier x stake = total return, rounded.","The labels below the board show all 17 multipliers.","Each edge has a 1 in 65,536 chance; the center is 19.64%.","Higher risk changes the paytable, not the path odds.","The animation follows the result supplied by the server."};
        case SCRATCH->new String[]{"Buy a ticket, then click/drag its squares or Reveal all.","Three or more of a symbol anywhere on the ticket qualify.","Only the highest qualifying symbol pays, once per ticket.","Returns: coal 2x, iron 3x, gold 5x, emerald 10x,", "diamond 25x, netherite 50x, nether star 150x.","Symbol weights: 35 / 25 / 18 / 10 / 6 / 4 / 2 percent.","The server settles your wallet when the ticket is bought.","Revealing is visual; it cannot change your result."};
        case CRASH->new String[]{"Start a round and cash out before the server crashes.","The displayed multiplier is the latest server update.","A successful cash-out returns stake x server multiplier.","The multiplier may change while your request travels.","A crash returns $0. There is a 4% instant-crash branch;", "the remaining branch also includes results at 1.00x.","Growth follows 1 + 0.09 x elapsed seconds squared.","Closing the menu does not pause it. No auto cash-out."};
        default->new String[]{"Choose a game to read its rules."};};}
    private static void rules(Canvas c,GameModel m,long now){
        c.fill(88,32,1364,954,0xE00A0D0C);panel(c,405,181,812,684);
        center(c,m.kind.title+" rules",810,225,38,GOLD,732);
        String[] lines=ruleLines(m.kind);for(int i=0;i<lines.length;i++)text(c,lines[i],442,310+i*49,21,WHITE,739);
        center(c,"Current server rules. No automatic repeat bets.",810,735,17,GRAY,730);
        button(c,m,"dismiss","Back to game",true,now);
    }
}
