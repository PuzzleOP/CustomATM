package local.customatm.economy;
import com.dyneco.econ.MarketData;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import net.neoforged.neoforge.event.RegisterCommandsEvent;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;

@Mod("customatm_economy")
public final class Economy {
    public Economy(IEventBus modBus) {
        // Clients use the same spread for displayed quotes as the host uses
        // for settlement. Waiting for applyValues alone only tunes the server.
        modBus.addListener(Economy::setup);
        NeoForge.EVENT_BUS.addListener(Economy::tick);
        NeoForge.EVENT_BUS.addListener(Economy::commands);
    }
    private static void setup(FMLCommonSetupEvent event) {
        event.enqueueWork(()->{Policy.load();Settings.apply();});
    }
    private static void tick(ServerTickEvent.Post e) {
        if(e.getServer().getTickCount()%20!=0)return;
        var data=MarketData.get(e.getServer());
        for(var player:e.getServer().getPlayerList().getPlayers()) {
            var a=data.account(player.getUUID());
            ((BudgetAccount)(Object)a).customatm$allowance().advance(1);
        }
        if(!e.getServer().getPlayerList().getPlayers().isEmpty())data.setDirty();
    }
    private static void commands(RegisterCommandsEvent e) {
        e.getDispatcher().register(Commands.literal("marketlimits").executes(ctx->{
            var p=ctx.getSource().getPlayerOrException();
            var a=MarketData.get(p.getServer()).account(p.getUUID());
            var b=((BudgetAccount)(Object)a).customatm$allowance();
            ctx.getSource().sendSuccess(()->Component.literal(String.format(java.util.Locale.ROOT,
                "Market demand available: $%.2f total. Bulk $%.2f; farming $%.2f; resources $%.2f; manufactured $%.2f. Recovers per online hour: total $10,000; groups $500/$1,500/$4,000/$10,000. Every sale uses both its group and total allowance. Unsold goods wait safely. Buyback ceilings per item/bucket: $250/$750/$2,000/$5,000; always check the sell quote.",b.get(0),b.availableCents(1)/100.0,b.availableCents(2)/100.0,b.availableCents(3)/100.0,b.availableCents(4)/100.0)),false);
            return 1;
        }));
    }
}
