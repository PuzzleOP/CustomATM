# Publishing CustomATM updates

The source repository is `PuzzleOP/CustomATM`. A pushed commit alone does not update installations. Only a published stable release with the required assets is consumed.

1. Close Minecraft and make/test changes in the local CurseForge profile. Keep this release line on ATM10 8.3 and NeoForge 21.1.259.
2. For new non-CurseForge mods, add the author's direct HTTPS download URL to `pack/extra-sources.json`. The builder reads other URLs from CurseForge's installed-addon metadata. Never add private/token-bearing URLs.
3. Add custom config/script paths to `pack/managed-paths.json` deliberately. Do not add saves, credentials, personal maps or entire profile exports. Never use the live profile's whole config directory as a publishing input. Keep base-pack content out of the public snapshot.
4. Build a new version, for example:

   ```powershell
   python tools/build_release.py --profile "C:\path\to\All the Mods 10 - ATM10" --version 1.1.0
   powershell -NoProfile -ExecutionPolicy Bypass -File tests/Test-Updater.ps1
   ```

5. Review `pack/current-manifest.json`, `pack/snapshot/` and the release notes. Commit the matching source and snapshot. Push that commit.
6. Run `python tools/publish_release.py --version 1.1.0 --notes release-notes/1.1.0.md`. This uploads all three assets to a draft, verifies remote hashes, then publishes it as the latest stable release.
7. Both players run Update Pack. The state receipt records the exact installed version. Test the release in game before broad use; a server must be updated separately to the same compatible content.

Publishing uses your existing Git Credential Manager GitHub login in memory. It does not write tokens into files, logs or release assets. Authentication is only needed by the maintainer; recipients use public read-only downloads.

The updater refuses automatic downgrades. To roll back content, publish a higher version containing the previous tested files. Do not blindly restore an entire old profile or overwrite worlds. Transaction backups are also available for manual recovery.

Full base-pack upgrades require a separate migration and a new base requirement. Do not press CurseForge's update-all button and assume the old manifest still matches. Keep the official base pinned until that migration is prepared.

## Profile bootstrap

Release 1.3.0 requires client version 4 and a one-time Setup ZIP refresh. `pack/known-runtime-forms.json` contains exact FTB-saved quest hashes tied to their old published hashes, verified with `QuestRewriteCheck.java`. Add a rewrite only after comparing its semantic content to the corresponding published chapter; never add arbitrary personal edits or allow whole config directories. All replacements still use normal transaction backups.

Client version 3 creates a native CurseForge profile through the running Standalone app's local agent. A GUID-bound `.customatm/bootstrap.json` receipt identifies profiles it owns; setup never adopts unrelated profiles just because they have the same display name. The ATM10 archive is downloaded from its original ForgeCDN URL and checked against a pinned SHA256. Only its base overrides are extracted locally; they are not republished. Four original shader packs are pinned in `client/base-extras.json`. The published mod manifest supplies the complete customized mod set.

`Setup-Profile.ps1` contains the adapter for the local agent API. Its temporary connection key stays in memory and is not shipped or logged. This is an internal interface verified with the installed Standalone build; future CurseForge changes may require updating this adapter. CurseForge must be installed and its Minecraft setup completed once. The bootstrap does not install CurseForge itself or support the Overwolf edition.

Build from the new CustomATM profile after editing it. The builder accepts its verified bootstrap receipt and retains known original download URLs from the preceding manifest. New third-party mods still need metadata from CurseForge or an entry in `extra-sources.json`.
