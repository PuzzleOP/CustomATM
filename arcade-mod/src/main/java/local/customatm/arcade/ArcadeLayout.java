package local.customatm.arcade;

import java.util.List;

/** One coordinate system for rendered art, native hit targets and offline preview. */
public final class ArcadeLayout {
    public static final int WIDTH = 1536, HEIGHT = 1024;
    public record Box(String id, int x, int y, int w, int h, String label) {
        public boolean contains(double px, double py) { return px >= x && py >= y && px < x+w && py < y+h; }
    }
    public static final String[] GAMES = {"Slots", "Coin Flip", "Mines", "Blackjack", "Roulette", "Plinko", "Scratch Ticket", "Crash"};
    public static final String[] TARGETS = {"slots", "coin_flip", "mines", "blackjack", "roulette", "plinko", "scratch", "crash"};
    public static final List<Box> CONTROLS = List.of(
        new Box("game0",130,139,310,83,GAMES[0]), new Box("game1",130,234,310,83,GAMES[1]),
        new Box("game2",130,329,310,83,GAMES[2]), new Box("game3",130,424,310,83,GAMES[3]),
        new Box("game4",130,519,310,83,GAMES[4]), new Box("game5",130,614,310,83,GAMES[5]),
        new Box("game6",130,709,310,83,GAMES[6]), new Box("game7",130,804,310,91,GAMES[7]),
        new Box("heads",548,566,255,65,"Heads"), new Box("tails",814,566,252,65,"Tails"),
        new Box("minus",762,666,58,59,"Decrease bet"), new Box("bet",825,668,303,57,"Bet amount in credits"),
        new Box("plus",1135,666,58,59,"Increase bet"),
        new Box("preset25",756,744,98,45,"Bet $25"), new Box("preset50",869,744,98,45,"Bet $50"),
        new Box("preset100",982,744,98,45,"Bet $100"), new Box("preset250",1096,744,98,45,"Bet $250"),
        new Box("flip",756,815,425,75,"Flip coin"), new Box("rules",1106,547,258,40,"Rules and payouts"),
        new Box("close",1246,920,151,37,"Close casino"), new Box("dismiss",674,732,250,58,"Back to game")
    );
    public static Box box(String id) { return CONTROLS.stream().filter(b -> b.id.equals(id)).findFirst().orElseThrow(); }
    public record Fit(double scale, double x, double y) {
        public double localX(double x) { return (x-this.x)/scale; }
        public double localY(double y) { return (y-this.y)/scale; }
    }
    public static Fit fit(int width, int height) {
        double s = Math.min(width/(double)WIDTH, height/(double)HEIGHT);
        return new Fit(s,(width-WIDTH*s)/2,(height-HEIGHT*s)/2);
    }
}
