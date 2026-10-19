package local.customatm.arcade;

import java.util.*;

/** Server-payload presentation model. No random outcomes or wallet mutations live here. */
public final class GameModel {
    public record Request(String action,int[] args) {}
    public record Wager(int type,int number,int amount) {}
    public final GameKind kind;
    public String input="100",pendingAction="",message="";
    public long balance,minBet=1,maxBet=100000,submitted,returned,started,animationEnd,lastPoll;
    public boolean active,pending,hasResult,rules,confirmedLeave;
    public int mines=5,safe,risk,selectedType=1,selectedNumber,winning=-1,bucket=8,pathMask,winningSymbol=-1;
    public int[] symbols={0,1,2},ticket=new int[9],cells=new int[25];
    public boolean[] scratched=new boolean[9];
    public List<Integer> player=List.of(),dealer=List.of();
    public final List<Wager> wagers=new ArrayList<>();
    public final List<Double> trail=new ArrayList<>();
    public double multiplier=1;
    public int resultSerial;
    public GameModel(GameKind kind){this.kind=kind;}
    public long bet(){try{return Long.parseLong(input);}catch(NumberFormatException e){return 0;}}
    public long totalWager(){return wagers.stream().mapToLong(Wager::amount).sum();}
    public long limit(){int gross=switch(kind){case SLOTS->200;case SCRATCH->150;case ROULETTE->36;case BLACKJACK->5;default->2;};return Math.min(maxBet,Integer.MAX_VALUE/gross);}
    public String invalid(long amount){if(amount<minBet)return "Minimum bet: "+CoinModel.money(minBet);if(amount>limit())return "Maximum total bet: "+CoinModel.money(limit());if(amount>balance)return "Not enough credits";return "";}
    public boolean locked(long now){return pending||now<animationEnd;}
    public boolean busy(long now){return locked(now)||active;}
    public boolean canStart(long now){return !rules&&!busy(now)&&invalid(kind==GameKind.ROULETTE?totalWager():bet()).isEmpty()&&(kind!=GameKind.ROULETTE||!wagers.isEmpty())&&(kind!=GameKind.SCRATCH||!hasResult||allScratched());}
    public void setBet(long amount){input=Long.toString(Math.max(minBet,Math.min(limit(),amount)));}
    public boolean allScratched(){for(boolean b:scratched)if(!b)return false;return true;}
    public boolean addWager(long now){if(busy(now)||rules||wagers.size()>=64||!invalid(bet()).isEmpty()||!invalid(totalWager()+bet()).isEmpty())return false;wagers.add(new Wager(selectedType,selectedNumber,(int)bet()));return true;}
    public double nextSafeChance(){return (25.0-mines-safe)/(25.0-safe);}
    public long nextMineReturn(){double mult=.97;for(int i=0;i<=safe;i++)mult*=(25.0-i)/(25.0-mines-i);return Math.round(submitted*mult);}
    public Request start(long now){
        if(kind==GameKind.HUB||kind==GameKind.COIN_FLIP||!canStart(now))return null;
        submitted=kind==GameKind.ROULETTE?totalWager():bet();returned=0;hasResult=false;winning=-1;message="";
        symbols=new int[]{0,1,2};Arrays.fill(cells,0);Arrays.fill(scratched,false);safe=0;multiplier=1;player=List.of();dealer=List.of();trail.clear();trail.add(1.0);
        return switch(kind){
            case SLOTS -> send("spin",now,1600,(int)submitted);
            case MINES -> send("start",now,200,(int)submitted,mines);
            case BLACKJACK -> send("start",now,450,(int)submitted);
            case PLINKO -> send("drop",now,2600,(int)submitted,risk);
            case SCRATCH -> send("buy",now,250,(int)submitted);
            case CRASH -> send("start",now,0,(int)submitted);
            case ROULETTE -> {int[] a=new int[1+wagers.size()*3];a[0]=wagers.size();for(int i=0;i<wagers.size();i++){var w=wagers.get(i);a[1+i*3]=w.type;a[2+i*3]=w.number;a[3+i*3]=w.amount;}yield send("spin",now,2300,a);}
            default -> null;
        };
    }
    private Request send(String action,long now,int animation,int...args){pending=true;pendingAction=action;started=now;animationEnd=now+animation;return new Request(action,args);}
    public Request action(String action,int cell,long now){
        if(rules||locked(now)||!active)return null;
        if(kind==GameKind.MINES){
            if(action.equals("reveal")&&cell>=0&&cell<25&&cells[cell]==0&&nextMineReturn()<=Integer.MAX_VALUE)return send("reveal",now,180,cell);
            if(action.equals("cashout"))return send("cashout",now,200);
        }
        if(kind==GameKind.BLACKJACK){
            if(action.equals("hit")||action.equals("stand"))return send(action,now,350);
            if(action.equals("double")&&player.size()==2&&invalid(submitted).isEmpty())return send(action,now,500);
        }
        if(kind==GameKind.CRASH&&action.equals("cashout"))return send(action,now,0);
        return null;
    }
    public Request poll(long now){if(kind!=GameKind.CRASH||!active||pending||now-lastPoll<300)return null;lastPoll=now;return new Request("poll",new int[0]);}
    private void finish(long payout){returned=payout;active=false;hasResult=true;resultSerial++;}
    private static void require(boolean valid){if(!valid)throw new IllegalArgumentException("Incomplete server result");}
    private static int symbol(int n){require(n>=0&&n<7);return n;}
    public boolean receive(String action,int[] d,String note,long now){
        // Crash poll replies can arrive while a cash-out is pending. Never unlock that cash-out early.
        boolean poll=kind==GameKind.CRASH&&action.equals("poll");
        if(!poll&&!pending&&!active)return false;
        if(poll&&!active)return false;
        if(d.length==0||d[0]!=1){
            if(!poll){pending=false;animationEnd=now;message=(note==null||note.isBlank()?"Server rejected the action.":note.replace("chips","credits"));}
            return false;
        }
        try {
            switch(kind){
                case SLOTS -> {require(d.length>=5);symbols=new int[]{symbol(d[1]),symbol(d[2]),symbol(d[3])};require(d[4]>=0);finish(d[4]);}
                case SCRATCH -> {require(d.length>=12);int[] t=new int[9];for(int i=0;i<9;i++)t[i]=symbol(d[i+1]);require(d[10]>=-1&&d[10]<7&&d[11]>=0);ticket=t;winningSymbol=d[10];finish(d[11]);}
                case PLINKO -> {require(d.length>=5&&d[1]>=0&&d[1]<=16&&d[3]>=0&&d[4]>=0);bucket=d[1];pathMask=d[2];multiplier=d[3]/100.0;finish(d[4]);}
                case ROULETTE -> {require(d.length>=3&&d[1]>=0&&d[1]<=36&&d[2]>=0&&d[2]<=64&&d.length>=3+d[2]*2);long pay=0;for(int i=0;i<d[2];i++){require(d[4+i*2]>=0);pay+=d[4+i*2];}winning=d[1];finish(pay);wagers.clear();}
                case MINES -> {
                    switch(action){
                        case "start" -> {active=true;returned=Math.round(submitted*.97);}
                        case "reveal" -> {
                            require(d.length>=3&&d[1]>=0&&d[1]<25);
                            if(d[2]==1){require(d.length>=28);for(int i=0;i<25;i++)if(d[3+i]==1)cells[i]=2;finish(0);}
                            else {require(d.length>=6&&d[4]>=0);if(cells[d[1]]==0)safe++;cells[d[1]]=1;multiplier=d[3]/100.0;returned=d[4];if(d[5]==1)finish(returned);}
                        }
                        case "cashout" -> {require(d.length>=28&&d[1]>=0);for(int i=0;i<25;i++)if(d[3+i]==1)cells[i]=2;finish(d[1]);}
                        default -> {return false;}
                    }
                }
                case BLACKJACK -> {
                    require(d.length>=8);int p=d[1];require(p>=1&&p<=52&&d.length>p+2);int q=d[2+p];int tail=3+p+q;
                    require(q>=1&&q<=52&&d.length>=tail+3);List<Integer> ph=new ArrayList<>(),dh=new ArrayList<>();
                    for(int i=0;i<p;i++){require(d[2+i]>=0&&d[2+i]<52);ph.add(d[2+i]);}
                    for(int i=0;i<q;i++){require(d[3+p+i]>=-1&&d[3+p+i]<52);dh.add(d[3+p+i]);}
                    boolean resolved=d[tail+1]==1;require(d[tail+2]>0);
                    if(resolved)require(d.length>tail+3&&d[tail+3]>=0);
                    player=List.copyOf(ph);dealer=List.copyOf(dh);submitted=d[tail+2];active=!resolved;
                    if(resolved)finish(d[tail+3]);
                }
                case CRASH -> {
                    switch(action){
                        case "start" -> {active=true;lastPoll=now-300;multiplier=1;}
                        case "poll" -> {require(d.length>=3&&d[1]>=100);multiplier=d[1]/100.0;trail.add(multiplier);if(trail.size()>300)trail.remove(0);return true;}
                        case "crashed" -> {require(d.length>=3&&d[1]>=100);multiplier=d[1]/100.0;finish(0);}
                        case "cashout" -> {require(d.length>=4&&d[1]>=100&&d[3]>=0);multiplier=d[1]/100.0;finish(d[3]);}
                        default -> {return false;}
                    }
                }
                default -> {return false;}
            }
            pending=false;pendingAction="";message=note==null?"":note.replace("chips","credits");return true;
        }catch(IllegalArgumentException e){
            // Keep the wager locked if the outcome cannot be parsed: do not offer a blind retry.
            message="Unrecognized server result. Reconnect before betting again.";return false;
        }
    }
    public String status(long now){
        if(locked(now))return now-started>10000?"Waiting for server. No repeat bet sent.":pending?"Waiting for server...":"Revealing result...";
        if(kind==GameKind.SCRATCH&&hasResult&&!allScratched())return "Click or drag over the ticket to reveal it.";
        if(hasResult)return "Returned "+CoinModel.money(returned)+"  |  "+(returned>=submitted?"Net +":"Net -")+CoinModel.money(Math.abs(returned-submitted));
        if(!message.isBlank())return message;
        if(active)return "Round in progress";
        return invalid(kind==GameKind.ROULETTE?Math.max(minBet,totalWager()):bet());
    }
    public static int total(List<Integer> cards){int t=0,a=0;for(int c:cards){if(c<0)continue;int r=c%13;if(r==0){a++;t+=11;}else t+=Math.min(10,r+1);}while(t>21&&a-->0)t-=10;return t;}
}
