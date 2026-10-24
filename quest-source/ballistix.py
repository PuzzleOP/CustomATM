"""Original, version-specific Ballistix workshop text. Keys are permanent quest identities."""
LANES = ['POWER & COMMISSIONING', 'YOUR FIRST MISSILE', 'RADAR & EARLY WARNING',
         'LAYERED DEFENSES', 'ADVANCED OPERATIONS']
QUESTS = []

def q(key, title, lane, deps, items, why, steps, tip, *, project=False, optional=False, image=None):
    QUESTS.append(dict(key=key, title=title, lane=lane, deps=deps.split(), items=items.split(),
                       why=why, steps=steps, tip=tip, project=project, optional=optional, image=image))

q('start', 'Ballistix: build an outpost', -1, '', '',
  'Ballistix turns a power network into a missile outpost: launchers deliver explosive payloads, radars detect threats, and turrets try to intercept them. The interesting contest in ATM10 is keeping an outpost operational; endgame armor does not make ordinary weapons a balanced player duel.',
  ['This chapter targets CustomATM with Ballistix 1.2.3 and Voltaic 1.2.0. Electrodynamics is not installed, so use FE from your existing generators and cables.',
   'Follow Power, then Your First Missile. Build Radar and Layered Defenses before trying a two-player battle. Advanced Operations is optional.',
   'Choose a disposable test outpost away from your factories and MineColonies settlement. Agree which structures count as targets. Claim protection and the existing MFFS mod have not been verified against these blasts.',
   'CustomATM removes nuclear, antimatter, large-antimatter and dark-matter explosives and their minecarts from crafting and the market. Other payloads can still cause substantial damage. Start with Condensive.'],
  'Search JEI for @ballistix. These quests teach connections and operation; JEI supplies the exact recipes for your pack.', image='overview')

q('legend', 'How this workshop completes', -1, 'start', '',
  'The map separates collecting equipment from demonstrating that it works. Owning a launcher is useful evidence of preparation, but it cannot prove that the launcher has power or the correct target.',
  ['Hexagons are equipment milestones: hold the listed items in your inventory. Items are not consumed, and equipment you already own counts.',
   'Book cards are references or setup instructions. Their checkmarks acknowledge that you have read and followed the lesson; they do not inspect your world.',
   'Large diamonds are practical projects. Complete their checkmark after observing the stated result. The quest system does not automatically detect a launch, a radar link, or an intercepted missile.',
   'Optional branches explain upgrades and alternate defenses. They are not prerequisites for finishing the main outpost project. Rewards are small, one-time XP awards.'],
  'If an item quest stays incomplete, put the item in your own inventory rather than leaving it in a chest or a placed machine.', optional=True)

q('buffer', 'A local power reserve', 0, 'start', 'mekanism:basic_energy_cube',
  'An outpost needs energy available when the alarm sounds. A local battery separates a brief supply interruption from an immediate loss of radar and weapons. You can use a stronger existing FE store; the Basic Energy Cube is the reference build for this branch.',
  ['Connect an existing FE generator to the Energy Cube and watch its stored energy rise. In the cube configuration, set the generator-facing side to input and the cable-facing side to output.',
   'Keep the cube accessible so you can see its charge during a test. A full battery shows stored energy, not that the generator can sustain every turret indefinitely.',
   'Build and commission one device at a time. Add a second power feed or reserve once the basic chain works.'],
  'If the cube drains while defenses idle, improve generation before adding more turrets. A larger battery only delays a sustained shortage.', image='power')

q('cables', 'Carry FE to the right face', 0, 'buffer', 'mekanism:basic_universal_cable*8',
  'In this pack, Voltaic exposes FE inputs without needing voltage converters or an Electrodynamics generator. Mekanism Universal Cables are a convenient reference; another compatible FE cable is fine when it supplies enough energy.',
  ['Run cable from the cube output to the Control Panel of a missile silo. The panel accepts power from its sides; putting power only into the Launch Platform does not energize the controller.',
   'For Search Radar, Fire Control Radar and all four turret types, route the cable underneath the base block. Their energy input is on the bottom.',
   'The compact VLS accepts power from any side. Reserve space beneath radar and turret bases before covering the wiring.',
   'Check both ends: the source must output, the cable must connect, and the machine energy display must increase.'],
  'A machine can look connected while the source face is configured as input. Diagnose from the battery outward.', image='power')

