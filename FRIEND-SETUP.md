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

**1.4.0: if you already updated to 1.3.0, just close Minecraft and run your existing Update CustomATM shortcut. No new ZIP is needed. Wait for Ready: CustomATM 1.4.0 on both computers.**

**Updating to 1.3.0: download and extract the new CustomATM-Setup.zip once, then run its Update Pack.cmd with Minecraft closed.** Updater version 4 recognizes verified FTB quest-file rewrites. Older shortcuts stop with an instruction to get the new Setup ZIP. Setup reuses your existing CustomATM tile and refreshes its updater/shortcut; it does not reinstall the base or copy worlds.

Close Minecraft and double-click **Update Pack.cmd** when the pack maintainer publishes an update. It checks the latest published release and downloads changed/missing managed files. You do not need to reinstall the whole pack or download the Setup ZIP again unless an update explicitly requires a newer updater.

Both players and the server need the matching release. This updater manages client profiles; it does not configure or update a dedicated server yet.

Your worlds, quest completion, wallet balances, screenshots, maps, server list and ordinary personal options are not distributed. The casino shortcut defaults to F8 when missing or still on H; an explicitly chosen other key is preserved. Fresh Setup installations also receive F8 before their first launch. In Controls, search by key name for **Open Casino** under **Casino Mod** (the mod does not call the category Gamble It). Press F8 while in a world with all menus closed. H conflicts with Essential and several base-pack mods.

## Invite a friend with Essential

CustomATM 1.2.0 includes Essential 1.5.1 (NeoForge 1.21.1). Both players should close Minecraft, run **Update CustomATM**, and wait for **Ready: CustomATM 1.2.0** or a later matching release.

Launch **CustomATM** in CurseForge, add each other through Essential's social menu, and open the world you want to share. In Essential's menu choose **Host**, then **Start Hosting**, and invite your friend using **Add Members**. Your friend accepts the invitation. If Essential presents first-use terms or account prompts, complete them yourself in game.

The host must leave Minecraft and the world open for the friend to stay connected. No separate server setup is needed. [Official hosting guide](https://essential.gg/en/wiki/start-hosting).

This release removes Crash Assistant and Drippy Loading Screen, which Essential lists as conflicting mods. Their jars are retained in update backups; FancyMenu and gameplay mods stay installed. [Compatibility notes](https://essential.gg/wiki/incompatible-mods).

## If it stops

- **CurseForge not ready:** open its Minecraft page and run Setup again. The automatic profile creation requires CurseForge Standalone; the Overwolf edition is not supported by this bootstrap.
- **Wrong base:** use the new Setup to create CustomATM. Do not change its Minecraft, loader, or base-pack version independently.
- **Extra mod:** the updater reports it without deleting it. Move it outside `mods` if you want to match this pack.
- **Local edits:** preserve your edits, then restore the last published file or ask the maintainer to include the change.
- **Download failed:** rerun. Downloads are verified before installation; incomplete downloads are not installed.
- **Interrupted update:** rerun. An unfinished transaction is restored from its backup before another update starts.

Backups and receipts are in `.customatm/transactions` inside the profile. Keep them until you have verified the update. The initial game content is customized but has not yet completed a full multiplayer playtest.

Profile creation uses CurseForge's local agent interface. If a future CurseForge update changes that interface, setup stops with an error rather than modifying another profile; download an updated Setup when available.
