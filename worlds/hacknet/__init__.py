import warnings
import math
from typing import Mapping, Any
from random import choice as random_choice

from BaseClasses import Tutorial, ItemClassification, Region
from worlds.AutoWorld import World, WebWorld

from .Options import HacknetOptions, hn_option_groups
from .Items import item_table, ItemData, HacknetItem
from .Locations import achievements_table, node_admin_table, mission_table, pointclicker_table, junebug_mission_id, \
    junebug_node_ids, HacknetLocData, HacknetLocation
from .Rules import set_rules
from .Presets import hacknet_option_presets

class HacknetWeb(WebWorld):
    tutorials = [
        Tutorial(
            "MultiWorld Setup Guide",
            "A guide to setting up Hacknet. This guide covers singleplayer, multiplayer, and web.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Autumn Rivers"]
        )
    ]

    option_groups = hn_option_groups
    options_presets = hacknet_option_presets
    theme = "ice"

class HacknetWorld(World):
    """
    Hacknet is a terminal-emulation game developed by Team Fractal Alligator,
    and published by Fellow Traveler Games.
    """

    game = "Hacknet"

    web = HacknetWeb()

    options_dataclass = HacknetOptions
    options: HacknetOptions
    topology_present = True

    ap_world_version = "0.0.1"

    hn_item_table = item_table
    hn_loc_table = mission_table

    _master_items_table = item_table
    _master_locations_table = mission_table + pointclicker_table + achievements_table + node_admin_table

    # item_name_to_id = {name: data.code for name, data in hn_item_table.items()}
    # location_name_to_id = {name: index for index, _region, name, _dlc, _ptc in hn_loc_table}
    item_name_to_id = {name: data.code for name, data in _master_items_table.items()}
    location_name_to_id =  {name: index for index, _region, name, _dlc, _ptc in _master_locations_table}

    def modify_item_table_by_options(self):
        options = self.options
        items_to_remove = {}

        # Option values
        shuffle_execs = int(options.shuffle_execs)
        limits = int(options.enable_limits)
        shuffle_pointclicker = int(options.shuffle_ptc)
        start_with_ftpssh = bool(options.start_with_ftp_and_ssh)
        sprint_replaces_bounce = bool(options.sprint_replaces_bounce)
        enable_etas_traps = bool(options.enable_etas_traps)
        shuffle_factions = bool(options.faction_access)

        def add_to_removed_items(items: dict[str, ItemData]):
            for key, value in items.items():
                items_to_remove[key] = value.code

        def _remove_execs_from_item_table():
            execs = {key: value for key, value in self.hn_item_table.items() if value.item_type != "exec"}
            add_to_removed_items(execs)

        def _remove_items_from_item_table(classification: ItemClassification, item_type: str, *excluding):
            # this is kind of ugly honestly. could probably make it nicer but should be fine for now
            cond = lambda item: ((item.classification != classification and item.item_type == item_type)
                                 or item.item_type != item_type)
            exclude_items = {key: value for key, value in self.hn_item_table if cond(value) and key not in excluding}
            add_to_removed_items(exclude_items)

        def _remove_items_from_item_table_inverse_class(classification: ItemClassification, item_type: str,
                                                        *excluding):
            hn_table = self.hn_item_table
            cond = lambda d: ((d.classification == classification and d.item_type == item_type) or
                              d.item_type != item_type)
            exclude_items = {key: value for key, value in hn_table if cond(value) and key not in excluding}
            add_to_removed_items(exclude_items)

        def _remove_items_by_name(*item_names):
            cond = lambda item_name: item_name not in item_names
            exclude_items = {key: value for key, value in self.hn_item_table.items() if cond(key)}
            add_to_removed_items(exclude_items)

        def _remove_items_by_type(*item_types):
            cond = lambda item: item.item_type not in item_types
            exclude_items = {key: value for key, value in self.hn_item_table.items() if cond(value)}
            add_to_removed_items(exclude_items)

        # Modify table according to options
        # Exclude executables
        if shuffle_execs == 4:
            _remove_execs_from_item_table()
        elif shuffle_execs == 3:
            _remove_items_from_item_table_inverse_class(ItemClassification.progression, "Executable",
                                                             "SecurityTracer")
        elif shuffle_execs == 2:
            _remove_items_from_item_table(ItemClassification.filler, "Executable")

        if sprint_replaces_bounce:
            _remove_items_by_name("FTPBounce")

        # Exclude Limit Items
        if limits in (2, 3):
            _remove_items_by_name("Progressive RAM")
        elif limits == 4:
            _remove_items_by_name("Progressive Shell Limit")
        elif limits == 5:
            _remove_items_by_name("Progressive Shell Limit", "Progressive RAM")

        # Exclude PointClicker
        if shuffle_pointclicker == 3:
            _remove_items_by_type("PointClicker Passive", "PointClicker Point", "PointClicker Trap")

        if not enable_etas_traps:
            _remove_items_by_name("ETAS Trap")

        if not shuffle_factions:
            _remove_items_by_type("Faction")

        for key, _value in items_to_remove.items():
            self.item_name_to_id.pop(key, None)

    def modify_location_table_by_options(self):
        options = self.options

        # Options
        exclude_junebug = bool(options.exclude_junebug)
        shuffle_dlc = bool(options.shuffle_labs)
        shuffle_pointclicker = int(options.shuffle_ptc)
        shuffle_achievements = bool(options.shuffle_achvs)
        shuffle_admin_access = bool(options.shuffle_nodes)

        locations_to_remove = []

        def _remove_junebug_mission():
            # cond = lambda loc: loc.id is not junebug_mission_id
            # self.hn_loc_table = [loc for loc in self.hn_loc_table if cond(loc)]
            # self.hn_loc_table = {key: value for key, value in self.hn_loc_table if cond(value)}
            locations_to_remove.append("CSEC -- Project Junebug")

        def _remove_labyrinths_missions():
            labs_missions = [loc for loc in self.hn_loc_table if not loc.is_dlc]
            for mission in labs_missions:
                locations_to_remove.append(mission.display_name)

        def _remove_labyrinths_nodes(node_table: list):
            labs_nodes = [loc for loc in node_table if loc.is_dlc]
            for node in labs_nodes:
                locations_to_remove.append(node.display_name)

        def _remove_junebug_nodes(node_table: list):
            jb_nodes = [loc for loc in node_table if loc.id in junebug_node_ids]
            for node in jb_nodes:
                locations_to_remove.append(node.display_name)

        if exclude_junebug:
            _remove_junebug_mission()

        if not shuffle_dlc:
            _remove_labyrinths_missions()

        if shuffle_pointclicker != 3:
            self.hn_loc_table += pointclicker_table
        else:
            ptc_locs = [loc for loc in self._master_locations_table if loc.region == "PointClicker"]
            for loc in ptc_locs:
                locations_to_remove.append(loc.display_name)

        if shuffle_achievements:
            self.hn_loc_table += achievements_table
        else:
            achv_locs = [loc for loc in self._master_locations_table if loc.display_name.startswith("Achievement --")]
            for loc in achv_locs:
                locations_to_remove.append(loc.display_name)

        if shuffle_admin_access:
            admin_access_table = node_admin_table

            if not shuffle_dlc:
                _remove_labyrinths_nodes(admin_access_table)
            if exclude_junebug:
                _remove_junebug_nodes(admin_access_table)

            self.hn_loc_table += admin_access_table
        else:
            non_event_nodes = [loc for loc in self._master_locations_table if loc.id is not None]
            nodes = [loc for loc in non_event_nodes if loc.id >= 133713370140]
            for loc in nodes:
                locations_to_remove.append(loc.display_name)

        for loc_name in locations_to_remove:
            print(f"Removing {loc_name}")
            self.location_name_to_id.pop(loc_name, None)
        print(f"Removed {len(locations_to_remove)} locations")
        print(len(self.location_name_to_id.keys()))

    # NOW we can generate
    def generate_early(self) -> None:
        """
        We check to make sure there's not too many items before we attempt to fill locations.
        If there's "not enough" items, doesn't matter, we can fill the rest with filler.
        But if there's not enough locations, then that's a BIG issue!
        We also don't need to calculate traps since that just goes with filler when locations are stocked.
        """
        pre_gen_item_pool = []
        options = self.options
        player = self.player

        shuffle_limits = int(options.enable_limits)
        shuffle_ptc = int(options.shuffle_ptc)
        shuffle_execs = int(options.shuffle_execs)
        start_with_basics = bool(options.start_with_ftp_and_ssh)
        sprint_replaces_bounce = bool(options.sprint_replaces_bounce)
        faction_access = int(options.faction_access)

        shuffle_labs = bool(options.shuffle_labs)

        mission_skips = int(options.max_mission_skips)
        forcehacks = int(options.max_forcehacks)

        exclude_junebug = bool(options.exclude_junebug)
        shuffle_nodes = bool(options.shuffle_nodes)

        # Modify Tables
        self.modify_item_table_by_options()
        self.modify_location_table_by_options()

        if shuffle_limits in (1, 2, 3):
            prog_shell = self.hn_item_table["Progressive Shell Limit"]
            pre_gen_item_pool += ["Progressive Shell Limit" for _ in range(prog_shell.max_amount)]
        if shuffle_limits in (1, 4):
            prog_ram = self.hn_item_table["Progressive RAM"]
            pre_gen_item_pool += ["Progressive RAM" for _ in range(prog_ram.max_amount)]

        if shuffle_ptc < 3:
            ptcp_10s = self.hn_item_table["PointClicker +10pt./s"]
            ptcp_100s = self.hn_item_table["PointClicker +100pt./s"]
            ptcp_1000s = self.hn_item_table["PointClicker +1000pt./s"]
            ptcp_m2 = self.hn_item_table["PointClicker Passive*2"]
            ptcp_m5 = self.hn_item_table["PointClicker Passive*5"]
            ptcp_m10 = self.hn_item_table["PointClicker Passive*10"]

            pre_gen_item_pool += ["PointClicker +10pt./s" for _ in range(ptcp_10s.max_amount)]
            pre_gen_item_pool += ["PointClicker +100pt./s" for _ in range(ptcp_100s.max_amount)]
            pre_gen_item_pool += ["PointClicker +1000pt./s" for _ in range(ptcp_1000s.max_amount)]
            pre_gen_item_pool += ["PointClicker Passive*2" for _ in range(ptcp_m2.max_amount)]
            pre_gen_item_pool += ["PointClicker Passive*5" for _ in range(ptcp_m5.max_amount)]
            pre_gen_item_pool += ["PointClicker Passive*10" for _ in range(ptcp_m10.max_amount)]

        if shuffle_execs < 4:
            filtered_execs = {key: value for key, value in self.hn_item_table.items() if value.item_type == "Executable"
                              and value.classification != ItemClassification.trap}
            for exe in map(self.create_item, filtered_execs):
                pre_gen_item_pool += [exe.name]

        if sprint_replaces_bounce:
            pre_gen_item_pool.pop()

        if start_with_basics:
            pre_gen_item_pool.pop()
            pre_gen_item_pool.pop()

        if mission_skips > 0:
            pre_gen_item_pool += ["Mission Skip" for _ in range(mission_skips)]
        if forcehacks > 0:
            pre_gen_item_pool += ["ForceHack" for _ in range(forcehacks)]

        if faction_access < 3:
            pre_gen_item_pool += ["Progressive Faction Access" for _ in range(3)]

        if shuffle_execs == 4 and shuffle_limits == 5 and not faction_access:
            warnings.warn("You're not shuffling executables, limits, or faction access. This will be a very short run. "
                          + "It is recommened to play with at least one of these enabled!")
        elif shuffle_execs == 4:
            warnings.warn("You're not shuffling executables. It's recommended to play with executables shuffled!")

        # and that should be everything, I think...?
        if len(pre_gen_item_pool) > len(self.hn_loc_table):
            raise Exception("Too many items! Generation will fail. Add more locations by enabling other options.\n" +
                            "If you consistently receive this error, try enabling Admin Access as Checks.")

        # Push some items to the starting inventory, if they're not already there
        def push_to_start_inv(item_name: str) -> None:
            item_exists = any(item.name == item_name for item in self.multiworld.precollected_items[self.player])
            if not item_exists:
                self.multiworld.push_precollected(self.create_item(item_name))

        if start_with_basics and shuffle_execs < 4:
            push_to_start_inv("SSHCrack")
            ftp_cracker = "FTPSprint" if sprint_replaces_bounce else "FTPBounce"
            push_to_start_inv(ftp_cracker)

        if faction_access == 2:
            self.multiworld.start_hints[self.player].value.add("Progressive Faction Access")
            self.multiworld.start_hints[self.player].value.add("Progressive Faction Access")
            if shuffle_labs:
                self.multiworld.start_hints[self.player].value.add("Progressive Faction Access")

        junebug_mission = "CSEC -- Project Junebug"
        junebug_nodes = [
            "CSEC -- Eidolon Soft Production Server",
            "CSEC -- KBT-PM 2.44 REG#10811",
            "CSEC -- Kellis Biotech Client Services",
            "CSEC -- Kellis Biotech Production Asset Server"
        ]

        if exclude_junebug:
            self.multiworld.exclude_locations[self.player].value.add(junebug_mission)
            if shuffle_nodes:
                for node in junebug_nodes:
                    self.multiworld.exclude_locations[self.player].value.add(node)
            if shuffle_execs < 4:
                push_to_start_inv("KBTPortTest")

        pass

    # item_name_to_id = {name: data.code for name, data in hn_item_table.items()}
    # location_name_to_id = {name: index for index, _region, name, _dlc, _ptc in hn_loc_table}

    def create_item(self, name: str) -> HacknetItem:
        print(f"Creating item {name} for player {self.player}")
        item = self._master_items_table[name]
        hn_item = HacknetItem(name, self.player, item, False)
        if item.max_amount > -1:
            hn_item.max_amount = item.max_amount

        options = self.options
        shuffle_achievements = bool(options.shuffle_achvs)

        if (shuffle_achievements and
            (name == "ClockEXE" or name == "ThemeChanger")):
            hn_item.classification = ItemClassification.progression

        if hn_item.index is not None:
            return hn_item

    def create_event(self, event: str) -> HacknetItem:
        return HacknetItem(event, self.player, (None, ItemClassification.progression, "Event", False, 1), True)

    already_filled_pool = False

    def create_items(self) -> None:
        filtered_items = self.hn_item_table
        options = self.options
        hn_item_pool: list[HacknetItem] = []
        player = self.player

        def is_item_in_precollected(item_name: str) -> bool:
            return any(item.name == item_name for item in self.multiworld.precollected_items[self.player])

        def get_random_filler_item() -> tuple[str, ItemData]:
            c_filler = ItemClassification.filler
            filler_items = {key: value for key, value in filtered_items.items() if value.classification == c_filler}
            random_item = random_choice(list(filler_items.items()))
            return random_item[0], random_item[1]

        exclude = [item for item in self.multiworld.precollected_items[player]]

        shuffle_limits = int(options.enable_limits)
        shuffle_execs = int(options.shuffle_execs)
        faction_access = int(options.faction_access)
        shuffle_ptc = int(options.shuffle_ptc)

        shuffle_labs = bool(options.shuffle_labs)

        mission_skips = int(options.max_mission_skips)
        forcehacks = int(options.max_forcehacks)

        def add_random_filler_item() -> None:
            filler_item = get_random_filler_item()
            is_exec = filler_item[1].item_type == "Executable"
            f_item = self.create_item(filler_item[0])
            exists_in_pool = f_item in hn_item_pool

            if is_exec and exists_in_pool:
                add_random_filler_item()
                return

            hn_item_pool.append(f_item)

        def add_to_item_pool(item_name: str) -> None:
            item = self.create_item(item_name)
            if item not in exclude:
                hn_item_pool.append(item)
                if item.classification == ItemClassification.progression:
                    exclude.append(item)
                print(hn_item_pool.count(item))
            else:
                filler_item_name = get_random_filler_item()[0]
                hn_item_pool.append(self.create_item(filler_item_name))

        def add_amount_to_item_pool(item_name: str, amount: int) -> None:
            item = self.create_item(item_name)
            remaining_amount = amount
            nonlocal hn_item_pool
            if item in exclude:
                excluded_amount = exclude.count(item)
                remaining_amount = amount - excluded_amount
                print(f"Item {item.name} excluded {excluded_amount} times in pool")
                hn_item_pool += [self.create_item(get_random_filler_item()[0]) for _ in range(excluded_amount)]

            if remaining_amount > 0:
                print(remaining_amount)
                for _ in range(remaining_amount):
                    print(f"{remaining_amount} {item.name}")
                    hn_item_pool.append(item)

        # First, we want to add progression items
        if shuffle_limits in (1, 2, 3):
            prog_shell = self.hn_item_table["Progressive Shell Limit"]
            # item_pool += [self.create_item(prog_shell) for _ in range(prog_shell.max_amount)]
            add_amount_to_item_pool("Progressive Shell Limit", prog_shell.max_amount)
        if shuffle_limits in (1, 4):
            prog_ram = self.hn_item_table["Progressive RAM"]
            # item_pool += [self.create_item(prog_ram) for _ in range(prog_ram.max_amount)]
            add_amount_to_item_pool("Progressive RAM", prog_ram.max_amount)

        # Shuffle Executables is next, if required
        if shuffle_execs < 4:
            execs_to_add = {key: value for key, value in filtered_items.items() if value.item_type == "Executable"}

            for exec_name in execs_to_add:
                add_to_item_pool(exec_name)

        # If faction access is enabled, then shuffle that
        if faction_access < 3:
            faction_amount = 3 if shuffle_labs else 2
            add_amount_to_item_pool("Progressive Faction Access", faction_amount)

        # If PointClicker upgrades are checks, then shuffle in passive upgrades
        if shuffle_ptc < 3:
            ptc_items = {key: value for key, value in self.hn_item_table.items() if
                         value.item_type == "PointClicker Passive"}
            for name, data in ptc_items.items():
                add_amount_to_item_pool(name, data.max_amount)

        # If mission skips and/or forcehacks are greater than 0, shuffle 'em
        if mission_skips > 0:
            add_amount_to_item_pool("Mission Skip", mission_skips)
        if forcehacks > 0:
            add_amount_to_item_pool("ForceHack", forcehacks)

        # And I think that is it... hopefully
        trap_percentage = int(options.trap_percentage)

        total_locations = len(self.multiworld.get_unfilled_locations(player))
        empty_locations = total_locations - len(hn_item_pool)
        print(f"Total locations: {total_locations}, Total items: {len(hn_item_pool)}, Empty locations: {empty_locations}")

        def recalculate_empty_locations():
            nonlocal empty_locations
            empty_locations = total_locations - len(hn_item_pool)
            print(
                f"Total locations: {total_locations}, Total items: {len(hn_item_pool)}, Empty locations: {empty_locations}")

        def get_random_trap_name():
            trap_items = {key: value for key, value in self.hn_item_table.items() if
                          value.classification == ItemClassification.trap}
            return random_choice(list(trap_items.keys()))

        def fill_out_empty_locations():
            print(f"There are {empty_locations} empty locations. Filling them with traps...")

            traps = 0
            if trap_percentage > 0:
                math.floor(empty_locations * (trap_percentage / 100))

            if traps > 0:
                for _ in range(traps):
                    add_to_item_pool(get_random_trap_name())

            recalculate_empty_locations()

            print(f"There are {empty_locations} empty locations. Filling them with filler...")

            if empty_locations == 0:
                return

            for _ in range(empty_locations):
                add_to_item_pool(get_random_filler_item()[0])

            recalculate_empty_locations()

            if empty_locations != 0:
                print(f"There are still {empty_locations} empty locations. Generation failed!?")
                raise Exception("Something went seriously, seriously wrong while filling the item pool.\n" +
                                "After filling in empty locations, there were either " +
                                "a) still locations with no items, or " +
                                "b) the value was somehow negative. Either way, panic!!!")

        if empty_locations > 0:
            fill_out_empty_locations()

        print(f"Adding {len(hn_item_pool)} items to item pool...")
        self.multiworld.itempool += hn_item_pool
        print(f"{len(hn_item_pool)} items added successfully!")

        pass # TODO

    def create_regions(self) -> None:
        print("Assigning regions...")

        filtered_locations = self.hn_loc_table
        player = self.player

        options = self.options
        player_goal = int(options.player_goal)
        shuffle_execs = int(options.shuffle_execs)
        faction_access = int(options.faction_access)
        shuffle_labs = bool(options.shuffle_labs)
        exclude_junebug = bool(options.exclude_junebug)

        dont_shuffle_execs = shuffle_execs == 4
        no_faction_access = faction_access == 3

        def create_real_location(loc_data: HacknetLocData) -> HacknetLocation:
            return HacknetLocation(player, loc_data.display_name, loc_data, loc_data.region)

        real_locations = [create_real_location(loc) for loc in filtered_locations]

        def add_locs_to_region(region: Region) -> None:
            excluded_events = []

            if player_goal not in (3, 5):
                excluded_events.append("Broke Into The Gibson")
            if player_goal not in (4, 5):
                excluded_events.append("Complete Every CSEC Mission")
                excluded_events.append("Complete Every Entropy Mission")
            if player_goal not in (2, 5):
                excluded_events.append("Watched Labyrinths Credits")

            region_locs = [loc for loc in real_locations if loc.raw_region == region.name and
                           loc.name not in excluded_events]
            print(f"Found {len(region_locs)} locations in {region.name}.")
            for loc in region_locs:
                loc.parent_region = region
            region.locations += region_locs

        menu_region = Region("Menu", player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        add_locs_to_region(menu_region)

        intro_region = Region("Intro", player, self.multiworld)
        self.multiworld.regions.append(intro_region)
        add_locs_to_region(intro_region)
        menu_region.connect(intro_region, "Finish Maiden Flight",
                            lambda state: (dont_shuffle_execs or state.has("SSHCrack", player) or
                                           state.has("WebServerWorm", player) or
                                           state.has("SMTPOverflow", player) or
                                           state.has("FTPBounce", player) or state.has("FTPSprint", player))
                            )

        entropy_region = Region("Entropy", player, self.multiworld)
        self.multiworld.regions.append(entropy_region)
        add_locs_to_region(entropy_region)
        intro_region.connect(entropy_region, "Join Entropy",
                             lambda state: (dont_shuffle_execs or state.has("SSHCrack", player) or
                                            state.has("WebServerWorm", player) or
                                            state.has("SMTPOverflow", player) or
                                            state.has("FTPBounce", player) or state.has("FTPSprint", player)) and
                                           (no_faction_access or state.has("Progressive Faction Access", player, 1))
                             )

        entropy_naix_region = Region("Entropy - Naix", player, self.multiworld)
        self.multiworld.regions.append(entropy_naix_region)
        add_locs_to_region(entropy_naix_region)
        entropy_region.connect(entropy_naix_region, "Attack Naix",
                               lambda state: (dont_shuffle_execs or
                                              (state.has("WebServerWorm", player) or
                                               state.has("SMTPOverflow", player) and
                                               (state.has("FTPBounce", player) or state.has("FTPSprint", player)))
                                              and state.has("eosDeviceScan", player)
                                              )
                               )

        elsec_intro_region = Region("/el Sec - Naix", player, self.multiworld)
        self.multiworld.regions.append(elsec_intro_region)
        add_locs_to_region(elsec_intro_region)
        entropy_naix_region.connect(elsec_intro_region, "Start /el Sec Intro",
                                    lambda state: (dont_shuffle_execs or
                                                   (state.has("WebServerWorm", player) and
                                                    state.has("SMTPOverflow", player) and
                                                    state.has("SSHCrack", player) and
                                                    (state.has("FTPBounce", player) or state.has("FTPSprint", player))
                                                    ))
                                    )

        elsec_polar_star_region = Region("/el Sec - Polar Star", player, self.multiworld)
        self.multiworld.regions.append(elsec_polar_star_region)
        add_locs_to_region(elsec_polar_star_region)
        elsec_intro_region.connect(elsec_polar_star_region, "Join /el Sec")

        elsec_seculock_region = Region("/el Sec - SecuLock", player, self.multiworld)
        self.multiworld.regions.append(elsec_seculock_region)
        add_locs_to_region(elsec_seculock_region)
        elsec_polar_star_region.connect(elsec_seculock_region, "Join /el Sec")

        csec_intro_region = Region("CSEC - Intro", player, self.multiworld)
        self.multiworld.regions.append(csec_intro_region)
        add_locs_to_region(csec_intro_region)
        elsec_polar_star_region.connect(csec_intro_region, "Receive CSEC Invitation")

        labs_exit_region = Region("Labyrinths - Altitude Loss", player, self.multiworld)

        # Labyrinths or CSEC sets? Which way, Western boy?
        def create_labs_regions():
            kaguya_trials_region = Region("Labyrinths - Kaguya Trials", player, self.multiworld)
            self.multiworld.regions.append(kaguya_trials_region)
            add_locs_to_region(kaguya_trials_region)
            csec_intro_region.connect(kaguya_trials_region, "Run KaguyaTrials.exe",
                                      lambda state: (dont_shuffle_execs or
                                                     state.has("TorrentStreamInjector", player)) and
                                                    (no_faction_access or
                                                     state.has("Progressive Faction Access", player, 2))
                                      )

            labs_set1_region = Region("Labyrinths - Set 1", player, self.multiworld)
            self.multiworld.regions.append(labs_set1_region)
            add_locs_to_region(labs_set1_region)
            kaguya_trials_region.connect(labs_set1_region, "Finish Kaguya Trials")

            labs_set2_region = Region("Labyrinths - Set 2", player, self.multiworld)
            self.multiworld.regions.append(labs_set2_region)
            add_locs_to_region(labs_set2_region)
            labs_set1_region.connect(labs_set2_region, "Obtain SSLTrojan",
                                     lambda state: dont_shuffle_execs or state.has("SSLTrojan", player)
                                     )

            labs_ha_region = Region("Labyrinths - Hermetic Alchemists", player, self.multiworld)
            self.multiworld.regions.append(labs_ha_region)
            add_locs_to_region(labs_ha_region)
            labs_set2_region.connect(labs_ha_region, "Finish Mission Set 2")

            labs_mf_region = Region("Labyrinths - Memory Forensics", player, self.multiworld)
            self.multiworld.regions.append(labs_mf_region)
            add_locs_to_region(labs_mf_region)
            labs_ha_region.connect(labs_mf_region, "Obtain Memory Forensics Suite",
                                   lambda state: dont_shuffle_execs or state.has("Mem Suite", player)
                                   )

            labs_striker_region = Region("Labyrinths - Striker", player, self.multiworld)
            self.multiworld.regions.append(labs_striker_region)
            add_locs_to_region(labs_striker_region)
            labs_mf_region.connect(labs_striker_region, "Finish Memory Forensics Mission")

            labs_set3_region = Region("Labyrinths - Set 3", player, self.multiworld)
            self.multiworld.regions.append(labs_set3_region)
            add_locs_to_region(labs_set3_region)
            labs_striker_region.connect(labs_set3_region, "Activate CoelTrain Protocol")

            labs_pals_region = Region("Labyrinths - Neopals", player, self.multiworld)
            self.multiworld.regions.append(labs_pals_region)
            add_locs_to_region(labs_pals_region)
            labs_set3_region.connect(labs_pals_region, "Finish Mission Set 3")

            labs_set4_region = Region("Labyrinths - Set 4", player, self.multiworld)
            self.multiworld.regions.append(labs_set4_region)
            add_locs_to_region(labs_set4_region)
            labs_pals_region.connect(labs_set4_region, "Finish Neopals Mission")

            labs_finale1_region = Region("Labyrinths - Take Flight", player, self.multiworld)
            self.multiworld.regions.append(labs_finale1_region)
            add_locs_to_region(labs_finale1_region)
            labs_set4_region.connect(labs_finale1_region, "Finish Mission Set 4")

            self.multiworld.regions.append(labs_exit_region)
            add_locs_to_region(labs_exit_region)
            labs_finale1_region.connect(labs_exit_region, "Obtain PacificPortcrusher",
                                        lambda state: dont_shuffle_execs or state.has("PacificPortcrusher", player)
                                        )

        if shuffle_labs:
            create_labs_regions()

        csec_main_region = Region("CSEC", player, self.multiworld)
        self.multiworld.regions.append(csec_main_region)
        add_locs_to_region(csec_main_region)
        if shuffle_labs:
            labs_exit_region.connect(csec_main_region, "Finish Labyrinths",
                                     lambda state: (dont_shuffle_execs or state.has("SQL_MemCorrupt", player)) and
                                                   (no_faction_access or
                                                    state.has("Progressive Faction Access", player, 3))
                                     )
        else:
            csec_main_region.connect(csec_intro_region, "Finish CSEC Intro",
                                     lambda state: (dont_shuffle_execs or state.has("SQL_MemCorrupt", player)) and
                                                   (no_faction_access or
                                                    state.has("Progressive Faction Access", player, 2))
                                     )

        csec_dec_region = Region("CSEC - DEC", player, self.multiworld)
        self.multiworld.regions.append(csec_dec_region)
        add_locs_to_region(csec_dec_region)
        csec_main_region.connect(csec_dec_region, "Obtain Decyphering Tools",
                                 lambda state: dont_shuffle_execs or state.has("DEC Suite", player))

        if shuffle_labs:
            post_labs_region = Region("Post-Labyrinths", player, self.multiworld)
            self.multiworld.regions.append(post_labs_region)
            add_locs_to_region(post_labs_region)
            csec_dec_region.connect(post_labs_region, "Finish DEC Missions")

        csec_bit_region = Region("CSEC - Bit", player, self.multiworld)
        self.multiworld.regions.append(csec_bit_region)
        add_locs_to_region(csec_bit_region)

        if not exclude_junebug:
            project_junebug_region = Region("CSEC - Project Junebug", player, self.multiworld)
            self.multiworld.regions.append(project_junebug_region)
            add_locs_to_region(project_junebug_region)
            csec_dec_region.connect(project_junebug_region, "Start Project Junebug",
                                    lambda state: dont_shuffle_execs or state.has("KBTPortTest", player)
                                    )

            project_junebug_region.connect(csec_bit_region, "Start Bit Contracts")
        else:
            csec_dec_region.connect(csec_bit_region, "Start Bit Contracts")

        finale_region = Region("Finale", player, self.multiworld)
        self.multiworld.regions.append(finale_region)
        add_locs_to_region(finale_region)
        csec_bit_region.connect(finale_region, "Finish Bit Contract",
                                lambda state: dont_shuffle_execs or state.has("KBTPortTest", player)
                                )

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.options, self.player, self)

    def generate_basic(self) -> None:
        multiworld = self.multiworld
        player = self.player

        multiworld.get_location("Join CSEC", player).place_locked_item(
            self.create_event("CSEC Member ID")
        )

        # Determine Victory Conditions
        multiworld.get_location("Stop PortHack.Heart", player).place_locked_item(
            self.create_event("Fulfill Bit's Final Request")
        )
        multiworld.completion_condition[player] = lambda state: state.has("Fulfill Bit's Final Request", player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data: dict[str, Any] = {
            "pointclicker_mode": "vanilla",
            "executable_shuffle": 0,
            "limits_mode": 0,
            "sprint_replaces_bounce": False,
            "deathlink": False,
            "randomization_seed": -1, # for future use
            "executable_grouping": 1,
            "enable_labyrinths": True
        }

        options = self.options

        shuffle_ptc = int(options.shuffle_ptc)
        shuffle_execs = int(options.shuffle_execs)
        shuffle_limits = int(options.enable_limits)
        sprint_replaces_bounce = bool(options.sprint_replaces_bounce)
        deathlink = bool(options.deathlink)
        shuffle_labs = bool(options.shuffle_labs)

        if shuffle_ptc == 1:
            slot_data["pointclicker_mode"] = "block_upgrade_effects"

        if shuffle_execs < 4:
            slot_data["executable_shuffle"] = shuffle_execs

        if shuffle_limits < 5:
            slot_data["limits_mode"] = shuffle_limits

        slot_data["sprint_replaces_bounce"] = sprint_replaces_bounce
        slot_data["deathlink"] = deathlink
        slot_data["enable_labyrinths"] = shuffle_labs

        return slot_data