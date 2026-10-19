package local.atm10.casinodyneco.mixin;

import com.togascasino.casinomod.client.screen.CasinoScreen;
import com.togascasino.casinomod.client.screen.game.GameScreenBase;
import local.atm10.casinodyneco.WalletLabels;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

@Mixin(value = {CasinoScreen.class, GameScreenBase.class}, remap = false)
public abstract class CasinoLabelsClientMixin {
    @ModifyVariable(method = "render", at = @At("STORE"), ordinal = 0)
    private String bridge$creditBalanceLabel(String text) { return WalletLabels.rewrite(text); }

    @ModifyArg(method = "render", at = @At(value = "INVOKE", target = "Lnet/minecraft/network/chat/Component;literal(Ljava/lang/String;)Lnet/minecraft/network/chat/MutableComponent;"), index = 0)
    private String bridge$marketHelp(String text) { return WalletLabels.rewrite(text); }
}
