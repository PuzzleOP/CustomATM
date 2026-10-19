# CustomATM quest workshops

The ten original chapters now contain **269 quests**, including **224 quests with item objectives**, **60 new workshop exercises**, **38 named branches**, three planet-visit tasks and ten original explanatory diagrams. This is a rebuild of the previous 209-quest guide set, not a replacement of ATM10's own chapters.

The local ATM10 8.3 Mekanism, AE2 and other advanced chapters were inspected as structural references: meaningful equipment nodes, topic branches, worked setups, illustrated explanations and rewards. Their writing and image assets are not copied into this repository. Our chapter headings and diagrams are original generated assets.

## What changed

- Replaced the repeated serpentine reading chain with separate branches for foundations, resource systems, optional integrations and projects.
- Added concrete material goals, real Ender IO conduit component data, the Structurize Build Tool ID, three Ad Astra destination checks, setup diagrams and small non-repeatable XP rewards.
- Added examples for RS processing/return paths, colony request delivery, SFM retention/furnace sides, XNet channels, ComputerCraft read-only dashboards, Astral's current port and RFTools card/recipe handling.
- Made ordinary equipment milestones complete through item detection. Their setup reminder checkmarks are optional. Final projects still ask for a practical confirmation because possessing a machine does not prove that it works.
- Kept the casino branch optional and independent of main progression; no gambling win, repeated betting or wallet balance is required.
- Preserved all 209 original quest IDs and ten chapter IDs. Existing item-task IDs are reused when the same item remains an objective. New objectives may require additional items; saved quest data is never overwritten by the updater.

## Rebuilding

`content.py` preserves the original explanations and stable quest order. `rework.py` adds branch plans, dependencies, concrete objectives, worked notes, program examples and new workshop quests. `legacy-ids.json` records the original IDs so titles and layouts can change without generating a new quest identity.

Run `python tools/build_quests.py` from the repository root. This writes only the sanitized snapshot. It does not modify the installed profile. Pillow and Windows Segoe UI fonts produce the original PNG diagrams/headings. `build-summary.json` records the chapter counts.

Validation:

```powershell
python tests/check_quests.py
python tests/check_economy.py
```

The quest checks cover unique IDs, acyclic/resolved dependencies, preserved quest identities, language entries, image references, item evidence from the installed pack, non-consuming tasks, bounded rewards, optional branches and node spacing. `QuestSnbtCheck.java` parses all 20 chapter/language files with Minecraft's actual SNBT parser without bootstrapping a game or loading a world. A generated map preview was also inspected.

The in-game FTB rendering and multiplayer progression have not yet been playtested for this release; the host requested no second game launch while playing. Item possession and checkmarks are deliberately described as different kinds of evidence.

## Technical references

The installed jars' language, recipe and guide resources supplied version-specific item names, conduit components, Ad Astra and Astral guide details. Additional primary references:

- [MineColonies request system](https://minecolonies.com/wiki/systems/request/)
- [MineColonies warehouse](https://minecolonies.com/wiki/buildings/warehouse/)
- [XNet author documentation](https://mcjty.eu/docs/mods/xnet)
- [RS processing recipes](https://refinedmods.com/refined-storage/guides/processing-recipes.html)
- [RS Autocrafter](https://refinedmods.com/refined-storage/autocrafting/autocrafter.html)
- [CC: Tweaked peripherals](https://tweaked.cc/module/peripheral.html)
- [SFM retention example](https://github.com/TeamDman/SuperFactoryManager/blob/1.19.2/examples/02-retention.sfm), cross-checked against the installed port's examples
- [Refined Types Network Energizer release notes](https://modrinth.com/mod/refined-types/version/1.21.1-0.2.0)
