package local.customatm.economy.mixin;
import com.dyneco.econ.*;
import local.customatm.economy.Policy;
import org.spongepowered.asm.mixin.*;
import org.spongepowered.asm.mixin.injection.*;

@Mixin(value=Consignment.class,remap=false)
public abstract class SalesMixin {
    @Shadow private static int buyerLot(MarketEntry e,int wanted){throw new AssertionError();}
    @Shadow private static int fluidBatch(MarketEntry e,double budget,int wanted){throw new AssertionError();}
    @ModifyVariable(method={"drainOrders","sellFromItemContainer","sellFromTank"},at=@At("HEAD"),argsOnly=true,ordinal=0)
    private static PlayerAccount customatm$account(PlayerAccount a){return Policy.enter(a);}
    @Redirect(method={"drainOrders","sellFromItemContainer"},at=@At(value="INVOKE",target="Lcom/dyneco/econ/Consignment;buyerLot(Lcom/dyneco/econ/MarketEntry;I)I"))
    private static int customatm$itemLimit(MarketEntry e,int wanted){return Policy.limit(e,buyerLot(e,wanted));}
    @Redirect(method="sellFromTank",at=@At(value="INVOKE",target="Lcom/dyneco/econ/Consignment;fluidBatch(Lcom/dyneco/econ/MarketEntry;DI)I"))
    private static int customatm$fluidLimit(MarketEntry e,double budget,int wanted){return Policy.limit(e,fluidBatch(e,budget,wanted));}
    @Redirect(method={"fillSellOrder","sellFromItemContainer","sellFromTank"},at=@At(value="INVOKE",target="Lcom/dyneco/econ/PlayerAccount;deposit(J)V"))
    private static void customatm$recordDemand(PlayerAccount a,long cents){Policy.deposit(a,cents);}
}
