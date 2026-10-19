package local.customatm.economy.mixin;
import com.dyneco.econ.MarketData;
import java.util.Map;
import local.customatm.economy.Policy;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.*;

@Mixin(value=MarketData.class,remap=false)
public abstract class PricesMixin {
    @ModifyVariable(method="applyValues",at=@At("HEAD"),argsOnly=true,ordinal=0)
    private Map<String,Double> customatm$prices(Map<String,Double> values){return Policy.reprice(values);}
}
