package local.atm10.casinodyneco.mixin;

import com.togascasino.casinomod.menu.CasinoMenu;
import local.atm10.casinodyneco.DisabledDepositSlot;
import net.minecraft.world.entity.player.Inventory;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = CasinoMenu.class, remap = false)
public abstract class CasinoMenuMixin {
    @Inject(method = "<init>", at = @At("RETURN"))
    private void bridge$disableDepositSlot(int id, Inventory inventory, CallbackInfo info) {
        CasinoMenu menu = (CasinoMenu) (Object) this;
        menu.slots.set(0, new DisabledDepositSlot(menu.slots.get(0)));
    }
}