q('panel_power', 'Commission the controller', 0, 'cables', 'ballistix:launchercontrolpaneltier1',
  'The Control Panel stores launch energy and target information. It is the powered part of the three-piece silo. Charging it before adding ammunition lets you diagnose the electrical system without accidentally launching anything.',
  ['Place a T1 Control Panel on the test pad and connect FE. Open its interface and let the energy reserve build.',
   'Leave redstone disconnected while building. A held signal can request repeated launches as cooldowns finish and more ammunition becomes available.',
   'If charging fails, confirm cube output, cable connection and available source energy. Recheck that the cable touches the actual panel block.',
   'Do not add Electrodynamics just to follow an older guide: that would change the pack and its power behavior.'],
  'Use the interface energy reading as your checkpoint. A working panel now makes later launch failures much easier to narrow down.')

q('charge_tools', 'Charge the Radar Gun', 0, 'buffer', 'ballistix:radargun',
  'The Radar Gun stores a block position. It can transfer target coordinates to a controller and identify the Fire Control Radar for a turret link. Sampling a new position requires charge, so an empty tool can make otherwise correct clicks appear ineffective.',
  ['Use an FE item charger, such as the charge-item slot of a powered Mekanism Energy Cube. Confirm that the tool energy bar or tooltip increases before taking it out.',
   'Aim at a harmless marker block and use the gun to record it. Inspect the tooltip for the stored coordinates; an aiming readout alone is not proof that the position was saved.',
   'If a GUI opens instead of sampling a machine, sneak while using the gun. Keep your other hand empty while learning the interaction.',
   'Resampling another block replaces the saved position. Check it again before applying the gun to a launcher or turret.'],
  'A gun carrying an old coordinate is still charged and functional; it is simply pointing your setup at the wrong block.')

q('power_test', 'Project: keep the lights on', 0, 'panel_power charge_tools', 'mekanism:basic_energy_cube mekanism:basic_universal_cable',
  'A reserve that fills while idle can still collapse under load. This project establishes a repeatable electrical check you can reuse when adding radars and higher-draw weapons.',
  ['With the controller connected, confirm that it charges and that the upstream cube remains stable or recovers.',
   'Charge the Radar Gun, record a marker, and inspect the saved coordinates. This tests the separate item-charging path.',
   'After you build the radar and defense branches, repeat the observation while those machines operate. Watch the source reserve before, during and after a test shot.',
   'Confirm this project once the controller and tool checks work. The later defense project checks the complete battle load.'],
  'Upgrade a bottleneck cable or source before replacing every machine. Work through one connection at a time.', project=True)

q('silo', 'Three blocks, three jobs', 1, 'panel_power', 'ballistix:launcherplatformtier1 ballistix:launchersupportframetier1',
  'A silo separates storage, control and accuracy. The Launch Platform holds the missile and payload; the Control Panel supplies power and targeting; the Support Frame reduces impact scatter. The frame is optional mechanically, but useful when learning.',
  ['Make a straight row of three adjacent base positions on the same level: CONTROL PANEL — LAUNCH PLATFORM — SUPPORT FRAME. Leave the machine volumes and launch path above them clear.',
   'Put the panel display on the outside of the row, with the platform directly behind the panel and the frame beyond the platform. The frame sits opposite the controller. See the placement sketch.',
   'Power the panel, then open the platform to find the missile and explosive slots. If the controller does nothing despite power and correct ammunition, check the panel orientation and adjacency first.',
   'Do not expect a cable or an item pipe to substitute for the adjacent platform.'],
  'Place the platform first, then the two neighboring components. Keep the first build exposed until it has fired successfully.', image='silo')

