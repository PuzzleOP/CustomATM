package local.customatm.economy;

/** Credit demand, not wallet money. Accrues only while online, and is saved. */
public final class Allowance {
    public static final double[] PER_HOUR = {10000, 500, 1500, 4000, 10000};
    private final double[] credits = {250, 25, 50, 100, 250};
    public void advance(double seconds) {
        if (!Double.isFinite(seconds) || seconds <= 0) return;
        for (int i=0;i<credits.length;i++) credits[i]=Math.min(PER_HOUR[i],credits[i]+PER_HOUR[i]*seconds/3600);
    }
    public long availableCents(int group) { return (long)Math.floor(Math.min(credits[0],credits[group])*100+1e-7); }
    public void spend(int group,long cents) {
        if (cents<0 || cents>availableCents(group)) throw new IllegalStateException("Sale exceeded available demand");
        credits[0]=Math.max(0,credits[0]-cents/100.0);
        credits[group]=Math.max(0,credits[group]-cents/100.0);
    }
    public double get(int index) { return credits[index]; }
    public void restore(int index,double value) { credits[index]=Double.isFinite(value)?Math.max(0,Math.min(PER_HOUR[index],value)):0; }
    public static int affordable(int requested,long cents,java.util.function.IntToLongFunction quote) {
        if (requested<=0 || cents<=0) return 0;
        int lo=0,hi=requested;
        while(lo<hi) {
            int mid=lo+(int)(((long)hi-lo+1)/2);
            long cost=quote.applyAsLong(mid);
            if(cost>=0 && cost<=cents) lo=mid; else hi=mid-1;
        }
        return lo>0 && quote.applyAsLong(lo)>0 ? lo:0;
    }
}
