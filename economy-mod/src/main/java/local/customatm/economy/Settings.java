package local.customatm.economy;
import com.dyneco.Config;
public final class Settings {
    private Settings() {}
    public static void apply() {
        Config.SPREAD.set(.60);
        Config.ELASTICITY.set(.9);
        Config.ELASTICITY_VALUE_SCALE.set(0.0);
        Config.ELASTICITY_MIN.set(.9);
        Config.ELASTICITY_MAX.set(.9);
        Config.PRICE_FLOOR_MULT.set(.03);
        Config.PRICE_CEIL_MULT.set(1.40);
        Config.PRICE_LAG_RATE.set(1.0);
        Config.STOCK_CONSTANT.set(400.0);
        Config.RESTOCK_RATE.set(.03);
        Config.CONSIGNMENT_BUDGET_PER_CHEST.set(false);
        Config.CONSIGNMENT_MAX_ITEMS.set(64);
        Config.LISTING_BUYER_CREDITS.set(25.0);
        Config.LISTING_BULK_CHANCE.set(.01);
        Config.DEMAND_VOLATILITY.set(.015);
    }
}