q('payload', 'Missile plus warhead', 1, 'silo', 'ballistix:missiletier1 ballistix:condensive',
  'A normal missile supplies flight; the explosive block supplies the effect on impact. A missile without a payload is not a harmless practice rocket in this system: a normal offensive launch requires both items.',
  ['Craft one Tier 1 Missile and one Condensive Explosive. Insert them into the separate missile and explosive slots of the Launch Platform.',
   'Use only one of each for the first shot. Keep automated supply disconnected and do not feed a stack of expensive payloads into an untested launcher.',
   'The platform must support the missile and payload tier, and the missile must support the payload tier. Higher-tier equipment can carry lower-tier payloads.',
   'Condensive is the starter payload for this chapter, but it still damages blocks. Do not test on a factory wall, colony building, or player storage.'],
  'If an inventory refuses the item, check its name and tier in JEI. Surface-to-Air Missiles belong to a different defense workflow.')

q('coordinates', 'Aim at a disposable target', 1, 'payload', 'ballistix:radargun',
  'Coordinate mistakes and launch scatter are different problems. Correct target coordinates choose the intended area; the support frame controls how accurately a conventional silo reaches it.',
  ['Choose a clearly marked target in the same dimension, comfortably inside the T1 platform range of 500 blocks. Keep a wide empty area around it; range is checked using the target coordinates, including height.',
   'Read the marker coordinates and enter X and Z in the T1 controller. T2 adds a Y field; T3 also adds frequency control. You can record the marker with a charged Radar Gun and apply it to the controller instead.',
   'Double-check signs: X -200 is a different place from X 200. Reopen the panel to verify the stored target before firing.',
   'A T1 frame still allows scatter. Make the target area large and disposable, not a tiny block beside something valuable.'],
  'Record launch and target coordinates in a note. When testing a new tier, change one setting and keep the other conditions the same.')

q('first_shot', 'Project: first controlled launch', 1, 'coordinates power_test', '',
  'The first successful shot proves that power, adjacency, ammunition and targeting work together. It is a commissioning exercise, not an invitation to begin firing at your friend immediately.',
  ['Confirm everyone is clear of the test area. Verify one missile, one Condensive payload, charged controller and no continuous redstone signal.',
   'Use the controller launch control once. Observe the missile leave, then inspect the agreed target area after impact. If it fails, use the troubleshooting reference rather than replacing random components.',
   'Compare the impact with the intended coordinates. Some scatter is expected with a low-tier frame. Check that only one missile and one payload were consumed.',
   'Remove remaining ammunition and record what worked. Tick this project only after observing a completed launch; the quest book cannot detect that event automatically.'],
  'A button pulse is preferable to a lever while learning redstone launches. A lever left on can keep requesting shots after cooldown.', project=True)

q('precision', 'Upgrade accuracy before payload', 1, 'first_shot', 'ballistix:launchersupportframetier3 ballistix:launchercontrolpaneltier2',
  'Upgrading the frame is often more useful than increasing explosive size. A T3 Support Frame removes the configured frame scatter; a T2 Control Panel adds target height. Neither requires a destructive high-tier warhead.',
  ['Replace the frame with T3 while retaining your working platform and a Condensive payload. The components can be mixed across tiers.',
   'Compare a second shot on the same isolated range. T1 frames allow up to 30 blocks of scatter, T2 up to 15, and T3 adds none with the current defaults. Collisions and interception can still affect the flight.',
   'Fit the T2 controller when you need an explicit Y target. Re-enter the target and verify power after replacing a controller.',
   'Treat accuracy and payload radius separately: a perfectly aimed large blast is still a large blast.'],
  'Keep your initial payload unchanged while comparing frames. Otherwise you cannot tell whether the improvement came from aim or blast size.', optional=True)

