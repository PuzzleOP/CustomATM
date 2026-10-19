"""Original guided quest text for this private ATM10 profile."""
CHAPTERS = []
current = None

def chapter(slug, title, icon, purpose, route):
    global current
    current = dict(slug=slug, title=title, icon=icon, quests=[])
    CHAPTERS.append(current)
    q('Start here: ' + title.split(':')[0], None, purpose,
      'Your route: ' + route,
      'Read the next guide card before building. This chapter teaches working setups; it does not replace JEI recipes or the mod\'s own manual.')
    q('How to use this guide', None,
      'Arrows suggest a learning order. Item tasks check what you carry; a checkmark is your own confirmation of a practical step. Neither is proof that an entire machine or colony works.',
      'Open a quest, read Why / Do / Tip, then click its item to inspect it in JEI. R shows recipes and U shows uses with the default bindings. Read ahead, complete the described experiment, and only then tick practical tasks. Items are not consumed.',
      'Use JEI for this pack\'s quantities and substitutions. Pick a small test area and keep outputs visible. Existing equipment can count; briefly pick it up only when safe. Troubleshooting and a final project are at the end.')

def q(title, item, why, action, tip, *, practice=False, deps=None, optional=False, code=None):
    current['quests'].append(dict(title=title,item=item,why=why,action=action,tip=tip,
                                 practice=practice,deps=deps,optional=optional,code=code or []))

chapter('minecolonies','MineColonies: A Living Colony','minecolonies:blockhuttownhall',
 'MineColonies turns a base into a working settlement. Citizens build blueprints, gather materials, cook, deliver supplies and research upgrades. You manage jobs and requests rather than placing every building block yourself. StyleColonies adds architectural choices to the build system.',
 'site and supplies -> Town Hall and builder -> housing and food -> warehouse and couriers -> production, research and defense -> a self-supplied expansion.')
q('Choose land and a style',None,'A colony needs room for future buildings, paths and changing elevations. A beautiful first house is less useful if every later blueprint overlaps a mountain.',
 'Scout a broad area near materials. Preview the style you want with the Build Tool, including higher building levels, before committing. Plan a central storage area and leave walking space between entrances.',
 'StyleColonies supplies styles, not a second colony system. Large styles can require unusual decorative materials; inspect the preview and resource list first.')
q('A supply camp or ship',None,'The supply structure gives you a starter shelter and colony equipment. It is a starting kit, not an operating colony.',
 'Use a Supply Camp on suitable land, or choose the Supply Ship alternative in JEI. Resolve the highlighted placement obstructions, place the structure, and collect its Town Hall and Build Tool.',
 'Choose either structure; this checklist accepts both routes. Do not place a second supply structure just for this guide.',deps=[2])
q('Found your settlement','minecolonies:blockhuttownhall','The Town Hall establishes the colony and gives access to citizen, work and permission management.',
 'Place the Town Hall with the Build Tool at your planned center. Open it, establish/name the colony and inspect its information. Keep the area reachable by ordinary walking paths.',
 'Placing a hut block and completing its building are different steps. Do not assume the blueprint has already been built.',practice=True)
q('Your first builder','minecolonies:blockhutbuilder','A builder constructs and upgrades the colony. Without one, a queue of hut blocks is only a queue of plans.',
 'Place a Builder\'s Hut blueprint with the Build Tool. Assign an available citizen if necessary, request its construction, and open the hut to inspect the active job and required resources.',
 'The builder can build their own initial hut. Queue one small project first so you learn the request system before expanding.',practice=True)
q('Read the request list','minecolonies:clipboard','Most stalled jobs are a specific missing item, tool or condition. The Clipboard helps you see colony requests instead of guessing.',
 'Read the builder\'s request, supply the exact requested material or a permitted substitution, then watch work resume. Use the hut resource interface and Clipboard to locate the next bottleneck.',
 'A similar-looking block from another mod may not be accepted. The request tells you which item is needed.',practice=True)
q('Keep workers fed','minecolonies:blockhutcook','Hungry citizens stop being productive. A Dining Hall distributes meals; the Chef\'s Kitchen is a separate production building.',
 'Build and staff a Dining Hall. Initially supply acceptable prepared food yourself and check that citizens can reach it and eat. Automate food production after this basic delivery loop works.',
 'A worker with food problems needs food access, not another task in their queue. Check citizen status messages first.',practice=True)
q('Housing and happiness','minecolonies:blockhutcitizen','Residences provide stable housing and support population growth. More people require food, jobs and beds, not just recruitment.',
 'Build a Residence and inspect assignments. Check citizen happiness, access to shelter and basic needs before recruiting more workers.',
 'Upgrade housing as your settlement grows. Avoid expanding population faster than your food supply and builders can support.',practice=True)
q('A reliable wood supply','minecolonies:blockhutlumberjack','Building consumes large amounts of wood. A Forester can turn an accessible planting area into a renewable supply.',
 'Build and staff the Forester\'s Hut. Supply the requested tool and saplings, check its work area, and confirm logs arrive in its inventory.',
 'Keep decorative trees outside the selected work zone. Watch one full planting/harvesting cycle before depending on the output.',practice=True)
q('Storage with a purpose','minecolonies:blockhutwarehouse','The Warehouse is the colony\'s shared store. It supports requests and crafting; an unrelated chest or RS disk is not automatically part of it.',
 'Build a Warehouse and stock it with common building materials. Inspect its racks and capacity, and keep access routes clear.',
 'Use colony-aware storage and delivery paths. Moving supplies into a warehouse is only half the system; couriers perform deliveries.',practice=True)
q('Connect the supply chain','minecolonies:blockhutdeliveryman','Couriers move requested supplies between the warehouse and workplaces, removing much of your manual delivery work.',
 'Build and staff a Courier\'s Hut. Trigger a small builder request using material already in the warehouse, then observe the courier delivering it.',
 'If delivery stalls, check path access, courier availability, warehouse space and whether the exact item is stocked.',practice=True)
q('Turn crops into meals','minecolonies:blockhutfarmer','A Farm provides ingredients; a complete food chain also needs cooking and delivery.',
 'Build a Farm, configure its fields, provide seeds and tools, and observe a harvest. Route ingredients toward the relevant cooking workplace and keep meals available at the Dining Hall.',
 'Do not empty every seed into a machine. Keep planting reserves and verify the crop type in the field setup.',practice=True)
q('Teach the sawmill','minecolonies:blockhutsawmill','A colony cannot fulfill a crafted-block request unless a suitable worker knows the recipe and has ingredients.',
 'Build and staff a Sawmill. Teach a simple supported wooden recipe, stock its inputs, and request that product through a building job.',
 'Recipe capacity and available recipes depend on building level and research. Test one recipe before teaching an entire style palette.',practice=True)
q('Stone and tools','minecolonies:blockhutstonemason','A Stonemason and later a Blacksmith help close the gap between raw resources and construction requests.',
 'Add a Stonemason, teach a needed stone recipe and test it. Plan a Blacksmith for suitable tools and metal products as its research/build requirements become available.',
 'Follow a request backward: final block -> crafter recipe -> ingredient supply -> courier. This reveals which link is actually missing.',practice=True)
q('Research with a reason','minecolonies:blockhutuniversity','Research unlocks buildings and improvements. Its prerequisites are part of colony progression, not a problem to bypass by crafting a hut early.',
 'Build a University when its requirements are met, assign a researcher, and select a research that solves a current need. Supply the requested materials and inspect the prerequisites and duration.',
 'Choose a useful unlock before chasing every branch. Keep the colony loaded for work to progress under your pack\'s chunk-loading rules.',practice=True)
q('Upgrade your capacity',None,'Upgrading the builder expands what they can construct. Higher-level workplaces also improve capabilities, storage and recipes.',
 'Read the next upgrade\'s material list and builder-level requirement. Upgrade the Builder\'s Hut when needed, then upgrade one bottleneck workplace and verify the benefit.',
 'Do not schedule every upgrade simultaneously. Preserve tools, food and access while your main builder is occupied.')
q('Protect the workers','minecolonies:blockhutguardtower','A larger colony needs guards and coverage near its workplaces. Walls alone do not equip or assign a guard.',
 'Build a Guard Tower, assign a guard, provide appropriate equipment and inspect patrol/guard settings. Light common paths and keep entrances usable by citizens.',
 'Balance defense with food and production. Citizens\' complaints and raid notifications are useful management signals.',practice=True)
q('Recruit deliberately','minecolonies:blockhuttavern','Visitors and new citizens are useful only when you can give them a home, food and a productive role.',
 'Build a Tavern when ready. Inspect recruitment requirements and citizen skills, then choose a recruit suited to a real vacancy rather than filling every slot immediately.',
 'Read the workplace\'s skill requirements. A suitable worker is more valuable than the first available name.',practice=True)
q('When a citizen stops',None,'Idle animation is not a diagnosis. A citizen may need a tool, recipe, food, research, safe path or a finished building.',
 'Inspect the citizen\'s status, their hut, open requests and active work order in that order. Fix one cause, wait for the worker to react, and confirm the job advances.',
 'Do not repeatedly break hut blocks to fix requests. Preserve their assignments and diagnose the missing condition instead.')
q('Project: supplied expansion',None,'A functioning colony is a repeatable production and delivery system, not merely a collection of completed buildings.',
 'Request one new building. Let your warehouse, couriers and crafters supply several of its materials. Resolve the remaining shortages, finish construction, staff it and explain its role in the colony.',
 'Use the same cycle for future expansion: identify a need, plan space, prepare materials, build, staff and verify.',practice=True)

chapter('ad_astra','Ad Astra: From Earth to Glacio','ad_astra:tier_1_rocket',
 'Ad Astra adds rockets, planets and space infrastructure. Progression combines manufacturing with life support: each new destination offers resources for the next tier, but travel also requires a way to breathe and return.',
 'steel workshop -> rocket and fuel -> suit and oxygen -> Moon and Desh -> Mars and Ostrum -> hot worlds and Calorite -> Glacio and an orbital base.')
q('Your flight manual','ad_astra:astrodux','The Astrodux explains the installed version\'s machines and environmental rules. It is especially useful when a recipe differs from an older video.',
 'Craft and open the Astrodux. Read The First Launch, then bookmark the oxygen and return-trip pages. Use JEI for the pack\'s actual machine and rocket recipes.',
 'This chapter follows the bundled 1.16.26 guide. Suit upgrades and oxygen systems are not optional just because another mod gives you strong armor.')
