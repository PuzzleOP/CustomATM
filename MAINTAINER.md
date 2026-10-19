# Publishing CustomATM updates

The source repository is `PuzzleOP/CustomATM`. A pushed commit alone does not update installations. Only a published stable release with the required assets is consumed.

1. Close Minecraft and make/test changes in the local CurseForge profile. Keep this release line on ATM10 8.3 and NeoForge 21.1.259.
2. For new non-CurseForge mods, add the author's direct HTTPS download URL to `pack/extra-sources.json`. The builder reads other URLs from CurseForge's installed-addon metadata. Never add private/token-bearing URLs.
3. Add custom config/script paths to `pack/managed-paths.json` deliberately. Do not add saves, credentials, personal maps or entire profile exports. Never use the live profile's whole config directory as a publishing input. Keep base-pack content out of the public snapshot.
4. Build a new version, for example:

   ```powershell
   python tools/build_release.py --profile "C:\path\to\All the Mods 10 - ATM10" --version 1.0.1
   powershell -NoProfile -ExecutionPolicy Bypass -File tests/Test-Updater.ps1
   ```

5. Review `pack/current-manifest.json`, `pack/snapshot/` and the release notes. Commit the matching source and snapshot. Push that commit.
6. Run `python tools/publish_release.py --version 1.0.1 --notes release-notes/1.0.1.md`. This uploads all three assets to a draft, verifies remote hashes, then publishes it as the latest stable release.
7. Both players run Update Pack. The state receipt records the exact installed version. Test the release in game before broad use; a server must be updated separately to the same compatible content.

Publishing uses your existing Git Credential Manager GitHub login in memory. It does not write tokens into files, logs or release assets. Authentication is only needed by the maintainer; recipients use public read-only downloads.

The updater refuses automatic downgrades. To roll back content, publish a higher version containing the previous tested files. Do not blindly restore an entire old profile or overwrite worlds. Transaction backups are also available for manual recovery.

Full base-pack upgrades require a separate migration and a new base requirement. Do not press CurseForge's update-all button and assume the old manifest still matches. Keep the official base pinned until that migration is prepared.
