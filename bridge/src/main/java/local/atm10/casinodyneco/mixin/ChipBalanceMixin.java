package local.atm10.casinodyneco.mixin;

import com.togascasino.casinomod.data.ChipBalanceData;
import java.util.UUID;
import local.atm10.casinodyneco.DynEcoWallet;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value = ChipBalanceData.class, remap = false)
public abstract class ChipBalanceMixin {
    @Inject(method = "getBalance(Ljava/util/UUID;)J", at = @At("HEAD"), cancellable = true)
    private void bridge$balance(UUID player, CallbackInfoReturnable<Long> result) {
        // Cancels the original getter, including its separate casino signup bonus.
        result.setReturnValue(DynEcoWallet.balance(player));
    }
    @Inject(method = "deposit(Ljava/util/UUID;J)Z", at = @At("HEAD"), cancellable = true)
    private void bridge$deposit(UUID player, long credits, CallbackInfoReturnable<Boolean> result) {
        result.setReturnValue(DynEcoWallet.deposit(player, credits));
    }
    @Inject(method = "withdraw(Ljava/util/UUID;J)Z", at = @At("HEAD"), cancellable = true)
    private void bridge$withdraw(UUID player, long credits, CallbackInfoReturnable<Boolean> result) {
        result.setReturnValue(DynEcoWallet.withdraw(player, credits));
    }
    @Inject(method = "setBalance(Ljava/util/UUID;J)V", at = @At("HEAD"), cancellable = true)
    private void bridge$setBalance(UUID player, long credits, CallbackInfo info) {
        DynEcoWallet.setBalance(player, credits);
        info.cancel();
    }
}