q('Power the workshop','ad_astra:coal_generator','Machines need FE before you can make plates, process fuel or load oxygen. A small independent workshop is easy to troubleshoot.',
 'Supply FE using the Coal Generator or an existing compatible source. Connect one machine, inspect its energy bar and run a simple process before adding more loads.',
 'Check machine sides and redstone settings when a cable touches a machine but no energy enters.',practice=True)
q('Steel for spacecraft','ad_astra:steel_ingot','Steel is a key structural material for your first space equipment. Its processing route is determined by this pack\'s recipes.',
 'Inspect Steel Ingot in JEI and make a small batch using an available route. Check the Etrionic Blast Furnace recipe and uses if you want an Ad Astra-focused workshop.',
 'Do not guess that every steel tag works in every rocket part. Check the actual ingredient slots before making a large batch.')
q('Make plates','ad_astra:compressor','The Compressor turns materials into components for machines and rockets.',
 'Power the Compressor, insert a recipe-compatible ingot and collect a plate. Compare its uses in JEI and reserve enough material for the engine, tanks and rocket body.',
 'Process a small batch first. Rocket assembly needs several distinct components, not just a pile of plates.',practice=True)
q('Refine rocket fuel','ad_astra:fuel_refinery','Oil is a feedstock; rockets need a supported fuel. The refinery converts collected oil into usable fuel.',
 'Find oil using the Astrodux guidance, collect it, and run a powered Fuel Refinery. Store the result in clearly separated containers. Prepare enough for both departure and return.',
 'Do not mix oil, oxygen and fuel plumbing. Read the fluid name on the tank before filling the rocket.',practice=True)
q('Rocket assembly bench','ad_astra:nasa_workbench','Rockets are assembled at the NASA Workbench using a complete set of parts.',
 'Craft the workbench and open the Tier 1 recipe. Make its required cone, plates, fins, tanks and engine, then assemble the rocket.',
 'Use the recipe for your selected tier. Higher-tier engines and tanks are not automatically interchangeable.',practice=True)
q('Launch pad and rocket','ad_astra:tier_1_rocket','The rocket needs its launch pad and fuel, not just an open patch of ground.',
 'Build a Launch Pad, place the Tier 1 Rocket at its center and open its inventory. Fuel it and inspect its storage. Keep the launch area clear above and around the craft.',
 'Avoid powering the launch pad accidentally: its redstone behavior can launch a fueled rocket.',practice=True)
q('A complete space suit','ad_astra:space_suit','The chestpiece stores oxygen, but a partial outfit is not a complete life-support solution.',
 'Craft the helmet, chestpiece, pants and boots. Equip the full set and inspect the oxygen readout. Check each piece rather than assuming your normal combat armor covers the same hazards.',
 'Any alternative suit integration must be configured and tested on Earth first. Keep the Ad Astra suit as your known working baseline.',practice=True)
q('Load oxygen','ad_astra:oxygen_loader','Oxygen is a consumable travel resource. Empty tanks and an unfilled chestpiece will not protect you.',
 'Power the Oxygen Loader and provide water as described in the Astrodux. Fill the suit and spare tanks through its interface. Confirm that the stored oxygen values increase.',
 'Hold right-click with a filled Oxygen Tank to distribute oxygen to compatible carried items, prioritizing armor.',practice=True)
q('Preflight: come home',None,'A successful launch includes landing, survival and a return trip. Your spare fuel should stay separate from your exploration budget.',
 'Pack a return Launch Pad and three buckets of ordinary fuel, or the verified equivalent for your chosen fuel. Bring full spare oxygen tanks, food, tools, solid blocks and soul torches/glowstone. Equip and fill the full suit before entering the rocket.',
 'The bundled guide specifies three ordinary fuel buckets for the return. Check the actual rocket gauge; do not spend your return reserve exploring.')
q('First Moon landing',None,'The Moon provides Desh for the next tier. Your first visit should establish a return point before a long mining expedition.',
 'Enter the rocket, use your jump key to launch, and choose the Moon. After landing, sneak-right-click the lander to retrieve your rocket and cargo. Secure the site and check oxygen before leaving.',
 'Ordinary torches and exposed crops are unsuitable for the Moon. Keep your suit equipped until a shelter is demonstrably safe.',practice=True)
q('Bring back Desh','ad_astra:desh_ingot','Desh unlocks better infrastructure and the Tier 2 rocket. Bringing a modest sample home proves the whole travel loop works.',
 'Mine Desh, process it with a recipe shown in JEI, then make a return trip using your reserved rocket, pad and fuel.',
 'Mark your landing site. A waypoint is navigation help, not a substitute for oxygen or a working return vehicle.',practice=True)
q('Build a breathable room','ad_astra:oxygen_distributor','An Oxygen Distributor makes a sealed room habitable when it has water and power. It is a base system, unlike the loader used for suit supplies.',
 'Build a small sealed room. Connect a powered Water Pump over an infinite source to the distributor, power both machines, and use the distributor\'s Show function to verify coverage and leaks.',
 'Cables and ordinary pipes may leave openings. Use the appropriate ducts through walls and check the room before removing your suit.',practice=True)
q('Measure the environment','ad_astra:ti_69','Habitability involves oxygen, temperature and gravity. A room that looks enclosed may still be unsafe.',
 'Use the Ti-69 to inspect local conditions. Add an Oxygen Sensor if you want a redstone status indicator; inspect its detection mode and compare the reading inside and outside the shelter.',
 'Use airlocks and confirm conditions after modifying walls. Treat a newly opened doorway as a reason to recheck life support.',practice=True)
q('Tier 2: Mars','ad_astra:tier_2_rocket','Mars is the next resource step after the Moon. Desh components enable the rocket needed to reach it.',
 'Assemble a Tier 2 Rocket using the NASA Workbench recipe. Repeat preflight checks, travel to Mars and obtain Ostrum for the next stage.',
 'Reuse your checklist on every trip. A better rocket does not automatically fill your suit or carry spare fuel.',practice=True)
q('Improve fuel and power','ad_astra:cryo_freezer','Cryo Fuel can make repeated flights more efficient, while solar generation helps support remote installations.',
 'Inspect Cryo Freezer recipes for ice-related inputs and produce a batch. Check how much your rocket needs, then retain a separate return supply. Inspect Solar Panel output on your chosen world.',
 'Generation varies with location and atmosphere. Size energy storage for periods when your source cannot support the base.',practice=True)
q('Protect against heat','ad_astra:netherite_space_suit','Hot planets require equipment beyond the basic space suit. Their resources should not be pursued with an untested outfit.',
 'Use Ostrum progression to obtain the upgraded space equipment shown in the Astrodux. Complete and fill the full upgraded set before planning a hot-world landing.',
 'A netherite chestplate from another mod is not the Netherite Space Suit. Verify the exact item names and full outfit.')
q('Tier 3 and Calorite','ad_astra:tier_3_rocket','The next rocket tier reaches the hot worlds where Calorite supports late spacecraft and equipment.',
 'Assemble a Tier 3 Rocket, verify your heat-capable suit, oxygen and return kit, then select the intended hot-world destination. Bring back Calorite and inspect its uses.',
 'Do not use a test of armor protection as your first survival experiment on Venus. Confirm the Astrodux requirements before departure.',practice=True)
q('Tier 4: Glacio','ad_astra:tier_4_rocket','Calorite enables travel beyond the initial solar system and completes the core rocket-tier progression.',
 'Build the Tier 4 Rocket, use the planet screen to travel toward Glacio, and establish a marked landing site. Measure local conditions rather than carrying assumptions over from the Moon.',
 'Bring a return kit even for a world with breathable oxygen. Breathable air does not create fuel or a landing pad for you.',practice=True)
q('An orbital outpost',None,'A space station is a platform for a permanent orbital base, with different movement and life-support needs from a planet.',
 'Inspect the station construction requirements in the planet screen. Create a station when supplied, secure walkways, then establish power and verified oxygen coverage before expanding.',
 'In low or zero gravity, control your momentum and keep solid boundaries nearby. A Gravity Normalizer is optional infrastructure with its own power cost.')
q('Project: repeatable expedition',None,'The real milestone is a trip you can repeat without rebuilding your preparation process every time.',
 'Create a labeled launch-supplies chest, maintain fuel and oxygen reserves, and complete an outbound-and-return trip. Leave one small outpost with a documented power and life-support arrangement.',
 'If something fails, check fuel, suit oxygen, environmental protection, machine power, water supply and sealing separately.',practice=True)

chapter('advanced_rs','Refined Storage: Working Systems','refinedstorage:pattern_grid',
 'Refined Storage turns inventories into a searchable network and can schedule crafting through patterns and machines. This companion chapter focuses on reliable production and the installed addons. The original Refined Storage chapter still covers the basic components.',
 'working network -> machine autocrafting -> stockkeeping -> extra resource types -> wireless, kitchen and building integrations -> a dependable automated workshop.')
q('A network you can explain','refinedstorage:controller','A controller, storage and grid have different jobs. Understanding those jobs prevents a full disk or disconnected cable from looking like a recipe bug.',
 'Build or inspect a powered network with a Controller, Disk Drive, storage disk and Grid. Insert a small stack, retrieve part of it and check capacity and energy usage.',
 'Do not store your only network-repair materials inside a network that has no backup power.',practice=True)
q('External storage priorities','refinedstorage:external_storage','External Storage makes existing drawers or inventories visible to RS; it does not turn them into unlimited disks.',
 'Attach External Storage to a test inventory. Check filters, access mode and priority, then insert a known stack through the grid and see where it goes.',
 'Use a disposable test stack before linking bulk storage. Avoid letting another network expose this same network back to itself.',practice=True)
q('Encode a simple pattern','refinedstorage:pattern_grid','A pattern tells RS how inputs become outputs. Start with a normal crafting recipe before adding machines or fluids.',
 'Use a Pattern Grid and blank Pattern to encode a simple recipe such as planks into sticks. Put it into an Autocrafter and request one craft from the grid.',
 'Keep a small buffer of raw materials. A pattern does not supply ingredients on its own.',practice=True)
q('Choose the correct recipe',None,'Several mods can use the same ingredient arrangement. A wrongly encoded result can make an otherwise valid crafting network produce the wrong thing.',
 'In a Crafting Grid or Pattern Grid, inspect the recipe-selection button added by RS Polymorph when ingredients match multiple recipes. Choose the intended result and verify the printed pattern\'s output.',
 'Test the resulting pattern once. Recipe selection solves ambiguity; it does not make missing ingredients or unavailable recipes appear.')
