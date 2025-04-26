import typing

from BaseClasses import Location, LocationProgressType

starting_index = 133713370000 # l33t hax0rz
junebug_mission_id = starting_index + 32
junebug_node_ids = (
    starting_index + 200, starting_index + 201,
    starting_index + 202, starting_index + 202
)

class HacknetLocData(typing.NamedTuple):
    id: int | None
    region: str
    display_name: str
    is_dlc: bool
    is_ptc: typing.Optional[bool] = False # ptc = PointClicker, default to false

class HacknetLocation(Location):
    game: str = "Hacknet"

    def __init__(self, player, name, data, region):
        self.player = player
        self.name = name
        self.address = data[0]
        self.raw_region = region

        self.parent_region = None

mission_table = [
    HacknetLocData(starting_index, "Menu", "Intro -- First Contact", False, False),
    HacknetLocData(starting_index + 1, "Intro", "Intro -- Maiden Flight", False, False),
    HacknetLocData(starting_index + 2, "Intro", "Intro -- Something in return", False, False),
    HacknetLocData(starting_index + 3, "Intro", "Intro -- Where to from here", False, False),
    HacknetLocData(starting_index + 4, "Intro", "Intro -- Getting some tools together", False, False),
    HacknetLocData(starting_index + 5, "Intro", "Entropy -- Confirmation Mission", False, False),
    HacknetLocData(starting_index + 6, "Intro", "Entropy -- Welcome", False, False),

    # Entropy
    HacknetLocData(starting_index + 10, "Entropy", "Entropy -- PointClicker (Mission)", False, False),
    HacknetLocData(starting_index + 11, "Entropy", "Entropy -- The famous counter-hack", False, False),
    HacknetLocData(starting_index + 12, "Entropy", "Entropy -- Back to School", False, False),
    HacknetLocData(starting_index + 13, "Entropy", "Entropy -- X-C Project", False, False),
    HacknetLocData(starting_index + 14, "Entropy", "Entropy -- Smash N' Grab", False, False),
    HacknetLocData(starting_index + 15, "Entropy", "Entropy -- eOS Device Scanning", False, False),
    HacknetLocData(starting_index + 16, "Entropy - Naix", "Entropy -- Naix", False, False),
    HacknetLocData(None, "Entropy", "Complete Every Entropy Mission", False, False),

    # /el
    HacknetLocData(starting_index + 1337, "/el Sec - Naix", "Naix -- Deface Nortron Website", False, False),
    HacknetLocData(starting_index + 1338, "/el Sec - Naix", "Naix -- Nortron Security Mainframe", False, False),
    HacknetLocData(starting_index + 1330, "/el Sec - Polar Star", "/el -- Head of Polar Star (Download Files)", False,
                   False),
    HacknetLocData(starting_index + 1331, "/el Sec - SecuLock", "/el -- SecuLock Drive", False, False),

    # CSEC
    HacknetLocData(starting_index + 20, "CSEC - Intro", "CSEC -- CFC Herbs & Spices", False, False),
    HacknetLocData(starting_index + 21, "CSEC", "CSEC -- Investigate a medical record", False, False),
    HacknetLocData(starting_index + 22, "CSEC", "CSEC -- Teach an old dog new tricks", False, False),
    HacknetLocData(starting_index + 23, "CSEC - DEC", "CSEC -- Locate or Create Decryption Software", False, False),
    HacknetLocData(starting_index + 24, "CSEC", "CSEC -- Remove a Fabricated Death Row Record", False, False),
    HacknetLocData(starting_index + 25, "CSEC - DEC", "CSEC -- Track an Encrypted File", False, False),
    HacknetLocData(starting_index + 26, "CSEC", "CSEC -- Check out a suspicious server", False, False),
    HacknetLocData(starting_index + 27, "CSEC", "CSEC -- Wipe clean an academic record", False, False),
    HacknetLocData(starting_index + 28, "CSEC", "CSEC -- Help an aspiring writer", False, False),
    HacknetLocData(starting_index + 29, "CSEC", "CSEC -- Add a Death Row record for a family member", False, False),
    HacknetLocData(starting_index + 30, "CSEC - DEC", "CSEC -- Decrypt a secure transmission", False, False),
    HacknetLocData(starting_index + 31, "CSEC", "CSEC -- Compromise an eOS Device", False, False),
    HacknetLocData(starting_index + 32, "CSEC - Project Junebug", "CSEC -- Project Junebug", False, False),
    HacknetLocData(starting_index + 33, "CSEC - Bit", "CSEC -- Investigate a CSEC member's disappearance", False, False),
    HacknetLocData(None, "CSEC", "Complete Every CSEC Mission", False, False),
    HacknetLocData(None, "CSEC", "Join CSEC", False, False),

    # V/Bit/Finale
    HacknetLocData(starting_index + 40, "Finale", "Bit -- Foundation", False, False),
    HacknetLocData(starting_index + 41, "Finale", "Bit -- Substantiation", False, False),
    HacknetLocData(starting_index + 42, "Finale", "Bit -- Investigation", False, False),
    HacknetLocData(starting_index + 43, "Finale", "Bit -- Propagation", False, False),
    HacknetLocData(starting_index + 44, "Finale", "Bit -- Termination", False, False),
    HacknetLocData(None, "Finale", "Stop PortHack.Heart", False, False),

    # Labyrinths
    # These are each given their own regions for purpose of grouping them with admin access checks
    HacknetLocData(starting_index + 50, "Labyrinths - Kaguya Trials", "Labyrinths -- Kaguya Trials", True, False),
    HacknetLocData(starting_index + 51, "Labyrinths - Set 1", "Labyrinths -- The Ricer", True, False),
    HacknetLocData(starting_index + 52, "Labyrinths - Set 2", "Labyrinths -- DDOSer on some critical servers", True,
                   False),
    HacknetLocData(starting_index + 53, "Labyrinths - Set 3", "Labyrinths -- Cleanup/It Follows", True, False),
    HacknetLocData(starting_index + 54, "Labyrinths - Set 4", "Labyrinths -- Bean Stalk/Expo Grave/The Keyboard Life",
                   True, False),
    HacknetLocData(starting_index + 55, "Labyrinths - Neopals", "Labyrinths -- Neopals", True, False),
    HacknetLocData(starting_index + 56, "Labyrinths - Memory Forensics", "Labyrinths -- Memory Forensics", True, False),
    HacknetLocData(starting_index + 57, "Labyrinths - Striker", "Labyrinths -- Striker's Stash", True, False),
    HacknetLocData(starting_index + 58, "Labyrinths - Hermetic Alchemists", "Labyrinths -- Hermetic Alchemists", True,
                   False),
    HacknetLocData(starting_index + 59, "Labyrinths - Take Flight", "Labyrinths -- Take Flight", True, False),
    HacknetLocData(starting_index + 60, "Labyrinths - Altitude Loss", "Labyrinths -- Take Flight Cont.", True, False),
    HacknetLocData(starting_index + 61, "Labyrinths - Altitude Loss", "Labyrinths -- Altitude Loss", True, False),
    HacknetLocData(starting_index + 62, "Post-Labyrinths", "CSEC -- Subvert Psylance Investigation", True, False),

    HacknetLocData(None, "Labyrinths", "Watched Labyrinths Credits", True, False),
    HacknetLocData(None, "Post-Labyrinths", "Broke Into The Gibson", True, False)
]

