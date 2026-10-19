import local.customatm.arcade.*;
import java.util.*;

public class ArcadeChecks {
    private static int checks;
    static void check(boolean v,String why) { if(!v)throw new AssertionError(why);checks++; }
    public static void main(String[] args) {
        CoinModel m=new CoinModel();m.balance=12450;
        check(m.canFlip(2000),"valid bet");check(CoinModel.payout(100)==196,"actual 1.96x server payout");
        for(int n=1;n<=100000;n++)check(CoinModel.payout(n)==Math.round(n*1.96d),"payout rounding matches server");
        for(String s:List.of("","0","-1","abc","2147483648","999999999999999999999")) {
            m.input=s;check(!m.canFlip(2000),"invalid/out of range blocked: "+s);
        }
        m.input="12500";check(!m.canFlip(2000),"insufficient wallet blocked");m.input="100";
        m.side=1;check(Arrays.equals(m.begin(2000),new int[]{100,1}),"request carries correct bet and side");
        check(m.begin(2100)==null,"double bet blocked");check(m.balance==12450,"client never debits wallet");
        m.receive(new int[]{1,1,1,196},"",2200);check(m.locked(2300),"wait for animation after fast server result");
        check(!m.locked(3200),"release lock after response and animation");
        check(m.message.equals("TAILS  YOU WIN  +$96"),"net profit rather than gross payout");
        m.begin(4000);check(m.locked(30000),"never resend after late response");check(m.status(30000).contains("Waiting for server"),"late response state");
        m.receive(new int[]{0},"Insufficient chips.",31000);check(!m.pending&&!m.resultReady,"server failure unlocks");check(m.message.equals("Insufficient credits."),"failure money terminology");
        m.begin(32000);m.receive(new int[]{1,0,0,0},"",32100);check(m.message.equals("HEADS  LOST $100"),"loss uses submitted amount");
        m.rules=true;check(!m.canFlip(34000),"modal blocks flip");check(!ArcadeView.enabled("game0",m,34000),"modal blocks navigation");
        check(ArcadeView.enabled("dismiss",m,34000),"modal dismissal enabled");m.rules=false;
        Set<String> ids=new HashSet<>();
        for(var b:ArcadeLayout.CONTROLS) {check(ids.add(b.id()),"unique control");check(b.x()>=0&&b.y()>=0&&b.x()+b.w()<=1536&&b.y()+b.h()<=1024,"control within frame");}
        for(int[] size:new int[][]{{1920,1080},{1280,720},{854,480},{640,360},{480,270},{320,240},{3440,1440}}) {
            var f=ArcadeLayout.fit(size[0],size[1]);
            for(var b:ArcadeLayout.CONTROLS) {
                double x=f.x()+(b.x()+b.w()/2.0)*f.scale(),y=f.y()+(b.y()+b.h()/2.0)*f.scale();
                check(b.contains(f.localX(x),f.localY(y)),"scaled hit target");
                check(x>=0&&x<=size[0]&&y>=0&&y<=size[1],"visible scaled target");
            }
        }
        System.out.println("PASS: "+checks+" offline checks: payout, requests, wallet isolation, failures, modal and scaled hit targets.");
    }
}
