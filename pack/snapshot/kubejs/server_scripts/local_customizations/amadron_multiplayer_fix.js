// PneumaticCraft 8.2.23 caches villager ItemStacks across registry reloads.
// Advanced Peripherals pocket/turtle upgrades in those cached offers can fail
// to encode in pneumaticcraft:sync_amadron_offers and disconnect joining players.
// Keep ordinary villagers and all recipe/player Amadron offers; omit only the
// random villager-offer import until the upstream registry-cache bug is fixed.
if (Platform.isLoaded('pneumaticcraft') && Platform.isLoaded('advancedperipherals')) {
  ServerEvents.recipes(event => {
    const ConfigHelper = Java.loadClass('me.desht.pneumaticcraft.common.config.ConfigHelper')
    const Integer = Java.loadClass('java.lang.Integer')
    ConfigHelper.common().amadron.numVillagerOffers.set(Integer.valueOf(0))
    console.info('[CustomATM multiplayer] Amadron villager-offer import disabled to prevent invalid upgrade registry packets; standard Amadron offers and ordinary villager trading remain enabled.')
  })
}