q('Your first machine pattern','refinedstorage:autocrafter','Processing patterns describe an external machine operation. The network must both deliver ingredients and receive the promised result.',
 'Choose one simple furnace-like recipe. Encode the actual input/output amounts as a processing pattern, point an Autocrafter at the machine\'s input or a buffer, and return output through an Importer. Request one batch.',
 'Keep the return path separate from the input path. If results never re-enter RS, the job can remain waiting even when the machine finished.',practice=True)
q('Diagnose a stalled craft','refinedstorage:autocrafting_monitor','The monitor separates missing ingredients from a processing job that is waiting on output.',
 'Inspect a small job in the Autocrafting Monitor. Follow the route from pattern to machine input, power/redstone state, output slot and Importer. Correct the first failing step before retrying.',
 'Do not repeatedly request the same stalled job. Check the queue and return any stranded ingredients before canceling or restarting.',practice=True)
q('Keep a useful item stocked','rsrequestify:requester','Requestify schedules crafts when stock falls below a target. It turns an on-demand recipe into a replenishment system.',
 'Connect a Requester to RS, select an item with a tested pattern and set a small target such as one stack. Remove a few items and observe a replacement job and restored stock.',
 'Start with a modest target. Stockkeeping can consume all available ingredients if you configure many large targets at once.',practice=True)
q('Scale after measuring',None,'ExtraStorage and Cable Tiers improve machine capacity and throughput. They are useful only after the underlying recipe and return path work.',
 'Identify whether your bottleneck is pattern slots, transfer speed, machine speed or power. Inspect the relevant upgraded Autocrafter, Importer or Exporter in JEI and upgrade just that bottleneck.',
 'A faster importer cannot speed up a slow furnace. Compare one timed batch before and after an upgrade.')
q('Use fluids directly',None,'Fluid substitution can avoid filling and emptying buckets for suitable recipes, but the stored fluid and the pattern must agree.',
 'Choose a recipe supported by Refined Fluid Substitution. Read its pattern item/interface, provide the required fluid in network storage, then request a single test craft and inspect consumption.',
 'Do not assume every bucket recipe supports substitution. Keep the original recipe available until the fluid-based version has succeeded.')
q('Refined Types: energy','refinedtypes:64k_energy_storage_disk','Refined Types lets the network store additional resource types. An energy disk is a resource store; the RS Controller still needs operating power.',
 'Create a small Energy Storage Disk, install it in the network and inspect the energy resource view. Configure a compatible transfer connection to a small energy source or buffer and verify the stored amount changes.',
 'Keep the Controller powered independently while learning this. The Network Energizer can consume energy stored on disks to sustain the network; test it with a charged reserve and retain an external recovery supply.',practice=True)
q('Refined Types: Source','refinedtypes:64b_source_storage_disk','Ars Nouveau Source is distinct from FE and ordinary fluid. It needs the relevant resource storage and a compatible connection.',
 'Install a Source Storage Disk. Connect a small Ars Source supply using the supported interface, inspect the Source channel in the grid, then test extraction to a consumer.',
 'If no Source moves, check the connection\'s resource type and whether the neighboring block exposes a supported capability.',practice=True)
q('Refined Types: Souls','refinedtypes:1k_soul_storage_disk','Industrial Foregoing Souls is another resource channel, not item experience or a mob stored in a Soul Vial.',
 'Inspect the Souls system in the Industrial Foregoing chapter first. Add a Soul Storage Disk when you have a real producer/consumer, then test one supported transfer in each direction.',
 'A Regulator Upgrade can prevent an Exporter dumping all Souls into a connected soul pipe. This optional branch is not required for ordinary item autocrafting.',practice=True)
q('Mekanism chemicals',None,'Mekanism integration provides chemical storage and transfer. Chemical channels are separate from ordinary fluids and from Refined Types\' Source.',
 'Choose one chemical you already produce. Inspect the Mekanism integration disks and supported transfer settings, add suitable storage, and test a small transfer between the network and a machine.',
 'Use the machine\'s chemical-side configuration. A fluid pipe connection is not evidence that a chemical output is exposed.')
q('One wireless workspace','universalgrid:wireless_universal_grid','Universal Grid combines useful wireless network views; range and access still depend on your network equipment.',
 'Charge and link a Universal Grid using its tooltip/interface, then test storage and crafting-monitor views near your transmitter. Add the installed interdimensional transmitter when ready for remote access.',
 'Wireless access still needs a loaded, powered network. Test ordinary local access before crossing dimensions.',practice=True)
q('Your inventory and the network',None,'Refined Wireless Upgrades adds convenience transfers and collection behavior. Powerful collection rules can also move things you meant to keep.',
 'Inspect its upgrades in JEI and choose one small convenience feature. Configure filters and test it with a few ordinary blocks before enabling it during an expedition.',
 'Exclude tools, building reserves and special component-bearing items until you understand the transfer rules.')
q('Cook from storage',None,'Refined Cooking connects Cooking for Blockheads kitchens to RS ingredients, so food preparation can use your central supplies.',
 'Place a Kitchen Station as part of the kitchen, a Kitchen Access Point on RS, and use the Kitchen Network Card to link them as described by their interfaces. Make one meal using stored ingredients.',
 'Confirm the ordinary kitchen works first. A connected storage network cannot replace the kitchen blocks a recipe needs.')
q('Build from storage',None,'Refined Construction Sticks lets building tools draw blocks from RS. This reduces inventory refills while keeping construction intentional.',
 'Inspect the addon\'s items and the stick\'s tooltip, configure network access, and build a small wall using a known stored block. Watch both the placed result and the network count.',
 'Keep a small manual supply until the connection is proven. Avoid testing with a rare decorative block or a huge placement area.')
q('Supply a Schematicannon',None,'Refined Schematics adds a Cannon Interface to feed a Create Schematicannon from RS.',
 'First make a tiny Create schematic and verify a normal cannon setup. Add the Cannon Interface and configure its connection, stock the required blocks in RS, then run the small build.',
 'Check the cannon\'s material list and build options before starting. A supply interface does not validate what the schematic will replace.')
q('Search and capacity tools',None,'Search History saves repeated queries. Storage Warnings helps catch disk and storage-block capacity problems before inserts fail.',
 'Use the grid search history to repeat a query. Inspect the warning triangle and per-resource settings. Compare free capacity for items, fluids and any extra resource channels you actually use.',
 'External storage is not included in the warning addon\'s capacity checks. Check drawer limits separately.')
q('Project: a small production cell',None,'A reliable system combines a tested pattern, sufficient inputs, clear output return and sensible stock targets.',
 'Automate one useful product through a real machine, keep a small stock with Requestify, access it wirelessly and demonstrate recovery from a missing-input condition. Write down the machine sides and return route.',
 'Keep your existing RS basics chapter as reference. Expand only after this cell runs correctly through several batches.',practice=True)

chapter('economy','DynEco: Trade and Play','dyneco:market_tablet',
 'DynEco adds an in-game market with simulated buyers, listings and changing prices. It helps turn surplus production into purchasing power. Gamble It is connected by your local addon to this same wallet; there is no separate deposit currency.',
 'tablet and power -> inspect prices -> a small purchase and sale -> linked storage and automation -> wallet checks -> optional casino rules. No quest requires a gambling win.')
q('Craft the Market Tablet','dyneco:market_tablet','The tablet is the market interface. It needs energy, so crafting it alone is not enough to start trading.',
 'Craft the Market Tablet with the current JEI recipe. Charge it in an FE charger, or use its supported redstone-block charging interaction, then right-click with it to open the market.',
 'If the interface does not open, check charge and the item\'s tooltip before changing economy settings.',practice=True)
q('Know your wallet',None,'A wallet balance is purchasing power, not inventory space. New DynEco accounts use the configured starting balance; this guide grants no extra credits.',
 'Inspect your balance in the tablet and compare it with /dyneco balance. Note the display currency and base-credit value before testing transactions.',
 'The casino always uses whole base credits. A different DynEco display currency can make the displayed numbers look different without changing the underlying money.')
q('Read a price before buying',None,'The broad market includes many machines and tools. A listed base item price is not a valuation of its enchantments, stored contents or upgrades.',
 'Search a common resource and inspect its current buy/listing information. Compare a few related materials and choose an inexpensive test purchase.',
 'Start with plain resources and empty replaceable machines. Do not use a unique upgraded tool as your first market experiment.')
q('Your first small purchase',None,'A tiny purchase lets you verify price, quantity, payment and delivery before committing a large balance.',
 'Buy a small quantity of an ordinary material. Check the confirmation, wallet change and delivered items. Locate the items before making a second order.',
 'Read quantities carefully. If a transaction seems delayed, inspect the current screen and order state rather than repeatedly clicking buy.')
q('List a surplus item',None,'Selling to simulated buyers is not the same as instantly exchanging every stack for cash. Listings may need time to find buyers.',
 'List a small surplus stack of a common resource. Record the starting balance and quantity, then inspect the listing after time passes and confirm an actual sale.',
 'Unsold listings are not earned credits. Keep materials needed for your next machine outside the first experiment.')
q('Supply, demand and patience',None,'Dynamic prices reward checking the market. Flooding one item or buying a large quantity can behave differently from a single small transaction.',
 'Observe the same item across a few ordinary trades. Compare demand, available supply and the displayed price without assuming a fixed sell value forever.',
 'Use the market to support your progression. A price derived from recipes is not a hand-balanced appraisal of every ATM10 machine.')
q('Link a storage chest','minecraft:chest','Linked storage makes repeated transfers easier, but the chosen chest should contain only the goods you intend to trade.',
 'Place a dedicated trade chest and sneak-right-click it with the tablet to link it. Verify the selected storage and test with a few low-value items before setting automation.',
 'Name or label the chest. Keeping your workshop\'s only tools in a trading chest is an easy way to sell something you still need.',practice=True)
q('Automate one export',None,'Automatic selling is most useful for genuine surplus from a renewable production line.',
 'Configure one ordinary item for automatic selling from the linked storage. Feed it a small batch, observe listings and completed sales, and check the resulting wallet change.',
 'Keep a reserve upstream. Let your production fill a buffer before diverting surplus to the trade chest.')
q('Buy to a budget',None,'Automatic buying should solve a known shortage without consuming the balance reserved for other projects.',
 'Inspect the tablet\'s automatic-buy controls and configure a small bounded requirement if suitable controls are available. Otherwise use manual purchases. Verify the item and storage destination.',
 'Do not enable an open-ended buying rule just to complete a quest. The goal is a predictable supply cost.')