q('range', 'Range, tier and frequency', 1, 'first_shot', 'ballistix:launcherplatformtier3 ballistix:launchercontrolpaneltier3 ballistix:missiletier3',
  'Platform tier limits the supported ammunition and range; controller tier adds targeting features. The actual permitted range is also limited by the missile. A T3 platform does not turn a T1 missile into a long-range missile.',
  ['Current platform defaults are 500 blocks for T1, 3,000 for T2 and 10,000 for T3. Inspect the missile you load as well as the platform.',
   'Use the T3 panel to assign a distinct launch frequency to your outpost. Record it so your own radars can ignore friendly missiles.',
   'A frequency is an identification value, not a password or a damage-protection setting. Agree different values with your friend before testing.',
   'Keep using a permitted conventional payload while learning the new tier. CustomATM restrictions remain in force on higher-tier platforms.'],
  'If a launch works nearby but not farther away, check the missile range and full target coordinates before blaming the power network.', optional=True)

q('vls', 'Optional: a compact VLS', 1, 'first_shot', 'ballistix:vls',
  'The Vertical Launch Silo packages a short-range launch station into one machine. It is useful for a temporary firing position or an alternate approach angle, without rebuilding the three-piece main silo.',
  ['Place the VLS on an open test pad. Feed FE from any side and load a T1 missile with a T1 conventional payload.',
   'Its default range is 500 blocks, but its targeting interface offers the advanced coordinate and frequency controls. Set and verify the target before issuing a single launch.',
   'Keep its trajectory clear. Do not hide it under your base roof and assume a missile can pass through construction.',
   'After the test, disconnect launch signals before moving or restocking it. Recheck coordinates at the new location.'],
  'The VLS is convenient, not a replacement for long-range platform progression. Use one missile and payload while commissioning each new site.', optional=True)

q('search', 'Search Radar: the early warning layer', 2, 'cables', 'ballistix:radar',
  'Search Radar answers whether a threat is nearby. It detects missiles and ESM towers and can raise an alarm. It does not supply the turret targeting link provided by a Fire Control Radar.',
  ['Place it above ground with access to sky light, and feed FE into its bottom base block. Keep the radar structure clear when building around it.',
   'Open the interface and confirm power. Its configured search range is 600 blocks in this pack.',
   'Bring the alarm wire to an accessible test point. The normal redstone output becomes active when it detects missiles or an ESM tower.',
   'For the first drill, leave friendly-frequency filtering disabled so you can observe a known test missile. Restore your intended filters afterward.'],
  'Do not bury the radar in a sealed bunker. Power alone is not enough when the machine has no sky light.', image='defense')

q('alarm', 'Wire a useful air-raid alarm', 2, 'search', 'ballistix:airraidsiren minecraft:redstone*8 minecraft:repeater',
  'An audible warning gives you time to check ammunition and power. The Air Raid Siren needs a redstone signal, not an FE cable. A simple alarm is easier to commission than an automatic retaliation circuit.',
  ['Run ordinary redstone from Search Radar to the siren; use a repeater where the signal route needs extending or isolating. Set a comfortable pitch, volume and radius in the siren interface.',
   'Test the siren temporarily with a lever, then remove that temporary input and test from the radar during a missile drill.',
   'Use normal redstone output for a basic missile alarm. The comparator output is different: 0 for missiles alone, 8 for ESM alone, and 15 when both are detected.',
   'Keep this circuit separate from offensive launch triggers while learning. An alarm should not unexpectedly fire a stocked silo.'],
  'A comparator reading zero does not prove that the Search Radar sees no missile. This distinction is a common cause of silent alarms.')

q('firecontrol', 'Fire Control Radar: guide the defenses', 2, 'search', 'ballistix:firecontrolradar',
  'Fire Control Radar supplies missile targets to linked turrets. Search Radar and Fire Control Radar have complementary roles: early warning and weapon guidance. One cannot be substituted for the other.',
  ['Place the Fire Control Radar above ground with sky light. Supply FE from underneath its base and leave enough nearby space for defense platforms.',
   'The current configured radar range is 550 blocks. Turrets must be within 32 blocks of the radar to bind; place them comfortably inside that distance.',
   'For commissioning, keep the radar enabled continuously. If you enable redstone control, it also needs the appropriate active signal.',
   'Current Ballistix has threat assignments for linked defenses. Older descriptions saying every turret must always target the same single missile do not describe the complete current implementation.'],
  'Start with an always-on radar. Add Search Radar-controlled switching only after a basic interception works.', image='defense')

