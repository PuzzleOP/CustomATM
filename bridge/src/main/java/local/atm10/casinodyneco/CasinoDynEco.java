package local.atm10.casinodyneco;

import com.togascasino.casinomod.menu.CasinoMenu;
import com.togascasino.casinomod.menu.GameMenuBase;
import com.togascasino.casinomod.network.payload.BalanceSyncPayload;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;

@Mod("atm10_casino_dyneco")
public final class CasinoDynEco {
    public CasinoDynEco() {
        NeoForge.EVENT_BUS.addListener(CasinoDynEco::refreshOpenWallets);
    }

    private static void refreshOpenWallets(ServerTickEvent.Post event) {
        if (event.getServer().getTickCount() % 20 != 0) return;
        for (var player : event.getServer().getPlayerList().getPlayers()) {
            if (player.containerMenu instanceof CasinoMenu || player.containerMenu instanceof GameMenuBase) {
                // Reflect automatic DynEco sales even while the player is idle in a game.
                PacketDistributor.sendToPlayer(player, new BalanceSyncPayload(DynEcoWallet.balance(player.getUUID())));
            }
        }
    }
}