pointclicker_table = [
    # Upgrades
    HacknetLocData(starting_index + 70, "PointClicker", "PointClicker -- Click Me!", False, True),
    HacknetLocData(starting_index + 71, "PointClicker", "PointClicker -- Autoclicker v1", False, True),
    HacknetLocData(starting_index + 72, "PointClicker", "PointClicker -- Autoclicker v2", False, True),
    HacknetLocData(starting_index + 73, "PointClicker", "PointClicker -- Pointereiellion", False, True),
    HacknetLocData(starting_index + 74, "PointClicker", "PointClicker -- Upgrade 4", False, True),
    HacknetLocData(starting_index + 75, "PointClicker", "PointClicker -- Upgrade 5", False, True),
    HacknetLocData(starting_index + 76, "PointClicker", "PointClicker -- Upgrade 6", False, True),
    HacknetLocData(starting_index + 77, "PointClicker", "PointClicker -- Upgrade 7", False, True),
    HacknetLocData(starting_index + 78, "PointClicker", "PointClicker -- Upgrade 8", False, True),
    HacknetLocData(starting_index + 79, "PointClicker", "PointClicker -- Upgrade 9", False, True),
    HacknetLocData(starting_index + 80, "PointClicker", "PointClicker -- Upgrade 10", False, True),
    HacknetLocData(starting_index + 81, "PointClicker", "PointClicker -- Upgrade 11", False, True),
    HacknetLocData(starting_index + 82, "PointClicker", "PointClicker -- Upgrade 12", False, True),
    HacknetLocData(starting_index + 83, "PointClicker", "PointClicker -- Upgrade 13", False, True),
    HacknetLocData(starting_index + 84, "PointClicker", "PointClicker -- Upgrade 14", False, True),
    HacknetLocData(starting_index + 85, "PointClicker", "PointClicker -- Upgrade 15", False, True),
    HacknetLocData(starting_index + 86, "PointClicker", "PointClicker -- Upgrade 16", False, True),
    HacknetLocData(starting_index + 87, "PointClicker", "PointClicker -- Upgrade 17", False, True),
    HacknetLocData(starting_index + 88, "PointClicker", "PointClicker -- Upgrade 18", False, True),
    HacknetLocData(starting_index + 89, "PointClicker", "PointClicker -- Upgrade 19", False, True),
    HacknetLocData(starting_index + 90, "PointClicker", "PointClicker -- Upgrade 20", False, True),
    HacknetLocData(starting_index + 91, "PointClicker", "PointClicker -- Upgrade 21", False, True),
    HacknetLocData(starting_index + 92, "PointClicker", "PointClicker -- Upgrade 22", False, True),
    HacknetLocData(starting_index + 93, "PointClicker", "PointClicker -- Upgrade 23", False, True),
    HacknetLocData(starting_index + 94, "PointClicker", "PointClicker -- Upgrade 24", False, True),
    HacknetLocData(starting_index + 95, "PointClicker", "PointClicker -- Upgrade 25", False, True),
    HacknetLocData(starting_index + 96, "PointClicker", "PointClicker -- Upgrade 26", False, True),
    HacknetLocData(starting_index + 97, "PointClicker", "PointClicker -- Upgrade 27", False, True),
    HacknetLocData(starting_index + 98, "PointClicker", "PointClicker -- Upgrade 28", False, True),
    HacknetLocData(starting_index + 99, "PointClicker", "PointClicker -- Upgrade 29", False, True),
    HacknetLocData(starting_index + 100, "PointClicker", "PointClicker -- Upgrade 30", False, True),
    HacknetLocData(starting_index + 101, "PointClicker", "PointClicker -- Upgrade 31", False, True),
    HacknetLocData(starting_index + 102, "PointClicker", "PointClicker -- Upgrade 32", False, True),
    HacknetLocData(starting_index + 103, "PointClicker", "PointClicker -- Upgrade 33", False, True),
    HacknetLocData(starting_index + 104, "PointClicker", "PointClicker -- Upgrade 34", False, True),
    HacknetLocData(starting_index + 105, "PointClicker", "PointClicker -- Upgrade 35", False, True),
    HacknetLocData(starting_index + 106, "PointClicker", "PointClicker -- Upgrade 36", False, True),
    HacknetLocData(starting_index + 107, "PointClicker", "PointClicker -- Upgrade 37", False, True),
    HacknetLocData(starting_index + 108, "PointClicker", "PointClicker -- Upgrade 38", False, True),
    HacknetLocData(starting_index + 109, "PointClicker", "PointClicker -- Upgrade 39", False, True),
    HacknetLocData(starting_index + 110, "PointClicker", "PointClicker -- Upgrade 40", False, True),
    HacknetLocData(starting_index + 111, "PointClicker", "PointClicker -- Upgrade 41", False, True),
    HacknetLocData(starting_index + 112, "PointClicker", "PointClicker -- Upgrade 42", False, True),
    HacknetLocData(starting_index + 113, "PointClicker", "PointClicker -- Upgrade 43", False, True),
    HacknetLocData(starting_index + 114, "PointClicker", "PointClicker -- Upgrade 44", False, True),
    HacknetLocData(starting_index + 115, "PointClicker", "PointClicker -- Upgrade 45", False, True),
    HacknetLocData(starting_index + 116, "PointClicker", "PointClicker -- Upgrade 46", False, True),
    HacknetLocData(starting_index + 117, "PointClicker", "PointClicker -- Upgrade 47", False, True),
    HacknetLocData(starting_index + 118, "PointClicker", "PointClicker -- Upgrade 48", False, True),
    HacknetLocData(starting_index + 119, "PointClicker", "PointClicker -- Upgrade 49", False, True),
    HacknetLocData(starting_index + 120, "PointClicker", "PointClicker -- Upgrade 50", False, True)
]