q('link', 'Bind a turret with the Radar Gun', 2, 'firecontrol charge_tools', 'ballistix:radargun',
  'A turret can have power and ammunition yet remain unable to engage missiles because it has no valid radar link. The Radar Gun transfers the radar block position; an energy cable does not make that link.',
  ['Charge the gun. Sneak-use it while aiming at the Fire Control Radar base to record that block, avoiding opening the machine GUI. Check the saved position in the gun tooltip.',
   'With that position still saved, sneak-use the gun on the turret base. Look for the Bound response and inspect the turret radar field.',
   'Stay within 32 blocks of the radar; use a short distance such as 8 to 16 blocks for the first setup. If too far away, reposition and bind again.',
   'If the gun sampled the wrong block, repeat from the radar. A stored Search Radar coordinate will not provide Fire Control guidance.'],
  'Bind each turret individually. After moving a radar, rebind the affected turrets rather than assuming their stored coordinates follow it.')

q('frequencies', 'Teach radar which missiles are friendly', 2, 'link', '',
  'Friendly-frequency filtering prevents your defenses from deliberately tracking your own identified missiles. It does not change explosive damage and does not make other players or colony citizens safe from entity-targeting turrets.',
  ['With a frequency-capable launcher, choose a distinct value and note it. In each radar Frequency Manager, add that value and enable Whitelist Mode.',
   'Configure Search Radar and Fire Control Radar separately. Saving a frequency while whitelist mode is disabled does not activate the filter.',
   'During a controlled test, compare a friendly filtered launch with a different unfiltered frequency. Confirm the warning and targeting behavior you intended.',
   'If you are still using the basic T1 controller, complete the first interception drill without filters. Return here after upgrading rather than assuming the basic panel has a frequency field.'],
  'If nothing detects your test missile, temporarily remove filtering as a diagnostic. Restore it once the reason is understood.', optional=True)

q('radar_drill', 'Project: detect before defending', 2, 'alarm firecontrol first_shot', '',
  'Separate a detection failure from a weapon failure. A controlled radar drill proves the signal path before you depend on an interceptor to save the outpost.',
  ['Have your friend launch one agreed conventional test missile toward a disposable marker near the defended outpost, or arrange an isolated local test. Keep it outside friendly-frequency exclusions.',
   'Watch the Search Radar and listen for the siren. Watch the Fire Control Radar acquire the incoming missile while it is in coverage.',
   'If the siren stays quiet, test its redstone route independently. If a radar is silent, check bottom power, sky light, redstone mode and frequency filtering.',
   'Confirm the project after observing detection and an alarm. This manual checkmark is not an automatic missile-tracking achievement.'],
  'Place the marker where a failed interception would be acceptable. Radar coverage is not itself protection against blast damage.', project=True)

q('sam', 'SAM: intercept at a distance', 3, 'link', 'ballistix:samturret ballistix:aamissile*4',
  'The SAM Turret is the outer missile-defense layer. It fires Surface-to-Air Missiles and needs a working Fire Control Radar. It does not shoot players, and its minimum engagement distance leaves a gap close to the outpost.',
  ['Place the turret outdoors, power its bottom and bind it to Fire Control Radar with the Radar Gun. Put Surface-to-Air Missiles in its ammo slot.',
   'Use ballistix:aamissile ammunition here. The Anti-Ballistic Missile is a different item for the dedicated silo workflow, not this turret slot.',
   'Current defaults give a 100-block minimum and a 300-block base maximum engagement range, with an 80-tick firing cooldown. A hit is not guaranteed to destroy the incoming missile.',
   'Inspect the status before testing: No Power, No Ammo, Unlinked and Out of Range point to different fixes. Add close-in coverage next.'],
  'A missile inside the SAM minimum range can be visible to radar while the turret correctly refuses to fire. That is why you need another defense layer.')

