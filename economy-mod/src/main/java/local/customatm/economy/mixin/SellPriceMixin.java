package local.customatm.economy.mixin;
import com.dyneco.econ.MarketEntry;
import local.customatm.economy.Policy;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value=MarketEntry.class,remap=false)
public abstract class SellPriceMixin {
    @Shadow public abstract String id();
    @Inject(method="sellPrice",at=@At("RETURN"),cancellable=true)
    private void customatm$buyback(CallbackInfoReturnable<Double> cir){cir.setReturnValue(Policy.sellPrice(id(),cir.getReturnValue()));}
    @Inject(method="recordSale",at=@At("TAIL"))
    private void customatm$priceImpact(double amount,org.spongepowered.asm.mixin.injection.callback.CallbackInfo ci){((MarketEntry)(Object)this).settlePrices();}
}
