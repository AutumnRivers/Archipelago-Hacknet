from BaseClasses import MultiWorld, ItemClassification, CollectionState
from Utils import visualize_regions

from worlds.generic.Rules import set_rule, forbid_items
from worlds.AutoWorld import World

from .Options import HacknetOptions

from .RuleSetter import HacknetRuleSetter
from .AdminAccessRules import set_node_rules

"""
[------- LAY OF THE LAND (RULES) -------]
Intro -> Entropy
Entropy -> /EL SEC(!!!!!!!! VERY IMPORTANT)
/el Sec -> CSEC
CSEC -> Labyrinths (if labs is enabled)
Labyrinths/CSEC -> Bit/Finale 
"""
def set_rules(multiworld: MultiWorld, options: HacknetOptions, player: int, world: World) -> None:
    shuffle_execs = int(options.shuffle_execs)
    shuffle_labs = bool(options.shuffle_labs)
    shuffle_achievements = bool(options.shuffle_achvs)
    shuffle_nodes = bool(options.shuffle_nodes)
    shuffle_ptc = int(options.shuffle_ptc)
    exclude_junebug = bool(options.exclude_junebug)
    player_goal = int(options.player_goal)

    rule_setter = HacknetRuleSetter(multiworld, options, player)

    def set_mission_rules():
        dont_shuffle_execs = shuffle_execs == 5

        # Intro
        rule_setter.set_basic_rule("Intro -- Maiden Flight", "Intro -- Getting some tools together")
        rule_setter.set_basic_rule("Intro -- Something in return", "Intro -- Maiden Flight")
        rule_setter.set_basic_rule("Intro -- Where to from here", "Intro -- Something in return")
        rule_setter.set_limits_rule("Intro -- Where to from here", 1, 0)
        rule_setter.set_basic_rule("Entropy -- Confirmation Mission", "Intro -- Where to from here")
        rule_setter.set_basic_rule("Entropy -- Welcome", "Entropy -- Confirmation Mission")
        rule_setter.set_limits_rule("Entropy -- Welcome", 1, 2)

        # Entropy Sets
        rule_setter.set_partial_rule("Entropy -- PointClicker (Mission)", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")
        rule_setter.set_partial_rule("Entropy -- The famous counter-hack", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")
        rule_setter.set_limits_rule("Entropy -- The famous counter-hack", 2, 2)
        rule_setter.set_partial_rule("Entropy -- Back to School", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")
        rule_setter.set_partial_rule("Entropy -- X-C Project", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")

        # Entropy - eOS Intro
        rule_setter.set_partial_rule("Entropy -- eOS Device Scanning", "Entropy -- Back to School", 1,
                         "eosDeviceScan")
        # This one below will implicitly check for faction access and eosDeviceScan, so it can be basic
        rule_setter.set_basic_rule("Entropy -- Smash N' Grab", "Entropy -- eOS Device Scanning")

        forbid_items(multiworld.get_location("Entropy -- Smash N' Grab", player),
                     {"eosDeviceScan"})
        forbid_items(multiworld.get_location("Entropy -- eOS Device Scanning", player),
                     {"eosDeviceScan"})

        if player_goal in (4, 5):
            entropy_missions = {
                "Entropy -- PointClicker (Mission)",
                "Entropy -- The famous counter-hack",
                "Entropy -- Back to School",
                "Entropy -- X-C Project",
                "Entropy -- eOS Device Scanning",
                "Entropy -- Smash N' Grab"
            }

            set_rule(multiworld.get_location("Complete Every Entropy Mission", player),
                     lambda state: rule_setter.player_can_reach_locations(state, entropy_missions))

        rule_setter.set_partial_rule("Entropy -- Naix", "Entropy -- Smash N' Grab", 1, "FTPBounce",
                                     "WebServerWorm", "SMTPOverflow")

        # /el Sec
        # IIRC, only Polar Star needs to be completed in /el...
        rule_setter.set_partial_rule("Naix -- Deface Nortron Website", "Entropy -- Naix",
                         1, "WebServerWorm", "SMTPOverflow")
        rule_setter.set_partial_rule("Naix -- Nortron Security Mainframe", "Naix -- Deface Nortron Website",
                         1, "FTPBounce", "SSHCrack")
        # From here on out, it's assumed the player has the base 4 executables (ftp, ssh, web, smtp)
        rule_setter.set_basic_rule("/el -- Head of Polar Star (Download Files)", "Naix -- Nortron Security Mainframe")

        # CSEC Intro
        rule_setter.set_basic_rule("CSEC -- CFC Herbs & Spices", "/el -- Head of Polar Star (Download Files)")

        # Set Labyrinths rules (if applicable)
        set_labyrinths_mission_rules()

        if shuffle_labs:
            rule_setter.set_partial_rule("Join CSEC", "Labyrinths -- Altitude Loss", 3, "SQL_MemCorrupt")
            rule_setter.set_basic_rule("CSEC -- Subvert Psylance Investigation", "Join CSEC")
        else:
            rule_setter.set_partial_rule("Join CSEC", "CSEC -- CFC Herbs & Spices", 2, "SQL_MemCorrupt")

        # CSEC Sets
        rule_setter.set_basic_rule("CSEC -- Investigate a medical record", "Join CSEC")
        rule_setter.set_basic_rule("CSEC -- Teach an old dog new tricks", "Join CSEC")
        rule_setter.set_basic_rule("CSEC -- Remove a Fabricated Death Row Record", "Join CSEC")
        rule_setter.set_basic_rule("CSEC -- Check out a suspicious server", "Join CSEC")
        rule_setter.set_basic_rule("CSEC -- Wipe clean an academic record", "Join CSEC")
        rule_setter.set_basic_rule("CSEC -- Add a Death Row record for a family member", "Join CSEC")
        rule_setter.set_basic_rule("CSEC -- Compromise an eOS Device", "Join CSEC")

        # CSEC DEC
        rule_setter.set_exec_rule_with_loc("CSEC -- Locate or Create Decryption Software", "Join CSEC",
                               "DEC Suite")
        rule_setter.set_basic_rule("CSEC -- Help an aspiring writer", "CSEC -- Locate or Create Decryption Software")
        rule_setter.set_basic_rule("CSEC -- Decrypt a secure transmission",
                                   "CSEC -- Locate or Create Decryption Software")
        rule_setter.set_basic_rule("CSEC -- Track an Encrypted File", "CSEC -- Locate or Create Decryption Software")

        # Junebug
        if not exclude_junebug:
            rule_setter.set_exec_rule_with_loc("CSEC -- Project Junebug",
                                   "CSEC -- Track an Encrypted File",
                                   "KBTPortTest")

        if player_goal in (4, 5):
            csec_missions: set[str] = {
                "CSEC -- Teach an old dog new tricks",
                "CSEC -- Investigate a medical record",
                "CSEC -- Remove a Fabricated Death Row Record",
                "CSEC -- Check out a suspicious server",
                "CSEC -- Wipe clean an academic record",
                "CSEC -- Add a Death Row record for a family member",
                "CSEC -- Compromise an eOS Device",
                "CSEC -- Locate or Create Decryption Software",
                "CSEC -- Help an aspiring writer",
                "CSEC -- Decrypt a secure transmission",
                "CSEC -- Track an Encrypted File"
            }

            if shuffle_labs:
                csec_missions.add("CSEC -- Subvert Psylance Investigation")

            if not exclude_junebug:
                csec_missions.add("CSEC -- Project Junebug")

            set_rule(multiworld.get_location("Complete Every CSEC Mission", player),
                     lambda state: rule_setter.player_can_reach_locations(state, csec_missions))

        # CSEC -> Bit
        bit_prev_loc = "CSEC -- Project Junebug"
        if exclude_junebug: bit_prev_loc = "CSEC -- Locate or Create Decryption Software"
        rule_setter.set_basic_rule("CSEC -- Investigate a CSEC member's disappearance", bit_prev_loc)

        # Finale
        # NO MORE EXECUTABLES ARE REQUIRED! HALLELUIJAH
        rule_setter.set_basic_rule("Bit -- Foundation", "CSEC -- Investigate a CSEC member's disappearance")
        rule_setter.set_basic_rule("Bit -- Substantiation", "Bit -- Foundation")
        rule_setter.set_basic_rule("Bit -- Investigation", "Bit -- Substantiation")
        rule_setter.set_basic_rule("Bit -- Propagation", "Bit -- Investigation")
        rule_setter.set_basic_rule("Bit -- Termination", "Bit -- Propagation")
        rule_setter.set_full_rule("Bit -- Termination", "Bit -- Propagation", 3,
                                  5, 10, "FTPBounce", "SSHCrack", "WebServerWorm",
                                  "SQL_MemCorrupt", "KBTPortTest", "SMTPOverflow")

        if player_goal in (1, 5):
            rule_setter.set_basic_rule("Stop PortHack.Heart", "Bit -- Termination")

        forbid_items(multiworld.get_location("Bit -- Propagation", player), {"Tracekill", "Mission Skip",
                                                                             "ForceHack"})
        forbid_items(multiworld.get_location("Bit -- Termination", player), {"Tracekill", "Mission Skip",
                                                                             "ForceHack",
                                                                             "Progressive Shell Limit",
                                                                             "Progressive RAM"})

    def set_labyrinths_mission_rules() -> None:
        if not shuffle_labs:
            return

        # Labyrinths
        rule_setter.set_partial_rule("Labyrinths -- Kaguya Trials", "CSEC -- CFC Herbs & Spices", 2,
                         "TorrentStreamInjector")
        rule_setter.set_basic_rule("Labyrinths -- The Ricer", "Labyrinths -- Kaguya Trials")
        rule_setter.set_partial_rule("Labyrinths -- DDOSer on some critical servers", "Labyrinths -- The Ricer", 2,
                         "SSLTrojan")
        rule_setter.set_basic_rule("Labyrinths -- Hermetic Alchemists", "Labyrinths -- DDOSer on some critical servers")
        rule_setter.set_exec_rule_with_loc("Labyrinths -- Memory Forensics", "Labyrinths -- Hermetic Alchemists",
                               "Mem Suite")
        rule_setter.set_basic_rule("Labyrinths -- Striker's Stash", "Labyrinths -- Memory Forensics")
        rule_setter.set_basic_rule("Labyrinths -- Cleanup/It Follows", "Labyrinths -- Striker's Stash")
        rule_setter.set_basic_rule("Labyrinths -- Neopals", "Labyrinths -- Cleanup/It Follows")
        rule_setter.set_basic_rule("Labyrinths -- Bean Stalk/Expo Grave/The Keyboard Life", "Labyrinths -- Neopals")
        rule_setter.set_basic_rule("Labyrinths -- Take Flight", "Labyrinths -- Bean Stalk/Expo Grave/The Keyboard Life")
        rule_setter.set_limits_rule("Labyrinths -- Take Flight", 6, 6)
        rule_setter.set_exec_rule_with_loc("Labyrinths -- Take Flight Cont.", "Labyrinths -- Take Flight",
                               "PacificPortcrusher")
        rule_setter.set_basic_rule("Labyrinths -- Altitude Loss", "Labyrinths -- Take Flight Cont.")

        if player_goal in (2, 5):
            rule_setter.set_basic_rule("Watched Labyrinths Credits", "Labyrinths -- Altitude Loss")

        if player_goal in (3, 5):
            rule_setter.set_full_rule("Broke Into The Gibson", "Labyrinths -- Altitude Loss", 2,
                          10, 10, "FTPSprint", "SSHCrack", "WebServerWorm",
                          "SQL_MemCorrupt", "SMTPOverflow", "KBTPortTest", "TorrentStreamInjector",
                          "PacificPortcrusher")

    def decompose_number(n):
        # Max values for each unit
        max_combo = (3, 3, 3)
        max_total = 3330

        # Shortcut if n exceeds the maximum possible total
        if n >= max_total:
            return max_combo

        best_combo = (0, 0, 0)
        closest_total = -1

        # This is kinda uglee but oh well
        for t in range(4):  # 0 to 3 for 1000s
            for h in range(4):  # 0 to 3 for 100s
                for te in range(4):  # 0 to 3 for 10s
                    total = t * 1000 + h * 100 + te * 10
                    if n >= total > closest_total:
                        closest_total = total
                        best_combo = (t, h, te)

        return best_combo  # (1000s, 100s, 10s)

    def set_pointclicker_rule(loc_name: str, target_rate: int, target_score: int) -> None:
        if shuffle_ptc > 1:
            return
        thousands_needed, hundreds_needed, tens_needed = decompose_number(target_rate)

        static_hundreds = target_score % 1000
        if static_hundreds > 5:
            static_hundreds = 5
        if target_score < 1000:
            static_hundreds = 0

        static_thousands = target_score % 100000
        if static_thousands > 5:
            static_thousands = 5
        if target_score < 100000:
            static_thousands = 0

        set_rule(multiworld.get_location(loc_name, player),
                 lambda state: (state.has("PointClicker Passive*10", player, tens_needed)) and
                               (state.has("PointClicker Passive*100", player, hundreds_needed)) and
                               (state.has("PointClicker Passive*1000", player, thousands_needed)) and
                               (state.has("PointClicker +100pt./s", player, static_hundreds)) and
                               (state.has("PointClicker +1000pt./s", player, static_thousands)))

    def set_pointclicker_rules():
        # Does PointClicker even need rules...?
        if shuffle_ptc == 3:
            return

        rule_setter.set_basic_rule("PointClicker -- Click Me!", "Entropy -- PointClicker (Mission)")
        rule_setter.set_basic_rule("PointClicker -- Autoclicker v1", "PointClicker -- Click Me!")
        rule_setter.set_basic_rule("PointClicker -- Autoclicker v2", "PointClicker -- Autoclicker v1")
        rule_setter.set_basic_rule("PointClicker -- Pointereiellion", "PointClicker -- Autoclicker v2")
        rule_setter.set_basic_rule("PointClicker -- Upgrade 4", "PointClicker -- Pointereiellion")

        for x in range(5, 51):
            rule_setter.set_basic_rule(f"PointClicker -- Upgrade {x}", f"PointClicker -- Upgrade {x - 1}")

        if shuffle_ptc == 2:
            return

        set_pointclicker_rule("PointClicker -- Click Me!", 10, 1000)
        set_pointclicker_rule("PointClicker -- Autoclicker v1", 20, 1000)
        set_pointclicker_rule("PointClicker -- Autoclicker v2", 50, 1000)
        set_pointclicker_rule("PointClicker -- Pointereiellion", 1000, 2000)
        set_pointclicker_rule("PointClicker -- Upgrade 8", 2000, 50000)
        set_pointclicker_rule("PointClicker -- Upgrade 16", 2500, 100000)
        set_pointclicker_rule("PointClicker -- Upgrade 30", 3330, 500000)
        set_pointclicker_rule("PointClicker -- Upgrade 50", 3330, 500000)

    def set_achievement_rules():
        rule_setter.set_exec_rule("Achievement -- Makeover!", "ThemeChanger")
        rule_setter.set_exec_rule("Achievement -- TRUE ULTIMATE POWER!", "ClockEXE")
        rule_setter.set_basic_rule("Achievement -- Join Entropy", "Entropy -- Confirmation Mission")
        rule_setter.set_basic_rule("Achievement -- Join CSEC", "Join CSEC")
        rule_setter.set_basic_rule("Achievement -- Rude//el Sec Champion", "/el -- Head of Polar Star (Download Files)")
        rule_setter.set_basic_rule("Achievement -- PointClicker", "Entropy -- PointClicker (Mission)")
        set_pointclicker_rule("Achievement -- PointClicker", 10, 1)
        rule_setter.set_basic_rule("Achievement -- You better not have clicked for those...",
                                   "Entropy -- PointClicker (Mission)")
        set_pointclicker_rule("Achievement -- You better not have clicked for those...",
                              3330, 500000)
        pass

    set_mission_rules()

    if shuffle_ptc:
        set_pointclicker_rules()
    if shuffle_achievements:
        set_achievement_rules()
    if shuffle_nodes:
        set_node_rules(rule_setter)

    visualize_regions(multiworld.get_region("Menu", player), "hacknet_test.puml")