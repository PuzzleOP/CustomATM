package local.atm10.casinodyneco;

import com.dyneco.econ.MarketData;
import com.dyneco.econ.PlayerAccount;
import com.dyneco.net.Sync;
import java.util.UUID;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.neoforge.server.ServerLifecycleHooks;

public final class DynEcoWallet {
    private DynEcoWallet() {}

    private record Wallet(MinecraftServer server, MarketData data, PlayerAccount account) {
        void changed(UUID playerId) {
            data.setDirty();
            ServerPlayer player = server.getPlayerList().getPlayer(playerId);
            if (player != null) Sync.sendAccount(player, data);
        }
    }

    private static Wallet resolve(UUID playerId) {
        MinecraftServer server = ServerLifecycleHooks.getCurrentServer();
        if (server == null || !server.isSameThread()) {
            throw new IllegalStateException("Casino wallet access requires the active server thread");
        }
        MarketData data = MarketData.get(server);
        // This applies DynEco's own starting balance once, with its existing save semantics.
        return new Wallet(server, data, data.account(playerId));
    }

    public static long balance(UUID playerId) {
        return CreditMath.wholeCredits(resolve(playerId).account().balance());
    }

    public static boolean deposit(UUID playerId, long credits) {
        if (CreditMath.positiveCents(credits) < 0) return false;
        Wallet wallet = resolve(playerId);
        if (!CreditMath.canDeposit(wallet.account().balance(), credits)) return false;
        wallet.account().deposit(CreditMath.positiveCents(credits));
        wallet.changed(playerId);
        return true;
    }

    public static boolean withdraw(UUID playerId, long credits) {
        if (CreditMath.positiveCents(credits) < 0) return false;
        Wallet wallet = resolve(playerId);
        if (!wallet.account().withdraw(CreditMath.positiveCents(credits))) return false;
        wallet.changed(playerId);
        return true;
    }

    /** Explicit casino admin setters replace the wallet; bets never use this method. */
    public static void setBalance(UUID playerId, long credits) {
        long cents = CreditMath.replacementCents(credits);
        Wallet wallet = resolve(playerId);
        wallet.account().setBalance(cents);
        wallet.changed(playerId);
    }
}
