package local.customatm.arcade.client;

import com.togascasino.casinomod.client.screen.game.CoinFlipScreen;
import net.minecraft.client.Minecraft;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import local.customatm.arcade.GameKind;

@EventBusSubscriber(modid="customatm_arcade", value=Dist.CLIENT)
public final class ArcadeClient {
    @SubscribeEvent
    public static void opening(ScreenEvent.Opening event) {
        // Match stock class names exactly; never intercept another addon's screens.
        if (event.getNewScreen() != null && event.getNewScreen().getClass() == CoinFlipScreen.class) {
            var old = (CoinFlipScreen)event.getNewScreen();
            var player = Minecraft.getInstance().player;
            if (player != null) event.setNewScreen(new RedstoneCoinScreen(old.getMenu(), player.getInventory(), old.getTitle()));
            return;
        }
        if(!(event.getNewScreen() instanceof AbstractContainerScreen<?> old))return;
        GameKind kind=switch(old.getClass().getName()){
            case "com.togascasino.casinomod.client.screen.CasinoScreen"->GameKind.HUB;
            case "com.togascasino.casinomod.client.screen.game.SlotsScreen"->GameKind.SLOTS;
            case "com.togascasino.casinomod.client.screen.game.MinesScreen"->GameKind.MINES;
            case "com.togascasino.casinomod.client.screen.game.BlackjackScreen"->GameKind.BLACKJACK;
            case "com.togascasino.casinomod.client.screen.game.RouletteScreen"->GameKind.ROULETTE;
            case "com.togascasino.casinomod.client.screen.game.PlinkoScreen"->GameKind.PLINKO;
            case "com.togascasino.casinomod.client.screen.game.ScratchScreen"->GameKind.SCRATCH;
            case "com.togascasino.casinomod.client.screen.game.CrashScreen"->GameKind.CRASH;
            default->null;
        };
        var player=Minecraft.getInstance().player;
        if(kind!=null&&player!=null)event.setNewScreen(new RedstoneGameScreen<>(old.getMenu(),player.getInventory(),old.getTitle(),kind));
    }
    @SubscribeEvent public static void tick(ClientTickEvent.Post event){GameRuntime.tick();}
}