q('When an item is missing',None,'The broad-market rules still exclude selected creative/admin items and honor DynEco\'s deny lists. Some resources can also lack useful pricing data.',
 'Check the item\'s exact ID with advanced tooltips and search again. If you have permission, /dyneco why <item_id> and /dyneco price <item_id> can explain eligibility or pricing.',
 'A missing market entry does not mean the item is absent from the pack. JEI and the mod\'s normal progression remain available.')
q('Project: a modest trade loop',None,'A useful economy setup has a clear input, retained reserves, sales and a practical purchase at the end.',
 'Produce a renewable resource, keep a reserve, sell a small surplus and spend part of the proceeds on something your next project needs. Confirm that your remaining balance matches your expectations.',
 'This is the main economy capstone. Everything below is an optional casino guide and is not required for the trading workflow.',practice=True)
q('Optional: open the casino',None,'Gamble It provides several chance-based games. In this profile, the wallet bridge makes bets and winnings change DynEco directly.',
 'Press F8 while in the world. If necessary, find Casino Mod > Open Casino in Controls. Compare the displayed whole-credit balance with your DynEco wallet before selecting a game.',
 'One casino credit equals one DynEco base credit; fractional cents stay in the wallet. The original item deposit/shop is disabled. Buy and sell through the Market Tablet.',optional=True,deps=[3])
q('Optional: read a game first',None,'A game\'s rules and payout display tell you what the selected stake means. Different games do not offer the same outcomes.',
 'Open Coin Flip or Slots and inspect the bet controls, rules and displayed results. You can complete this reading task without placing a bet.',
 'A losing result is normal gameplay, not proof that the wallet bridge is broken. No strategy here promises profit.',optional=True)
q('Optional: staged rounds',None,'Mines, Blackjack and Crash involve choices during a round. Their in-game cash-out controls remain available even though the separate item shop is disabled.',
 'Read the chosen game\'s instructions and locate its round controls before starting. If you play, finish the round while connected and then inspect the wallet.',
 'Gamble It discards unfinished sessions on logout without a refund. Close out active rounds before leaving the world.',optional=True)
q('Optional: a tiny wallet test',None,'A controlled test checks integration without making a win a progression requirement.',
 'If you want to play, choose the smallest accepted stake and finish one round. Compare the wallet before and after, accounting for the displayed payout. Otherwise inspect the rules and acknowledge that you skipped the wager.',
 'Market sales can also change the balance while the casino is open. Use a quiet test period when checking the arithmetic.',optional=True)
q('A useful stopping point',None,'The economy and casino share money. A budget for entertainment is separate from the resources you need to finish your colony or workshop.',
 'Choose a reserve for your next practical build and keep it available. Return to trading, crafting or exploration after your chosen session; the guide has no repeated betting or jackpot requirement.',
 'If you need a repair, report the game, stake, before/after base-credit balance and whether automatic sales were active.',optional=True)

chapter('enderio','Ender IO: Compact Automation','enderio:alloy_smelter',
 'Ender IO provides processing machines, alloys, compact conduit networks and soul-based automation. Its strength is fitting several transport systems into a small space while keeping filters and machine sides under control.',
 'machine parts and power -> alloys and crushing -> conduits -> automatic processing -> soul tools and farming -> a compact production cell.')
q('Read the machine chain',None,'Ender IO\'s recipes and available machines differ across releases. This installed 8.2 version should be learned through its actual JEI categories.',
 'Search @enderio in JEI. Inspect the Alloy Smelter, SAG Mill, chassis and capacitor recipes, then identify which starting resources your workshop can already produce.',
 'Do not follow an old guide\'s machine name blindly. Use the exact item shown by this pack and inspect all recipe tabs.')
q('Power and a buffer','enderio:basic_capacitor_bank','A capacitor bank stores FE and gives your processing machines a visible energy buffer.',
 'Connect a Basic Capacitor Bank to an available FE source, configure its input/output faces and power one machine. Watch the stored energy while the machine processes.',
 'Stored energy is not generation. If the bank drains steadily, improve supply or reduce simultaneous machine demand.',practice=True)
q('Alloy Smelter','enderio:alloy_smelter','The Alloy Smelter combines materials into the alloys used throughout Ender IO.',
 'Supply power and any capacitor required by the machine interface. Select an alloy recipe in JEI, insert the exact ingredients and collect the output.',
 'Check the machine\'s smelting mode and redstone control if it processes an unexpected recipe or stays idle.',practice=True)
q('Build an alloy shelf','enderio:energetic_alloy_ingot','Different alloys unlock different devices. Keeping a small sample of each useful tier makes the progression easier to see.',
 'Inspect Energetic, Pulsating, Redstone and Conductive Alloy uses. Make the alloy needed for your next machine or conduit rather than crafting every available metal at once.',
 'Tag substitutions are recipe-specific. Verify the accepted ingredient before automating alloy production.')
q('SAG Mill processing','enderio:sag_mill','The SAG Mill handles crushing recipes and can provide different outputs from ordinary smelting.',
 'Power the mill, inspect the desired recipe in JEI and process a small sample. Read the output amounts and any optional grinding-ball effects before supplying a bulk input.',
 'A grinding ball is an optimization, not permission to assume every ore doubles. Check the displayed recipe and secondary outputs.',practice=True)
q('Machine sides and slots',None,'A machine can have power and ingredients nearby while still exposing the wrong input or output face.',
 'Inspect the machine\'s side configuration. Set a clear input face and output route, then test each with an ordinary inventory before connecting a complex conduit bundle.',
 'Keep a chest at the output during testing. Visible intermediate results make it easier to diagnose where a stack stopped.')
q('Item conduits','enderio:conduit','Item conduits move resources between inventories using per-connection settings.',
 'Connect two test chests with Item Conduits. Set the source connection to extract and the destination to insert, choose matching routing settings and check redstone behavior. Move a small stack.',
 'A connected cable is not an enabled extractor. Inspect both ends when nothing moves.',practice=True)
q('Filter before expanding',None,'Filters stop a shared pipe from moving every item in a machine or storage chest.',
 'Add an appropriate item filter at the relevant connection. Allow one test material, put a different material beside it and verify that only the intended stack moves.',
 'Use separate routing colors/channels where supported for unrelated flows. Keep inputs and finished outputs from feeding each other in a loop.')
q('Energy beside items',None,'Conduit bundles can combine different transport types in the same space, reducing cable clutter.',
 'Add the installed energy conduit type to a short tested item-conduit route. Connect a machine, configure its power faces and verify both item movement and energy delivery.',
 'A compact bundle still contains separate transport rules. Debug the energy route independently of the item route.')
q('Fluids and dedicated lines',None,'Fluid routing has its own tanks, accepted fluids and extraction settings. Mixing incompatible fluids can stall processing.',
 'Use the fluid conduit type suited to your needs. Move one ordinary fluid between two tanks and verify the amount and direction before connecting an Ender IO fluid machine.',
 'Keep a single-fluid test network first. Check whether the chosen conduit tier supports the behavior you want.')
q('Capacitors and throughput',None,'Machine capacitors and upgrades can change performance and energy demand. Faster operation is useful only when inputs and power keep up.',
 'Compare the machine\'s supported capacitor options in JEI and its GUI. Upgrade one machine, run the same small recipe batch and compare its energy use and completion time.',
 'Loot capacitors can have different properties. Read their information rather than treating every capacitor as an identical tier.')
q('Project: automated alloy',None,'A repeatable alloy setup combines controlled ingredients, a powered smelter and a reliable output route.',
 'Feed one tested alloy recipe from a dedicated input chest and return its output to a separate chest or RS. Run several batches and confirm ingredients do not overfill unintended slots.',
 'For RS, encode the real input/output quantities as a processing pattern. Do not let an independent stock system endlessly refill the same machine input.',practice=True)
q('Capture a sample soul','enderio:soul_vial','Soul Vials carry eligible creatures for Ender IO\'s soul-based recipes. This is different from the numeric Souls resource in Industrial Foregoing.',
 'Craft a Soul Vial, read its tooltip and inspect recipes that use captured entities. Choose an eligible ordinary creature and test the capture interaction.',
 'Inspect the filled vial\'s entity information before using it. Different recipes require different creatures.',practice=True)
q('The Soul Binder','enderio:soul_binder','The Soul Binder combines a captured soul with ingredients to produce specialized components.',
 'Inspect a Soul Binder recipe in JEI, including its entity and XP requirements. Supply the machine\'s needs and complete one recipe that supports your next device.',
 'If progress does not begin, check entity type, ingredients, energy, capacitor and required experience separately.',practice=True)
q('Powered spawning','enderio:powered_spawner','A Powered Spawner is a controllable mob-production system with substantial power and containment needs.',
 'Follow the installed recipe path for configuring the desired mob. Build a contained test chamber, provide a stop control, and run a short spawning test only after you have a collection/handling plan.',
 'Check eligible mobs and space conditions. Start with an ordinary target and keep the farm disabled while editing it.',practice=True)
q('Experience handling','enderio:xp_obelisk','An XP Obelisk provides a dedicated experience buffer for your own use and compatible workflows.',
 'Place the obelisk, inspect deposit/withdraw controls and test with a small amount of experience. Identify the XP form accepted by any connected machine before adding pipes.',
 'XP Juice, ordinary fluid and unrelated experience resources are not automatically interchangeable.',practice=True)
q('A Farming Station','enderio:farming_station','The Farming Station can automate supported plants when supplied with the required tools, power and inventory space.',
 'Place it beside a small suitable growing area. Provide the requested tools and seeds/saplings, configure the farm, and watch a complete harvest and replant cycle.',
 'Reserve seeds or saplings for replanting and leave output capacity. A full inventory can look like a broken farm.',practice=True)
q('Choose a specialist device',None,'Ender IO also offers utility devices such as chargers, tanks, enchanting and obelisks. These should solve a need in your base.',
 'Inspect the Enchanter, Wired Charger and available obelisks in JEI. Choose one useful device, read its requirements and prove its function with a small test.',
 'Skip devices you do not need yet. The goal is understanding their role, not crafting every item in the mod.')
q('Project: compact workshop',None,'A good compact system remains understandable after the cables are hidden.',
 'Combine your tested alloy or crushing setup with item return, power buffering and a visible stop control. Label its inputs and outputs, then demonstrate how you diagnose a missing-input or power problem.',
 'Keep machine access faces reachable. Hide conduits only after filters, directions and recovery behavior are proven.',practice=True)

chapter('astral','Astral Sorcery: Read the Sky','astralsorcery:tome',
 'This Astral Sorcery 2.0 port uses constellation discovery, focal points, staged altars, Liquid Starlight and lumen networks. It differs substantially from older Astral Sorcery tutorials. The bundled Tome is the primary reference for structures and unlocking knowledge.',
 'Tome and Astrolabe -> focal-point crafting -> Illuminated and Resonating tables -> Luminous altar and attunement -> lumen and focused starlight -> Iridescent crafting.')
