"""Original expanded guides and branch plans. Indexes refer to content.py.

Keep legacy indexes stable. New quests use stable slugs for their IDs.
Amounts below are workshop demonstration targets, not invented recipe ratios.
"""
LANES = {
 'minecolonies': [('FOUNDATIONS',[2,3,4,5,6,16]),('PEOPLE & FOOD',[8,7,12,18,17]),('SUPPLY & RESEARCH',[9,10,11,15,13,14]),('COLONY PROJECTS',[19,20])],
 'ad_astra': [('ROCKET WORKSHOP',[2,3,4,5,7,8]),('FIRST EXPEDITION',[6,9,10,11,12,13]),('PLANETARY PROGRESSION',[16,18,19,20]),('LIFE SUPPORT & BASES',[14,15,17,21,22])],
 'advanced_rs': [('AUTOCRAFTING',[2,4,5,6,7,8,9,21]),('RESOURCE NETWORKS',[3,10,11,12,13,14]),('WIRELESS & BUILDING',[15,16,17,18,19,20])],
 'economy': [('FIRST TRANSACTIONS',[2,3,4,5,6,7]),('FACTORY EXPORTS',[8,9,10,11,12,17]),('OPTIONAL CASINO',[13,14,15,16])],
 'enderio': [('ALLOY WORKSHOP',[2,3,4,5,6,7,12]),('CONDUIT SYSTEMS',[8,9,10,11,13,20]),('SOULS & SPAWNERS',[14,15,16,17]),('FARMING & UTILITIES',[18,19])],
 'astral': [('DISCOVERY',[2,3,4,5,6,7,8,9]),('CRAFTING & INFUSION',[10,11,12,13,14,15]),('ATTUNEMENT & LIGHT',[16,17,20]),('LUMEN & MASTERY',[18,19,21,22,23,24])],
 'sfm': [('FIRST PROGRAM',[2,3,4,5,12]),('ITEM PROCESSING',[6,7,8,9,10,11,13]),('RESOURCE CHANNELS',[14,15,16]),('FACTORY PROJECTS',[17,18])],
 'xnet': [('FIRST CHANNEL',[2,3,4,5]),('PROCESSING & STOCK',[6,7,8,12]),('FLUIDS, POWER & CONTROL',[9,10,11]),('ROUTING & PROJECTS',[13,14,15,16,17])],
 'computercraft': [('THE TERMINAL',[2,3,4,8,9,10,18]),('PERIPHERAL NETWORK',[5,6,7,14,15,16]),('TURTLE WORKSHOP',[11,12,13]),('DASHBOARDS',[17,19])],
 'rftools': [('STORAGE TOOLS',[2,3,4,5,6]),('BUILDER & CARDS',[7,8,9,10,11,12,13]),('WORKSHOP UTILITIES',[14,15,16,19]),('TRAVEL & PROJECTS',[17,18,20,21])],
}
# Entry prerequisites replace lane defaults. Branches are independent where possible.
DEPS = {
 'minecolonies': {8:[4],9:[5],10:[5],15:[10,11],13:[15,9],14:[15],19:[5],20:[11,13,14],16:[5]},
 'ad_astra': {6:[3],9:[4],10:[3],11:[8,9,10,6],12:[11],13:[12],16:[13],18:[16],19:[16,18],14:[13],22:[14,16]},
 'advanced_rs': {3:[2],10:[4],11:[2],12:[2],13:[2],14:[2],15:[2],17:[2],18:[2],19:[2],20:[2],21:[6,8]},
 'economy': {8:[2,6],11:[2],12:[7,9,10],13:[3],17:[12]},
 'enderio': {8:[4],14:[5],15:[14,4],18:[5],19:[4],20:[13]},
 'astral': {10:[9],13:[9,10,12],14:[13],15:[13,14],16:[15],18:[15],20:[17],21:[18,19],22:[15,20,21]},
 'sfm': {6:[4],12:[2],14:[4],15:[4],16:[4],17:[4],18:[10,12]},
 'xnet': {6:[4],9:[4],10:[4],11:[4],13:[4],14:[13],16:[4],17:[7,10]},
 'computercraft': {5:[2],6:[4],7:[6],11:[2],14:[6],15:[6],16:[6],17:[9,7],19:[5,7,17]},
 'rftools': {7:[0],14:[0],16:[0],17:[0],19:[7],20:[7],21:[9,14]},
}

# Real item evidence replaces reading-only goals where it can verify useful work.
ITEMS = {
 'minecolonies': {2:['structurize:sceptergold'],16:['minecolonies:clipboard'],20:['minecraft:oak_stairs*32','minecraft:stone_bricks*32']},
 'ad_astra': {9:['ad_astra:space_helmet','ad_astra:space_suit','ad_astra:space_pants','ad_astra:space_boots'],11:['ad_astra:launch_pad','minecraft:cooked_beef*16'],12:['ad_astra:moon_cobblestone*16'],18:['ad_astra:netherite_space_helmet','ad_astra:netherite_space_suit','ad_astra:netherite_space_pants','ad_astra:netherite_space_boots'],21:['ad_astra:oxygen_distributor'],22:['ad_astra:ostrum_ingot*16']},
 'advanced_rs': {2:['refinedstorage:controller','refinedstorage:disk_drive','refinedstorage:1k_storage_disk','refinedstorage:crafting_grid'],5:['refinedstorage:pattern*4'],6:['refinedstorage:autocrafter','refinedstorage:importer'],9:['refinedstorage:speed_upgrade*2'],10:['refinedstorage:64b_fluid_storage_disk'],15:['universalgrid:wireless_universal_grid','refinedstorage:wireless_transmitter'],19:['create:schematicannon'],20:['refinedstorage:detector'],21:['refinedstorage:basic_processor*16']},
 'economy': {4:['minecraft:cobblestone*64'],5:['minecraft:iron_ingot'],6:['minecraft:oak_log*16'],9:['minecraft:chest*2'],10:['minecraft:iron_ingot*16'],12:['dyneco:market_tablet','minecraft:chest*2']},
 'enderio': {2:['enderio:conduit_binder*8'],5:['enderio:energetic_alloy_ingot*4','enderio:conductive_alloy_ingot*4'],7:['enderio:yeta_wrench'],9:['enderio:basic_item_filter'],11:['enderio:fluid_tank'],12:['enderio:double_layer_capacitor'],13:['enderio:energetic_alloy_ingot*16'],19:['enderio:enchanter'],20:['enderio:vibrant_alloy_ingot*16']},
 'astral': {3:['astralsorcery:aquamarine*8','astralsorcery:marble_raw*32'],6:['astralsorcery:astrolabe'],11:['astralsorcery:starmetal_ingot','astralsorcery:stardust'],12:['astralsorcery:focus_relay*4'],17:['astralsorcery:attuned_rock_crystal'],20:['astralsorcery:starlight_focus_rock_crystal','astralsorcery:linking_tool'],23:['astralsorcery:iridescent_crystal_pickaxe'],24:['astralsorcery:lumen_crystal']},
 'sfm': {2:['sfm:manager','sfm:cable*8'],3:['sfm:labelgun','minecraft:chest*2'],6:['minecraft:iron_ingot*8'],7:['minecraft:cobblestone*64'],8:['minecraft:chest*4'],9:['minecraft:furnace'],10:['minecraft:iron_ingot*16'],11:['minecraft:furnace*3'],13:['minecraft:oak_log*8','minecraft:birch_log*8'],14:['sfm:water_tank'],15:['sfm:cable*8'],16:['minecraft:lever'],18:['minecraft:iron_ingot*32']},
 'xnet': {3:['xnet:connector_blue*2','xnet:netcable_blue*8'],4:['minecraft:chest*2'],5:['minecraft:iron_ingot*8'],6:['minecraft:furnace'],7:['minecraft:iron_ingot*16'],8:['minecraft:chest*2'],9:['rftoolsutility:tank*2'],10:['xnet:connector_blue*2'],11:['minecraft:lever'],12:['xnet:advanced_connector_blue'],13:['xnet:netcable_red*8','xnet:connector_red*2'],17:['minecraft:iron_ingot*32']},
 'computercraft': {5:['computercraft:monitor_advanced*4'],6:['computercraft:cable*8','computercraft:wired_modem*2'],7:['minecraft:chest'],10:['computercraft:disk','computercraft:disk_drive'],12:['minecraft:stone*8'],13:['minecraft:coal*4'],17:['computercraft:computer_advanced'],19:['computercraft:monitor_advanced*4']},
 'rftools': {3:['rftoolsstorage:modular_storage','rftoolsstorage:storage_module0'],5:['minecraft:chest*2'],6:['rftoolsstorage:storage_control_module'],8:['rftoolsbuilder:shape_card_def'],9:['minecraft:stone_bricks*64'],10:['rftoolsbuilder:shape_card_quarry'],11:['minecraft:cobblestone*16'],12:['rftoolsbuilder:shape_card_pump'],15:['minecraft:oak_planks*16','minecraft:stick*16'],16:['rftoolsutility:screen_controller','rftoolsutility:screen'],17:['rftoolsutility:matter_transmitter','rftoolsutility:matter_receiver','rftoolsutility:dialing_device'],18:['rftoolsutility:charged_porter'],19:['rftoolsbase:dimensionalshard'],21:['minecraft:stone_bricks*64']},
}

