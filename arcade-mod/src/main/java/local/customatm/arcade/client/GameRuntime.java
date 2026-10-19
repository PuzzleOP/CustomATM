package local.customatm.arcade.client;

import java.util.EnumMap;
import local.customatm.arcade.*;
import com.togascasino.casinomod.CasinoConfig;
import com.togascasino.casinomod.client.ClientPayloadHandler;
import com.togascasino.casinomod.network.payload.*;
import com.togascasino.casinomod.util.CasinoGame;
import net.minecraft.client.Minecraft;
import net.neoforged.neoforge.network.PacketDistributor;

/** Client-session cache, scoped to the current connection; no persistent economy state. */
public final class GameRuntime {
    private static Object connection;
    private static final EnumMap<GameKind,GameModel> models=new EnumMap<>(GameKind.class);
    private static CoinModel coin=new CoinModel();
    static long now(){return System.nanoTime()/1_000_000L;}
    private static void connection(){Object current=Minecraft.getInstance().getConnection();if(current!=connection){connection=current;models.clear();coin=new CoinModel();}}
    static CoinModel coin(){connection();return coin;}
    static GameModel model(GameKind kind){connection();return models.computeIfAbsent(kind,GameModel::new);}
    static void refresh(GameModel m){m.balance=ClientPayloadHandler.getBalance();m.minBet=CasinoConfig.MIN_BET.get();m.maxBet=CasinoConfig.MAX_BET.get();}
    static void send(GameModel m,GameModel.Request request){if(request!=null)PacketDistributor.sendToServer(new CasinoActionPayload(CasinoGame.valueOf(m.kind.name()),request.action(),request.args()));}
    static void route(GameResultPayload reply){
        if(reply==null)return;
        if(reply.game()==CasinoGame.COIN_FLIP){if(coin.pending&&reply.action().equals("bet")){ClientPayloadHandler.handleBalanceSync(new BalanceSyncPayload(reply.newBalance()));coin.receive(reply.data(),reply.message(),now());}return;}
        try{GameKind kind=GameKind.valueOf(reply.game().name());GameModel m=models.get(kind);if(m!=null&&(m.pending||m.active)&&(!reply.action().equals("poll")||m.active)){ClientPayloadHandler.handleBalanceSync(new BalanceSyncPayload(reply.newBalance()));m.receive(reply.action(),reply.data(),reply.message(),now());}}catch(IllegalArgumentException ignored){}
    }
    /** Called on the network handler's enqueued client task, before its one-slot mailbox can lose replies. */
    public static boolean accept(GameResultPayload reply){
        connection();if(connection==null)return false;
        if(reply.game()==CasinoGame.COIN_FLIP){if(!coin.pending)return false;route(reply);return true;}
        try{GameModel m=models.get(GameKind.valueOf(reply.game().name()));if(m==null||(!m.pending&&!m.active))return false;route(reply);return true;}catch(IllegalArgumentException ignored){return false;}
    }
    static void tick(){
        connection();if(connection==null)return;
        route(ClientPayloadHandler.consumeResult());
        GameModel crash=models.get(GameKind.CRASH);if(crash!=null)send(crash,crash.poll(now()));
    }
}