q('ciws', 'CIWS: cover the inner gap', 3, 'sam', 'ballistix:ciwsturret ballistix:bullet*64',
  'CIWS fires a stream of bullets at close threats. It complements SAM coverage, but spends ammunition quickly and needs a clear firing path. Its base missile engagement range is 100 blocks with current defaults.',
  ['Place a CIWS turret on a clear outdoor mount, feed bottom power and bind it to your Fire Control Radar. Load Ballistix Bullets.',
   'Keep walls and other machines out of the barrel path. Do not assume a turret under a decorative roof will retain useful coverage or sky light.',
   'Set entity targeting to None while commissioning missile defense. This prevents the entity-targeting mode from turning your test site into an unintended player or colony trap.',
   'Observe ammo before and after one incoming missile. Keep a reserve nearby before connecting automated supply.'],
  'One stack of bullets is a test supply, not a complete defense budget. A dry CIWS looks operational until a real target arrives.')

q('laser', 'Optional: trade ammunition for power', 3, 'sam', 'ballistix:laserturret',
  'The Laser Turret removes the bullet supply requirement but replaces it with a larger power demand and heat management. It is an alternative inner layer, not a free upgrade to an unlimited defense.',
  ['Mount it outside, supply bottom power and bind it to Fire Control Radar. Keep entity targeting set to None for missile-only testing.',
   'The laser needs no ammo stack. Watch its temperature and the upstream Energy Cube while it engages a test target.',
   'If Overheated appears, allow cooling. If No Power appears, inspect generation and cable throughput; a heat problem and an electrical problem need different remedies.',
   'Leave a clear sightline and supplement it with another defense type rather than relying on continuous fire from one turret.'],
  'Measure the reserve during firing. A battery that stays full with an idle laser may still drain rapidly when it shoots.', optional=True)

q('railgun', 'Optional: iron-fed heavy defense', 3, 'sam', 'ballistix:railgunturret minecraft:iron_ingot*16',
  'The Railgun Turret fires powerful projectiles with a cooldown between shots. In CustomATM without Electrodynamics, its ammunition is ordinary iron ingots. Advice requiring Electrodynamics steel rods does not apply to this configuration.',
  ['Power the bottom, bind the turret to Fire Control Radar and place iron ingots in its ammo slot. Keep entity targeting at None during missile tests.',
   'Give it an unobstructed firing path and watch both ammo consumption and power. It is a higher-draw option than SAM or CIWS.',
   'The configured cooldown is 100 ticks between shots. Keep another layer available while it reloads or waits for the next firing opportunity.',
   'Do not feed expensive modded rods at random if the slot rejects them: the current no-Electrodynamics branch explicitly accepts minecraft:iron_ingot.'],
  'This is a useful alternate defense when your factory has spare iron and power, but it still needs a functioning radar link.', optional=True)

q('target_modes', 'Keep allies and colonists out of the crossfire', 3, 'ciws', '',
  'Missile guidance and entity targeting are separate controls. CIWS, laser and railgun can engage living targets as well as incoming missiles; SAM is dedicated to missiles. A player whitelist does not automatically classify a MineColonies citizen as an ally.',
  ['Use Targeting Mode None for a missile-defense-only outpost. Current Ballistix also offers Hostile Mobs, which is useful for a separate anti-mob test.',
   'If you deliberately enable player combat, inspect the player whitelist and add the intended allies. Verify behavior at a disposable test station before placing it near a settlement.',
   'Do not use an all-living-target mode beside colonists, pets or villagers and assume faction integration. This chapter does not install MineColonies allegiance support.',
   'For ATM10 player duels, agree an equipment limit separately. These quests do not rebalance MekaSuit or other endgame protection.'],
  'For the first two-player missile match, leave entity targeting off. Let the outpost equipment be the objective instead of trying to defeat endgame armor.')