DETAILS = {}
def detail(slug, index, *paragraphs): DETAILS[(slug,index)]=list(paragraphs)

detail('minecolonies',5,
 'WORK ORDER: Open the hut block, choose Build Options and request Build Building. A citizen must be assigned as the builder. The hut block alone is not a finished workplace: the citizen still has to place its schematic.',
 'FIRST JOB: Keep only one construction request active while learning. Put requested blocks in the builder inventory and provide the requested tool. When an item appears supplied but work is stopped, inspect the citizen interaction window for food, tool or path messages.',
 'UPGRADE RULE: A builder cannot construct arbitrary higher-level buildings. Improve the Builder\'s Hut when its level becomes the bottleneck. Preview the upgraded building footprint before building a road through it.')
detail('minecolonies',11,
 'REQUEST TRACE: Builder asks for oak stairs -> Warehouse checks stock -> a trained Sawmill can craft missing stairs -> Courier moves inputs and the finished product. If the Sawmill does not know the recipe, adding more logs to storage will not solve the request.',
 'TEST: Stock 32 oak logs, teach the actual stair recipe used by your style, then queue a job that needs those stairs. Watch one delivery arrive. This is the point where your colony begins supplying construction rather than waiting for you at every step.')
detail('minecolonies',15,
 'PRIORITY: Open the research tree and select the unlock needed by your next production building. Read each node\'s building and material prerequisites before making its hut block. Research, a staffed finished hut and a taught recipe are three separate requirements.',
 'PLAN: Wood supply and food keep the settlement running; research should remove the next recurring shortage. A Sawmill saves repeated plank/stair crafting, while a Stonemason supports a stone-heavy style.')
detail('ad_astra',8,
 'PAD SETUP: Make a 3 by 3 square of Launch Pads and place the Tier 1 Rocket on it. Open the rocket interface and load supported fuel. A rocket in your inventory proves you built it; it does not prove the fuel tank or your suit is ready.',
 'RETURN KIT: Carry a separate set of nine Launch Pads and enough supported fuel for another launch, plus food and charged oxygen equipment. The Moon trip below waits for the preflight branch so rocket construction cannot skip life-support preparation.')
detail('ad_astra',10,
 'LOADER LOOP: Feed power and water to the Oxygen Loader, then insert the compatible suit/tank in its charging slot. Look for the oxygen amount to rise. Water in a pipe beside the machine is not evidence that water entered its tank.',
 'CHECK BOTH RESOURCES: A stalled oxygen fill can mean no FE, no water, or an incompatible item. Verify those three bars/slots before changing your whole workshop. Keep a refill station at your Overworld landing pad.')
detail('ad_astra',14,
 'SMALL ROOM FIRST: Use a fully enclosed room with solid walls, floor and roof. Supply water and FE to the distributor and check its status with your helmet still on. Start with a small volume so a leak is easy to locate.',
 'AIRLOCK HABIT: Opening a wall directly to the outside can invalidate the room. Use an airlock or an entry arrangement appropriate to the distributor\'s rules. Test oxygen with the TI-69 instead of assuming a sealed-looking decorative block counts.')
detail('advanced_rs',6,
 'WORKED EXAMPLE: Encode a processing pattern that consumes one raw basic processor and produces one basic processor. Aim the Autocrafter at the input of a furnace that accepts it. Return the furnace output through an Importer or another tested insertion path into this same network.',
 'REQUEST ONE: With raw materials in storage, request one basic processor from the Grid. Watch the raw processor leave, the furnace finish, and the finished processor return. The Autocrafting Monitor should then clear the job.',
 'WAITING FOREVER? If ingredients arrived, inspect the exact output promised by the pattern. RS cannot finish a recipe that promised two items but returns one, or whose output was sent to an unrelated chest.')
detail('advanced_rs',3,
 'DRAWER PATTERN: Connect External Storage to the drawer controller, lock the intended drawer types, and give that storage a higher insertion priority than the disk store. New cobble should go to its drawer instead of filling your general-purpose disk.',
 'TEST THE FALLBACK: Insert one stack and inspect the physical drawer. Temporarily fill the target and check where further inserts go. An attached empty drawer can accept an unintended item unless its type is locked.')
detail('advanced_rs',11,
 'TWO POWER ROLES: Energy disks hold FE as a network resource. The Network Energizer lets the storage network use that stored FE for its own operating demand. A charged disk alone is not the same thing as an installed, active Energizer.',
 'USE THE ADDON: Bootstrap the network with ordinary external power and fill an energy disk through a compatible input. Add the Network Energizer, inspect its redstone mode, and confirm stored FE can sustain the network. Retain external power as a fallback while testing.')
detail('advanced_rs',8,
 'SMALL STOCK TARGET: First make a successful manual craft of your basic processor pattern. Then ask Requestify to keep a target such as 16 in stock. Remove four, watch one replenishment job, and confirm the count settles back at the target.',
 'AVOID A LOOP: Do not export the entire target into a machine that returns it under the same rule. The requester sees the shortage and can schedule endless work. Choose a buffer and target you can explain.')
