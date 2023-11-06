from BaseClasses import Item, Tutorial, ItemClassification, Region, Entrance

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType
from worlds.generic.Rules import set_rule, add_rule

from .Items import HacknetItem, ap_id_to_hacknet_item, hacknet_item_to_ap_id, item_table
from .Locations import HacknetLocation, ap_id_to_hacknet_loc, hacknet_loc_to_ap_id
from .LocationList import location_table

from .Options import hacknet_options, get_option_value

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
    Hacknet is a terminal-based hacking simulator. Includes Labyrinths DLC support!
    """
    game = "Hacknet"
    topology_present = False
    web = HacknetWeb()
    data_version = 1

    option_definitions = hacknet_options

    item_name_to_id = {item_name: hacknet_item_to_ap_id(data, False) for item_name, data in item_table.items()}
    item_id_to_name = ap_id_to_hacknet_item

    location_name_to_id = {item_name: hacknet_loc_to_ap_id(data[1]) for item_name, data in location_table.items()}
    location_id_to_name = ap_id_to_hacknet_loc

    # Rules
    def create_item(self, name: str) -> HacknetItem:
        hn_item = HacknetItem(name, self.player, item_table[name], False)

        if hn_item.index is not None:
            print(f"Creating item: {hn_item}")
            return hn_item

    def create_event(self, event: str) -> HacknetItem:
        return HacknetItem(event, self.player, item_table[event], True)

    def create_items(self) -> None:
        exclude = [item for item in self.multiworld.precollected_items[self.player]]

        item_pool: List[HacknetItem] = []

        for item in map(self.create_item, item_table):
            if item in exclude:
                exclude.remove(item)
            elif item is None:
                continue
            else:
                item_pool.append(item)
        
        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        shuffle_achievements = get_option_value(self.multiworld, self.player, "shuffle_achievements")
        include_labs = get_option_value(self.multiworld, self.player, "include_labyrinths")
        shuffle_postgame = get_option_value(self.multiworld, self.player, "shuffle_postgame")

        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        for loc in range(6):
            if shuffle_achievements is False:
                continue

            offset = 46

            real_location = {k:v for (k,v) in location_table.items() if v[1] == (loc + offset)}
            loc_name = list(real_location.keys())[0]
            loc_data = next(iter(real_location.values()))

            menu_region.locations.append(HacknetLocation(self.player, loc_name, loc_data, menu_region)) # Achievements

        menu_region.locations.append(HacknetLocation(self.player, "INTRO Complete Introduction", ("Intro", 56, False, False, True), menu_region))

        # Entropy
        entropy_region = Region("Entropy", self.player, self.multiworld)
        self.multiworld.regions.append(entropy_region)

        menu_region.add_exits({"Entropy": "ENT Intro / Confirmation"},
        {"Entropy": lambda state: state.has("SSHCrack", self.player)})

        menu_region.connect(entropy_region, rule=lambda state: state.has("SSHCrack", self.player))

        for loc in range(9):
            real_location = {k:v for (k,v) in location_table.items() if v[1] == (loc + 1)}
            loc_name = list(real_location.keys())[0]
            loc_data = next(iter(real_location.values()))

            hn_location = HacknetLocation(self.player, loc_name, loc_data, entropy_region)

            print(f"Entropy: Registering ({loc_name}) (A:{hn_location.address})")

            entropy_region.locations.append(hn_location)

        # Naix Recovery Event
        naix_recover_location = {k:v for (k,v) in location_table.items() if v[1] == 48}
        naix_loc_name = "NAIX Recover"
        naix_loc_data = next(iter(naix_recover_location.values()))

        entropy_region.locations.append(HacknetLocation(self.player, naix_loc_name, naix_loc_data, entropy_region))

        set_rule(self.multiworld.get_location("ENT PointClicker", self.player), lambda state: state.has("FTPBounce", self.player))
        set_rule(self.multiworld.get_location("ENT eOS Intro", self.player), lambda state: state.has("eosDeviceScan", self.player))
        set_rule(self.multiworld.get_location("ENT Naix", self.player), lambda state: state.has("eosDeviceScan", self.player))

        # CSEC
        csec_region = Region("CSEC", self.player, self.multiworld)
        self.multiworld.regions.append(csec_region)

        # Entropy -> CSEC
        entropy_region.add_exits({"CSEC": "CSEC CFC Herbs and Spices"},
        {"CSEC": lambda state: state.has("WebServerWorm", self.player) and state.has("SQL_MemCorrupt", self.player)
        and state.has("FTPBounce", self.player) and state.has("eosDeviceScan", self.player)})

        #entropy_region.connect(csec_region)

        for loc in range(16):
            offset = 10

            real_location = {k:v for (k,v) in location_table.items() if v[1] == (loc + offset)}
            loc_name = list(real_location.keys())[0]
            loc_data = next(iter(real_location.values()))

            csec_region.locations.append(HacknetLocation(self.player, loc_name, loc_data, csec_region))

        if shuffle_postgame is True:
            psylance_location = {k:v for (k,v) in location_table.items() if v[1] == 47}
            psylance_loc_name = "CSEC Subvert Psylance Investigation"
            psylance_loc_data = next(iter(psylance_location.values()))

            csec_region.locations.append(HacknetLocation(self.player, psylance_loc_name, psylance_loc_data, csec_region))

        # VBit - Finale
        vbit_region = Region("VBit", self.player, self.multiworld)
        self.multiworld.regions.append(vbit_region)

        # CSEC -> VBit
        csec_region.add_exits({"VBit": "VBIT Foundation"},
        {"VBit": lambda state:
        state.has("KBTPortTest", self.player) and state.has("Decypher", self.player) and state.has("DECHead", self.player)})

        # VBit Locations
        for loc in range(7):
            offset = 24

            real_location = {k:v for (k,v) in location_table.items() if v[1] == (loc + offset)}
            loc_name = list(real_location.keys())[0]
            loc_data = next(iter(real_location.values()))

            if shuffle_postgame is False and loc_name == "VBIT Reunion":
                continue

            vbit_region.locations.append(HacknetLocation(self.player, loc_name, loc_data, vbit_region))

        vbit_region.locations.append(HacknetLocation(self.player, "VBIT Finish Sequencer", ("VBit", None, False, False, False), vbit_region))

        set_rule(self.multiworld.get_location("VBIT Finish Sequencer", self.player), lambda state: self.multiworld.get_location("VBIT Foundation", self.player).can_reach(state))

        if include_labs is False:
            return None

        # Labyrinths
        labs_region = Region("Labyrinths", self.player, self.multiworld)
        self.multiworld.regions.append(labs_region)

        # Entropy -> Labyrinths
        entropy_region.add_exits({"Labyrinths": "LABS Finish Kaguya Trials"},
        {"Labyrinths": lambda state: state.has("FTPBounce", self.player) and state.has("eosDeviceScan", self.player)
        and state.has("FTPSprint", self.player) and state.has("TorrentStreamInjector", self.player)})

        csec_region.connect(labs_region, rule=lambda state:
        state.has("FTPSprint", self.player) and state.has("TorrentStreamInjector", self.player))
        labs_region.connect(csec_region, rule=lambda state:
        state.has("SSLTrojan",self.player) and self.multiworld.get_location("LABS Take Flight", self.player).can_reach(state))

        for loc in range(14):
            offset = 33

            if shuffle_postgame is False and loc_name == "LABS Break Into Gibson":
                continue

            real_location = {k:v for (k,v) in location_table.items() if v[1] == (loc + offset)}
            loc_name = list(real_location.keys())[0]
            loc_data = next(iter(real_location.values()))

            labs_region.locations.append(HacknetLocation(self.player, loc_name, loc_data, labs_region))

        set_rule(self.multiworld.get_location("LABS Take Flight", self.player), lambda state:
        state.has("PacificPortcrusher", self.player) and state.has("MemDumpGenerator", self.player) and state.has("MemForensics", self.player))

        if shuffle_postgame is True:
            gibson_location = {k:v for (k,v) in location_table.items() if v[1] == 49}
            gibson_loc_name = "LABS Break Into Gibson"
            gibson_loc_data = next(iter(gibson_location.values()))

            labs_region.locations.append(HacknetLocation(self.player, gibson_loc_name, gibson_loc_data, labs_region))

    def generate_basic(self):
        win_condition = get_option_value(self.multiworld, self.player, "victory_condition")

        self.multiworld.get_location("VBIT Finish Sequencer", self.player).place_locked_item(self.create_event("Stop PortHack.Heart"))

        if win_condition == 1:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Stop PortHack.Heart", self.player)
        elif win_condition == 2:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Watched Labs Credits", self.player)
        elif win_condition == 3:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Gained Gibson Admin", self.player)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Stop PortHack.Heart", self.player)