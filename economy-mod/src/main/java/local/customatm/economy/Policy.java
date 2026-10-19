package local.customatm.economy;

import com.google.gson.JsonParser;
import java.nio.file.*;
import java.util.*;
import com.dyneco.econ.*;
import com.dyneco.econ.Currency;
import net.neoforged.neoforge.server.ServerLifecycleHooks;

public final class Policy {
    private record Price(double value,int group) {}
    private static Map<String,Price> prices;
    private static final ThreadLocal<PlayerAccount> account = new ThreadLocal<>();
    private static final ThreadLocal<Integer> group = ThreadLocal.withInitial(()->4);
    private Policy() {}
    public static synchronized void load() {
        if(prices!=null)return;
        Path path=Path.of("config/customatm_economy/catalog.json");
        try(var reader=Files.newBufferedReader(path)) {
            var json=JsonParser.parseReader(reader).getAsJsonObject();
            if(json.get("schema").getAsInt()!=1)throw new IllegalStateException("Unsupported catalogue");
            var parsed=new HashMap<String,Price>();
            for(var e:json.getAsJsonObject("items").entrySet()) {
                var p=e.getValue().getAsJsonObject(); double value=p.get("value").getAsDouble();
                int g=switch(p.get("group").getAsString()){case "bulk"->1;case "farming"->2;case "resources"->3;case "manufactured"->4;default->throw new IllegalStateException("Invalid income group");};
                if(!Double.isFinite(value)||value<.01)throw new IllegalStateException("Invalid price: "+e.getKey());
                parsed.put(e.getKey(),new Price(value,g));
            }
            if(parsed.size()<50000)throw new IllegalStateException("Incomplete ATM10 catalogue");
            prices=Map.copyOf(parsed);
        } catch(Exception e) { throw new IllegalStateException("CustomATM economy catalogue could not be loaded",e); }
    }
    public static Map<String,Double> reprice(Map<String,Double> original) {
        load();Settings.apply();var result=new HashMap<String,Double>();
        original.forEach((id,value)->{
            if(!id.matches(".*(creative|spawn_egg|debug|command_block|structure_block|structure_void|jigsaw|barrier).*"))
                result.put(id,prices.containsKey(id)?prices.get(id).value:Math.max(.01,value*.1));
        });
        return result;
    }
    public static int group(String id) { load();return prices.containsKey(id)?prices.get(id).group:4; }
    public static double sellPrice(String id,double value) {
        // Huge compressed stacks and endgame equipment retain retail value, but
        // have a disclosed wholesale buyback ceiling so one unit can settle.
        return Math.min(value,Allowance.PER_HOUR[group(id)]/2);
    }
    public static PlayerAccount enter(PlayerAccount value) { account.set(value);return value; }
    public static int limit(MarketEntry entry,int requested) {
        PlayerAccount a=account.get();var server=ServerLifecycleHooks.getCurrentServer();
        if(a==null || server==null || server.getPlayerList().getPlayer(a.id)==null)return 0;
        int g=group(entry.id());group.set(g);
        double unit=Commodity.isFluid(entry.id())?1000.0:1.0;
        return Allowance.affordable(requested,((BudgetAccount)(Object)a).customatm$allowance().availableCents(g),
            count->Currency.toCents(entry.quoteSell(count/unit)));
    }
    public static void deposit(PlayerAccount a,long cents) {
        if(account.get()!=a)throw new IllegalStateException("Sale account mismatch");
        ((BudgetAccount)(Object)a).customatm$allowance().spend(group.get(),cents);
        a.deposit(cents);
    }
}