detail('economy',7,
 'DEMAND IS SHARED: /marketlimits shows your remaining total and category allowances. Recovery is $10,000 per online hour overall; bulk $500, farming $1,500, resources $4,000 and manufactured goods $10,000, all inside that shared total. Extra chests do not create extra buyers.',
 'PRICE EXAMPLE: Neutral cobblestone base value is $0.01 and a diamond pickaxe is about $352.02. A normal spread makes the pickaxe roughly $457.63 to buy and $246.42 to sell before demand changes. The market rounds a batch, not every fractional-cent unit.',
 'EXPENSIVE GOODS: Per-item/bucket buyback ceilings are $250 bulk, $750 farming, $2,000 resources and $5,000 manufactured. High compression keeps retail value but does not guarantee a good resale deal. Check the displayed sell quote.')
detail('economy',9,
 'TWO BUFFERS: Production fills your personal reserve first; only surplus enters the trade chest. Choose one resource and record wallet plus chest quantity, wait for a completed sale, then compare both. A listing is not income until it settles.',
 'AFTER THE LIMIT: Remaining goods should wait. Allowance refills only while online and persists across reconnects. Saved demand supports a later burst, so a single large sale is different from a sustainable hourly income.')
detail('economy',13,
 'OPENING: The CustomATM default casino key is F8. If you changed it, search Open Casino under Casino Mod in Controls. The casino uses the same server-side DynEco wallet; you do not need to buy or deposit a separate token.',
 'OPTIONAL BRANCH: These quests do not require wins, repeated bets or a particular balance. Use a small amount you already intend to spend for entertainment. Closing the interface is a valid end to the session.')
detail('enderio',8,
 'TWO CHESTS FIRST: Put a conduit connection on each chest. Configure the source connection for extraction and the destination for insertion on the same item-channel color. Enable extraction without a redstone signal for this first test, then transfer a few cobble.',
 'SHARED SPACE: Different conduit types can occupy one block space. Their settings are still independent: an item route does not power the machine. Add energy after the item route works, then verify both tabs.',
 'VERSION NOTE: This Ender IO version stores the conduit type as item data. The quest uses the actual Item Conduit variant rather than an empty generic conduit that has no useful type.')
detail('enderio',4,
 'PROVE THE RECIPE: Install the capacitor required by the machine, supply FE, select an appropriate alloy/smelting mode and run one JEI recipe by hand. Keep an output slot free. Automation should reproduce this known working setup.',
 'SIDES: Use the machine\'s side configuration/Yeta Wrench and conduit connection settings together. The machine must expose the intended inventory on the face being used; a conduit set to insert cannot override a disabled machine input.')
detail('enderio',16,
 'SPAWNER CHAIN: Capture the intended mob in a Soul Vial, inspect the Soul Binder recipe for changing a broken spawner, supply its FE/XP requirements, then follow the installed recipe for the Powered Spawner. A plain empty Soul Vial is only a tool, not a configured mob source.',
 'BEFORE ENABLE: Build an enclosure with a collection method, a stop signal and enough output storage. Start at low throughput. A faster capacitor can raise the power demand beyond what the same supply handled at the previous tier.')
detail('astral',13,
 'THREE CHECKS: First read the altar tier required by the recipe. Next verify its exact marble and relay structure with the Wand preview. Finally check time/sky and the item placements. More relays do not compensate for the wrong altar tier.',
 'THIS PORT: The installed 2.x sequence is Illuminated -> Resonating -> Luminous -> Iridescent. The names, focal points and lumen system differ from many older videos; use the installed Tome for the actual structure drawing.')
detail('astral',19,
 'KEEP SYSTEMS DISTINCT: Liquid Starlight is a stored fluid. Lumen uses arrays and filaments. Focused starlight uses an attuned focus and Linking Tool under a matching constellation. A pipe carrying the first cannot replace either of the other two.',
 'ONE CONSUMER TEST: Label the producer with its type, connect the shortest valid link and watch a single consumer. Extend only after consumption is visible. A network with many unverified links is much harder to diagnose.')
detail('astral',22,
 'PREPARE FOUR INVENTORIES: Item ingredients, Liquid Starlight, the required lumen aspects and the correctly attuned focus/starlight supply. Read whether the focus is consumed before dedicating your best crystal.',
 'CHECKPOINT: Complete the Wand structure preview before waiting for the correct night. Then observe one ingredient transfer or consumption event at a time. If the ritual stops, identify which resource stopped changing rather than rebuilding the entire altar.')
detail('sfm',4,
 'WIRING: Connect the Manager and both chests to the same Inventory Cable network. With the Label Gun, give the source the exact label input and the destination output. Labels belong to blocks; naming a chest with an anvil is not the same operation.',
 'PROGRAM FLOW: INPUT chooses resources from matching labeled inventories. OUTPUT chooses their destination. Save the disk in the Manager and check compilation before expecting movement. Stop the program, change one label, and observe the error/no-transfer symptom so you can recognize it later.')
detail('sfm',7,
 'RESERVE IS A LOCATION: Decide whether you want to retain stock in the source or maintain a target in the destination. Those are different rules. A factory that needs 64 cobble for itself must not export all 64 just because a trade chest can accept them.',
 'EXERCISE: Begin with 80 cobble in the source and an empty destination. Use a 64-item source retention rule, run it, and check that 16 moved while 64 remained. Then add 10 and verify only those 10 become surplus.')
detail('sfm',10,
 'VANILLA FURNACE FACES: The top accepts smelting inputs; horizontal faces accept fuel; the bottom exposes output and fuel-container handling. Configure this demonstration with coal and keep the fuel insertion on a horizontal face.',
 'TEST THREE STAGES: First deliver one raw iron to the top. Next supply coal from a side. Finally pull the ingot from the bottom into results. Only combine the rules after every stage works. FORGET separates the remembered resources for each independent job.')
detail('xnet',4,
 'CONTROLLER SCREEN: Choose an unused channel and make it an Item channel. In the connector list for that channel, set the source to Extract and the destination to Insert. Both rows must be enabled. Put eight iron ingots in the source and observe them arrive.',
 'TWO DIFFERENT COLORS: Cable colors separate physical networks. Item-channel filters/priorities control a route within one controller. Changing a cable color is not a substitute for configuring the source and destination rows.')
detail('xnet',6,
 'FURNACE EXERCISE: A vanilla furnace wants ore through its top, fuel through a horizontal side, and output removed below. With ordinary connectors, place connections on the appropriate physical faces. An advanced connector can provide more face-control options.',
 'SPLIT THE JOB: Use separate item channels or deliberate filters for raw material, fuel and finished ingots. If your output rule has no filter and points at an input inventory, it can take material back before the furnace uses it.')
detail('xnet',14,
 'TWO WORKING NETWORKS: Each controller should already move an item locally. Publish the intended channel with a clear name, attach the controller-side network to the router arrangement, then connect the matching published channel through routing.',
 'TEST THE BOUNDARY: Move one known stack across the two systems. If each local channel works but the cross-system transfer does not, inspect the published names, router connections and routing cable network before changing machine-side settings.')
detail('computercraft',6,
 'WIRED SETUP: Put a Wired Modem against the computer, connect Networking Cable, and put another Wired Modem against the chest. Right-click the chest modem to expose the inventory; its generated name appears in chat. Run peripherals in the shell to confirm visibility.',
 'NAME VERSUS SIDE: A local chest might be called left, while the wired chest might be minecraft:chest_0. Use the name your own computer reports. Copying a name from someone else\'s world can point at nothing.')
