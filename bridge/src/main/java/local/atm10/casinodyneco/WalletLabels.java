package local.atm10.casinodyneco;

public final class WalletLabels {
    private WalletLabels() {}
    public static String rewrite(String text) {
        if (text.startsWith("Balance: ")) return "Credits: " + text.substring(9).replace(" chips", "");
        if (text.equals("Deposit any item, browse all items to cash out")) return "Trade items with your Market Tablet.";
        if (text.startsWith("House fee: ")) return "Bets and winnings use your DynEco wallet.";
        return text;
    }
}
