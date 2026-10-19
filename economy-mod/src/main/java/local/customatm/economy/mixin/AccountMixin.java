package local.customatm.economy.mixin;
import com.dyneco.econ.PlayerAccount;
import java.util.UUID;
import local.customatm.economy.*;
import net.minecraft.nbt.CompoundTag;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(value=PlayerAccount.class,remap=false)
public abstract class AccountMixin implements BudgetAccount {
    @Unique private final Allowance customatm$demand = new Allowance();
    public Allowance customatm$allowance(){return customatm$demand;}
    @Inject(method="save",at=@At("RETURN"))
    private void customatm$save(CallbackInfoReturnable<CompoundTag> cir) {
        var tag=new CompoundTag();for(int i=0;i<5;i++)tag.putDouble("credit"+i,customatm$demand.get(i));
        cir.getReturnValue().put("customatm_demand_v1",tag);
    }
    @Inject(method="load",at=@At("RETURN"))
    private static void customatm$load(UUID id,CompoundTag tag,CallbackInfoReturnable<PlayerAccount> cir) {
        if(tag.contains("customatm_demand_v1",10)) {
            var b=((BudgetAccount)(Object)cir.getReturnValue()).customatm$allowance();
            var saved=tag.getCompound("customatm_demand_v1");
            for(int i=0;i<5;i++)b.restore(i,saved.getDouble("credit"+i));
        }
    }
}