detail('computercraft',7,
 'FIRST PROGRAM: In the shell, type edit stock.lua. The example below wraps one known inventory and reads its occupied slots with list(). Each stack has a name and count; empty slots are absent from that table.',
 'RUN AND CHECK: Save/exit the editor and type stock. Compare the printed count with the physical chest, then add one stack and run again. No item-moving calls are needed to make a useful stock report.')
detail('computercraft',13,
 'POSITION RULE: Only advance your logical position after turtle.forward() returns true. A wall, mob or unloaded boundary may prevent movement. If you ignore that return value, later digging coordinates no longer match reality.',
 'BOUNDED JOB: For the first drill, inspect the block ahead and move at most four spaces in an empty test corridor. Stop on the first failure. Do not turn a demonstration into an unlimited mining loop before adding fuel and inventory checks.')
detail('rftools',8,
 'FIRST CARD: Use a normal Shape Card for placement, choose a hollow box and small dimensions such as 5 by 5 by 5. Preview/support mode shows the selection relative to the Builder. The diagram is a workflow, not a multiblock blueprint.',
 'VERIFY OFFSET: Walk around all six boundaries and confirm the selected volume is clear of machines. Leave the Builder disabled until the preview matches your intended shell. This catches coordinate mistakes before they become a building or quarrying job.')
detail('rftools',14,
 'TWO-STAGE RECIPE: Teach logs -> planks and planks -> sticks. Keep intermediate planks inside the Crafter for the second recipe; send the final sticks to the output. If both recipes send everything outward, the second one never receives its ingredient.',
 'REMEMBER SLOTS: Reserve ingredient slots before feeding a large amount of logs. Test with a small batch and inspect where each result goes. Throughput upgrades are useful only once recipe order and internal/external result handling are correct.')
detail('rftools',17,
 'THREE DEVICES: The transmitter is the departure point, the receiver is the named arrival point, and the Dialing Device chooses the connection. Power the endpoints and dial a nearby receiver with clear headroom.',
 'ROUND TRIP: A destination receiver does not by itself send you home. Provide a reverse setup or bind a charged porter to your home receiver. Test both directions before relying on a remote destination.')

EXTRAS = {}
def add(slug,key,title,item,after,body,action,tip,*,code=None):
 EXTRAS.setdefault(slug,[]).append(dict(key=key,title=title,item=item,after=after,why=body,action=action,tip=tip,code=code or [],practice=True))

add('minecolonies','build_tool','The blueprint is the plan','structurize:sceptergold',2,
 'The Build Tool selects style, rotation, position and level. The hut block is the management anchor of the finished structure; dropping it on the ground is not equivalent to selecting a blueprint.',
 'Preview a Builder\'s Hut, rotate it so the entrance meets your future road, and inspect the higher-level footprint. Cancel the preview once, then place it deliberately. Keep this tool for every new colony building.',
 'Reserve space for upgrades now. A later level can need a wider or taller footprint even when level 1 fits.')
add('minecolonies','forester_output','A full cycle of timber','minecraft:oak_log*32',9,
 'A Forester is useful when it can cut, collect and replace trees while supplied with tools. A one-time harvest is not yet a renewable production loop.',
 'Use an ordinary oak area for the first test. Supply the requested axe and saplings, observe cutting and replanting, then gather a 32-log sample. Add the courier route only after the worker can produce on their own.',
 'This inventory milestone records the sample, not who harvested it. Confirm the replanting behavior yourself before marking the practical task.')
add('minecolonies','sawmill_output','Logs become a building palette','minecraft:oak_stairs*32',13,
 'Styles consume stairs, slabs, fences and doors as well as raw logs. Teaching the Sawmill the frequently requested products makes a small log supply much more useful.',
 'Teach oak planks and oak stairs through supported recipes. Stock logs, allow an actual building request to trigger production, then collect a sample of the finished stairs. Return them to construction storage afterward.',
 'Check the requested wood species. Oak stairs cannot satisfy a request for spruce stairs just because their shapes match.')
add('minecolonies','blacksmith','Keep the tool supply running','minecolonies:blockhutblacksmith',15,
 'Production eventually stops when workers wear out their tools. A Blacksmith turns tool replacement from a recurring personal errand into part of the colony supply chain.',
 'Meet the visible research/building prerequisites, build and staff the hut, then teach one supported tool recipe requested by an existing worker. Stock the ingredients and follow one request to delivery.',
 'Use a tool grade the workplace can accept at its current level. More expensive is not automatically usable.')
add('minecolonies','food_buffer','Dinner before expansion','minecraft:bread*32',12,
 'A food reserve prevents a new construction project from consuming all your attention while citizens go hungry. Ingredients alone do not guarantee accessible meals.',
 'Build a reserve of 32 bread as a simple demonstration. Put acceptable food where your Dining Hall can use it, watch a citizen eat, and identify how the reserve will be replenished during the next build.',
 'Bread is a demonstration item, not the only allowed food. Diversify meals according to the colony\'s actual needs.')
add('minecolonies','second_builder','Parallel construction, planned','minecolonies:blockhutbuilder',16,
 'A second Builder can reduce a construction queue, but it adds another demand stream for materials, tools and deliveries.',
 'After food and the warehouse route are reliable, prepare a second Builder\'s Hut in a different work area. Compare its workload and level with the first before assigning simultaneous upgrades.',
 'If both builders wait on the same missing recipe, more builders will not solve the bottleneck.')

add('ad_astra','rocket_parts','Engine, tanks and structure','ad_astra:steel_engine',7,
 'The NASA Workbench combines several kinds of components. Making all your steel into plates first can leave you unable to craft the engine or tanks.',
 'Pin the Tier 1 rocket recipe in JEI. Make its Steel Engine, then prepare the listed tanks, fins and body ingredients. Lay the components out in a chest before moving them into the workbench.',
 'The quest checks the engine as a milestone. Use the installed recipe for the rest of the bill of materials; amounts can differ between packs.')
add('ad_astra','landing_pad','A launch pad for the way home','ad_astra:launch_pad*9',8,
 'A second launch site turns a successful landing into a returnable expedition. Supplies consumed on departure cannot also be your emergency reserve.',
 'Pack nine spare Launch Pads. On your destination, build the 3 by 3 return pad in open space, set up the recovered rocket and verify that your reserved fuel can support the return flight before exploring.',
 'Keep return fuel and pads in a separate inventory section so they are not confused with base-building supplies.')
add('ad_astra','moon_sample','Lunar resource survey','ad_astra:raw_desh*8',12,
 'Desh is the reason your first Moon trip unlocks more than scenery. Recovering it and getting it home proves that launch, landing, mining and return all work.',
 'Mark your landing site, check oxygen, collect eight Raw Desh and return to the pad while you still have a comfortable oxygen reserve. Process the sample at home and inspect its Tier 2 uses.',
 'Do not spend the entire oxygen tank hunting a perfect deposit. The first trip should be short and repeatable.')
