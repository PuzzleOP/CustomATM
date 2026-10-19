package local.atm10.casinodyneco.mixin;

import com.togascasino.casinomod.network.ServerPayloadHandler;
import com.togascasino.casinomod.network.payload.HubActionPayload;
import com.togascasino.casinomod.network.payload.OpenGamePayload;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = ServerPayloadHandler.class, remap = false)
public abstract class CasinoShopMixin {
    @Inject(method = "handleHubAction", at = @At("HEAD"), cancellable = true)
    private static void bridge$keepMarketTradingInDynEco(ServerPlayer player, HubActionPayload payload, CallbackInfo info) {
        player.displayClientMessage(Component.literal("Your casino uses DynEco credits. Trade items using the Market Tablet."), false);
        info.cancel();
    }
    @Inject(method = "handleOpenGame", at = @At("HEAD"), cancellable = true)
    private static void bridge$blockSeparateShop(ServerPlayer player, OpenGamePayload payload, CallbackInfo info) {
        if ("cash_out".equals(payload.target())) {
            player.displayClientMessage(Component.literal("Winnings are already in your DynEco wallet. Use the Market Tablet to buy items."), false);
            info.cancel();
        }
    }
}
