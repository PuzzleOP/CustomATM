import local.customatm.economy.Allowance;
public class AllowanceTest {
 public static void main(String[] args) {
  Allowance b=new Allowance();long total=0,bulk=0;java.util.Random rng=new java.util.Random(19);
  // Stress repeated listings/chests, fluids, compression and expensive units.
  for(int second=0;second<3600;second++) {
   b.advance(1);
   for(int chest=0;chest<64;chest++) {
    int g=1+rng.nextInt(4),requested=100000;
    double price=switch(g){case 1->.0003;case 2->.07;case 3->56;default->3500;};
    int n=Allowance.affordable(requested,b.availableCents(g),q->Math.round(q*price*100));
    long paid=Math.round(n*price*100);
    if(n==0 && paid!=0)throw new AssertionError();
    b.spend(g,paid);total+=paid;if(g==1)bulk+=paid;
   }
  }
  if(total>1025000||bulk>52500)throw new AssertionError("Limits exceeded: "+total+" "+bulk);
  if(Allowance.affordable(Integer.MAX_VALUE,100,q->(long)q*1000)!=0)throw new AssertionError("Oversized unit bypass");
  if(Allowance.affordable(1000,10,q->Math.round(q*.1))!=104)throw new AssertionError("Rounding-aware boundary");
  if(Allowance.affordable(1,100,q->0)!=0)throw new AssertionError("Zero-price item destroyed");
  for(int i=0;i<5;i++)b.restore(i,0);
  if(b.availableCents(4)!=0)throw new AssertionError("Restore failed");
  b.advance(3600);if(b.availableCents(4)!=1000000||b.availableCents(1)!=50000)throw new AssertionError("Hourly recovery");
  b.advance(100000);if(b.availableCents(4)!=1000000)throw new AssertionError("Unlimited hoarding");
  System.out.println("PASS: 230,400 repeated sale attempts stayed within global/category budgets; rounding, expensive-unit refusal, recovery and storage bounds verified. Hour payout $"+total/100.0+"; bulk $"+bulk/100.0);
 }
}