add('ad_astra','mars_sample','Ostrum opens the next tier','ad_astra:ostrum_ingot*8',16,
 'Mars supplies the material needed to move beyond the Desh stage. A new rocket tier is a manufacturing chain, not just a destination button.',
 'Bring home a small Ostrum sample, process eight ingots and pin the Tier 3 recipe. Identify which components consume Ostrum and which life-support equipment needs upgrading before the next destination.',
 'Finish the heat-protection branch before a hot-world expedition. Strong ordinary armor does not establish that the environment is safe.')
add('ad_astra','calorite_sample','Calorite for deep-space travel','ad_astra:calorite_ingot*8',19,
 'Calorite supports the final rocket stage and advanced equipment. Harvesting it is only useful if your travel setup can survive the resource destination.',
 'After testing the correct environmental suit, bring back a modest Calorite sample and make eight ingots. Reserve those for the Tier 4 chain rather than spending the first batch on decoration.',
 'Check temperature and oxygen separately; fixing one environmental hazard does not fix the other.')
add('ad_astra','remote_power','A powered landing outpost','ad_astra:solar_panel',14,
 'A permanent outpost needs a power plan for oxygen and other machines. Solar generation changes with exposure, so a working panel alone is not proof of continuous life support.',
 'Install a Solar Panel with clear exposure and connect it to a suitable energy buffer. Run the oxygen system, observe supply and consumption, and keep suit oxygen available while testing interruptions.',
 'Size the buffer around the actual world and loads. Avoid assuming Overworld daylight behavior is identical at every destination.')

add('advanced_rs','processors','Three processor tiers','refinedstorage:advanced_processor*4',4,
 'Basic, Improved and Advanced Processors recur throughout RS construction. Automating the raw-processor recipe and its smelting step makes later machines far less repetitive.',
 'Start with the Basic Processor processing lesson. Extend the same tested pattern to the improved and advanced variants, then request four Advanced Processors in one job and verify that the monitor clears.',
 'Each pattern must promise the actual cooked processor. A pattern for a raw processor does not automatically include the furnace step.')
add('advanced_rs','interface_buffer','Give machines a clean boundary','refinedstorage:interface',6,
 'An Interface can provide a defined boundary between the network and external automation. A small buffer makes it easier to see what was delivered and what returned.',
 'Place an Interface on a separate test branch, inspect its stocking/insertion controls and move a known item through it. Compare that behavior with an Importer before choosing how to return machine products.',
 'Avoid two independent systems trying to stock and drain the same buffer. Assign one clear producer and one clear consumer.')
add('advanced_rs','energizer','Energy is a resource type','refinedtypes:network_energizer',11,
 'The Network Energizer allows FE stored on energy disks to sustain the storage network. This connects the resource storage function to the network\'s operating cost.',
 'Start with external power, charge a compatible energy disk, connect the Energizer and enable its redstone mode. Briefly remove the external feed and check that the network stays online while stored FE decreases; reconnect the feed afterward.',
 'An empty disk or inactive Energizer cannot sustain the network. Keep an accessible external supply so a failed bootstrap does not strand the test.')
add('advanced_rs','network_link','Reach a second workshop','refinedstorage:network_transmitter',15,
 'A transmitter/receiver link extends a network without a continuous cable run. It still needs a correctly configured card and a powered, loaded destination.',
 'Place a Network Receiver in a nearby second room, bind the Network Card as its tooltip describes, and put it into a connected Network Transmitter. Check a simple Grid at the receiver before moving farther away.',
 'First prove the link inside loaded chunks. Wireless access and chunk loading are separate problems.')
add('advanced_rs','permissions','Share storage deliberately','refinedstorage:security_manager',15,
 'A shared world can have different access requirements for your main storage and public supplies. Security settings control the network; being an Essential friend does not explain every RS permission.',
 'Inspect the Security Manager and card permissions with your friend present. Test opening a Grid and inserting/removing a cheap item. Keep a way to restore the owner configuration before restricting access.',
 'Change one permission at a time and test the intended account, rather than inferring friend access from what the owner can do.')
add('advanced_rs','backpressure','A full output is a real test','refinedstorage:autocrafting_monitor',7,
 'A network that works only with empty buffers has not demonstrated reliable processing. Full output and absent ingredients are routine conditions, not rare accidents.',
 'Use a cheap processing recipe, temporarily block its output and request one craft. Identify the waiting state in the monitor, restore space, and confirm the same job completes without cancelling and resubmitting it.',
 'Keep the batch tiny. The point is to learn recovery, not to leave hundreds of promised items spread through machines.')

add('economy','bulk_test','Benchmark a bulk export','minecraft:cobblestone*64',7,
 'A cobble generator can outproduce simulated buyer demand by many orders of magnitude. Its value is a low-effort trickle, not an unlimited source of spending money.',
 'Record /marketlimits and your wallet, offer 64 cobble, and inspect the completed payout. Feed more into the same trade buffer and compare the price and available bulk demand after sales.',
 'Bulk demand recovers at $500 per online hour inside the $10,000 shared total. A full buffer can simply wait for demand; adding chests does not increase the allowance.')
add('economy','resource_test','Resources have their own market','minecraft:iron_ingot*16',9,
 'Processed resources earn more per item than common blocks but remain automatable through farms and ore-processing chains.',
 'Offer a small iron surplus while retaining your construction reserve. Compare the resource allowance and total allowance before/after a completed sale, then contrast it with the cobble experiment.',
 'The resource category recovers at $4,000 per online hour. Those credits are part of the shared total, not an extra allowance added on top.')
add('economy','factory_test','Price a finished product','minecraft:diamond_pickaxe',10,
 'A finished product has a recipe cost and an opportunity cost: selling its ingredients separately may produce a different result. Machines should be manufactured to a useful plan rather than blindly crafted for sale.',
 'Compare the current diamond pickaxe buy and sell quotes with the ingredients. Make or inspect one plain pickaxe, calculate the expected margin, and choose whether selling it makes sense. The quest does not require you to sell it.',
 'Enchantments, damage and stored contents are not a guaranteed premium. Keep unique equipment out of an automated sale chest.')
add('economy','reserve_chest','Production comes before exports','minecraft:chest*2',8,
 'An export buffer should be downstream of your own stock requirement. Otherwise a fast selling system can empty the resources needed to expand the factory.',
 'Label one chest Reserve and the other Exports. Use your preferred logistics mod to maintain a modest reserve and send only overflow to Exports. Connect only Exports to the market and test with inexpensive blocks.',
 'The SFM and XNet chapters both teach bounded transfers. Pick one controller for this job so competing rules do not fight over the same items.')
add('economy','compression_test','Compression changes quantity, not demand','minecraft:iron_block',7,
 'One iron block represents nine ingots. High compression can make transport easier, but it cannot multiply your per-player buyer allowance.',
 'Compare the block and ingot sell quotes before moving valuable compressed stock. Read the category buyback ceiling in /marketlimits and decide which form is sensible to offer. Keep the block if the quote is poor.',
 'Very expensive compressed blocks can hit the per-item ceiling. Buying one and unpacking it for resale is not a substitute for checking actual prices and limited demand.')
add('economy','trade_journal','A factory you can budget','minecraft:writable_book',12,
 'Useful balance is measured over time. One large sale after stored demand accumulated does not establish what the factory earns continuously.',
 'Use a Book and Quill to record starting wallet, purchases, payouts, elapsed online time and /marketlimits. Observe a normal session and compare net earnings with the resources you actually consumed.',
 'The target is around $10,000/hour for a developed factory, not a guaranteed payment. Market demand and product choices can put actual earnings below the ceiling.')

