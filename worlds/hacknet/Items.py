"""
Defines progression, junk and event items for Hacknet
"""
import typing

from BaseClasses import Item, ItemClassification, Location

offset = 13370000

def hacknet_item_to_ap_id(data, event):
    if data[1] is None:
        return None
    else:
        return offset + data[1]

def ap_id_to_hacknet_item(ap_id):
    val = ap_id - offset
    
    hn_item = [item for item in item_table if item_table[item][1] == val]

    if len(hn_item) > 1:
        raise Exception(f'List returned more than one item')
    elif hn_item[0] is None:
        raise Exception(f'Item does not exist')
    else:
        return hn_item[0]

class HacknetItem(Item):
    """
    Item from the game Hacknet
    """
    game: str = "Hacknet"

    def __init__(self, name, player, data, event):
        # (advancement type, index, is exclusive to Labyrinths)
        (advancement, index, isLabs) = data

        if name == "SSHCrack" or name == "FTPBounce":
            self.classification = ItemClassification.progression_skip_balancing
        elif name == "ETASTrap":
            self.classification = ItemClassification.trap
        elif advancement == "progression":
            self.classification = ItemClassification.progression
        elif advancement == "useful":
            self.classification = ItemClassification.useful
        elif advancement == "aesthetic":
            self.classification = ItemClassification.filler
        else:
            self.classification = ItemClassification.filler
        
        self.index = index
        self.internal = False

        self.name = name
        self.player = player

        if index is not None:
            self.location = None
            self.code = self.index + offset
        else:
            self.code = None
            self.location = None

item_table = {
    "SSHCrack" : ("progression", 21, False),
    "FTPBounce" : ("progression", 22, False),
    "SMTPOverflow" : ("progression", 25, False),
    "SQL_MemCorrupt" : ("progression", 1433, False),
    "WebServerWorm" : ("progression", 80, False),
    "KBTPortTest" : ("progression", 104, False),
    "Decypher" : ("progression", 111, False),
    "DECHead" : ("progression", 112, False),
    "eosDeviceScan" : ("progression", 3659, False),

    "OpShell" : ("useful", 113, False), # This isn't usually in the base game, but let's have fun
    "Tracekill" : ("useful", 114, False),

    "ThemeChanger" : ("aesthetic", 115, False),
    "Clock" : ("aesthetic", 116, False),
    "HexClock" : ("aesthetic", 117, False),

    "SecurityTracer" : ("junk", 118, False),
    "HacknetEXE" : ("junk", 127, False),
    # Forces the player into the Emergency Trace Aversion System (CSEC_Member flag is applied on game load w/ mod)
    "ETASTrap" : ("trap", 119, False),

    # Labyrinths Programs
    "TorrentStreamInjector" : ("progression", 6881, True),
    "SSLTrojan" : ("progression", 443, True),
    "FTPSprint" : ("progression", 211, True),
    "MemDumpGenerator" : ("progression", 120, True),
    "MemForensics" : ("progression", 121, True),
    "SignalScrambler" : ("progression", 32, True),
    "PacificPortcrusher" : ("progression", 192, True),

    "ComShell" : ("useful", 122, True),
    "NetmapOrganizer" : ("useful", 123, True),

    "DNotes" : ("aesthetic", 124, True),
    "Tuneswap" : ("aesthetic", 125, True),
    "ClockV2" : ("aesthetic", 126, True),

    # Events
    "Finish Tutorial" : ("progression", None, False),
    "Join Entropy" : ("progression", None, False),
    "Hacked by Naix" : ("progression", None, False),
    "Join CSEC" : ("progression", None, False),
    "Join /el Sec" : ("useful", None, False),
    "Get Sequencer" : ("progression", None, False),
    "Stop PortHack.Heart" : ("progression", None, False),

    # Labs Events
    "Finish Kaguya Trials" : ("progression", None, True),
    "Finish Alchemists" : ("progression", None, True),
    "CoelTrain Recovery" : ("progression", None, True),
    "Altitude Loss" : ("progression", None, True),

    "Crash The Plane" : ("progression", None, True),
    "Save The Plane" : ("progression", None, True),
    "Crash Both Planes" : ("progression", None, True),

    "Watched Labs Credits" : ("progression", None, True),
    "Gained Gibson Admin" : ("progression", None, True)
}