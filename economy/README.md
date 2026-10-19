# Farm-aware economy — CustomATM 1.3.0

This patch was prepared separately from the running CustomATM profile and is distributed with the 1.3.0 quest update. Both players must download and extract the new Setup ZIP once, close Minecraft, and run its Update Pack.cmd to refresh the updater to client version 4. Existing balances are preserved. Full in-game and multiplayer validation remains pending; the checks completed without opening another game are documented below.

The target is up to **$10,000 per online hour per player** from a developed factory, with substantially less from basic farms. These are base DynEco credits; another display currency can show different numbers.

## Prices and demand

The catalogue assigns a base value and income group to all **64,236 entries** in the current DynEco report. It reduces cheap renewable inputs and recalculates downstream recipe values. Metal forms and compressed resources follow their underlying material. Explicit endgame values protect ATM Stars, shards, ATM alloys and antimatter from known bad automatic estimates.

| Item | Base value | Normal buy quote | Normal sell quote |
|---|---:|---:|---:|
| Cobblestone | $0.01 | $0.013 | $0.007 |
| Iron ingot | $8 | $10.40 | $5.60 |
| Diamond | $100 | $130 | $70 |
| Diamond pickaxe | $352.02 | about $457.63 | about $246.42 |

Quotes above assume neutral demand. Stock and demand still move prices. Transactions round the **whole batch** to cents; individual items can have a fractional-cent price. A batch with no payout is left unsold.

Prices alone cannot contain ATM10's practically unlimited resource generators. Every player's sales therefore consume a persistent shared demand allowance:

| Income group | Demand recovered per online hour | Maximum saved allowance |
|---|---:|---:|
| Bulk natural blocks, water and lava | $500 | $500 |
| Farming, wood, food and basic crafted derivatives | $1,500 | $1,500 |
| Resources, metals, gems and essences | $4,000 | $4,000 |
| Manufactured goods and equipment | $10,000 | $10,000 |
| **Shared total across every group** | **$10,000** | **$10,000** |

A sale consumes both its category allowance and the shared total. Multiple linked chests, tanks and listings share these limits. Unused allowance permits a later burst; this is a sustained income ceiling, not a strict rolling-hour limit or guaranteed income. The existing market may buy less. New allowance records start with $250 total ($25/$50/$100/$250 category allowances), which is **not money deposited into the wallet**.

Allowance recovers once per 20 server ticks while online: roughly a real second at normal speed, slower during lag. Offline selling is paused. Logout, reconnect and restart retain the saved allowance. Existing wallet balances are not reset. Unsold quantities remain in their container or listing.

Use **`/marketlimits`** to see current available demand and recovery rates. Bulk sales also depress that item's price immediately, instead of waiting for the next market day.

Very expensive items retain their retail value, but buyback is capped per item (or fluid bucket): **$250 bulk / $750 farming / $2,000 resources / $5,000 manufactured**. This allows individual expensive goods to settle within finite demand. High compression does not create additional allowance. Do not assume a costly machine or compressed block sells for its purchase price; inspect the sell quote first.

Creative/admin items remain excluded. Catalogue coverage does not imply all entries are available in the shop: registry availability, discovery and existing eligibility rules still apply. Gambling and other non-market rewards keep their existing behavior; these limits govern DynEco sales.

## Source and verification

- `price-audit.csv`: old/new base values, groups and original pricing source for every entry.
- `../tools/balance_economy.py`: generator. Use the **original baseline** report, not the output of this rebalance. Its SHA256 is recorded in `catalog.json`.
- `../economy-mod/`: original compatibility addon, pinned to DynEco 1.2.0 / NeoForge 21.1.259 / Minecraft 1.21.1.
- `../tests/check_economy.py`: file-only coverage, progression, compression and packaging checks.
- `../tests/AllowanceTest.java`: stress tests for shared/category allowances, rounding and recovery.

This is an automation-aware balance pass, not a manual appraisal of every recipe. DynEco's report omits some recipe paths and includes fallback estimates. The shared allowance contains missed high-output farms, but progression prices and category assignments still need playtesting.

The first isolated runtime probe verified transformation hooks, account persistence and basic price replacement, then stopped on a missing compressed-item fixture in its minimal mod set. That fixture has been corrected. The full probe and actual chest/tank/multiplayer sale tests remain pending. **Do not run the probe while Minecraft is open.** It now requires `--game-closed` and refuses to start when any Java game process is running.

Next playtest: with the game closed, rerun the isolated probe; then test inventory listings, multiple linked chests, a fluid tank, expensive compressed goods, reconnect/save persistence, and friend-side quotes. The numbered release is built from a temporary staging directory outside CurseForge Instances, using the previous canonical payload plus this patch. Do not overwrite the active profile while it is running.
