// CustomATM: keep the largest destructive warheads out of survival and DynEco.
// This is an acquisition restriction, not claim protection or a creative-mode ban.
if (Platform.isLoaded('ballistix')) {
  ServerEvents.recipes(event => {
    let blocked = [
      'ballistix:nuclear', 'ballistix:antimatter',
      'ballistix:largeantimatter', 'ballistix:darkmatter',
      'ballistix:minecartnuclear', 'ballistix:minecartantimatter',
      'ballistix:minecartlargeantimatter', 'ballistix:minecartdarkmatter'
    ]
    blocked.forEach(id => event.remove({ output: id }))
    if (Platform.isLoaded('dyneco')) {
      let config = Java.loadClass('com.dyneco.Config')
      let TreeSet = Java.loadClass('java.util.TreeSet')
      let ArrayList = Java.loadClass('java.util.ArrayList')
      let denied = new TreeSet()
      denied.addAll(config.DENY_ITEMS.get())
      let allowed = new TreeSet()
      allowed.addAll(config.ALLOW_ITEMS.get())
      blocked.forEach(id => { denied.add(id); allowed.remove(id) })
      let denyList = new ArrayList()
      denyList.addAll(denied)
      config.DENY_ITEMS.set(denyList)
      let allowList = new ArrayList()
      allowList.addAll(allowed)
      config.ALLOW_ITEMS.set(allowList)
    }
    console.info('[CustomATM Ballistix] Removed crafting and market access for 8 restricted warhead/minecart items.')
  })
}
