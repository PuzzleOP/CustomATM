import dev.latvian.mods.rhino.Context;
import dev.latvian.mods.rhino.ContextFactory;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

/** Executes the actual scripts in the pack's Rhino engine, without launching Minecraft. */
public class BallistixPolicySmoke {
    public static void main(String[] args) throws Exception {
        Context cx = new ContextFactory().enter();
        var scope = cx.initStandardObjects();
        cx.addToScope(scope, "TestConfig", cx.wrapJavaClass(scope, BroadMarketSmoke.Config.class));
        cx.addToScope(scope, "TestRegistries", cx.wrapJavaClass(scope, BroadMarketSmoke.Registries.class));
        cx.addToScope(scope, "TestTreeSet", cx.wrapJavaClass(scope, TreeSet.class));
        cx.addToScope(scope, "TestArrayList", cx.wrapJavaClass(scope, ArrayList.class));
        cx.evaluateString(scope, """
            var removed = [];
            var Platform = {isLoaded: function(id) {return true;}};
            var ServerEvents = {recipes: function(callback) {
                callback({remove: function(filter) {removed.push(filter.output);}});
            }};
            var console = {info: function(text) {}};
            var Java = {loadClass: function(name) {
                if (name === 'com.dyneco.Config') return TestConfig;
                if (name === 'net.minecraft.core.registries.BuiltInRegistries') return TestRegistries;
                if (name === 'java.util.TreeSet') return TestTreeSet;
                if (name === 'java.util.ArrayList') return TestArrayList;
                throw new Error(name);
            }};
            """, "fixture", 1, null);
        var blocked = Set.of("ballistix:nuclear", "ballistix:antimatter", "ballistix:largeantimatter",
                "ballistix:darkmatter", "ballistix:minecartnuclear", "ballistix:minecartantimatter",
                "ballistix:minecartlargeantimatter", "ballistix:minecartdarkmatter");
        String policy = Files.readString(Path.of(args[0]));
        String market = Files.readString(Path.of(args[1]));
        // Both event orders, repeated reloads, and pre-existing explicit allows.
        for (boolean reverse : List.of(false, true)) {
            BroadMarketSmoke.Config.DENY_ITEMS.set(new ArrayList<>(List.of("example:forbidden", "minecraft:barrier")));
            var allows = new ArrayList<>(blocked);
            allows.addAll(List.of("example:manual_allow", "ballistix:condensive", "ballistix:samturret"));
            BroadMarketSmoke.Config.ALLOW_ITEMS.set(allows);
            for (int run = 0; run < 2; run++) {
                cx.evaluateString(scope, "removed = [];", "reset", 1, null);
                cx.evaluateString(scope, reverse ? market : policy, "first", 1, null);
                cx.evaluateString(scope, reverse ? policy : market, "second", 1, null);
                var denied = BroadMarketSmoke.Config.DENY_ITEMS.get();
                var allowed = BroadMarketSmoke.Config.ALLOW_ITEMS.get();
                if (!denied.containsAll(blocked) || denied.size() != 10) throw new AssertionError(denied);
                if (allowed.stream().anyMatch(blocked::contains)) throw new AssertionError(allowed);
                if (!allowed.containsAll(List.of("ballistix:condensive", "ballistix:samturret",
                        "example:manual_allow", "minecraft:diamond_sword"))) throw new AssertionError(allowed);
                String removed = String.valueOf(cx.evaluateString(scope, "removed.sort().join(',')", "read", 1, null));
                if (!new HashSet<>(Arrays.asList(removed.split(","))).equals(blocked)) throw new AssertionError(removed);
            }
        }
        System.out.println("PASS: real Rhino policy removes 8 recipes and market allows; preserves conventional gear and existing denies; works in either callback order and on reload.");
    }
}
