package local.atm10.casinodyneco.mixin;

import com.togascasino.casinomod.client.screen.CasinoScreen;
import java.util.ArrayList;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = CasinoScreen.class, remap = false)
public abstract class CasinoHubClientMixin extends Screen {
    protected CasinoHubClientMixin(Component title) { super(title); }

    @Inject(method = "init", at = @At("TAIL"))
    private void bridge$showLinkedWallet(CallbackInfo info) {
        int left = 0, top = 0;
        for (var child : new ArrayList<>(children())) {
            if (child instanceof Button button) {
                String label = button.getMessage().getString();
                if ("Deposit".equals(label)) {
                    left = button.getX() - 26;
                    top = button.getY();
                    removeWidget(button);
                } else if ("Cash Out".equals(label)) removeWidget(button);
            }
        }
        Button linked = Button.builder(Component.literal("DynEco wallet connected"), button -> {})
            .bounds(left, top, 216, 20)
            .tooltip(Tooltip.create(Component.literal("Bets use whole DynEco credits. Winnings return automatically. Trade items in the Market Tablet.")))
            .build();
        linked.active = false;
        addRenderableWidget(linked);
    }
}
