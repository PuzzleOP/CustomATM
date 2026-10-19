# Install CustomATM with CurseForge

Windows 10/11 with **CurseForge Standalone** (the standalone Windows app). No GitHub account, Git, Python, or manual ATM10 installation is needed.

1. Install/open CurseForge Standalone and open its **Minecraft** page. Complete its first-time Minecraft setup if prompted.
2. Close Minecraft.
3. Download **CustomATM-Setup.zip** from https://github.com/PuzzleOP/CustomATM/releases/latest and **extract** it into a folder.
4. Double-click **Update Pack.cmd**.
5. Wait for **Ready: CustomATM [version]**, then launch the **CustomATM** tile in CurseForge.

Setup creates a separate profile through CurseForge, installs Minecraft **1.21.1 / NeoForge 21.1.259**, downloads the official **ATM10 8.3** base, and installs our custom mods and quests. It reuses identical installed mod files when available; otherwise it downloads them from their authors' hosts. The first installation can take several minutes. Leave CurseForge and the setup window open until it finishes.

Running Setup again finds the profile it created and updates it instead of creating another tile. Older installations made by Setup 1.0.x remain separate; the new setup does not copy their worlds or personal settings. Use the new **CustomATM** tile. Existing ATM10 is not renamed or overwritten.

The first run installs a permanent **Update Pack.cmd** inside the profile and an **Update CustomATM** desktop shortcut. In CurseForge, use the profile menu's **Open Folder** to find the updater if a desktop shortcut could not be created.

## Future updates

Close Minecraft and double-click **Update Pack.cmd** when the pack maintainer publishes an update. It checks the latest published release and downloads changed/missing managed files. You do not need to reinstall the whole pack or download the Setup ZIP again unless an update explicitly requires a newer updater.

Both players and the server need the matching release. This updater manages client profiles; it does not configure or update a dedicated server yet.

Your worlds, quest completion, wallet balances, screenshots, maps, server list and ordinary personal options are not distributed. The casino shortcut defaults to F8 when unbound or still on H; an explicitly chosen other key is preserved. If you have never launched the base game and have no options file yet, set Casino Mod > Open Casino to F8 in Controls after the first launch.

## If it stops

- **CurseForge not ready:** open its Minecraft page and run Setup again. The automatic profile creation requires CurseForge Standalone; the Overwolf edition is not supported by this bootstrap.
- **Wrong base:** use the new Setup to create CustomATM. Do not change its Minecraft, loader, or base-pack version independently.
- **Extra mod:** the updater reports it without deleting it. Move it outside `mods` if you want to match this pack.
- **Local edits:** preserve your edits, then restore the last published file or ask the maintainer to include the change.
- **Download failed:** rerun. Downloads are verified before installation; incomplete downloads are not installed.
- **Interrupted update:** rerun. An unfinished transaction is restored from its backup before another update starts.

Backups and receipts are in `.customatm/transactions` inside the profile. Keep them until you have verified the update. The initial game content is customized but has not yet completed a full multiplayer playtest.

Profile creation uses CurseForge's local agent interface. If a future CurseForge update changes that interface, setup stops with an error rather than modifying another profile; download an updated Setup when available.
