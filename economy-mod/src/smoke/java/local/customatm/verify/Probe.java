package local.customatm.verify;
import java.nio.file.*;
import java.util.*;
import local.customatm.economy.*;
import com.dyneco.econ.*;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
@Mod("customatm_economy_probe")
public class Probe {
 public Probe(IEventBus bus){bus.addListener(this::verify);}
 private void verify(FMLCommonSetupEvent event){event.enqueueWork(()->{
  try {
   check("com.dyneco.econ.Consignment","customatm$account","customatm$itemLimit","customatm$fluidLimit","customatm$recordDemand");
   check("com.dyneco.econ.PlayerAccount","customatm$save","customatm$load");
   check("com.dyneco.econ.MarketData","customatm$prices");
   check("com.dyneco.econ.MarketEntry","customatm$buyback","customatm$priceImpact");
   PlayerAccount a=new PlayerAccount(UUID.randomUUID());
   var allowance=((BudgetAccount)(Object)a).customatm$allowance();
   allowance.advance(3600);allowance.spend(1,12345);
   PlayerAccount restored=PlayerAccount.load(a.id,a.save());
   var restoredAllowance=((BudgetAccount)(Object)restored).customatm$allowance();
   if(restoredAllowance.availableCents(1)!=allowance.availableCents(1))throw new AssertionError("Demand did not persist");
   var data=new MarketData();
   data.applyValues(Map.of("i:minecraft:cobblestone",2.0,"i:minecraft:diamond",1500.0,"i:minecraft:barrier",5.0));
   if(data.entry("i:minecraft:cobblestone").baseValue()!=.01)throw new AssertionError("Cobble price not applied");
   if(data.entry("i:minecraft:diamond").baseValue()!=100)throw new AssertionError("Diamond price not applied");
   if(data.entry("i:minecraft:barrier")!=null)throw new AssertionError("Admin item retained");
   // AllTheCompressed is deliberately absent from this minimal harness.
   // Construct its entry directly rather than looking up an unregistered item.
   var compressed=new MarketEntry("i:allthecompressed:cobblestone_9x",3874204.89);
   if(compressed.sellPrice()>250)throw new AssertionError("Compression ceiling missing");
   var diamond=data.entry("i:minecraft:diamond");double before=diamond.sellPrice();diamond.recordSale(10000);
   if(diamond.sellPrice()>=before)throw new AssertionError("Sale impact delayed");
   if(Policy.limit(diamond,64)!=0)throw new AssertionError("Offline sales allowed");
   String report="PASS: real NeoForge transformations, live price replacement, creative exclusion, shared allowance save/load, sell ceiling, immediate demand response and offline-sale gate verified.\n";
   Files.writeString(Path.of("probe-result.txt"),report);System.out.print(report);System.exit(0);
  } catch(Throwable e){e.printStackTrace();try{Files.writeString(Path.of("probe-result.txt"),"FAIL: "+e);}catch(Exception ignored){}System.exit(2);}
 });}
 private static void check(String name,String... names)throws Exception {
  var type=Class.forName(name);
  for(String n:names)if(Arrays.stream(type.getDeclaredMethods()).noneMatch(m->m.getName().contains(n)))throw new AssertionError(name+" missing "+n);
 }
}
