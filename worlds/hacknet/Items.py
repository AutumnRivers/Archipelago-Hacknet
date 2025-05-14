import typing

from BaseClasses import Item, ItemClassification

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification
    item_type: str
    is_dlc: bool
    max_amount: typing.Optional[int] = -1 # -1 = unlimited
    # Progression items default to 1 instead of unlimited

class HacknetItem(Item):
    game: str = "Hacknet"

    def __init__(self, name, player, data, event):
        (index, classification, category, is_dlc, _max_amount) = data
        self.classification = classification
        self.index = index
        self.internal = False
        self.name = name
        self.player = player
        self.is_dlc = is_dlc
        self.max_amount = -1 # -1 = unlimited

        if index is not None:
            self.location = None
            self.code = index
        else:
            self.location = None
            self.code = None

        pass

# Starting index is 133713370000, because hax0rz

item_table = {
    # Executables
    "FTPBounce": ItemData(21, ItemClassification.progression, "Executable", False),
    "SSHCrack": ItemData(22, ItemClassification.progression, "Executable", False),
    "WebServerWorm": ItemData(80, ItemClassification.progression, "Executable", False),
    "SMTPOverflow": ItemData(25, ItemClassification.progression, "Executable", False),
    "SQL_MemCorrupt": ItemData(1433, ItemClassification.progression, "Executable", False),
    "KBTPortTest": ItemData(104, ItemClassification.progression, "Executable", False),
    "DEC Suite": ItemData(111, ItemClassification.progression, "Executable", False),
    "eosDeviceScan": ItemData(3659, ItemClassification.progression, "Executable", False),

    "OpShell": ItemData(113, ItemClassification.useful, "Executable", False),
    "Tracekill": ItemData(114, ItemClassification.progression, "Executable", True), # progression bcs EnTech
    "ThemeChanger": ItemData(115, ItemClassification.useful, "Executable", False),

    "ClockEXE": ItemData(116, ItemClassification.useful, "Executable", False, 1),
    "HexClock": ItemData(117, ItemClassification.filler, "Executable", False, 1),
    "HacknetEXE": ItemData(1337, ItemClassification.filler, "Executable", False, 1),

    "Progressive Faction Access": ItemData(119, ItemClassification.progression, "Faction", False, 3),

    # Labyrinths Executables
    "TorrentStreamInjector": ItemData(6881, ItemClassification.progression, "Executable", True),
    "SSLTrojan": ItemData(443, ItemClassification.progression, "Executable", True),
    "FTPSprint": ItemData(221, ItemClassification.progression, "Executable", False), # technically not a dlc item
    "Mem Suite": ItemData(120, ItemClassification.progression, "Executable", True),
    "PacificPortcrusher": ItemData(192, ItemClassification.progression, "Executable", True),
    "SignalScramble": ItemData(193, ItemClassification.progression, "Executable", True), # progression bcs Take Flight

    "ComShell": ItemData(122, ItemClassification.useful, "Executable", True, 1),
    "NetmapOrganizer": ItemData(123, ItemClassification.useful, "Executable", True, 1),
    "DNotes": ItemData(124, ItemClassification.useful, "Executable", True, 1),

    "Tuneswap": ItemData(125, ItemClassification.filler, "Executable", True, 1),
    "ClockV2": ItemData(126, ItemClassification.filler, "Executable", True, 1),

    # Limits
    "Progressive Shell Limit": ItemData(130, ItemClassification.progression, "Limit", False, 10),
    "Progressive RAM": ItemData(131, ItemClassification.progression, "Limit", False, 10),

    # Filler
    "Mission Skip": ItemData(140, ItemClassification.useful, "Mission Skip", False),
    "ForceHack": ItemData(141, ItemClassification.useful, "Node Skip", False),
    "l33t hax0r skillz": ItemData(142, ItemClassification.filler, "Junk", False),
    "Random IRC Log": ItemData(143, ItemClassification.filler, "Junk", False),
    
    # PointClicker Filler
    "PointClicker +1pt.": ItemData(150, ItemClassification.filler, "PointClicker Point", False),
    "PointClicker +5pt.": ItemData(151, ItemClassification.filler, "PointClicker Point", False),
    "PointClicker +25pt.": ItemData(152, ItemClassification.filler, "PointClicker Point", False),
    "PointClicker +100pt.": ItemData(153, ItemClassification.filler, "PointClicker Point", False),

    "PointClicker +100pt./s": ItemData(155, ItemClassification.progression_skip_balancing, "PointClicker Passive",
                                       False, 5),
    "PointClicker +1000pt./s": ItemData(156, ItemClassification.progression_skip_balancing, "PointClicker Passive",
                                        False, 5),
    "PointClicker Passive*2": ItemData(157, ItemClassification.progression_skip_balancing, "PointClicker Passive",
                                       False, 3),
    "PointClicker Passive*5": ItemData(158, ItemClassification.progression_skip_balancing, "PointClicker Passive",
                                       False, 3),
    "PointClicker Passive*10": ItemData(159, ItemClassification.progression_skip_balancing, "PointClicker Passive",
                                        False, 3),

    # Traps
    "ETAS Trap": ItemData(666, ItemClassification.trap, "Trap", False),
    "Fake Connection": ItemData(667, ItemClassification.trap, "Trap", False),
    "Reset PointClicker Points": ItemData(668, ItemClassification.trap, "PointClicker Trap", False),
    "ForkBomb": ItemData(669, ItemClassification.trap, "Trap", False),

    # Events
    "Fulfill Bit's Final Request": ItemData(None, ItemClassification.progression, "Event", False), # Stop PortHack.Heart
    "Altitude Loss": ItemData(None, ItemClassification.progression, "Event", True), # Finish Final Labs Mission
    "Become A Veteran": ItemData(None, ItemClassification.progression, "Event", True), # Break Into The Gibson

    "Entropy VIP": ItemData(None, ItemClassification.progression, "Event", False), # Complete EVERY Entropy Mission
    "CSEC VIP": ItemData(None, ItemClassification.progression, "Event", False), # Complete EVERY CSEC Mission*
    "CSEC Member ID": ItemData(None, ItemClassification.progression, "Event", False), # Join CSEC
    # *(Excluding Project Junebug, if exclude_junebug is enabled)

    # Executable Groups
    # Regional
    "Intro Executable Pack": ItemData(1000, ItemClassification.progression, "Executable Region", False),
    "Entropy Executable Pack": ItemData(1001, ItemClassification.progression, "Executable Region", False),
    "CSEC Executable Pack": ItemData(1002, ItemClassification.progression, "Executable Region", False),
    "Labyrinths Executable Pack": ItemData(1003, ItemClassification.progression, "Executable Region", True),
    "Finale Executable Pack": ItemData(1004, ItemClassification.progression, "Executable Region", False),

    # Practicality
    "Portcrusher Pack": ItemData(1005, ItemClassification.progression, "Executable Pack", False),
    "Labyrinths Portcrusher Pack": ItemData(1006, ItemClassification.progression, "Executable Pack", True),
    "Clock Pack": ItemData(1007, ItemClassification.useful, "Executable Pack", False, 1),
    "Misc. Executables Pack": ItemData(1008, ItemClassification.useful, "Executable Pack", False, 1),

    # Mission Items
    # "Corrupted PM Firmware": ItemData(2000, ItemClassification.progression, "MacGuffin", False),
    # "Database Password Reset": ItemData(2001, ItemClassification.progression, "MacGuffin", True),
}