achievements_table = [
    HacknetLocData(starting_index + 130, "Menu", "Achievement -- Quickdraw", False, False),
    HacknetLocData(starting_index + 131, "Entropy", "Achievement -- To the Wire", False, False),
    HacknetLocData(starting_index + 132, "CSEC", "Achievement -- Makeover!", False, False),
    HacknetLocData(starting_index + 133, "Entropy", "Achievement -- Join Entropy", False, False),
    HacknetLocData(starting_index + 134, "CSEC", "Achievement -- Join CSEC", False, False),
    HacknetLocData(starting_index + 135, "/el Sec", "Achievement -- TRUE ULTIMATE POWER!", False, False),
    HacknetLocData(starting_index + 136, "/el Sec", "Achievement -- Rude//el Sec Champion", False, False),
    HacknetLocData(starting_index + 137, "PointClicker", "Achievement -- PointClicker", False, False),
    HacknetLocData(starting_index + 138, "PointClicker", "Achievement -- You better not have clicked for those...",
                   False, False)
]

node_admin_table = [
    # oh boy here we go
    HacknetLocData(starting_index + 140, "Menu", "Intro -- Player's PC", False), # basically a freebie, fires after tutorial is finished
    HacknetLocData(starting_index + 157, "Menu", "Intro -- Archipelago Backups", False),
    HacknetLocData(starting_index + 141, "Intro", "Intro -- Bitwise Test PC", False),
    HacknetLocData(starting_index + 142, "Intro", "Intro -- P. Anderson's Bedroom PC", False),
    HacknetLocData(starting_index + 143, "Intro", "Intro -- Entropy test Server", False),
    HacknetLocData(starting_index + 144, "Intro", "Intro -- Viper-Battlestation", False),

    # Entropy
    HacknetLocData(starting_index + 145, "Entropy", "Entropy -- Slash-Bot News Network", False),
    HacknetLocData(starting_index + 146, "Entropy", "Entropy -- Entropy Asset Server", False),
    HacknetLocData(starting_index + 147, "Entropy", "Entropy -- Milburg High IT Office", False),
    HacknetLocData(starting_index + 148, "Entropy", "Entropy -- PointClicker (Admin Access)", False),
    HacknetLocData(starting_index + 149, "Entropy", "Entropy -- PP Marketing Inc.", False), # hehe pp
    HacknetLocData(starting_index + 150, "Entropy", "Entropy -- X-C Project Tablet#001//RESEARCH", False),
    HacknetLocData(starting_index + 151, "Entropy", "Entropy -- Jason's PowerBook Plus", False),
    HacknetLocData(starting_index + 152, "Entropy", "Entropy -- JDel Home PC", False),
    HacknetLocData(starting_index + 153, "Entropy", "Entropy -- Jacob's ePhone 4", False),
    HacknetLocData(starting_index + 154, "Entropy - Naix", "Entropy -- Naix Root Gateway", False),
    HacknetLocData(starting_index + 155, "Entropy - Naix", "Entropy -- Proxy_Node-X22", False),
    HacknetLocData(starting_index + 156, "Entropy - Naix", "Entropy -- Proxy_Node-X04", False),

    # Naix/el
    HacknetLocData(starting_index + 160, "/el Sec - Naix", "Naix -- Nortron Security Web Server", False),
    HacknetLocData(starting_index + 161, "/el Sec - Naix", "Naix -- Nortron Internal Services Server", False),
    HacknetLocData(starting_index + 162, "/el Sec - Naix", "Naix -- Nortron Mainframe", False),
    # Nortron Mail is skipped since you're not meant to get into it...

    # This has its region set to Finale since it needs finale portcrackers
    HacknetLocData(starting_index + 163, "Finale", "/el -- /el Message Board", False),
    HacknetLocData(starting_index + 164, "/el Sec - SecuLock", "/el -- COME AT ME /EL's Secure SecuLock Drive", False),
    HacknetLocData(starting_index + 165, "/el Sec - SecuLock", "/el -- Stormrider", False),

    # Polar Star
    HacknetLocData(starting_index + 166, "/el Sec - Polar Star", "/el -- Shrine of the Polar Star", False),
    HacknetLocData(starting_index + 167, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Patience", False),
    HacknetLocData(starting_index + 168, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Haste", False),
    HacknetLocData(starting_index + 169, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Diligence", False),
    HacknetLocData(starting_index + 170, "/el Sec - Polar Star", "/el -- Tail of Diligence", False),
    HacknetLocData(starting_index + 171, "/el Sec - Polar Star", "/el -- Polar Star - Trial of Focus", False),
    HacknetLocData(starting_index + 172, "/el Sec - Polar Star", "/el -- Head of the Polar Star (Admin Access)", False),
    # This has its region set to CSEC since it needs SQL_MemCorrupt
    # Logically, the player could also get it before this via Labyrinths, but, eh...
    HacknetLocData(starting_index + 173, "CSEC", "/el -- Timekeeper's Vault", False),

    # CSEC
    HacknetLocData(starting_index + 180, "CSEC", "CSEC -- www.cfc.com", False),
    HacknetLocData(starting_index + 181, "CSEC", "CSEC -- CFC Corporate Mainframe", False),
    HacknetLocData(starting_index + 182, "CSEC", "CSEC -- CFC Records Repository", False),
    HacknetLocData(starting_index + 183, "CSEC", "CSEC -- CSEC Crossroads Server", False),
    HacknetLocData(starting_index + 184, "CSEC", "CSEC -- CSEC Public Drop Server", False),
    HacknetLocData(starting_index + 185, "CSEC", "CSEC -- Sal_Home_Workstation", False),
    HacknetLocData(starting_index + 186, "CSEC", "CSEC -- CCC Hacksquad Filedump", False),
    HacknetLocData(starting_index + 187, "CSEC", "CSEC -- Jason's LackBook Pro", False),
    HacknetLocData(starting_index + 188, "CSEC", "CSEC -- Death Row Records Database", False),
    HacknetLocData(starting_index + 189, "CSEC", "CSEC -- International Academic Database", False),
    HacknetLocData(starting_index + 190, "CSEC", "CSEC -- Universal Medical", False),
    HacknetLocData(starting_index + 191, "CSEC - DEC", "CSEC -- DEC Solutions Mainframe", False),
    HacknetLocData(starting_index + 192, "CSEC - DEC", "CSEC -- DEC Solutions Web Server", False),
    HacknetLocData(starting_index + 193, "CSEC - DEC", "CSEC -- Joseph Scott's Battlestation", False),
    HacknetLocData(starting_index + 194, "CSEC - DEC", "CSEC -- Macrosoft Workhorse Server 04", False),
    HacknetLocData(starting_index + 195, "CSEC", "CSEC -- CSEC (Contracts Server)", False),

    # CSEC/Project Junebug
    HacknetLocData(starting_index + 200, "CSEC - Project Junebug", "CSEC -- Eidolon Soft Production Server", False),
    HacknetLocData(starting_index + 201, "CSEC - Project Junebug", "CSEC -- KBT-PM 2.44 REG#10811", False),
    HacknetLocData(starting_index + 202, "CSEC - Project Junebug", "CSEC -- Kellis Biotech Client Services", False),
    HacknetLocData(starting_index + 203, "CSEC - Project Junebug", "CSEC -- Kellis Biotech Production Asset Server",
                   False),

    # CSEC/Bit
    HacknetLocData(starting_index + 204, "CSEC - Bit", "CSEC -- Bitwise Drop Server", False),
    HacknetLocData(starting_index + 205, "CSEC - Bit", "CSEC -- Bitwise Relay 01", False),

    # Bit/Finale
    HacknetLocData(starting_index + 210, "Finale", "Bit -- Bitwise Repo Base", False),
    HacknetLocData(starting_index + 211, "Finale", "Bit -- EnTech External Contractor Relay Server", False),
    HacknetLocData(starting_index + 212, "Finale", "Bit -- EnTech Web Server", False),
    HacknetLocData(starting_index + 213, "Finale", "Bit -- En_Prometheus", False),
    HacknetLocData(starting_index + 214, "Finale", "Bit -- En_Romulus", False),
    HacknetLocData(starting_index + 215, "Finale", "Bit -- EnWorkstationCore", False),
    HacknetLocData(starting_index + 216, "Finale", "Bit -- EnTech Workstation _008", False),
    HacknetLocData(starting_index + 217, "Finale", "Bit -- EnTech_Zeus", False),
    HacknetLocData(starting_index + 218, "Finale", "Bit -- EnTech_Offline_Cycling_Backup", False),
    HacknetLocData(starting_index + 219, "Post-Game", "Post-Game -- Credits Server", False),

    # Labyrinths
    HacknetLocData(starting_index + 230, "Labyrinths", "Kaguya Trials -- Kaguya Sprint Trial", True),
    HacknetLocData(starting_index + 231, "Labyrinths", "Kaguya Trials -- Kaguya Push Trial", True),
    HacknetLocData(starting_index + 232, "Labyrinths", "Kaguya Trials -- Kaguya Source", True),
    HacknetLocData(starting_index + 233, "Labyrinths - Core", "Labyrinths -- Bibliotheque DropServer", True),
    HacknetLocData(starting_index + 234, "Labyrinths - Core", "Labyrinths -- Bibliotheque Ghost Storage", True),
    HacknetLocData(starting_index + 235, "Labyrinths - Set 1", "Labyrinths -- Ricer PC", True),
    HacknetLocData(starting_index + 236, "Labyrinths - Set 2", "Labyrinths -- r00t_Tek Battlestation", True),
    HacknetLocData(starting_index + 237, "Labyrinths - Set 2", "Labyrinths -- L. Shaffer's NetBook", True),
    # Sets 3 & 4 are ignored since they aren't linear and are, therefore, missable
    HacknetLocData(starting_index + 238, "Labyrinths - Memory Forensics", "Labyrinths -- Petunia Verres' Powerbook +",
                   True),
    HacknetLocData(starting_index + 239, "Labyrinths - Memory Forensics", "Labyrinths -- iodependency~Atlas", True),
    HacknetLocData(starting_index + 240, "Labyrinths - Memory Forensics", "Labyrinths -- Snackintosh_PASSTHRU", True),
    HacknetLocData(starting_index + 241, "Labyrinths - Memory Forensics", "Labyrinths -- Snackintosh_Proxy", True),
    HacknetLocData(starting_index + 242, "Labyrinths - Memory Forensics", "Labyrinths -- Lihota Productions", True),
    HacknetLocData(starting_index + 243, "Labyrinths - Memory Forensics", "Labyrinths -- Raven Dataworks", True),

    HacknetLocData(starting_index + 244, "Labyrinths - Hermetic Alchemists",
                   "Labyrinths -- School of the Hermetic Alchemists", True),
    HacknetLocData(starting_index + 245, "Labyrinths - Hermetic Alchemists", "Labyrinths -- HA_Solve", True),
    HacknetLocData(starting_index + 246, "Labyrinths - Hermetic Alchemists", "Labyrinths -- HA_Rebis", True),
    HacknetLocData(starting_index + 247, "Labyrinths - Hermetic Alchemists", "Labyrinths -- Nate's ePhone 4S", True),
    HacknetLocData(starting_index + 248, "Labyrinths - Hermetic Alchemists", "Labyrinths -- Nate Wesson Home", True),
    HacknetLocData(starting_index + 249, "Labyrinths - Hermetic Alchemists",
                   "Labyrinths -- Nate Wesson_STOR-DRIVE(tm)", True),
    HacknetLocData(starting_index + 250, "Labyrinths - Hermetic Alchemists", "Labyrinths -- HA_Coagula", True),

    HacknetLocData(starting_index + 251, "Labyrinths - Striker", "Labyrinths -- Striker Cache", True),
    HacknetLocData(starting_index + 252, "Labyrinths - Striker", "Labyrinths -- Striker Proxy", True),
    HacknetLocData(starting_index + 253, "Labyrinths - Striker", "Labyrinths -- Striker_Battlestation", True),

    HacknetLocData(starting_index + 254, "Labyrinths - Neopals", "Labyrinths -- Neopals Homepage", True),
    HacknetLocData(starting_index + 255, "Labyrinths - Neopals", "Labyrinths -- Neopals_Mainframe", True),
    HacknetLocData(starting_index + 256, "Labyrinths - Neopals", "Labyrinths -- Neopals_Authentication", True),
    HacknetLocData(starting_index + 257, "Labyrinths - Neopals", "Labyrinths -- Neopals_VersionControl", True),
    HacknetLocData(starting_index + 258, "Labyrinths - Neopals", "Labyrinths -- Thomas_Office", True),
    HacknetLocData(starting_index + 259, "Labyrinths - Neopals", "Labyrinths -- Ash-ALIENGEAR13", True),
    HacknetLocData(starting_index + 260, "Labyrinths - Neopals", "Labyrinths -- Tiff Doehan_PersonalPowerbook", True),

    HacknetLocData(starting_index + 261, "Labyrinths - Take Flight", "Labyrinths -- LAX_Pacific_Server", True),
    HacknetLocData(starting_index + 262, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_Network_Hub", True),
    HacknetLocData(starting_index + 263, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_Whitelist_Authenticator",
                   True),
    HacknetLocData(starting_index + 264, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_Network_Hub", True),
    HacknetLocData(starting_index + 265, "Labyrinths - Take Flight", "Labyrinths -- Faith Morello's Laptop", True),
    HacknetLocData(starting_index + 266, "Labyrinths - Take Flight", "Labyrinths -- Vito McMichael's Laptop", True),
    HacknetLocData(starting_index + 267, "Labyrinths - Take Flight", "Labyrinths -- Mark Robertson's Office Computer",
                   True),
    HacknetLocData(starting_index + 268, "Labyrinths - Take Flight", "Labyrinths -- Kim Burnaby's Office Computer",
                   True),
    HacknetLocData(starting_index + 269, "Labyrinths - Take Flight", "Labyrinths -- Yasu Arai's eBook Touch", True),
    HacknetLocData(starting_index + 270, "Labyrinths - Take Flight", "Labyrinths -- PacificAir_BookingsMainframe",
                   True),

    HacknetLocData(starting_index + 271, "Labyrinths - Altitude Loss", "Labyrinths -- Pacific_ATC_RoutingHub", True),
    HacknetLocData(starting_index + 272, "Labyrinths - Altitude Loss",
                   "Labyrinths -- Pacific_ATC_WhitelistAuthenticator", True),
    HacknetLocData(starting_index + 273, "Labyrinths - Altitude Loss", "Labyrinths -- Pacific_ATC_Skylink", True),
    HacknetLocData(starting_index + 274, "Labyrinths - Altitude Loss", "Labyrinths -- PA_747_0022 Flight Computer",
                   True),
    HacknetLocData(starting_index + 275, "Labyrinths - Altitude Loss", "Labyrinths -- PA_747_0018 Flight Computer",
                   True),

    HacknetLocData(starting_index + 276, "Labyrinths - Credits", "Labyrinths -- Kaguya_Projects", True),
    HacknetLocData(starting_index + 277, "Labyrinths - Credits", "Labyrinths -- Kaguya_Gateway", True),
    HacknetLocData(starting_index + 278, "Labyrinths - Credits", "Labyrinths -- Labyrinths_DevChat", True),

    # Post-Labyrinths
    HacknetLocData(starting_index + 279, "Post-Labyrinths", "Labyrinths -- Coel__Gateway", True),
    HacknetLocData(starting_index + 280, "Post-Labyrinths", "Naix -- Pellium Box", True),
    HacknetLocData(starting_index + 281, "Post-Labyrinths", "CSEC -- Psylance Internal Archives", True),
    HacknetLocData(starting_index + 282, "Post-Labyrinths", "CSEC -- Psylance Internal Services", True),
    # Gibson gets its own region that requires EVERY executable, and follows after both,
    # "Labyrinths - Altitude Loss" AND "CSEC - Bit"
    HacknetLocData(starting_index + 283, "Gibson", "Labyrinths -- The Gibson (Veteran)", True)

    # ok. i THINK that's all... around 140 new locations, jesus
]