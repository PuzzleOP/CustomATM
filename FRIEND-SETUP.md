# Install CustomATM with CurseForge

Windows 10/11. Keep using CurseForge; no GitHub account or Git installation is needed.

1. Install **All the Mods 10 - ATM10, version 8.3** in CurseForge. Required Minecraft: **1.21.1**, loader: **NeoForge 21.1.259**. Use the pack's version list to choose 8.3 specifically.
2. Close Minecraft. Keep this as a dedicated CustomATM profile; do not independently update the base pack or individual mods.
3. Download **CustomATM-Setup.zip** from https://github.com/PuzzleOP/CustomATM/releases/latest . Extract it into a folder before running anything.
4. Double-click **Update Pack.cmd**. It finds your ATM10 8.3 profile, or asks you to select its folder if there is more than one. The correct folder contains `mods` and `minecraftinstance.json`.
5. Wait for **Ready: CustomATM [version]**, then launch that profile normally in CurseForge.

The first run installs a permanent **Update Pack.cmd** inside the profile. In CurseForge, use the profile menu's **Open Folder** to find it. You can create a desktop shortcut to it.

## Future updates

Close Minecraft and double-click **Update Pack.cmd** when the pack maintainer publishes an update. It checks the latest published release and downloads changed/missing managed files. You do not need to reinstall the whole pack or download the Setup ZIP again unless an update explicitly requires a newer updater.

Both players and the server need the matching release. This updater manages client profiles; it does not configure or update a dedicated server yet.

Your worlds, quest completion, wallet balances, screenshots, maps, server list and ordinary personal options are not distributed. The casino shortcut defaults to F8 when unbound or still on H; an explicitly chosen other key is preserved. If you have never launched the base game and have no options file yet, set Casino Mod > Open Casino to F8 in Controls after the first launch.

## If it stops

- **Wrong base:** choose ATM10 8.3 / NeoForge 21.1.259 through CurseForge. Other ATM10 versions and ATM10 Sky are different packs.
- **Extra mod:** the updater reports it without deleting it. Move it outside `mods` if you want to match this pack.
- **Local edits:** preserve your edits, then restore the last published file or ask the maintainer to include the change.
- **Download failed:** rerun. Downloads are verified before installation; incomplete downloads are not installed.
- **Interrupted update:** rerun. An unfinished transaction is restored from its backup before another update starts.

Backups and receipts are in `.customatm/transactions` inside the profile. Keep them until you have verified the update. The initial game content is customized but has not yet completed a full multiplayer playtest.
