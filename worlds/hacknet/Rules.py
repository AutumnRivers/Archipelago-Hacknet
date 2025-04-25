from BaseClasses import MultiWorld, ItemClassification

from worlds.generic.Rules import set_rule, add_rule, forbid_items_for_player
from worlds.AutoWorld import World

from .Options import HacknetOptions
from .Items import HacknetItem

"""
[------- LAY OF THE LAND (RULES) -------]
Intro -> Entropy
Entropy -> /EL SEC(!!!!!!!! VERY IMPORTANT)
/el Sec -> CSEC
CSEC -> Labyrinths (if labs is enabled)
Labyrinths/CSEC -> Bit/Finale 
"""
def set_rules(multiworld: MultiWorld, options: HacknetOptions, player: int) -> None:
    shuffle_execs = int(options.shuffle_execs)
    shuffle_labs = bool(options.shuffle_labs)
    shuffle_achievements = bool(options.shuffle_achvs)
    shuffle_nodes = bool(options.shuffle_nodes)
    shuffle_ptc = int(options.shuffle_ptc)
    shuffle_limits = int(options.enable_limits)
    exclude_junebug = bool(options.exclude_junebug)
    faction_access = int(options.faction_access)
    player_goal = int(options.player_goal)

    def create_event(event: str) -> HacknetItem:
        return HacknetItem(event, player, (None, ItemClassification.progression, "Event", False), True)

    def set_basic_rule(loc_name: str, prev_loc: str):
        """
        Sets a "basic" rule - basically, can the player reach this previous location?
        """
        set_rule(multiworld.get_location(loc_name, player),
                 lambda state: multiworld.get_location(prev_loc, player).can_reach(state))

    def set_exec_rule(loc_name: str, *execs: str):
        """
        Sets an "executable" rule - does the player have all these executables?
        """
        if shuffle_execs == 4 or len(execs) == 0:
            return
        for exec_name in execs:
            if exec_name == "FTPBounce":
                set_rule(multiworld.get_location(loc_name, player),
                         lambda state: state.has("FTPBounce", player) or state.has("FTPSprint", player))
            else:
                set_rule(multiworld.get_location(loc_name, player),
                         lambda state: state.has(exec_name, player))

    def set_exec_rule_with_loc(loc_name: str, prev_loc: str, *execs: str):
        set_basic_rule(loc_name, prev_loc)
        set_exec_rule(loc_name, *execs)

    def set_faction_access_rule(loc_name: str, amount_needed: int):
        """
        Does what it says on the tin. Self-explanatory.
        1 - Entropy
        2 - Kaguya Trials
        3 - CSEC
        """
        if faction_access == 3:
            return
        set_rule(multiworld.get_location(loc_name, player),
                 lambda state: state.has("Progressive Faction Access", player, amount_needed))

    def set_limits_rule(loc_name: str, shells_needed: int, ram_upgrades_needed: int):
        """
        This is only used for finale nodes, really.
        Altitude Loss and EnTech Backups logically require ~5 shells and maximum RAM.
        Gibson logically requires maximum shells and maximum RAM.
        """
        if shuffle_limits == 5:
            return

        has_shell_limits = shuffle_limits in (1, 2, 3)
        has_ram_limits = shuffle_limits in (1, 4)

        set_rule(multiworld.get_location(loc_name, player),
                 lambda state: (not has_shell_limits or state.has("Progressive Shell Limit", player, shells_needed)) and
                               (not has_ram_limits or state.has("Progressive RAM", player, ram_upgrades_needed))
                 )

    def set_partial_rule(loc_name: str, prev_loc: str, faction_access_needed: int,
                         *execs: str):
        """
        Same thing as below, but without limit requirements. For early nodes.
        """
        set_basic_rule(loc_name, prev_loc)
        set_exec_rule(loc_name, *execs)
        set_faction_access_rule(loc_name, faction_access_needed)

    def set_full_rule(loc_name: str, prev_loc: str, faction_access_needed: int,
                      shells_needed: int, ram_upgrades_needed: int, *execs: str):
        """
        The amalgamation of everything above. The full package. Oh, yeah, baby.
        """
        set_basic_rule(loc_name, prev_loc)
        set_exec_rule(loc_name, *execs)
        set_faction_access_rule(loc_name, faction_access_needed)
        set_limits_rule(loc_name, shells_needed, ram_upgrades_needed)

    def set_mission_rules():
        dont_shuffle_execs = shuffle_execs == 5
        no_faction_access = faction_access == 3

        # Intro
        for loc in multiworld.get_locations(player):
            print(loc.name)
        set_rule(multiworld.get_location("Intro -- Maiden Flight", player),
                 lambda state: state.has("SSHCrack", player) or
                               state.has("SMTPOverflow", player) or
                               state.has("WebServerWorm", player) or
                               (state.has("FTPBounce", player) or state.has("FTPSprint", player)) or
                                dont_shuffle_execs
                 )
        set_basic_rule("Intro -- Something in return", "Intro -- Maiden Flight")
        set_basic_rule("Intro -- Where to from here", "Intro -- Something in return")
        set_basic_rule("Entropy -- Confirmation Mission", "Intro -- Where to from here")
        set_basic_rule("Entropy -- Welcome", "Entropy -- Confirmation Mission")

        # Entropy Sets
        set_partial_rule("Entropy -- PointClicker (Mission)", "Entropy -- Welcome", 1)
        set_partial_rule("Entropy -- The famous counter-hack", "Entropy -- Welcome", 1)
        set_partial_rule("Entropy -- Back to School", "Entropy -- Welcome", 1)
        set_partial_rule("Entropy -- X-C Project", "Entropy -- Welcome", 1)

        # Entropy - eOS Intro
        set_partial_rule("Entropy -- Smash N' Grab", "Entropy -- Welcome", 1,
                         "eosDeviceScan")
        # This one below will implicitly check for faction access and eosDeviceScan, so it can be basic
        set_basic_rule("Entropy -- eOS Device Scanning", "Entropy -- Smash N' Grab")
        set_rule(multiworld.get_location("Entropy -- Naix", player),
                 lambda state: (((state.has("WebServerWorm", player) or state.has("SMTPOverflow", player)) and
                               (state.has("FTPBounce", player) or state.has("FTPSprint", player))) or
                               dont_shuffle_execs) and
                               multiworld.get_location("Entropy -- Smash N' Grab", player).can_reach(state)
                 )

        # /el Sec
        # IIRC, only Polar Star needs to be completed in /el...
        set_partial_rule("Naix -- Deface Nortron Website", "Entropy -- Naix",
                         0, "WebServerWorm", "SMTPOverflow")
        set_partial_rule("Naix -- Nortron Security Mainframe", "Naix -- Deface Nortron Website",
                         0, "FTPBounce", "SSHCrack")
        # From here on out, it's assumed the player has the base 4 executables (ftp, ssh, web, smtp)
        set_basic_rule("/el -- Head of Polar Star (Download Files)", "Naix -- Nortron Security Mainframe")
        set_basic_rule("/el -- SecuLock Drive", "Naix -- Nortron Security Mainframe")

        # CSEC Intro
        set_basic_rule("CSEC -- CFC Herbs & Spices", "/el -- Head of Polar Star (Download Files)")

        # Set Labyrinths rules (if applicable)
        set_labyrinths_mission_rules()

        if shuffle_labs:
            set_rule(multiworld.get_location("Join CSEC", player),
                     lambda state: multiworld.get_location("Labyrinths -- Altitude Loss", player).can_reach(state) and
                                   (no_faction_access or state.has("Progressive Faction Access", player, 3)) and
                                   (dont_shuffle_execs or state.has("SQL_MemCorrupt", player))
                     )
            set_basic_rule("CSEC -- Subvert Psylance Investigation", "Join CSEC")
        else:
            set_rule(multiworld.get_location("Join CSEC", player),
                     lambda state: multiworld.get_location("CSEC -- CFC Herbs & Spices", player).can_reach(state) and
                                   (no_faction_access or state.has("Progressive Faction Access", player, 2)) and
                                   (dont_shuffle_execs or state.has("SQL_MemCorrupt", player))
                     )

        # CSEC Sets
        set_basic_rule("CSEC -- Investigate a medical record", "Join CSEC")
        set_basic_rule("CSEC -- Teach an old dog new tricks", "Join CSEC")
        set_basic_rule("CSEC -- Remove a Fabricated Death Row Record", "Join CSEC")
        set_basic_rule("CSEC -- Check out a suspicious server", "Join CSEC")
        set_basic_rule("CSEC -- Wipe clean an academic record", "Join CSEC")
        set_basic_rule("CSEC -- Add a Death Row record for a family member", "Join CSEC")
        set_basic_rule("CSEC -- Compromise an eOS Device", "Join CSEC")

        # CSEC DEC
        set_exec_rule_with_loc("CSEC -- Locate or Create Decryption Software", "Join CSEC",
                               "DEC Suite")
        set_basic_rule("CSEC -- Help an aspiring writer", "CSEC -- Locate or Create Decryption Software")
        set_basic_rule("CSEC -- Decrypt a secure transmission", "CSEC -- Locate or Create Decryption Software")

        # Junebug
        set_exec_rule_with_loc("CSEC -- Project Junebug", "CSEC -- Locate or Create Decryption Software",
                               "KBTPortTest")

        # CSEC -> Bit
        set_basic_rule("CSEC -- Investigate a CSEC member's disappearance", "CSEC -- Project Junebug")

        # Finale
        # NO MORE EXECUTABLES ARE REQUIRED! HALLELUIJAH
        set_basic_rule("Bit -- Foundation", "CSEC -- Investigate a CSEC member's disappearance")
        set_basic_rule("Bit -- Substantiation", "Bit -- Foundation")
        set_basic_rule("Bit -- Investigation", "Bit -- Substantiation")
        set_basic_rule("Bit -- Propagation", "Bit -- Investigation")
        set_basic_rule("Bit -- Termination", "Bit -- Propagation")
        set_basic_rule("Stop PortHack.Heart", "Bit -- Termination")

        # Determine Victory Conditions
        if player_goal == 1:
            multiworld.get_location("Stop PortHack.Heart", player).place_locked_item(
                create_event("Fulfill Bit's Final Request")
            )
            multiworld.completion_condition[player] = lambda state: state.has("Fulfill Bit's Final Request", player)

    def set_labyrinths_mission_rules() -> None:
        # Labyrinths
        set_partial_rule("Labyrinths -- Kaguya Trials", "CSEC -- CFC Herbs & Spices", 2,
                         "TorrentStreamInjector")
        set_basic_rule("Labyrinths -- The Ricer", "Labyrinths -- Kaguya Trials")
        set_partial_rule("Labyrinths -- DDOSer on some critical servers", "Labyrinths -- The Ricer", 2,
                         "SSLTrojan")
        set_basic_rule("Labyrinths -- Hermetic Alchemists", "Labyrinths -- DDOSer on some critical servers")
        set_exec_rule_with_loc("Labyrinths -- Memory Forensics", "Labyrinths -- Hermetic Alchemists",
                               "Mem Suite")
        set_basic_rule("Labyrinths -- Striker's Stash", "Labyrinths -- Memory Forensics")
        set_basic_rule("Labyrinths -- Cleanup/It Follows", "Labyrinths -- Striker's Stash")
        set_basic_rule("Labyrinths -- Neopals", "Labyrinths -- Cleanup/It Follows")
        set_basic_rule("Labyrinths -- Bean Stalk/Expo Grave/The Keyboard Life", "Labyrinths -- Neopals")
        set_basic_rule("Labyrinths -- Take Flight", "Labyrinths -- Bean Stalk/Expo Grave/The Keyboard Life")
        set_exec_rule_with_loc("Labyrinths -- Take Flight Cont.", "Labyrinths -- Take Flight",
                               "PacificPortcrusher")
        set_basic_rule("Labyrinths -- Altitude Loss", "Labyrinths -- Take Flight Cont.")
        pass

    def set_pointclicker_rules():
        # Does PointClicker even need rules...?
        if shuffle_ptc == 3:
            return
        pass

    def set_achievement_rules():
        pass

    def set_node_rules(): # this one is gonna be the most annoying :/
        pass

    set_mission_rules()