add('enderio','binder','The conduit workshop starts here','enderio:conduit_binder*16',2,
 'Conduit Binder is a recurring ingredient in Ender IO transport. Making a small stock now keeps you from stopping the machine lesson for another crafting trip.',
 'Inspect Binder Composite and Conduit Binder in JEI, make a small batch of the composite and process it through the displayed route. Collect 16 binder and reserve part of it for the first item and energy lines.',
 'Use the recipe shown in this pack. Do not assume a familiar-looking gravel/clay mixture has the same quantities as an older version.')
add('enderio','conductive','Start the alloy ladder','enderio:conductive_alloy_ingot*8',4,
 'Conductive Alloy is a useful early output for the transport and power branch. A stable alloy recipe proves that the smelter receives the correct ingredients and energy.',
 'Run the JEI recipe by hand and collect eight ingots. Then supply exactly one recipe batch through your intended input face and confirm that the result is the same.',
 'Wrong result? Check machine mode and recipe competition before blaming the conduit. Keep unrelated smeltable ingredients out of the first trial.')
add('enderio','vibrant','Make a later alloy on demand','enderio:vibrant_alloy_ingot*8',5,
 'Later alloys depend on earlier alloy production. Treat this as a short chain with an intermediate buffer, rather than an unlabelled chest full of every ingredient.',
 'Pin the Vibrant Alloy recipe and trace each ingredient back one step in JEI. Produce eight ingots, then reserve the earlier alloy needed to repeat the batch.',
 'If an earlier alloy is also exported to storage or the market, keep a reserve so the next machine in the chain does not starve.')
add('enderio','sag_output','A processing recipe, measured','enderio:sag_mill',6,
 'SAG Mill recipes can have multiple outputs and recipe-specific modifiers. Automation must allow room for byproducts as well as the material you wanted.',
 'Choose one inexpensive JEI recipe, record the input amount and expected main output, then run a short batch. Inspect every resulting slot before connecting output extraction.',
 'Do not promise a probabilistic bonus as a guaranteed RS processing output. Encode only an output the machine can reliably return.')
add('enderio','capacitor_bank','Buffer the demand spikes','enderio:advanced_capacitor_bank',12,
 'A larger capacitor bank stores energy between bursts of work. It does not increase generation by itself, and fast machines can still empty it.',
 'Compare stored FE with the workshop idle and with two machines running. Add a suitable bank when the measured buffer is too small, then watch whether it refills after the batch.',
 'If it never recovers, generation is below average demand. More storage only delays the eventual stop.')
add('enderio','xp_buffer','Separate experience from items','enderio:xp_obelisk',17,
 'The XP Obelisk is an experience buffer. It can support an XP workflow, but item transport and XP transfer remain different resources.',
 'Deposit a small known amount using the obelisk interface, retrieve part of it and compare the displayed totals. Only then connect a supported automation route used by your Soul Binder setup.',
 'Keep the first XP experiment reversible. A machine waiting for experience can have plenty of FE and all its item ingredients.')

add('astral','marble_palette','Stone that fits the structure','astralsorcery:marble_pillar*8',9,
 'Astral structures distinguish raw, engraved, chiseled, pillar and other marble forms. A white block in the right position is not sufficient if its variant is wrong.',
 'Make a small selection of the exact marble variants shown by your next Tome structure, including eight pillars. Store them separately from ordinary building stone and compare their tooltips with the structure preview.',
 'Use the Wand to locate incorrect positions. Do not replace every block when the preview highlights just one wrong variant.')
add('astral','liquid_stock','A reserve of Liquid Starlight','astralsorcery:liquid_starlight_bucket',10,
 'Liquid Starlight feeds several later operations. A stable supply begins with the Lightwell and a catalyst, then needs storage that does not interfere with its clear space.',
 'Produce and collect one bucket. Refill the collection setup and observe another production cycle. Keep a reserve for the next upgrade before starting several infusion operations.',
 'The catalyst is consumable. A stopped Lightwell may need a replacement rather than a larger surrounding structure.')
add('astral','chalice_buffer','Refill the ritual, not the whole altar','astralsorcery:chalice',14,
 'The Containment Chalice supports Liquid Starlight supply near suitable processes. It helps separate a valid structure from a fluid shortage during repeated crafting.',
 'Place it according to the installed Tome, provide Liquid Starlight, and run one supported Infuser operation. Inspect the pool and chalice levels afterward to learn what was consumed and replenished.',
 'A chalice does not provide lumen or constellation starlight. Check which magical resource the recipe actually lists.')
add('astral','crystal_shelf','Keep crystal purposes separate','astralsorcery:rock_crystal*2',8,
 'Crystals carry properties and can later carry attunement. Treating every crystal as an interchangeable ingredient makes it easy to consume the one intended for a focus.',
 'Collect two ordinary Rock Crystals, compare their tooltips, and reserve one for progression. Label storage for ordinary, attuned and focus crystals before beginning recipes that consume them.',
 'The inventory goal counts crystals, not their properties. Selecting the appropriate crystal remains a deliberate part of the recipe.')
add('astral','lumen_crystal','Make the resource visible','astralsorcery:lumen_crystal',19,
 'A Lumen Crystal gives you a tangible milestone in the lumen branch. Its production depends on the relevant array, supply and crystallizing process.',
 'Read the Lumen Crystallizer entry, choose one available aspect and establish its direct supply. Produce one crystal and compare the producer and consumer before and after the craft.',
 'A full producer and idle consumer usually point to the link, resource type or consumer conditions rather than a shortage of catalysts.')
add('astral','linking_tool','A link with a purpose','astralsorcery:linking_tool',20,
 'The Linking Tool belongs to the focused-starlight system. The current port has other magical transport methods, so not every pair of nearby blocks should be linked with it.',
 'Use an appropriately attuned focus at a matching focal point and link one valid target with clear line of sight. Check the required constellation and observe that target while the sky conditions are suitable.',
 'Focus Relays for altar ingredients are positioned, not linked this way. Lumen Filaments also belong to a different system.')

add('sfm','cable_kit','Build a network you can see','sfm:cable*16',2,
 'Inventory Cable gives the Manager access to connected inventories. It does not move items merely because it touches them; the program selects transfers.',
 'Lay a short visible cable run connecting the Manager and two chests. Use the Network Tool to inspect it before hiding cables in walls. Put a few cheap items in only one chest.',
 'A visible test network separates wiring faults from program faults. Keep the first labels distinct from your main factory.')
add('sfm','filter_demo','Only the named item moves','minecraft:iron_ingot*8',6,
 'An exact item filter protects unrelated stock from a general INPUT statement. The item ID matters more than the translated display name.',
 'Put iron and cobble in the source. Run an INPUT rule filtered to minecraft:iron_ingot and send its result to the destination. Verify iron moved and cobble stayed.',
 'Use the installed disk editor examples for grammar. After the test, widen the filter only if the destination can accept every newly matched item.')
