import dev.latvian.mods.rhino.Context;
import dev.latvian.mods.rhino.ContextFactory;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;

/** Runs the real market script with the installed Rhino engine and a small registry fixture. */
public class BroadMarketSmoke {
    public static class Value {
        private List<String> value;
        public Value(String... values) { value = new ArrayList<>(List.of(values)); }
        public List<String> get() { return value; }
        public void set(List<String> next) { value = next; }
    }
    public static class Config {
        public static final Value DENY_ITEMS = new Value("minecraft:barrier", "example:forbidden");
        public static final Value DENY_MODS = new Value("blocked");
        public static final Value ALLOW_ITEMS = new Value("example:manual_allow");
    }
    public static class Key {
        private final String id;
        public Key(String id) { this.id = id; }
        public String getNamespace() { return id.split(":")[0]; }
        public String getPath() { return id.split(":")[1]; }
        public String toString() { return id; }
    }
    public static class Registry {
        public Set<Key> keySet() {
            Set<Key> keys = new LinkedHashSet<>();
            for (String id : List.of("minecraft:iron_ingot", "minecraft:diamond_sword",
                    "example:machine", "example:creative_machine", "example:forbidden",
                    "blocked:ingot", "minecraft:barrier", "minecraft:pig_spawn_egg",
                    "dyneco:market_tablet")) keys.add(new Key(id));
            return keys;
        }
    }
    public static class Registries { public static final Registry ITEM = new Registry(); }
    public static void main(String[] args) throws Exception {
        Context cx = new ContextFactory().enter();
        var scope = cx.initStandardObjects();
        cx.addToScope(scope, "TestConfig", cx.wrapJavaClass(scope, Config.class));
        cx.addToScope(scope, "TestRegistries", cx.wrapJavaClass(scope, Registries.class));
        cx.addToScope(scope, "TestTreeSet", cx.wrapJavaClass(scope, TreeSet.class));
        cx.addToScope(scope, "TestArrayList", cx.wrapJavaClass(scope, ArrayList.class));
        String setup = """
            var Platform = {isLoaded: function(id) { return true; }};
            var ServerEvents = {recipes: function(callback) { callback({}); }};
            var console = {info: function(text) {}};
            var Java = {loadClass: function(name) {
              if (name === 'com.dyneco.Config') return TestConfig;
              if (name === 'net.minecraft.core.registries.BuiltInRegistries') return TestRegistries;
              if (name === 'java.util.TreeSet') return TestTreeSet;
              if (name === 'java.util.ArrayList') return TestArrayList;
              throw new Error(name);
            }};
            """;
        cx.evaluateString(scope, setup, "fixture", 1, null);
        String script = Files.readString(Path.of(args[0]));
        for (int run = 0; run < 2; run++) {
            cx.evaluateString(scope, script, "dyneco_broad_market.js", 1, null);
            var expected = List.of("example:machine", "example:manual_allow", "minecraft:diamond_sword", "minecraft:iron_ingot");
            if (!Config.ALLOW_ITEMS.get().equals(expected)) throw new AssertionError(Config.ALLOW_ITEMS.get());
        }
        System.out.println("PASS: real script includes equipment/machines, preserves explicit allows, excludes denied/creative items, and reloads without duplication.");
    }
}
