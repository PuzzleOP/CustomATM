package local.atm10.casinodyneco;

import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

public final class DisabledDepositSlot extends Slot {
    public DisabledDepositSlot(Slot original) {
        super(original.container, 0, original.x, original.y);
        this.index = original.index;
    }
    @Override public boolean mayPlace(ItemStack stack) { return false; }
    @Override public boolean isActive() { return false; }
}
