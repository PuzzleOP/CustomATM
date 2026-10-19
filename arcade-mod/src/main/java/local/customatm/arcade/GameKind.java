package local.customatm.arcade;
public enum GameKind {
    HUB("Arcade",-1,"Choose a game. Your DynEco wallet follows you."),
    SLOTS("Slots",0,"Three reels. Clear matches. One spin at a time."),
    COIN_FLIP("Coin Flip",1,"Pick a side. One coin, one result."),
    MINES("Mines",2,"Reveal emeralds. Cash out before you hit a mine."),
    BLACKJACK("Blackjack",3,"Build your hand. Beat the dealer without passing 21."),
    ROULETTE("Roulette",4,"Choose your positions, place bets, then spin."),
    PLINKO("Plinko",5,"Pick your risk. Follow the ball to its payout."),
    SCRATCH("Scratch Ticket",6,"Reveal nine symbols. Three matching symbols can pay."),
    CRASH("Crash",7,"Watch the multiplier. Cash out before the crash.");
    public final String title,description;public final int nav;
    GameKind(String title,int nav,String description){this.title=title;this.nav=nav;this.description=description;}
    public String target(){return this==HUB?"hub":name().toLowerCase(java.util.Locale.ROOT);}
}
