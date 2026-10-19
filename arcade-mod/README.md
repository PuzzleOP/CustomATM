# Redstone Arcade: all-game UI

Native Minecraft 1.21.1 / NeoForge 21.1.259 client UI for Gamble It 1.0.0 and the ATM10 Casinoâ€“DynEco Wallet bridge. Version 0.2.0 redesigns the hub and all eight games using the selected Redstone Arcade concept. The existing menus and server remain responsible for validation, randomness and money.

## Implemented screens

- Hub: eight game cards and a shared sidebar, wallet and close control.
- Coin Flip: animated gold/silver coin, Heads/Tails, actual 1.96x gross return and net-profit preview.
- Slots: three illustrated reels, staggered stops and real symbol/payout rules.
- Mines: 25 interactive tiles, 1â€“24 mine selector, next-safe odds and cash-out return.
- Blackjack: copper/parchment cards, hidden dealer card, hand totals, Hit/Stand/Double and actual settlement display.
- Roulette: all 37 numbers and nine outside positions, add/undo/clear wagers, total stake and result.
- Plinko: 16-row board, three risk levels, all 17 payout buckets and animation along the server-provided path.
- Scratch Ticket: nine revealable squares, click/drag or reveal-all, symbol paytable and winning-symbol highlights.
- Crash: server multiplier, sampled history chart, explicit cash-out and live polling while connected.

Each game has whole-credit bet editing, presets, pending/rejection states and rules. Returns include the original stake; the result line also shows net gain/loss. The sample wallet and outcomes in previews are demonstration data.

Native widgets provide keyboard focus/narration and input. An explicit press sends one action; duplicate wagers and keyboard auto-repeat are blocked. Blank-space clicks are consumed so the retained stock menu cannot expose invisible inventory-slot interactions. The header returns to the hub; the sidebar changes games when a round is not busy.

Models remain cached only for the current connection, so closing/reopening a menu can resume a pending result or active Mines, Blackjack or Crash round. Closing Crash does not pause or automatically cash out. Disconnecting clears the client cache. Server logout behavior remains unchanged.

A narrow client-only mixin delivers owned game results before the stock one-result mailbox can overwrite them. This prevents closely timed Crash poll/cash-out replies or replies from different cached games from being lost. It targets the inspected, pinned Gamble It 1.0.0 method without remapping. No server handlers, currencies, money APIs or network channels are added.

## Existing rules remain in force

This is a presentation and interaction pass, not a game-economy rebalance. Current server weights, odds, rounding and payouts are shown in each Rules panel. Small-bet rounding and the existing paytables still affect the economy. Do not describe all games as balanced by this update.

The Blackjack result parser reads the appended payout field rather than mistaking the stake for the return. This corrects what the UI displays; it does not alter what the server pays.

## Build and offline verification

```powershell
python arcade-mod/build.py --profile "..\CustomATM (1)"
python arcade-mod/verify.py --profile "..\CustomATM (1)"
```

These compile code and run bounded, headless Java checks/renderers. They do not launch Minecraft/NeoForge, load a world, install the addon, invoke the updater or modify the profile. Compilation uses a fresh classes directory and a 128 MB heap; tests use 64 MB and previews 128 MB. The candidate is `.work/arcade-build/customatm-arcade-0.2.0.jar`.

Test classes, extracted vanilla item textures/font, downloaded inspection tools and third-party decompiled sources are not packaged. Runtime item images reference Minecraft's own resources. Generated art is copied unchanged into the addon.

`design/preview/all-games-overview.png` shows all nine screens. The 59 state previews execute the production `ArcadeView`/`GameView` routines through Java2D with a locally extracted Minecraft bitmap font. They are offline renders, not in-game screenshots. Resource packs and GUI scaling may change runtime appearance.

## Release and later playtest

Pack release 1.4.0 distributes addon 0.2.0 through the managed updater. Preparation and publishing do not install it into the live profile. Close Minecraft and run Update CustomATM to install it. Never copy a jar into a running profile.

Offline compilation, protocol/input checks, asset/package checks and visual review pass. Native event replacement, mixin application, input/focus, sound, live wallet synchronization and Essential multiplayer still need an in-game playtest when the user is ready. No runtime or pixel-perfect claim is made before that check.

Later: open the usual casino with F8; visit every game; test keyboard and mouse input, rules/Escape and bet rejection; place small wagers and compare displayed return/net with wallet changes; resume Mines/Blackjack after closing; verify Crash continues while closed and accepts one cash-out; check slot/Plinko animations, Roulette multi-position bets and scratch drag; check GUI scales 2â€“4 and a friend-hosted world. No launch or live installation is part of the offline preparation.

Art reference and prompts: `design/concept-1.png`, `design/asset-prompts.md`. Visual review: `design/design-qa.md`.
