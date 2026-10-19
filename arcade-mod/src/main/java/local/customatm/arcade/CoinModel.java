package local.customatm.arcade;

/** Client presentation state only. The existing casino server owns all money and randomness. */
public final class CoinModel {
    public String input = "100";
    public int side;
    public long balance;
    public long minBet = 1, maxBet = 100000;
    public boolean pending, resultReady, won, rules;
    public long started, submitted, returned;
    public int landed;
    public String message = "";

    public long bet() {
        try { return Long.parseLong(input); } catch (NumberFormatException e) { return 0; }
    }
    public static long payout(long bet) { return Math.round(bet * 1.96d); }
    public String validation() {
        long n = bet();
        if (n < minBet) return "Minimum bet: " + money(minBet);
        // The existing result payload stores the gross return in a signed int.
        if (n > limit()) return "Maximum bet: " + money(limit());
        if (n > balance) return "Not enough credits";
        return "";
    }
    public long limit() { return Math.min(maxBet, Integer.MAX_VALUE / 2); }
    public boolean locked(long now) { return pending || (resultReady && now - started < 1200); }
    public boolean canFlip(long now) { return !rules && !locked(now) && validation().isEmpty(); }
    public int[] begin(long now) {
        if (!canFlip(now)) return null;
        submitted = bet(); started = now; pending = true; resultReady = false; message = "";
        return new int[]{(int)submitted, side};
    }
    public void receive(int[] data, String error, long now) {
        if (!pending) return;
        pending = false;
        if (data.length < 4 || data[0] != 1 || data[1] < 0 || data[1] > 1 || (data[2] != 0 && data[2] != 1) || data[3] < 0) {
            resultReady = false;
            message = error == null || error.isBlank() ? "Server did not accept this bet." : error.replace("chips", "credits");
            return;
        }
        landed = data[1]; won = data[2] == 1; returned = data[3]; resultReady = true;
        message = (landed == 0 ? "HEADS" : "TAILS") + (won ? "  YOU WIN  +" + money(returned - submitted) : "  LOST " + money(submitted));
    }
    public String status(long now) {
        if (locked(now)) return now - started > 10000 ? "Waiting for server. No new bet sent." : "Flipping...";
        if (!message.isEmpty()) return message;
        return validation();
    }
    public static String money(long n) { return "$" + String.format(java.util.Locale.US, "%,d", n); }
}
