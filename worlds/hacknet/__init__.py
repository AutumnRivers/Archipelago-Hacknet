import random

from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType
from worlds.generic.Rules import set_rule, add_rule

from .Items import HacknetItem, ap_id_to_hacknet_item, hacknet_item_to_ap_id, item_table
from .Locations import HacknetLocation, ap_id_to_hacknet_loc, hacknet_loc_to_ap_id, create_location_descriptions
from .LocationList import location_table

from .Options import hacknet_options, get_option_value

from .Rules import set_rules, set_labs_rules, set_achv_rules

class HacknetWeb(WebWorld):
    theme = "ice"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Hacknet in an Archipelago MW.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AutumnRivers"]
    )]

class HacknetWorld(World):
    """
    Hacknet is a terminal-based hacking simulator. Get placed into the dark and murky worlds of hackers in order to
    investigate the disappearance of a well-known hacker. Includes support for the Labyrinths DLC campaign.
    """
    game = "Hacknet"
    topology_present = False
    web = HacknetWeb()
    data_version = 1

    location_descriptions = create_location_descriptions()

    option_definitions = hacknet_options

    item_name_to_id = {item_name: hacknet_item_to_ap_id(data, False) for item_name, data in item_table.items()}
    item_id_to_name = ap_id_to_hacknet_item

    location_name_to_id = {item_name: hacknet_loc_to_ap_id(data[1]) for item_name, data in location_table.items()}
    location_id_to_name = ap_id_to_hacknet_loc

    etas_placed = 0

    # Rules
    def create_item(self, name: str) -> HacknetItem:
        hn_item = HacknetItem(name, self.player, item_table[name], False)

        if hn_item.index is not None:
            #print(f"Creating item: {hn_item}")
            return hn_item

    def create_event(self, event: str) -> HacknetItem:
        return HacknetItem(event, self.player, item_table[event], True)

    def create_items(self) -> None:
        exclude = [item for item in self.multiworld.precollected_items[self.player]]

        exclude.append("l33t hax0r skillz")
        exclude.append("the sudden urge to play PointClicker")
        exclude.append("matt")

        item_pool: List[HacknetItem] = []

        for item in map(self.create_item, item_table):
            if item in exclude:
                exclude.remove(item)
            elif item is None:
                continue
            else:
                item_pool.append(item)

        while(self.etas_placed < 2):
            self.etas_placed += 1
            item_pool.append(self.create_item("ETASTrap"))

        while((len(self.location_names) - len(item_pool) - len(exclude)) > 0):
            item_pool.append(random.choice([
                self.create_item("l33t hax0r skillz"),
                self.create_item("the sudden urge to play PointClicker"),
                self.create_item("matt"),
                self.create_item("Fake Connect")
            ]))
        
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        shuffle_achievements = get_option_value(self.multiworld, self.player, "shuffle_achievements")
        include_labs = get_option_value(self.multiworld, self.player, "include_labyrinths")
        shuffle_postgame = get_option_value(self.multiworld, self.player, "shuffle_postgame")
        shuffle_nodes = get_option_value(self.multiworld, self.player, "shuffle_nodes")
        win_condition = get_option_value(self.multiworld, self.player, "victory_condition")
        exclude_locations = ["VBIT Finish Sequencer"]

        if shuffle_postgame is False and win_condition <= 2:
            exclude_locations.append("LABS Break Into Gibson")
            exclude_locations.append("CSEC Subvert Psylance Investigation")
            exclude_locations.append("VBIT Reunion")

        def assign_regions(category, target_region):
            region_locs = {k:v for (k,v) in location_table.items() if v[0] == (category)}

            print(f"[Hacknet - Player {self.player}] Assigning locations for {category} Region")

            for loc in region_locs:
                if loc in exclude_locations or (
                    shuffle_achievements is False and
                    region_locs[loc][3] is not False # Achievement = True
                ) or (
                    shuffle_nodes is False and
                    loc.startswith("NODE")
                ):
                    continue

                loc_name = loc
                loc_data = region_locs[loc]

                target_region.locations.append(
                    HacknetLocation(self.player, loc_name, loc_data, target_region)
                )

        # Menu / Achievements
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        assign_regions("Intro", menu_region)

        # Entropy
        entropy_region = Region("Entropy", self.player, self.multiworld)
        self.multiworld.regions.append(entropy_region)

        # Require SSHCrack for Entropy's entrance
        menu_region.connect(entropy_region, rule=lambda state: 
        state.has("SSHCrack", self.player) and (
            state.has("FTPBounce", self.player) or
            state.has("FTPSprint", self.player))
        )

        if shuffle_nodes is not False:
            set_rule(self.multiworld.get_location("NODE Entropy Asset Cache", self.player),
            lambda state: state.has("SSHCrack", self.player))

        assign_regions("Entropy", entropy_region)

        # CSEC
        csec_region = Region("CSEC", self.player, self.multiworld)
        self.multiworld.regions.append(csec_region)

        # Entropy -> CSEC
        entropy_region.connect(csec_region, rule=lambda state:
        state.has("WebServerWorm", self.player) and
        state.has("SQL_MemCorrupt", self.player) and
        state.has("eosDeviceScan", self.player))

        assign_regions("CSEC", csec_region)

        # VBit - Finale
        vbit_region = Region("VBit", self.player, self.multiworld)
        self.multiworld.regions.append(vbit_region)

        # CSEC -> VBit
        csec_region.add_exits({"VBit": "VBIT Foundation"},
        {"VBit": lambda state:
        state.has("KBTPortTest", self.player) and
        state.has("Decypher", self.player) and
        state.has("DECHead", self.player)})

        # VBit Locations
        assign_regions("VBit", vbit_region)

        vbit_region.locations.append(HacknetLocation(self.player, "VBIT Finish Sequencer",
        ("VBit", None, False, False, False), vbit_region))

        set_rules(self.multiworld, self.player)

        if shuffle_achievements is True:
            set_achv_rules(self.multiworld, self.player)

        if include_labs is False and win_condition == 1:
            return None

        # Labyrinths
        labs_region = Region("Labyrinths", self.player, self.multiworld)
        self.multiworld.regions.append(labs_region)

        # Entropy -> Labyrinths
        entropy_region.add_exits({"Labyrinths": "LABS Finish Kaguya Trials"},
        {"Labyrinths": lambda state:
        state.has("FTPBounce", self.player) and
        state.has("eosDeviceScan", self.player) and
        state.has("FTPSprint", self.player) and
        state.has("TorrentStreamInjector", self.player)})

        # CSEC -> Labyrinths
        # csec_region.connect(labs_region, rule=lambda state:
        # state.has("FTPSprint", self.player) and
        # state.has("TorrentStreamInjector", self.player))

        # Labyrinths -> CSEC (or Entropy)
        labs_region.connect(csec_region, rule=lambda state:
        state.has("SSLTrojan",self.player) and
        self.multiworld.get_location("LABS Take Flight", self.player).can_reach(state))

        # Assign Labyrinths locations
        assign_regions("Labyrinths", labs_region)

        labs_region.locations.append(HacknetLocation(self.player, "LABS Remote Shutdown",
        ("Labyrinths", None, True, False, False), labs_region))

        if shuffle_postgame is True:
            labs_region.locations.append(HacknetLocation(self.player, "LABS Broke Into Gibson",
            ("Labyrinths", None, True, False, False), labs_region))

        set_labs_rules(self.multiworld, self.player)

    def generate_basic(self):
        win_condition = get_option_value(self.multiworld, self.player, "victory_condition")

        self.multiworld.get_location("VBIT Finish Sequencer", self.player).place_locked_item(
            self.create_event("Stop PortHack.Heart"))

        self.multiworld.get_location("LABS Remote Shutdown", self.player).place_locked_item(
            self.create_event("Watched Labs Credits"))

        self.multiworld.get_location("LABS Broke Into Gibson", self.player).place_locked_item(
            self.create_event("Gained Gibson Admin"))

        if win_condition == 1: # Heartstopper
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                "Stop PortHack.Heart", self.player)
        elif win_condition == 2: # Altitude Loss
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                "Watched Labs Credits", self.player)
        elif win_condition == 3: # Veteran
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                "Gained Gibson Admin", self.player)
        elif win_condition == 4: # Completionist
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                "Watched Labs Credits", self.player) and state.has(
                "Gained Gibson Admin", self.player) and state.has(
                "Stop PortHack.Heart", self.player)
        else: # Default to Heartstopper
            self.multiworld.completion_condition[self.player] = lambda state: state.has(
                "Stop PortHack.Heart", self.player)

    def fill_slot_data(self):
        slot_data = {}

        for option_name in hacknet_options:
            slot_data[option_name] = get_option_value(
                self.multiworld, self.player, option_name
            )
        
        return slot_data