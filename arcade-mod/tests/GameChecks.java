import local.customatm.arcade.*;
import java.util.*;

/** Pure protocol and interaction regressions; no game classes/bootstrap. */
public final class GameChecks {
    static int checks;
    static void check(boolean b,String why){checks++;if(!b)throw new AssertionError(why);}
    static GameModel model(GameKind k){GameModel m=new GameModel(k);m.balance=100000;return m;}
    static void request(GameModel.Request r,String action,int...args){check(r!=null&&r.action().equals(action)&&Arrays.equals(r.args(),args),"Wrong request: "+action);}
    public static void main(String[] args){
        for(GameKind kind:GameKind.values()){
            var m=model(kind);Set<String> ids=new HashSet<>();
            for(var b:GameControls.boxes(kind)){check(ids.add(b.id()),"Duplicate control "+kind+" "+b.id());check(b.x()>=88&&b.y()>=32&&b.x()+b.w()<=1452&&b.y()+b.h()<=986,"Control off canvas");}
            m.rules=true;for(var b:GameControls.boxes(kind))check(GameControls.enabled(b.id(),m,0)==(b.id().equals("dismiss")||b.id().equals("close")),"Modal leaks input");m.rules=false;
            if(kind==GameKind.HUB||kind==GameKind.COIN_FLIP)continue;
            m.balance=10;check(!m.canStart(0),"Insufficient credits");m.balance=100000;
            if(kind==GameKind.ROULETTE)m.addWager(0);
            check(m.start(1000)!=null,"Valid start "+kind);check(m.start(1001)==null,"Duplicate bet "+kind);
            check(!GameControls.enabled("game1",m,20000),"Navigation while pending "+kind);
            check(m.status(12000).contains("Waiting"),"Late reply state");
            check(!m.receive("start",new int[]{0},"Rejected",13000),"Rejected bet accepted");check(!m.pending,"Rejected bet unlock");
        }
        var slots=model(GameKind.SLOTS);request(slots.start(1000),"spin",100);check(slots.receive("spin",new int[]{1,6,6,6,20000},"",1100),"Slots parse");check(slots.returned==20000&&!slots.canStart(2000)&&slots.canStart(3000),"Slots animation gating");
        slots.start(4000);check(!slots.receive("spin",new int[]{1,7,0,0,0},"",4200)&&slots.pending,"Malformed result fail closed");
        var mines=model(GameKind.MINES);request(mines.start(1000),"start",100,5);mines.receive("start",new int[]{1},"",1100);check(mines.active&&mines.returned==97,"Initial mines cashout");check(Math.abs(mines.nextSafeChance()-.8)<.0001,"Mines safe chance");
        request(mines.action("reveal",0,1400),"reveal",0);check(mines.action("reveal",0,1401)==null,"Duplicate reveal");mines.receive("reveal",new int[]{1,0,0,121,121,0},"",1500);check(mines.safe==1&&mines.cells[0]==1&&mines.returned==121,"Safe tile");check(mines.action("reveal",0,2000)==null,"Revealed cell replay");
        request(mines.action("cashout",0,2000),"cashout");int[] mineCash=new int[28];mineCash[0]=1;mineCash[1]=121;mineCash[2]=1;mineCash[7]=1;mines.receive("cashout",mineCash,"",2100);check(!mines.active&&mines.returned==121&&mines.cells[4]==2,"Mines cashout board");
        var bj=model(GameKind.BLACKJACK);request(bj.start(1000),"start",100);bj.receive("start",new int[]{1,2,9,32,2,11,-1,0,0,100},"",1200);check(bj.active&&bj.player.size()==2&&bj.dealer.contains(-1),"Blackjack hidden hand");check(GameModel.total(bj.player)==17,"Blackjack total");
        request(bj.action("double",0,1600),"double");bj.receive("double",new int[]{1,2,9,32,2,11,-1,0,0,100},"Insufficient chips",1700);check(bj.active&&!bj.pending&&bj.submitted==100,"Failed double retains round");
        request(bj.action("stand",0,2300),"stand");bj.receive("resolve",new int[]{1,2,9,32,2,11,5,1,1,100,200},"",2400);check(!bj.active&&bj.returned==200&&bj.submitted==100,"Blackjack payout uses appended field, not stake");
        check(GameModel.total(List.of(0,13,9))==12,"Soft aces");check(GameModel.total(List.of(0,9))==21,"Natural total");
        var natural=model(GameKind.BLACKJACK);natural.start(1000);natural.receive("resolve",new int[]{1,2,0,9,2,11,5,1,1,100,250},"",1200);check(natural.returned==250&&!natural.active,"Natural resolves start");
        var roulette=model(GameKind.ROULETTE);check(!roulette.canStart(1000),"Empty roulette");check(roulette.addWager(1000),"Red bet");roulette.selectedType=0;roulette.selectedNumber=17;roulette.input="25";roulette.addWager(1000);request(roulette.start(1000),"spin",2,1,0,100,0,17,25);roulette.receive("spin",new int[]{1,17,2,0,0,1,900},"",1200);check(roulette.returned==900&&roulette.submitted==125&&roulette.wagers.isEmpty(),"Roulette totals");
        var capped=model(GameKind.ROULETTE);capped.balance=150;check(capped.addWager(0)&&!capped.addWager(0),"Aggregate wallet limit");
        var plinko=model(GameKind.PLINKO);plinko.risk=2;request(plinko.start(1000),"drop",100,2);plinko.receive("drop",new int[]{1,8,255,5,5},"",1200);check(plinko.bucket==8&&plinko.pathMask==255&&plinko.multiplier==.05&&plinko.returned==5,"Plinko authoritative path");
        var scratch=model(GameKind.SCRATCH);request(scratch.start(1000),"buy",100);scratch.receive("buy",new int[]{1,3,0,3,2,1,5,3,0,2,3,1000},"",1100);check(scratch.returned==1000&&scratch.winningSymbol==3&&!scratch.canStart(2000),"Scratch paid but hidden");Arrays.fill(scratch.scratched,true);check(scratch.canStart(2000),"Scratch new ticket after reveal");
        var crash=model(GameKind.CRASH);request(crash.start(1000),"start",100);crash.receive("start",new int[]{1},"",1100);request(crash.poll(1100),"poll");check(crash.poll(1200)==null,"Crash polling rate");request(crash.action("cashout",0,1200),"cashout");crash.receive("poll",new int[]{1,150,1},"",1250);check(crash.pending&&crash.pendingAction.equals("cashout"),"Late poll cannot unlock cashout");check(crash.poll(2000)==null,"No polling while cashout pending");crash.receive("cashout",new int[]{1,156,1,156},"",1300);check(!crash.active&&!crash.pending&&crash.returned==156,"Crash settle");check(!crash.receive("poll",new int[]{1,199,1},"",1350)&&crash.multiplier==1.56,"Ignore stale post-settlement poll");
        crash.start(2000);crash.receive("start",new int[]{1},"",2100);crash.receive("crashed",new int[]{1,100,0},"",2200);check(crash.returned==0&&!crash.active,"Instant crash");
        System.out.println("PASS: "+checks+" additional game protocol/input checks.");
    }
}