q('Open the living Tome','astralsorcery:tome','The Tome reveals more as your knowledge advances. A dark entry can indicate an unmet discovery or progression condition.',
 'Craft the Tome, open its research chart and read Welcome, Ores and Astrolabe. Follow its connections alongside these quests; use its structure and recipe pages for exact layouts.',
 'These quests explain the current port. Old instructions involving a different telescope or altar sequence may not apply.')
q('Marble and Aquamarine','astralsorcery:aquamarine','Early tools and structures need Astral materials. Aquamarine comes from shale around suitable waters; Marble supplies precise structural blocks.',
 'Find Aquamarine Shale and gather Aquamarine. Collect the mod\'s Marble and inspect the cut variants in JEI. Keep raw and decorative forms organized for future structure recipes.',
 'A similar white stone from another mod is not a valid substitute for an Astral structure block unless explicitly accepted.')
q('Study constellation paper','astralsorcery:constellation_paper','A constellation drawing tells you a pattern and its visible moon phases. Reading paper is not the same as discovering the stars.',
 'Find Constellation Paper in exploration loot and study it with right-click. Note its shape and moon phases, then check the matching entry in the Tome.',
 'Keep a paper reference while observing. If the constellation is absent tonight, check the lunar schedule instead of repeatedly retracing it.')
q('Observe through an Astrolabe','astralsorcery:astrolabe','The Astrolabe helps discover constellations and locate the focal points used for early crafting.',
 'At a clear suitable night, look through it. Use the mouse wheel to adjust its angle marker. Hold sneak to trace the paper\'s constellation connections; release sneak to clear an incorrect attempt.',
 'Also search for a focal-point light column and look directly at it to record it. Bare patches in the grass can help you find candidate locations.',practice=True)
q('Find your focal point',None,'A focal point concentrates a constellation\'s light onto a world column. It is a location, not a block you craft and carry.',
 'Locate and mark a focal point using the Astrolabe at night. Clear a small working area there and keep its sky access open. Confirm its position before dropping recipe ingredients.',
 'Keep item collectors and magnets away while doing ground transformations; disturbing the recipe pile can stop the process.')
q('Make the Resonating Wand','astralsorcery:wand','The Wand starts starlight devices, reveals missing structure pieces and helps locate buried Rock Crystal Ore.',
 'Read the Tome\'s Wand recipe. Place its ingredients together on open ground at your focal point and let the transformation finish. Collect the Wand and test its structure-preview interaction later.',
 'Use the current recipe page for quantities. Do not try to craft this port\'s Wand by copying an old workbench recipe.')
q('Find a Rock Crystal','astralsorcery:rock_crystal','Rock Crystals have individual properties and support several later systems. They are not all equally valuable.',
 'Use the Wand\'s response to search deep underground. Mine the ore yourself with a suitable pick and collect the crystal nearby. Read its properties before choosing how to use it.',
 'The bundled Tome warns that crystals released without a nearby player can be lost. Save a good specimen instead of using it as your first disposable catalyst.')
q('Illuminated Crafting Table','astralsorcery:altar_illumination','Your first Astral table is made by a focal-point transformation and unlocks further knowledge when obtained.',
 'Follow the Tome recipe to transform a crafting table with the required materials at a focal point. Place the result, arrange a supported recipe and activate it with the Wand at night.',
 'This first table needs no surrounding multiblock. Do not build a later altar structure around it to compensate for an incorrect recipe.',practice=True)
q('Draw Liquid Starlight','astralsorcery:lightwell','The Lightwell extracts liquid from a catalyst. Liquid Starlight becomes a recurring crafting and infrastructure resource.',
 'Place a Lightwell with clear space above. Add Aquamarine or a crystal and collect Liquid Starlight when enough accumulates. Keep a modest reserve for your first upgrades.',
 'The catalyst cannot be recovered and eventually breaks. A block above the basin destroys it; pipes can draw from below.',practice=True)
q('Use starlight transformations','astralsorcery:starmetal_ingot','Starmetal and other transformed materials connect early focal-point work to later tools and altars.',
 'Inspect the Tome\'s Starmetal instructions and current JEI transformations. Produce the required material through a supported route, then inspect Stardust and Chisel uses.',
 'Do not infer every transformation from an item\'s name. Check the recipe type: table, focal point and infusion are different processes.')
q('Relay ingredients','astralsorcery:focus_relay','Focus Relays hold ingredients outside the table grid. Their physical placement lets an altar find them.',
 'Make relays and place them according to the next altar\'s structure page. Right-click to place an item; use an empty hand to retrieve it. Keep the air above each relay clear.',
 'Relays are not linked with the Linking Tool. Position matters; their stored ingredients appear in the altar interface.',practice=True)
q('Resonating table upgrade','astralsorcery:altar_resonance','This upgrade replaces the first table in place and requires a surrounding structure before it can work.',
 'Prepare the upgrade recipe, Liquid Starlight and the indicated marble/relay structure. Perform the nighttime upgrade, then use the Wand to reveal any missing structure pieces.',
 'Start with the smaller required layout. Later recipes can demand the expanded outer ring and additional ingredients.',practice=True)
q('Infusion and a chalice','astralsorcery:infuser','The Starlight Infuser uses a structure and surrounding liquid pools to transform materials. A chalice can supply liquid and spare the pools.',
 'Build the exact Tome layout, fill every required pool, place a supported input and activate with the Wand. Refill consumed liquid between crafts, or configure a nearby Containment Chalice.',
 'The Infuser works day or night; missing liquid or structure blocks will not be fixed by waiting for midnight.',practice=True)
q('Luminous Crafting Altar','astralsorcery:altar_luminance','The Luminous tier expands the structure again and introduces a constellation-focus slot for later recipes.',
 'Follow the upgrade page: prepare the outer relays, ground ingredients and nearby chalices before starting. Finish the larger structure and inspect the focus slot in the new altar.',
 'Some later recipes consume an attuned focus crystal. Read that requirement before using your best crystal.',practice=True)
q('Attune yourself','astralsorcery:attunement_altar','Attunement opens a constellation\'s perk path. The altar is a separate structure from your crafting altar.',
 'Build the open-sky plaza shown in the Tome. At night, hold the correct paper to place relays in its pattern. Once the discovered constellation is visible and the pattern lights, stand on the altar without sneaking.',
 'Read the available paths before choosing. Attunement is not something to change casually with an unfamiliar reset item.',practice=True)
q('Attune a crystal',None,'An attuned crystal carries a constellation identity for altar recipes and focused-starlight equipment.',
 'With the attunement pattern active under the correct constellation, drop a Rock or Celestial Crystal onto the altar. Retrieve and inspect the resulting attuned crystal.',
 'Label or separate crystals by constellation. A valid crystal with the wrong attunement still cannot satisfy a recipe that asks for another focus.')
q('Produce your first lumen','astralsorcery:lumen_array','Lumen is typed magical energy derived from Liquid Starlight and constellation flowers. Each array becomes associated with its produced type.',
 'Fill a Lumen Array with Liquid Starlight, add a suitable flower catalyst and watch its reserve grow. Build separate arrays for different types rather than trying to switch one repeatedly.',
 'Arrays need neither sky nor a multiblock. They slow near empty/full reserves; redstone stops production but does not make the catalyst permanent.',practice=True)
q('Move and bind lumen','astralsorcery:lumen_filament','Generating lumen is only useful when a consumer can receive the required type. Filaments form the distribution network.',
 'Read the Tome\'s filament and binding pages, connect one producer to one supported consumer and demonstrate an effect or stored amount changing. Then inspect the Lumen Crystallizer and binding recipes.',
 'Prove one short connection before building a web. Compare resource type, reach and consumer requirements when nothing flows.',practice=True)
q('Focused starlight','astralsorcery:starlight_focus_rock_crystal','A Starlight Focus Crystal supplies a constellation\'s starlight when it sits in a matching focal-point column.',
 'Make a focus from an appropriately attuned crystal, place it at a matching focal point with sky access, and use the Linking Tool to link a nearby valid target with clear line of sight.',
 'The constellation must be present for its flow. Multiple links share output; this network is different from lumen filaments.',practice=True)
q('Combine lumen aspects','astralsorcery:lumen_alchemy_array','Alchemy Arrays combine nearby aspects into higher-tier lumen for stronger bindings and advanced crafting.',
 'Choose one second-rank lumen recipe in the Tome. Place the feeding arrays within direct reach and line of sight, provide starlight and the correct catalyst, then confirm the combined output.',
 'Filaments do not supply an Alchemy Array\'s recipe inputs in this port; its source arrays must be nearby directly.',practice=True)
q('Iridescent crafting','astralsorcery:altar_radiance','The final altar upgrade brings together liquid, lumen, focused starlight and a constellation focus.',
 'Read the full upgrade recipe before beginning. Prepare the required five basic lumen types, Armara starlight and focus, ground materials and chalices. Complete the larger structure and upgrade at night.',
 'The upgrade consumes its focus. Diagnose the four systems separately: structure, item ingredients, liquid and magical supply.',practice=True)
q('Choose a useful reward',None,'Late Astral progression offers tools, movement, enchantment support and stronger bindings. Choose something that serves your play style.',
 'Inspect the Iridescent Tools, Resplendent Prism and movement-wand pages. Craft one useful upgrade and test its actual ability in a small controlled area.',
 'Tool areas and special attacks can be larger than a normal action. Learn their controls before using them near your base.')
q('Project: a mapped observatory',None,'An observatory is maintainable when its focal points, constellations and resource networks are identifiable.',
 'Label your focal points and arrays, store paper references and backup catalysts, and complete one advanced recipe without guessing which system supplies it. Explain how you would restore it after a shortage.',
 'Use the Tome\'s live unlocks as the final authority. These guide tasks do not grant Astral research or bypass its discoveries.',practice=True)

chapter('sfm','Super Factory Manager: Program a Factory','sfm:manager',
 'Super Factory Manager moves items and other resources through a cable network according to a readable program. Labels describe inventories, and timed rules decide what moves, where it goes and how much stays behind. It is especially useful when one complicated production line would otherwise need many filters.',
 'manager and labels -> a two-chest transfer -> filters and limits -> a furnace line -> diagnostics and a maintainable factory.')