add('sfm','distribution','Feed three furnaces fairly','minecraft:furnace*3',11,
 'A shared label can refer to several machines. A rule that fills the first available inventory may leave later machines idle, while an EACH rule can distribute a bounded amount to each.',
 'Give three furnaces the same label. Start with an output limit of a few items to EACH furnace, supply fuel separately, and compare their input slots. Then collect all finished outputs into one results chest.',
 'Equal input is not the same as equal processing speed. Compare identical machines before diagnosing distribution behavior.')
add('sfm','tank_demo','Prove fluid direction','sfm:water_tank',14,
 'Fluid movement uses a fluid resource identifier and compatible tank capabilities. An item rule targeting a water bucket does not establish that water itself is being transferred.',
 'Use ordinary water and two compatible tanks. Inspect the bundled fluid example, substitute the labels of your test tanks, then transfer a small amount and compare both tank volumes.',
 'Keep item and fluid stages separate with clear labels. Never start this lesson with a fluid you cannot afford to lose.')
add('sfm','buffer','Pause at a known boundary','minecraft:barrel',16,
 'An ordinary barrel can give a network a deliberate staging point. It makes a multi-step job easier to inspect than a direct transfer between hidden machine inventories.',
 'Add the buffer to a small test route, label it and send only a small item batch through it. Stop the program halfway and identify exactly where the batch waits, then resume.',
 'A buffer is finite. Decide how the program behaves when the next machine is full instead of treating extra storage as an unlimited fix.')
add('sfm','production_proof','A complete batch, accounted for','minecraft:iron_ingot*32',18,
 'A finished processing cell should move a known batch from input to finished storage and then settle idle without recirculating the product.',
 'Feed enough raw iron for a 32-ingot demonstration, maintain a separate fuel reserve, and run the cell. Count the finished ingots, inspect for leftovers, then run it with no new input and confirm nothing circulates.',
 'Account for the actual furnace recipe rather than assuming every modded ore-processing recipe is one input to one output.')

add('xnet','wired_kit','Two endpoints, one controller','xnet:connector_blue*2',3,
 'Connectors expose adjacent inventories to the controller. A cable running past a chest without the appropriate connector does not give the channel an endpoint.',
 'Connect two chests with two matching-color connectors and a short cable run to a powered controller. Open its interface and locate both connectors before configuring any channels.',
 'Name endpoints Source and Results where the interface allows. Those names make later channel setup easier to verify.')
add('xnet','raw_input','Give the furnace a recipe','minecraft:raw_iron*8',6,
 'Item movement is only useful if the receiving face accepts the intended slot. The top of a vanilla furnace is a convenient demonstration of sided inventory access.',
 'Configure a raw-iron extraction rule from a source chest and insert through the furnace top. Start with eight raw iron and verify its input slot fills while fuel and output slots remain distinct.',
 'If the source drains but the furnace is empty, stop and locate the items before changing the filter or adding more.')
add('xnet','fuel_route','Fuel uses its own route','minecraft:coal*8',6,
 'Fuel should enter the furnace fuel slot, not compete with ore for the top input. A separate channel makes this distinction visible.',
 'Add a coal-only route through a horizontal furnace face. Keep its stocking amount small, run the raw-input route, and confirm the furnace processes one batch.',
 'The output route should remove the product from below. Test each face individually before combining all three channels.')
add('xnet','connector_upgrade','Upgrade a measured bottleneck','xnet:connector_upgrade',12,
 'Advanced connectors offer capabilities beyond a basic connection. Use them when a real side-access or transfer requirement warrants the upgrade.',
 'Compare the basic and advanced connector controls in the installed manual/UI. Upgrade one endpoint, change only the needed setting and repeat your previous successful transfer test.',
 'A faster connection cannot fix a full destination, disabled controller, or item filter that excludes the product.')
add('xnet','routing_kit','Separate the routing network','xnet:netcable_routing*8',14,
 'Routing cable links routing infrastructure rather than acting as an ordinary colored item network. Keep the two roles visually distinct.',
 'Prepare a small routing cable run for two already-working local controller networks. Publish clearly named channels and check the router sees the intended pair before sending a test stack.',
 'If no published channel appears, inspect the controller/router attachment and channel name. More ordinary cable does not publish a channel.')
add('xnet','backpressure','Full chest, controlled recovery','minecraft:chest*2',17,
 'Automation must handle a full destination without silently moving products somewhere unintended. A controlled stop is a normal operating state.',
 'Fill a disposable output chest with cheap blocks, run a tiny furnace batch and watch the finished item wait. Clear space, verify extraction resumes and confirm it still uses the intended destination.',
 'Keep an obvious off switch for the controller or upstream supply. Diagnose one channel at a time.')

add('computercraft','disk_backup','Keep a working copy','computercraft:disk',10,
 'An in-game program is useful documentation as well as automation. A backup lets you recover after an experiment without rewriting the working version from memory.',
 'Place a Disk Drive beside the computer and insert a disk. In the shell, use ls to locate its mounted directory, then copy your tested stock.lua to that directory. Open the copy to verify it contains the expected program.',
 'Mounted names can differ if multiple drives are attached. Inspect the mount rather than assuming every drive is always called disk.')
add('computercraft','stock_report','Count the stock that matters','minecraft:chest',7,
 'A generic inventory exposes occupied slots. A useful stock report adds the count of only the item your workshop cares about instead of counting every object in the chest.',
 'Adapt the supplied stock-report example to minecraft:iron_ingot. Put iron and an unrelated item in the chest, run the report, and compare its total with the physical stack count.',
 'Use item IDs from the list() results. Display names and registry IDs are different strings.')
add('computercraft','monitor_layout','Make the number readable','computercraft:monitor_advanced*4',5,
 'A dashboard needs a stable cursor position and labels. Repeatedly printing without clearing or positioning can leave stale digits on the screen.',
 'Join four matching advanced monitors into a small display, wrap the monitor peripheral, clear it and set the cursor before writing each refresh. Show an item name, count and unit on separate lines.',
 'When a value shrinks from 100 to 9, clearing the line prevents old digits from making it look like 900.')
add('computercraft','turtle_fuel','Fuel before movement','minecraft:coal*4',11,
 'Turtle fuel is a movement resource. A powered-looking computer interface does not mean that a turtle has fuel to walk back after its work.',
 'Put coal in the selected turtle slot, inspect turtle.getFuelLevel(), use turtle.refuel(1), and inspect the amount again. Make one forward/backward trip in a clear area.',
 'A configuration can report unlimited fuel. Handle that result separately instead of treating it as a number in arithmetic.')
add('computercraft','redstone_demo','One output, no surprises','minecraft:redstone_lamp',3,
 'A redstone output is a simple way to learn control before commanding a machine. A lamp makes the effect visible without moving items or breaking blocks.',
 'Place a lamp on a known computer side, run redstone.setOutput("back", true) for that side, then set it false. Wrap the two actions around a short sleep and observe one complete cycle.',
 'Use the side relative to the computer. A program ending unexpectedly can leave an output in its last state; turn it off deliberately after the lesson.')
add('computercraft','restart_test','Survive a missing device','computercraft:computer_advanced',17,
 'A startup dashboard should tolerate the monitor being absent during boot. An error with a useful message is better than a loop that crashes without explanation.',
 'Save a working read-only dashboard as startup.lua, reboot and verify it starts. Detach the monitor, reboot again and report the missing peripheral. Restore it and verify the program can be restarted normally.',
 'Keep the named source file as well as startup.lua. Use delayed retries only when they yield with sleep and report what they are waiting for.')