q('intercept', 'Project: stop an incoming missile', 3, 'target_modes radar_drill', 'ballistix:samturret ballistix:ciwsturret',
  'Layering gives the outpost more than one opportunity to respond. An outer SAM and inner CIWS have different ranges and failure modes, so one missed shot or empty inventory does not immediately end the defense.',
  ['Prepare a powered, linked and stocked SAM plus CIWS. Confirm the radar is active, the siren works and the test frequency is not ignored.',
   'Arrange one conventional incoming missile toward a disposable marker. Observe the radar, turret status, ammunition and battery reserve throughout the attempt.',
   'If it survives, identify the failed stage: detection, link, range, power, ammunition or firing path. Change that part and retry under the same conditions.',
   'Confirm only after observing a successful interception and checking that the reserve remains usable. A successful trial is not a guarantee against every trajectory or volley.'],
  'Add redundancy after the single-target drill works. More turrets cannot fix a shared unpowered radar or the wrong frequency filter.', project=True, image='defense')

q('antiballistic', 'Optional: a dedicated interceptor silo', 4, 'intercept', 'ballistix:aamissilemk2 ballistix:launchercontrolpaneltier2',
  'The Anti-Ballistic Missile uses a silo-based interception path. It is distinct from the smaller Surface-to-Air Missile loaded into the SAM turret. This is an optional extension once the ordinary turret defense works.',
  ['Prepare a dedicated silo near the Fire Control Radar, comfortably less than 32 blocks away. Use a controller with XYZ entry so you can enter the radar base position exactly.',
   'Load the Anti-Ballistic Missile into the platform missile slot and leave the explosive slot empty. This defensive missile must not be paired with a conventional warhead.',
   'Set the controller target to the Fire Control Radar base coordinates, then provide the redstone launch signal. The special interception path requires redstone and an actively tracked missile beyond its close-range exclusion.',
   'Test with one interceptor loaded. Keep this station separate from your offensive silo so a leftover target or explosive cannot confuse the setup.'],
  'The coordinate fields point at your radar for this workflow, not at the incoming missile or the enemy base.', optional=True)

q('esm', 'Optional: understand radar emissions', 4, 'intercept', 'ballistix:esmtower',
  'An ESM Tower is an electronic reconnaissance tool. It can reveal nearby active Fire Control Radar positions and indicate Search Radar activity. Running defense electronics can therefore make an outpost easier to locate.',
  ['Place the ESM Tower outdoors with sky light and feed FE into the bottom of its base. Its current configured search radius is 200 blocks.',
   'With your friend, test against a known nearby radar and compare the displayed information for Search Radar and Fire Control Radar.',
   'Consider switching Fire Control Radar on from an early-warning circuit only after proving that the circuit responds reliably. An unpowered guidance radar cannot support the defense merely because a turret still has energy.',
   'This is reconnaissance, not a reason to enable automatic counterfire near your factories. Keep retaliation manual during the first matches.'],
  'An always-on radar is simpler and more reliable while learning. Emission control introduces another failure point to test.', optional=True)

q('designator', 'Optional: launch from the field', 4, 'first_shot', 'ballistix:laserdesignator',
  'The Laser Designator selects a target and requests a launch remotely. Unlike the Radar Gun, it is a firing tool. Treat a linked, charged designator as an armed control whenever its launcher has ammunition.',
  ['Charge the designator in an FE item charger. Prepare a working frequency-capable silo or VLS, then use the designator on it to synchronize its frequency; the advanced controller Sync slot is another linking route.',
   'Verify the selected launcher and load only one missile with a permitted conventional payload. Move to a disposable target and remain within the current 1,000-block designator range of the launcher.',
   'Use the designator on the intended target to pass coordinates and request the shot. The target must still be within the loaded missile and platform range.',
   'Unload the launcher before carrying the linked tool around valuable structures. Entered target coordinates persist after firing.'],
  'Use a Radar Gun when you only want to copy coordinates. Do not substitute the designator during a harmless targeting demonstration.', optional=True)

