// Local ATM10 customization: broad DynEco market, normal DynEco prices.
// Recipe loading happens before DynEco's ServerStartedEvent price calculation.
// Rebuild from the live registry on world load/reload, including KubeJS items.
// Remove this script to return to DynEco's normal equipment/machine filtering.

if (Platform.isLoaded('dyneco')) {
  ServerEvents.recipes(event => {
    const config = Java.loadClass('com.dyneco.Config')
    const registry = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries').ITEM
    const TreeSet = Java.loadClass('java.util.TreeSet')
    const ArrayList = Java.loadClass('java.util.ArrayList')
    const allowed = new TreeSet()
    const deniedItems = new TreeSet(config.DENY_ITEMS.get())
    const deniedMods = new TreeSet(config.DENY_MODS.get())

    // Preserve the user's explicit allow list. DynEco's deny lists still win.
    allowed.addAll(config.ALLOW_ITEMS.get())
    const ids = registry.keySet().iterator()
    while (ids.hasNext()) {
      const key = ids.next()
      const id = String(key.toString())
      const namespace = String(key.getNamespace())
      const path = String(key.getPath())

      // Keep administrative and creative-tier items outside the automatic list.
      // Spawn eggs and internal display items also retain DynEco's filtering.
      if (namespace === 'dyneco' || deniedItems.contains(id) || deniedMods.contains(namespace)) continue
      if (/creative|debug|command_block|structure_block|structure_void|jigsaw|barrier|spawn_egg/.test(path)) continue
      if (/^(air|cave_air|void_air|light|bedrock|knowledge_book|player_head)$/.test(path)) continue
      if (/(^|\/)(test|dummy|internal)(_|\/|$)/.test(path)) continue

      allowed.add(id)
    }

    // An explicit allow list overrides DynEco's equipment/block-entity checks.
    // Apply in memory: do not replace the player's on-disk allow list with
    // thousands of generated entries. Re-applied every time recipes load.
    config.ALLOW_ITEMS.set(new ArrayList(allowed))
    console.info('[ATM10 local economy] Broad DynEco market: ' + allowed.size() + ' allowed item IDs; default pricing and market simulation retained.')
  })
}