add('rftools','storage_module','The module holds the inventory','rftoolsstorage:storage_module0',3,
 'The removable storage module is the valuable part of Modular Storage once it contains items. The block and module serve different roles.',
 'Put a few named test items in Modular Storage, inspect the module and learn how the interface reports capacity. Read the upgrade recipe before using a filled module as an ingredient.',
 'Start with disposable items. Never discover whether a recipe preserves contents by testing it on your only valuable storage module.')
add('rftools','shape_card','A card for construction','rftoolsbuilder:shape_card_def',7,
 'A normal Shape Card tells the Builder which shape to place. Quarry and void cards are different operations even though they fit the same machine.',
 'Configure a small hollow box, keep the Builder disabled and inspect the support preview. Supply ordinary stone bricks only after the bounds match your test plot.',
 'Read the operation name every time you swap cards. Reusing the same machine does not make the new card behave like the old one.')
add('rftools','quarry_output','Give the quarry somewhere to put drops','minecraft:chest*2',10,
 'A quarry needs output capacity. Increasing its area without increasing the storage route can leave it stopped on a full adjacent inventory.',
 'Attach a visible output chest and use a tiny selected region away from your base. Run the normal quarry briefly, count recovered blocks, then test that the machine stops/resumes predictably when output fills and clears.',
 'Normal, clearing and void operations have different outcomes. Use a keeping-drops variant for this demonstration.')
add('rftools','crafter_sticks','Keep the intermediate inside','minecraft:stick*32',14,
 'A multi-step Crafter should retain the plank intermediate and export the final sticks. This is a practical example of why result handling matters.',
 'Teach logs -> planks and planks -> sticks, reserve their slots and run a small batch. Collect 32 sticks, then inspect leftover planks inside the machine to confirm the intermediate stayed available.',
 'If the second recipe has no ingredients while planks are in the output chest, change the first recipe\'s result handling.')
add('rftools','receiver','Name the arrival point','rftoolsutility:matter_receiver',17,
 'A named receiver is easier to select correctly than several anonymous destinations. Arrival space, power and loading are part of the endpoint.',
 'Place the home receiver in a clear room, give it an unmistakable name and verify its energy. Dial it from a nearby transmitter and test arrival before setting up a distant route.',
 'Leave headroom and a walkable exit. A receiver inside a decorative enclosure can be a poor teleport destination even when the network connects.')
add('rftools','screen_readout','Display one useful quantity','rftoolsutility:screen',16,
 'A screen becomes useful when a module displays a quantity that changes and tells you something about the workshop.',
 'Configure one supported module, connect its target as the manual describes, and show a stock or energy reading. Change the underlying quantity and verify the display responds.',
 'If the value never changes, verify the target/module configuration before increasing the controller range or screen size.')

DIAGRAMS = {
 'minecolonies': ('A colony supply loop',['Forester / Farm','Warehouse','Courier','Workplace'],['Raw resources enter shared storage','Crafting workers need taught recipes','Requests drive delivery; keep paths clear']),
 'ad_astra': ('A repeatable expedition',['Rocket + fuel','Suit + oxygen','Land + return pad','Mine + return'],['Workshop branch and life-support branch meet before launch','Moon: Desh | Mars: Ostrum | Later tiers: Calorite','Check the environment before leaving the landing site']),
 'advanced_rs': ('A processing job must close its loop',['RS storage','Autocrafter','External machine','Importer -> RS'],['Pattern input must match the machine recipe','Promised output must return to this network','The monitor completes only when the output returns']),
 'economy': ('Surplus earns money within demand',['Production','Personal reserve','Trade buffer','Shared demand'],['Bulk 500 | Farming 1,500 | Resources 4,000 per online hour','All categories share the 10,000/hour total','Unsold goods wait; extra chests do not multiply demand']),
 'enderio': ('A compact alloy workshop',['Input buffer','Item conduit','Alloy Smelter','Output storage'],['Configure extraction, insertion and matching item channel','Supply FE through the energy conduit separately','Machine face, recipe mode and capacitor must be valid']),
 'astral': ('Three different magical supplies',['Lightwell: fluid','Arrays: lumen','Focus: starlight','Altar / consumer'],['Liquid Starlight uses fluid storage and supported supply','Lumen uses arrays/filaments; focused light uses links','Check tier, structure, ingredients and sky conditions separately']),
 'sfm': ('A program chooses the transfer',['Labeled source','INPUT selection','OUTPUT rule','Labeled target'],['Inventory Cable exposes the endpoints to the Manager','FORGET separates unrelated jobs','Filter resources and test with a small batch']),
 'xnet': ('One furnace, three clear routes',['Ore -> TOP','Fuel -> SIDE','Furnace process','BOTTOM -> output'],['Each route needs enabled source and destination connectors','Use filters to keep ingredients and products separate','Configure power and fluids on their own channels']),
 'computercraft': ('Read first, automate second',['Peripheral name','wrap / methods','Read + calculate','Display + sleep'],['Discover names from your own network','list() reads occupied inventory slots','Check missing devices and yield between refreshes']),
 'rftools': ('Preview before the Builder runs',['Choose card','Set shape + offset','Preview bounds','Supply + enable'],['Placement, quarry, clearing and void cards are different jobs','Verify a tiny region before increasing size','Keep energy, input and output visible during the first run']),
}

OVERRIDES = {
 ('advanced_rs',11):dict(action='Build an energy storage disk and fill it through a compatible resource input while the network has external power. The Network Energizer can then use stored FE to sustain the network itself; complete its side quest for that test.',tip='A disk stores energy; the Energizer makes that stored energy available for network operation. Keep external startup power available until this loop is proven.'),
 ('sfm',7):dict(code=['NAME "Keep a building reserve"','EVERY 20 TICKS DO','  INPUT RETAIN 64 minecraft:cobblestone FROM input','  OUTPUT TO output','END']),
}
for q in EXTRAS['computercraft']:
 if q['key']=='stock_report':q['code']=['local inv = peripheral.find("inventory")','assert(inv, "Connect one test chest")','local total = 0','for _, stack in pairs(inv.list()) do','  if stack.name == "minecraft:iron_ingot" then','    total = total + stack.count','  end','end','print("Iron ingots: " .. total)']
 if q['key']=='monitor_layout':q['code']=['local m = peripheral.find("monitor")','assert(m, "Connect an advanced monitor")','m.setTextScale(1)','m.clear()','m.setCursorPos(1, 1)','m.write("Workshop stock")','m.setCursorPos(1, 2)','m.write("Iron ingots: 16")']
 if q['key']=='turtle_fuel':q['code']=['print("Before:", turtle.getFuelLevel())','local ok = turtle.refuel(1)','print("Refuel accepted:", ok)','print("After:", turtle.getFuelLevel())']
 if q['key']=='redstone_demo':q['code']=['redstone.setOutput("back", true)','sleep(2)','redstone.setOutput("back", false)']
 if q['key']=='restart_test':q['code']=['local m = peripheral.find("monitor")','if not m then','  print("Monitor missing; reconnect and rerun")','  return','end','for refresh = 1, 5 do','  m.clear()','  m.setCursorPos(1, 1)','  m.write("Refresh " .. refresh)','  sleep(1)','end']