q('The manager and its program','sfm:manager','The Manager executes the program stored on a disk. Cables connect accessible inventories; the program supplies the transfer rules.',
 'Make a Manager, Program Disk, Inventory Cable and Label Gun. Place the Manager near two ordinary chests and connect both with cable. Open its interface and locate the disk editor and examples.',
 'Start with ordinary chests. Machine-side restrictions introduce a second problem before you have learned the language.')
q('Name the endpoints','sfm:labelgun','A label is a name the program uses to select network endpoints. A typo or missing label can make correct-looking code select nothing.',
 'Use the Label Gun controls shown in its tooltip to label one chest input and the other output. Apply/synchronize its labels to the Manager, then inspect the network to confirm both names.',
 'Use short, distinct names. When copying a setup, verify the Manager has the labels rather than assuming the gun alone configured it.',practice=True)
q('Your first working program','sfm:disk','A timed block repeatedly gathers candidate resources with INPUT and transfers them with OUTPUT. INPUT alone does not move items into a hidden buffer.',
 'Put a few cobblestone in input. Enter the example below, save the disk and run it. Confirm the cobblestone appears in output, then stop the program and move it back.',
 '20 ticks is about one second at normal server speed. An empty source or full destination is not necessarily a syntax error.',practice=True,
 code=['NAME "Two chest transfer"','EVERY 20 TICKS DO','  INPUT FROM "input"','  OUTPUT TO "output"','END'])
q('Read errors before changing hardware',None,'The editor can catch malformed syntax, while execution diagnostics reveal rules that select nothing or cannot transfer.',
 'Read the Manager\'s error/status display. Deliberately change input to an unused label, observe the result, then restore it. Compare that problem with a missing END in the editor.',
 'Change one thing at a time. A successful parse only proves the language is valid; it cannot guarantee your chest contains the requested item.',practice=True)
q('Filter by exact item',None,'Explicit identifiers prevent a broad transfer from emptying supplies that belong elsewhere.',
 'Change the input line to INPUT minecraft:cobblestone FROM "input". Put cobblestone and dirt together in the source and verify only cobblestone moves.',
 'Use the actual registry identifier from advanced tooltips or the network inspector. Display names and translated item names are not identifiers.',practice=True)
q('Keep a reserve',None,'Limits control the amount selected or delivered. A reserve prevents automation from taking every ingredient you need by hand.',
 'Open the bundled limits example and compare INPUT 5 RETAIN 3 minecraft:cobblestone FROM "input" with your unrestricted rule. Test a source of ten cobblestone and observe several cycles.',
 'An input limit applies per execution, not forever. RETAIN protects a stock level; a transfer of five repeated every second can still drain the rest.',practice=True)
q('Separate unrelated jobs with FORGET',None,'Within a trigger, selected resources remain available to later statements. FORGET clears that selection before another independent transfer.',
 'Read the bundled furnace_manager example and identify each FORGET between ingredients, fuel and results. Add a second independent transfer to your chest test, separated by FORGET.',
 'If a later output receives an unexpected earlier ingredient, inspect selection lifetime before adding more filters.',practice=True)
q('Respect machine faces',None,'Many machines expose different inventory slots from different sides. A cable connection does not make every slot available from every direction.',
 'Connect a vanilla furnace, an ore chest, a fuel chest and a result chest. Label them feed, fuel, furnace and results. Read the slots_and_sides example before attempting a transfer.',
 'For a vanilla furnace, top accepts smelting ingredients; bottom can extract results and accepts fuel through its exposed fuel slot. Modded machines may behave differently.',practice=True)
q('Run a small furnace line',None,'This program maintains a small ingredient buffer, supplies fuel and removes results without mixing the three jobs.',
 'Use the program below with the labels from the previous step. Add a few raw iron and coal, run it, then verify iron ingots reach results. Keep the output chest visible.',
 'Use plain coal for the first experiment. Fuel-container leftovers such as buckets deserve a separate tested rule.',practice=True,
 code=['NAME "Workshop furnace"','EVERY 20 TICKS DO','  INPUT FROM feed','  OUTPUT 8 TO EACH furnace TOP SIDE','  FORGET','  INPUT minecraft:coal FROM fuel','  OUTPUT RETAIN 1 TO EACH furnace BOTTOM SIDE','  FORGET','  INPUT FROM furnace BOTTOM SIDE','  OUTPUT TO results','END'])
q('Scale to several machines',None,'A shared label can represent several machines. EACH changes whether a quantity applies separately to each endpoint.',
 'Connect a second furnace under the same label. Compare distribution with the bundled limits and round_robin examples, then choose whether both furnaces should hold a small reserve or receive work in rotation.',
 'Do not assume the first matching inventory is the only target. Inspect how many endpoints carry a shared label before using a large transfer.',practice=True)
q('Inspect the live network','sfm:network_tool','The Network Tool reveals connections and endpoint details that are hard to see through walls or machine casings.',
 'Inspect one working chest and one machine with the tool. Locate its inventory inspection controls in the tooltip, then compare exposed slots and resource types from two sides.',
 'Use this evidence to choose sides and identifiers. Guessing slot numbers from the GUI can fail because internal inventory numbering differs.',practice=True)
q('Tags and families of ingredients',None,'Tags let one rule match a compatible family such as a category of ingots. This is useful only if the receiving recipe accepts that family too.',
 'Read the bundled tag_matching and filtering examples. Adapt one to a harmless chest sorting test, and verify both an intended match and an item that should stay behind.',
 'A broad tag can include valuable variants. Test with small quantities and inspect matches before connecting bulk storage.',practice=True)
q('Fluids are a separate resource type',None,'SFM can move supported resources besides items. A fluid rule needs fluid endpoints and the fluid resource type; an item rule will not move the contents of a tank.',
 'Connect two tanks and consult the bundled resource_types example. Test INPUT fluid::water FROM water_source followed by OUTPUT fluid:: TO water_destination inside a timed block.',
 'Label the tanks exactly as written. Verify exposed tank faces and available destination capacity before increasing the amount.',practice=True)
q('Energy and other integrations',None,'Supported resource types depend on the installed integrations. The live example and inspector tell you what this build can access.',
 'Open resource_types in the installed Manager and inspect its generated resource-type list. Choose an available energy integration and build a tiny source-to-buffer test using its exact syntax.',
 'Copy the installed example\'s type name rather than guessing from a web tutorial for another SFM version. Keep power distribution independent from item-selection state.',practice=True)
q('Pause on purpose',None,'A production line should be controllable when storage is full, ingredients are scarce or you want to work on the machine.',
 'Read the bundled redstone_signals and if_statements examples. Add one simple condition or use the Manager\'s run control to stop your furnace line, and confirm it resumes cleanly.',
 'Do not build a complicated condition until the unconditional transfer works. A stopped trigger and a failed transfer require different fixes.',practice=True)
q('Troubleshoot in a fixed order',None,'Most silent failures come from labels, resource matching, exposed sides or destination capacity.',
 'Check parse status, trigger timing, endpoint labels, source contents, filters, side/slot access and output space in that order. Temporarily reduce the line to one input and one output to isolate the fault.',
 'Keep a working copy of your program outside the disk before major edits. Comments and descriptive labels save more time than clever compressed code.')
q('Project: a readable processing cell',None,'A good SFM program is a small operating manual for your factory, not just a transfer that happened to work once.',
 'Run two furnaces with filtered input, retained fuel and a separate output. Demonstrate empty input, full output and restart behavior, then add comments explaining each block and save a backup copy.',
 'Use slower triggers for ordinary storage work. Increase frequency only when observation shows the transfer interval is the actual bottleneck.',practice=True)

chapter('xnet','XNet: Channels and Control','xnet:controller',
 'XNet combines item, fluid, energy and control routing through a compact cable network. A Controller holds channels; each channel defines a job and connector settings determine how each endpoint participates. It suits factories that need central configuration without writing a program.',
 'powered controller -> connected inventories -> item channel -> filters and faces -> fluids and energy -> multiple machines -> routers and a complete processing cell.')
q('Build the control point','xnet:controller','The Controller is where the network\'s channels are configured. It needs power and reachable connectors to do useful work.',
 'Craft a Controller, compatible network cable and connectors. Supply FE, connect two chests, and open the Controller to check that the endpoints are listed.',
 'Keep your first network in one loaded area and use one cable color. Different colored networks are intentionally separated.',practice=True)
q('Cable is the road; connectors are the doors',None,'A cable run links the network, while connectors expose adjacent blocks to the Controller. A cable merely passing a machine is not enough.',
 'Inspect where each connector touches its chest. Rename or otherwise identify the endpoints in your layout. Disconnect one temporarily and observe which entry disappears.',
 'Leave physical access to machine faces. A neat cable bundle is less helpful if it prevents you reaching the input side you need.',practice=True)
q('One channel, one job',None,'Channels describe the resource and transfer behavior. Starting with one job makes every setting easier to understand.',
 'Create an item channel. Configure one chest connection to extract and the other to insert, enable the channel, and transfer a few cobblestone.',
 'Check both the channel and endpoint settings when nothing moves. Listing an inventory in the Controller does not automatically assign a transfer job.',practice=True)
q('Filter before connecting valuables',None,'Filters limit which items a connection handles. An unrestricted extract can move everything in a mixed chest.',
 'Set a cobblestone filter at the extracting endpoint. Mix cobblestone and dirt in the source and confirm dirt stays behind. Inspect the available matching options before using tagged or component-bearing items.',
 'Use a small test stack of enchanted or named items when learning matching behavior; never assume all variants are interchangeable.',practice=True)
q('Make machine sides explicit',None,'Machine inventories are exposed according to their own side configuration. XNet cannot insert through a face that the machine refuses.',
 'Replace the destination chest with a powered processing machine. Set its input side, inspect the connector settings, and feed one known recipe ingredient.',
 'First prove the machine runs when supplied by hand. That separates recipe or power problems from transport problems.',practice=True)
q('Remove the finished product',None,'Supplying ingredients without extracting output eventually stops production. The return route is a distinct job worth checking on its own.',
 'Add an output connection/channel as needed. Configure extraction from the machine\'s output side into a result chest, then process several batches.',
 'Keep input and output filters distinct. Broad rules attached to the same inventory can circulate ingredients endlessly.',practice=True)
q('Stock levels and priorities',None,'Limits keep a machine supplied without hoarding the entire network\'s ingredients. Priority decides which eligible destination should be served first.',
 'Inspect the item connector\'s available count and priority controls. Give a primary machine a small stock target, add a second destination, and observe how a limited supply is shared.',
 'Test behavior at the target stock level and with a full destination. Priority is a routing preference, not an ingredient generator.',practice=True)