q('resupply', 'Optional: automate the stockroom', 4, 'intercept', 'minecraft:chest minecraft:hopper*2',
  'Once a defense works manually, item transport can keep it stocked. Automation should preserve the distinction between defensive ammunition and offensive payloads rather than filling every machine with everything.',
  ['Use separate labeled containers for SAM missiles, CIWS bullets and railgun iron. Start with one hopper route and inspect which inventory slot receives the item.',
   'The launch platform and turret ammo inventories expose item input; use the pack transport system you already understand and filter each route to the correct ammunition.',
   'Keep offensive missile/payload supply disconnected until the match is armed. A held redstone trigger plus automatic resupply can keep launching after the first shot.',
   'Test restocking with a small batch, then compare stock levels after a controlled drill. Add a visible low-ammo reminder rather than assuming an exporter can never run dry.'],
  'A transport system cannot compensate for using Anti-Ballistic Missiles in a SAM turret. Check the exact accepted item before adding filters.', optional=True)

q('diagnostics', 'Troubleshooting: follow the failed stage', 4, 'start', '',
  'Most commissioning problems can be narrowed down without dismantling the entire outpost. Follow the chain in order and compare one observation at a time.',
  ['No Power: verify source reserve and output side, then cable, then machine input. Radar and turrets require bottom input; a silo needs power at its controller.',
   'No launch: check platform adjacency behind the panel, one supported missile and payload, target range, energy and cooldown. A normal missile needs an explosive; an anti-ballistic setup needs an empty explosive slot.',
   'Unlinked or no radar target: re-sample the Fire Control Radar base, bind within 32 blocks, and check sky light, redstone control and frequency filtering.',
   'No Ammo / Out of Range / Overheated: use the correct ammo, remember the SAM 100-block inner gap, and let a laser cool. Do not confuse these states.',
   'Alarm missing: test the siren with redstone directly. For a simple missile alarm use Search Radar normal output, not its special comparator code.'],
  'For a reproducible problem, record the machine names, coordinates, ammo, displayed status and battery behavior before changing anything.', optional=True)

q('match_rules', 'Optional: a two-player outpost match', 4, 'intercept', '',
  'A small agreed objective keeps the competition fun in a pack with extreme resource generation. Expensive recipes alone do not limit a mature ATM10 factory, and this chapter does not install automated match enforcement.',
  ['Pick two disposable military outposts and a visible objective in each. Keep main factories, storage networks and colonies outside the agreed battlefield.',
   'Agree a limited missile allowance, permitted payloads and a start/stop signal. Begin with one incoming missile at a time; increase the challenge only after both defenses work.',
   'Avoid terrain-resetting Rejuvination and other large-area payloads for these matches even if an item is available. The pack restriction list is not a complete protection system.',
   'At ceasefire, remove launch signals and unload offensive magazines. Agree how to repair damage and count a win before the first attack.'],
  'A good first objective is disabling the outpost alarm or power supply. This makes logistics and repairs matter without requiring a kill through endgame armor.', optional=True)

q('graduation', 'Project: a working missile outpost', 5, 'first_shot radar_drill intercept', '',
  'Your outpost is ready for a controlled match when each subsystem works and you can explain how to recover from a failure. Completing the quest means you performed the checks; it does not certify that every modded shield or claim system blocks explosions.',
  ['Demonstrate one controlled conventional launch with a checked target and a deliberate single-shot trigger.',
   'Demonstrate Search Radar detection and an audible alarm, plus a working Fire Control Radar link to the defensive turrets.',
   'Demonstrate an interception with stock remaining and a power reserve that can recover. Identify how you would fix a broken cable or empty magazine.',
   'Unload offensive launchers after the test and agree the battle area with your friend. Confirm this final project only when all three drills have been performed.'],
  'Keep the exposed prototype as a reference until the decorated outpost passes the same checks. Hiding wiring should not hide the only way to diagnose it.', project=True, image='overview')
