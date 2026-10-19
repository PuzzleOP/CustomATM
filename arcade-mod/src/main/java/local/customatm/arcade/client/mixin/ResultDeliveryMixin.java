package local.customatm.arcade.client.mixin;

import com.togascasino.casinomod.client.ClientPayloadHandler;
import com.togascasino.casinomod.network.payload.GameResultPayload;
import local.customatm.arcade.client.GameRuntime;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Deliver every owned result immediately; two replies in one tick must not overwrite each other. */
@Mixin(value=ClientPayloadHandler.class,remap=false)
public abstract class ResultDeliveryMixin {
    @Inject(method="handleGameResult",at=@At("HEAD"),cancellable=true,remap=false)
    private static void arcadeResult(GameResultPayload payload,CallbackInfo ci){if(GameRuntime.accept(payload))ci.cancel();}
}
