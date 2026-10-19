import dev.latvian.mods.rhino.Context;
import dev.latvian.mods.rhino.ContextFactory;
import java.nio.file.Files;
import java.nio.file.Path;

/** Verifies the real workaround script against the installed Rhino engine. */
public class AmadronConfigSmoke {
    public static class ConfigValue<T> {
        private T value;
        public ConfigValue(T initial) { value = initial; }
        public void set(T next) { value = next; }
        public T get() { return value; }
    }
    public static class IntValue extends ConfigValue<Integer> {
        public IntValue(int initial) { super(initial); }
    }
    public static class Amadron {
        public final IntValue numVillagerOffers = new IntValue(20);
        public final IntValue numPeriodicOffers = new IntValue(10);
    }
    public static class Config { public final Amadron amadron = new Amadron(); }
    public static class ConfigHelper {
        private static final Config INSTANCE = new Config();
        public static Config common() { return INSTANCE; }
    }
    public static void main(String[] args) throws Exception {
        String script = Files.readString(Path.of(args[0]));
        for (boolean loaded : new boolean[] {false, true}) {
            Context cx = new ContextFactory().enter();
            var scope = cx.initStandardObjects();
            cx.addToScope(scope, "TestHelper", cx.wrapJavaClass(scope, ConfigHelper.class));
            cx.addToScope(scope, "TestInteger", cx.wrapJavaClass(scope, Integer.class));
            cx.evaluateString(scope, "var enabled=" + loaded + ";" + """
                var Platform = {isLoaded: function(id) { return enabled; }};
                var ServerEvents = {recipes: function(callback) { callback({}); }};
                var console = {info: function(text) {}};
                var Java = {loadClass: function(name) {
                  if (name === 'me.desht.pneumaticcraft.common.config.ConfigHelper') return TestHelper;
                  if (name === 'java.lang.Integer') return TestInteger;
                  throw new Error(name);
                }};
                """, "fixture", 1, null);
            for (int run = 0; run < 2; run++) {
                cx.evaluateString(scope, script, "amadron_multiplayer_fix.js", 1, null);
                // The typed read also detects accidentally storing a JS Double.
                int actual = ConfigHelper.common().amadron.numVillagerOffers.get();
                if (actual != (loaded ? 0 : 20)) throw new AssertionError(actual);
                if (ConfigHelper.common().amadron.numPeriodicOffers.get() != 10) throw new AssertionError("Changed standard offers");
            }
        }
        System.out.println("PASS: typed villager count is zero only with required mods loaded; standard offers stay at ten; repeat recipe reload succeeds.");
    }
}