q('Give fluids their own channel',None,'Fluid movement follows tank capacity and exposed faces rather than item slots. Separate channels make the intended path clear.',
 'Connect two tanks, add a fluid channel and transfer water from one to the other. Set the relevant fluid filter and demonstrate that a full destination safely stops transfer.',
 'Confirm that the destination accepts the fluid. Similar-looking liquids from different mods can have different registry identifiers.',practice=True)
q('Distribute FE deliberately',None,'Energy channels let the same network power multiple machines, but the Controller and source must remain able to operate.',
 'Add an energy channel from a charged buffer to a machine. Observe the buffer and machine energy levels while processing. Keep a dependable supply to the Controller itself.',
 'A factory can fail because it lacks total generation even when every channel is configured correctly. Watch energy over several cycles, not just one moment.',practice=True)
q('Use control signals',None,'Redstone and channel conditions can stop production when a switch is off or a condition is not met.',
 'Read the installed XNet manual\'s channel and logic pages. Add one visible control condition to your test line and demonstrate enabled and disabled states.',
 'Add control after ordinary routing works. Record what the condition means so a future stopped machine is easy to diagnose.',practice=True)
q('When advanced connectors help',None,'Advanced connectors offer additional capability and higher transfer performance. They are useful where an ordinary connection is the measured bottleneck.',
 'Compare normal and advanced connector tooltips and settings in JEI/the Controller. Upgrade one busy endpoint and observe whether transfer behavior improves.',
 'A faster connector cannot accelerate a slow machine recipe or compensate for inadequate FE. Upgrade the constrained part of the system.',practice=True)
q('Separate neighboring networks',None,'Cable colors provide physical separation between systems that happen to pass near one another.',
 'Build a second short cable run in another color beside your test network. Confirm it does not silently become part of the first Controller\'s endpoint list.',
 'Choose a consistent color convention for production areas, then label it. Color alone does not describe the job of each channel.',practice=True)
q('Routers connect larger systems','xnet:router','A Router lets controllers exchange published channels through a routing network. It is an expansion tool after local channels work.',
 'Read the installed router manual page. Make two small working local networks, publish a test channel through the routing setup and connect the receiving controller according to the router interface.',
 'Use routing cables where required by the router setup. Do not treat a router as an ordinary longer cable and assume every channel is shared.',practice=True)
q('Wireless routing','xnet:wireless_router','Wireless routers extend routing between separated areas using an antenna arrangement. Antenna construction determines the supported range.',
 'Consult the wireless-router and antenna pages, build the described antenna above the router, and test a short link before increasing distance.',
 'Both ends still need functioning local routing, power and loaded chunks. Wireless reach does not automatically keep a remote factory loaded.',practice=True)
q('Trace a stalled transfer',None,'The Controller centralizes diagnosis: endpoint visibility, channel state, direction, filters, limits and conditions can all stop a transfer.',
 'Choose a stalled step and trace one item from source to destination. Verify source contents, extraction, enabled channel, insertion, machine side and free space. Inspect power lastingly, not only at idle.',
 'Temporarily use two chests to isolate the network from a complicated machine. Restore the machine only after the simpler route works.')
q('Project: one-cable processing cell',None,'A useful XNet cell combines distinct jobs while keeping them understandable in the Controller.',
 'Build a machine cell with FE supply, filtered ingredient input, output extraction and an on/off condition. Add a second machine without breaking the first, then name the channels and document their purpose.',
 'Keep a small buffer and a visible output while learning. Expand to a base-wide router network only after each local cell has predictable behavior.',practice=True)

chapter('computercraft','ComputerCraft: Useful Little Programs','computercraft:computer_advanced',
 'CC:Tweaked adds programmable computers, monitors and turtles using Lua. Advanced Peripherals connects those programs to more modded systems, including storage networks and colonies. Start with small programs you understand, then use them to observe or automate a specific job.',
 'terminal and editor -> Lua basics -> peripherals -> monitor -> inventory reports -> turtle movement -> Advanced Peripherals -> a safe, useful dashboard.')
q('Your first terminal','computercraft:computer_advanced','A computer gives you a shell for commands and an editor for Lua programs. The advanced model adds a color display and mouse support.',
 'Place the computer, open it and run help, then programs to see installed commands. Run edit hello.lua, enter the example, save and exit through the editor menu, then run hello.',
 'The editor menu is reached with Ctrl. Save changes before leaving; the shell runs the saved file, not unsaved text in the editor.',practice=True,
 code=['print("Hello, workshop!")'])
q('Values and a small calculation',None,'Lua variables store values and functions perform actions. A tiny calculation is easier to debug than a complete factory controller.',
 'Create supplies.lua using the example below. Change stacks and rerun it. Add another print line that explains the unit so you can interpret the result later.',
 'Quoted text is a string; an unquoted number can be used in arithmetic. Read an error\'s filename and line number before changing unrelated code.',practice=True,
 code=['local stacks = 3','local items = stacks * 64','print("Items in full stacks: " .. items)'])
q('Find connected peripherals',None,'Peripherals are devices a computer can call. A local side such as left or a wired network name identifies a specific device.',
 'Attach a monitor or another supported peripheral and run peripherals. Then run the example to list the names and types visible to this computer.',
 'A device on another cable network will not appear just because it is nearby. Use discovered names rather than inventing a device address.',practice=True,
 code=['for _, name in ipairs(peripheral.getNames()) do','  print(name, peripheral.getType(name))','end'])
q('A monitor that says something useful','computercraft:monitor_advanced','A monitor displays a program\'s output where you can see it without opening the computer.',
 'Connect an Advanced Monitor and run the example. Extend the screen with matching monitor blocks if desired, then adjust the text scale and layout only after the message appears.',
 'peripheral.find returns a matching device; with several monitors, use peripheral.wrap and a specific discovered name for predictable placement.',practice=True,
 code=['local m = peripheral.find("monitor")','assert(m, "Connect a monitor first")','m.clear()','m.setCursorPos(1, 1)','m.write("Workshop online")'])
q('Reach devices with a wired network','computercraft:cable','Wired modems and networking cable make distant peripherals accessible to one computer.',
 'Attach wired modems to the computer and a supported inventory or monitor, connect them with cable, and activate peripheral sharing on the relevant modem. Run peripherals again.',
 'Record the name printed when a peripheral is made available. A cable connection and an exposed peripheral are separate steps.',practice=True)
q('Inspect inventory without moving it',None,'Read-only reports are a useful first automation project because you can learn the API without rearranging storage.',
 'Expose a chest through the wired network and run the example. Compare the reported slots, item identifiers and counts with the chest contents.',
 'An inventory\'s list is indexed by occupied slots, so pairs is appropriate. An empty chest can legitimately print nothing.',practice=True,
 code=['local inv = peripheral.find("inventory")','assert(inv, "Expose a chest on the wired network")','for slot, item in pairs(inv.list()) do','  print(slot, item.name, item.count)','end'])
q('Discover methods before calling them',None,'Peripherals expose different functions. A storage bridge and a vanilla chest are not interchangeable APIs.',
 'Choose a name from peripherals and substitute it for the placeholder below. Inspect the returned method names, then consult that peripheral\'s documentation before calling a method with arguments.',
 'Method discovery tells you names, not parameter meanings. Begin with information queries before trying export, craft or movement methods.',practice=True,
 code=['local name = "REPLACE_WITH_PERIPHERAL_NAME"','assert(peripheral.isPresent(name), "Check the peripheral name")','textutils.pagedTabulate(peripheral.getMethods(name))'])
q('Repeat politely',None,'A repeating program must yield so the computer can handle events. Unbounded work without pauses can be terminated as too long without yielding.',
 'Run this bounded five-step loop, then adapt it to refresh a read-only value. Stop a running program with Ctrl+T when you need to regain the shell.',
 'Start with a finite loop while debugging. A one-second refresh is usually plenty for a status display.',practice=True,
 code=['for step = 1, 5 do','  print("Refresh " .. step)','  sleep(1)','end'])
q('Keep settings in a file',None,'Separating device names and thresholds from program logic makes a setup easier to maintain.',
 'Copy your working program before editing it. Use the built-in help for settings and files, then store one device name or threshold as a setting and read it back.',
 'Use list, copy and edit to inspect and preserve your files. Back up working code before making it run automatically.',practice=True)
q('Meet the turtle','computercraft:turtle_advanced','A turtle is a mobile computer with an inventory. Movement uses fuel unless the server configuration makes fuel unlimited.',
 'Place it in a clear test area, give it a label with label set GuideTurtle, inspect its inventory and use the refuel program with suitable fuel. Run the example to attempt one forward move.',
 'A failed move returns a reason; handle it rather than assuming movement succeeded. Keep a labeled starting position and avoid edges while testing.',practice=True,
 code=['print("Fuel:", turtle.getFuelLevel())','local ok, reason = turtle.forward()','print(ok, reason)'])
q('Inspect before digging',None,'A turtle program should know what is ahead before it breaks blocks. A failed action must not silently corrupt its idea of its position.',
 'Place a disposable block in front of the turtle and run turtle.inspect in a small program. Print the returned block name when inspection succeeds, then try with empty space.',
 'Keep mining experiments outside your base. Never turn an untested movement loop into an unattended quarry.',practice=True,
 code=['local found, block = turtle.inspect()','if found then','  print(block.name)','else','  print("No block in front")','end'])
q('A bounded turtle job',None,'Useful automation needs a stopping condition, fuel awareness and a plan for full inventory or blocked movement.',
 'Write a three-step movement experiment that stops immediately on a failed move and prints the reason. Run it in a clear marked lane, then intentionally block the lane and test again.',
 'Only add digging, placement or harvesting after movement and failure handling work. Keep the first job small enough to inspect by eye.',practice=True)
q('Connect Refined Storage','advancedperipherals:rs_bridge','The RS Bridge exposes supported Refined Storage information and operations to a computer. The storage network still needs its ordinary power and connections.',
 'Connect the bridge to your working RS network and computer. Discover its peripheral name and methods, then use the installed-version documentation to query a small piece of network information.',
 'Begin read-only. Export and crafting methods can consume resources or request large jobs; add explicit quantities and limits only after you understand their arguments.',practice=True)
q('Observe your colony','advancedperipherals:colony_integrator','The Colony Integrator makes supported MineColonies information available to a computer, which can turn it into a useful local status report.',
 'Place the integrator where it can access your colony, attach it to the computer and discover its methods. Choose a documented read-only query such as basic colony information or requests, then display a short summary.',
 'Check ownership/permissions and colony access if the peripheral exists but returns no useful colony data. Integration does not replace the colony\'s own request system.',practice=True)
