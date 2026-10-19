# CustomATM

Versioned updates for PuzzleOP's customized **ATM10 8.3**, while continuing to use CurseForge.

**[Install / update instructions](FRIEND-SETUP.md)** · **[Download the latest release](https://github.com/PuzzleOP/CustomATM/releases/latest)**

Open Minecraft in CurseForge Standalone, extract the latest Setup ZIP, then run **Update Pack.cmd**. It creates a separate **CustomATM** tile and installs the ATM10 8.3 base automatically. No GitHub account is required for downloads. The updater receives changes only from published, non-prerelease GitHub releases; pushing an unfinished source change does not update anyone's game.

Included customizations: Essential friend invites/world hosting, DynEco broad market, a shared-wallet Gamble It bridge, Refined Storage addons, Cubes Without Borders, and 10 guided quest chapters containing 209 quests. MineColonies, Ad Astra and the other base mods come from the original ATM10 installation.

## Update behavior

- Pins the exact client mod inventory and file checksums.
- Retrieves third-party jars from their original download services. They are not checked into this repository or bundled in our payload.
- Ships original custom quests/scripts and our bridge in a small overlay archive.
- Installs the pinned ATM10 8.3 base and matching Minecraft/NeoForge versions automatically through CurseForge Standalone. Repeat setup reuses the CustomATM profile.
- Stages and checks every changed file before applying changes.
- Backs up replacements/removals and uses a recovery journal. Interrupted updates restore the prior state on the next run.
- Removes only known obsolete or previously managed files whose hashes match. Unknown additional mods cause a clear stop instead of silent deletion.
- Protects locally edited managed files on subsequent updates.
- Leaves saves, personal maps and account/launcher data outside the managed files. Quest definitions are updated; saved quest progress is not copied or reset.

The English quest split files are merged by the pack's FTB language splitter on launch. The updater adds our group without replacing the base questbook. Keep custom quest IDs stable when editing so completion stays attached to the same quests.

## Playing with a friend

Both players run **Update CustomATM** before launching. Release **1.2.0** adds Essential **1.5.1** for NeoForge 1.21.1. Add each other in Essential, open the world, then use **Host > Start Hosting > Add Members** to invite your friend. Keep the host's game and world open. See the [official hosting guide](https://essential.gg/en/wiki/start-hosting).

Crash Assistant and Drippy Loading Screen are removed because Essential lists them as conflicting mods; the updater backs up their jars. FancyMenu remains installed. See [Essential's compatibility notes](https://essential.gg/wiki/incompatible-mods).

## Publishing an update

See [MAINTAINER.md](MAINTAINER.md). Build and test a numbered release, then publish it. Both players run their shortcut before joining. Server packaging is separate and is not implemented by this client updater.

ATM10 and third-party mods remain their authors' work. This is a custom companion updater, not an official AllTheMods release. Initial quest/content changes still require an in-game and multiplayer playtest; the updater's automated tests are documented with each release.
