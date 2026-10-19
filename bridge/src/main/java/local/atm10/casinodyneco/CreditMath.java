package local.atm10.casinodyneco;

/** Casino amounts are whole base credits; DynEco stores hundredths of a credit. */
public final class CreditMath {
    public static final long CENTS_PER_CREDIT = 100L;
    private CreditMath() {}

    public static long wholeCredits(long cents) {
        if (cents < 0) throw new IllegalArgumentException("Negative wallet balance");
        return cents / CENTS_PER_CREDIT;
    }

    public static long positiveCents(long credits) {
        if (credits <= 0 || credits > Long.MAX_VALUE / CENTS_PER_CREDIT) return -1;
        return credits * CENTS_PER_CREDIT;
    }

    public static boolean canDeposit(long balance, long credits) {
        long cents = positiveCents(credits);
        return balance >= 0 && cents > 0 && balance <= Long.MAX_VALUE - cents;
    }

    public static boolean canWithdraw(long balance, long credits) {
        long cents = positiveCents(credits);
        return cents > 0 && balance >= cents;
    }

    public static long replacementCents(long credits) {
        return Math.multiplyExact(Math.max(0L, credits), CENTS_PER_CREDIT);
    }
}