q('Measure the factory','advancedperipherals:energy_detector','Advanced Peripherals adds detectors for observing systems beyond ordinary inventories. A useful measurement tells you what action to take.',
 'Read the Energy Detector documentation and place it in a suitable energy path. Discover the installed methods, query a supported measurement and compare idle with running machinery.',
 'Distinguish throughput from stored energy. A cable detector and a battery report may measure different things; label the number and its unit.',practice=True)
q('Start a dashboard automatically',None,'A startup program runs when the computer boots. It is convenient only after the program handles missing devices and ordinary failures.',
 'Save a proven read-only dashboard as startup.lua. Reboot the computer, confirm it starts, then disconnect its monitor and make the program report a useful error rather than repeatedly attempting world-changing actions.',
 'Keep a normal named backup of the program. Startup timing can differ from device availability, so plan for reconnects or a short delayed retry.',practice=True)
q('Troubleshoot by layers',None,'Syntax errors, missing peripherals, unsupported methods and incorrect arguments are different failure classes.',
 'Read the error and line number, check the device appears in peripherals, inspect its methods, then confirm arguments against the matching version documentation. Reduce a failing program to one query before rebuilding the loop.',
 'Print intermediate values while debugging. Avoid catching every error without reporting it; a silent dashboard can be more misleading than an obvious stopped program.')
q('Project: a workshop status board',None,'A good first computer project saves you checking several interfaces while leaving production easy to control manually.',
 'Build a monitor showing at least two useful readings, such as a chest stock count and a supported colony or energy status. Label units, refresh with a delay, handle a missing device and preserve the working source.',
 'Local examples are also saved beside this profile\'s guide documentation. Type them into the in-game editor or import them using your normal ComputerCraft file workflow.',practice=True)

chapter('rftools','RFTools: Build, Process and Travel','rftoolsbuilder:builder',
 'RFTools is a family of practical machines. Builder shapes, places or removes blocks using cards; Utility adds crafting, displays and teleportation; Storage offers modular inventories and a scanner for existing chests. You can adopt one useful tool without building the entire family.',
 'power and manuals -> storage modules/scanner -> controlled Builder job -> quarry distinctions -> crafters -> screens and transport -> a workshop project.')
q('Read the right manual',None,'Builder, Utility and Storage are separate RFTools modules with different interfaces. Their installed manuals explain the exact controls available here.',
 'Find the RFTools manuals in JEI and inspect one page from each installed module. Choose a small powered test area, with an energy buffer and ordinary input/output chests.',
 'RFTools Dimensions is a separate mod. These quests teach the installed Builder, Utility and Storage tools, not dimension creation.')
q('Storage with a removable module','rftoolsstorage:modular_storage','Modular Storage holds items in a storage module. The module is important: it carries the contents and determines capacity.',
 'Craft Modular Storage and a compatible storage module from JEI. Insert the module, add a few test items, and learn its sorting, filtering and crafting interface.',
 'Treat a filled module as valuable storage. Check upgrade recipes and component handling before replacing or crafting with one.',practice=True)
q('Find items across existing chests','rftoolsstorage:storage_scanner','A Storage Scanner provides an interface to nearby inventories without requiring you to move everything into one new storage system.',
 'Power the scanner, place two labeled test chests within range, set its radius and scan. Search for a known item and verify which inventory contains it.',
 'A scan discovers accessible inventories in its area. A chest outside the radius or unloaded area is not automatically part of the system.',practice=True)
q('Decide which inventories are routable',None,'Scanner visibility and permission to use an inventory for routing are different concerns. You may want to see a supply chest without making it a general insertion destination.',
 'Inspect the scanner\'s inventory list and routable settings. Enable only your test storage for automation, then verify insertion/extraction behavior with a small stack.',
 'Avoid enabling every machine buffer and personal chest at once. Deliberate routing prevents an item from ending up in an unexpected inventory.',practice=True)
q('Take storage access with you',None,'A Storage Control Module links the supported tablet interface to a scanner for convenient remote access.',
 'Find the Storage Control Module and tablet in JEI. Follow their tooltips/manual to link the module to your scanner, assemble the tablet setup and test retrieving one item nearby.',
 'The scanner still needs power, accessible inventories and loaded chunks. The old Remote Storage system is different from scanner/tablet access.',practice=True)
q('The Builder follows a card','rftoolsbuilder:builder','The Builder is a powered executor. Its inserted card defines the operation and area; supplying FE alone does not tell it what to do.',
 'Place a Builder in an empty test area, supply modest power, and inspect its card slot, redstone control and preview/support controls. Start with an ordinary placement shape card from JEI.',
 'ATM10 replaces the Builder recipe with one requiring Allthemodium nuggets. Leave it disabled while configuring the area. Card names matter: placement, quarry, clearing, void and pump operations have different consequences.',practice=True)
q('Select and preview a tiny area',None,'Shape size, offset and anchor determine where the Builder acts. A wrong offset can put an otherwise correct shape in the wrong place.',
 'Configure a small box in the card GUI, or follow the card\'s selection tooltip to select corners. Use the Builder\'s preview/support feature to inspect every edge before enabling it.',
 'Begin with a small hollow shape in open space. Zero offset centers a shape relative to the Builder; it does not necessarily mean the box starts at your feet.',practice=True)
q('Place a test structure',None,'A placement job consumes building materials from an accessible supply and needs energy while working.',
 'Provide an ordinary building block in the correct adjacent inventory, enable the Builder and complete your small previewed shape. Disable it and inspect the finished result.',
 'If nothing happens, check redstone state, energy, the card operation and material access before increasing area size.',practice=True)
q('Quarry cards: understand the difference',None,'A normal quarry removes blocks and replaces them with filler; a clearing quarry leaves the excavated area empty. Silk and fortune variants change harvesting behavior.',
 'Compare the available quarry cards in JEI and the installed manual. Choose the behavior you actually want, then prepare a disposable small test area with a chest able to accept the drops.',
 'Void operations remove blocks without keeping their drops. Do not substitute a void card for a quarry just because both clear an area.')
q('Run a controlled quarry test',None,'A quarry is useful only when its bounds, output capacity and stop controls are predictable.',
 'Preview a tiny quarry region away from structures, connect output storage, supply power and run one test. Confirm drops arrive, then stop and inspect the region before enlarging it.',
 'Claims, protected blocks, energy cost and full output can all stop progress. Keep the output visible and retain a way to disable the machine immediately.',practice=True)
q('Pump liquids separately',None,'Pump cards handle liquids and need a destination that can store the extracted fluid. A clearing variant changes what remains behind.',
 'Read the pump-card page, preview a small water area and connect a compatible tank. Run a short test and verify both the tank contents and the resulting world area.',
 'Never assume an item chest can store pumped fluid. Confirm the tank accepts the exact fluid and has enough space.',practice=True)
q('Scan a structure for construction','rftoolsbuilder:scanner','The Builder Scanner records shape information for the building tools. It is different from the Storage Scanner that searches inventories.',
 'Read the Scanner page. Supply its input card with a small area definition, scan a disposable arrangement and inspect the output card. Compare the result before using it in a construction workflow.',
 'Start with a tiny pattern of cheap blocks. A successful scan does not supply the materials needed to reproduce the structure.',practice=True)
q('Craft repetitive recipes','rftoolsutility:crafter3','An RFTools Crafter stores recipes and processes them from its internal inventory. Tier 3 supports multiple recipe steps in one machine.',
 'Power a Crafter, teach one simple recipe and provide ingredients. Set the recipe\'s result handling deliberately, then verify the output before adding an intermediate recipe.',
 'Output handling controls whether an intermediate stays available internally or leaves the machine. Wrong handling can starve a later recipe even with plenty of raw materials.',practice=True)
q('Remember ingredient slots',None,'Remembered slots reserve inventory positions for specific ingredients. This prevents one abundant resource from occupying every available slot.',
 'Use the Crafter\'s Remember controls to reserve your ingredients, then supply them in uneven quantities. Verify the less common ingredient still has room when it arrives.',
 'Use Forget when changing recipes and inspect every old reservation. A stale slot assignment can look like a transport failure.',practice=True)
q('A screen for the workshop','rftoolsutility:screen_controller','Screens and modules display selected information. The Screen Controller supplies the powered support for screens in its working area.',
 'Power a Screen Controller, place a nearby screen, add one suitable information module and scan/configure it according to the manual. Show one useful stock or machine reading.',
 'Start inside the controller\'s ordinary range. A blank screen may lack a configured module, a scanned controller connection or power.',practice=True)
q('Build a teleport pair','rftoolsutility:matter_transmitter','Matter Transmitters send you to Matter Receivers through a dialed connection. The Dialing Device establishes the route.',
 'Build powered transmitter and receiver endpoints with a safe arrival space. In the Dialing Device select the source, select the destination, then use Dial or Dial Once and test a short local trip.',
 'Keep a physical return route for the first test. Verify destination power, access and chunk availability before relying on a long-distance link.',practice=True)
q('Carry a route home',None,'A charged porter gives portable access to an assigned Matter Receiver. It still depends on a working destination.',
 'Find the Charged Porter in JEI, charge it and bind it to your receiver using its tooltip instructions. Test from nearby, then compare the advanced version if you need multiple destinations.',
 'Check charge and binding before exploring. A portable return device is not a replacement for a powered, loaded and safe receiving area.',practice=True)
q('Infusion and specialist machines',None,'RFTools upgrades and specialist tools can improve a working setup, but their benefits depend on the particular machine.',
 'Read the installed manual\'s infusion information and inspect improvements for one machine you already use. Browse the Environmental Controller and shield system as optional projects with their own module and power requirements.',
 'Upgrade for a measured need. Larger areas, stronger effects or faster work can raise power demand and do not fix a misconfigured card or recipe.')
q('Troubleshoot the operation, not just power',None,'A powered RFTools machine can still have the wrong card, invalid area, blocked output, missing module or disabled control state.',
 'Inspect the machine\'s status, operation/card, redstone mode, area or range, resource supply and output space. Reduce the job to a tiny known example and compare it with the manual.',
 'Storage Scanner and Builder Scanner solve different problems. Check the exact block name when a tutorial seems to describe an interface you do not have.')
q('Project: a practical workshop expansion',None,'RFTools is most useful as a collection of tools that solve your own building and logistics problems.',
 'Use a previewed Builder job for a small workshop shell, a Crafter for one recurring ingredient and a scanner or screen for supply access. Add a tested return receiver if useful, then document how each system stops and restarts.',
 'Keep quarrying and destructive shape operations away from the workshop. Save the card settings for the construction job you have already verified.',practice=True)
