from BaseClasses import MultiWorld, ItemClassification, CollectionState
from Utils import visualize_regions

from worlds.generic.Rules import set_rule, forbid_items
from worlds.AutoWorld import World

from .Options import HacknetOptions
from .Items import HacknetItem, exec_is_in_pack

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
    shuffle_limits = int(options.enable_limits)
    exclude_junebug = bool(options.exclude_junebug)
    faction_access = int(options.faction_access)
    player_goal = int(options.player_goal)
    sprint_replaces_bounce = bool(options.sprint_replaces_bounce)
    exec_grouping = int(options.exec_grouping)

    def create_event(event: str) -> HacknetItem:
        return HacknetItem(event, player, (None, ItemClassification.progression, "Event", False, 1), True)

    def set_basic_rule(loc_name: str, prev_loc: str):
        """
        Sets a "basic" rule - basically, can the player reach this previous location?
        """
        set_rule(multiworld.get_location(loc_name, player),
                 lambda state: multiworld.get_location(prev_loc, player).can_reach(state))

    def player_can_reach_locations(state: CollectionState, locs: set[str]) -> bool:
        can_reach: bool = True
        for loc in locs:
            if not can_reach:
                break
            real_loc = multiworld.get_location(loc, player)
            can_reach = real_loc.can_reach(state)
        return can_reach

    exec_packs_added: set[str] = set()

    def set_exec_rule(loc_name: str, *execs: str):
        """
        Sets an "executable" rule - does the player have all these executables?
        """
        if shuffle_execs == 4 or len(execs) == 0:
            return
        for exec_name in execs:
            real_name = exec_name
            if exec_name == "FTPBounce" and sprint_replaces_bounce:
                real_name = "FTPSprint"

            if exec_name == "FTPBounce" and exec_grouping == 1:
                set_rule(multiworld.get_location(loc_name, player),
                         lambda state: state.has("FTPBounce") or state.has("FTPSprint"))
            elif exec_grouping == 1:
                set_rule(multiworld.get_location(loc_name, player),
                         lambda state: state.has(real_name, player))
            elif exec_grouping in (2, 3):
                exec_pack = exec_is_in_pack(exec_name, exec_grouping == 2)
                if exec_pack in exec_packs_added:
                    continue
                set_rule(multiworld.get_location(loc_name, player),
                         lambda state: state.has(exec_pack, player))
                exec_packs_added.add(exec_pack)

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

    def has_required_execs(state: CollectionState, *execs: str) -> bool:
        meets_requirement: bool = False
        for exec_name in execs:
            if meets_requirement:
                break
            if exec_name == "FTPBounce":
                meets_requirement = state.has("FTPBounce", player) or state.has("FTPSprint", player)
                continue
            meets_requirement = state.has(exec_name, player)
        return meets_requirement

    def has_amount_of_req_execs(state: CollectionState, amount_required: int,
                                *execs: str) -> bool:
        meets_requirement: bool = False
        has_amount: int = 0
        for exec_name in execs:
            if has_amount >= amount_required:
                meets_requirement = True
                break
            if exec_name == "FTPBounce":
                has_ftp_cracker = state.has("FTPBounce", player) or state.has("FTPSprint", player)
                if has_ftp_cracker:
                    has_amount += 1
                continue
            if state.has(exec_name, player):
                has_amount += 1
        return meets_requirement

    def set_mission_rules():
        dont_shuffle_execs = shuffle_execs == 5

        # Intro
        set_rule(multiworld.get_location("Intro -- Maiden Flight", player),
                 lambda state: (state.has("SSHCrack", player) or
                               state.has("SMTPOverflow", player) or
                               state.has("WebServerWorm", player) or
                               (state.has("FTPBounce", player) or state.has("FTPSprint", player)) or
                                dont_shuffle_execs) and
                               (multiworld.get_location("Intro -- First Contact", player).can_reach(state))
                 )
        set_basic_rule("Intro -- Something in return", "Intro -- Maiden Flight")
        set_basic_rule("Intro -- Where to from here", "Intro -- Something in return")
        set_basic_rule("Entropy -- Confirmation Mission", "Intro -- Where to from here")
        set_basic_rule("Entropy -- Welcome", "Entropy -- Confirmation Mission")

        # Entropy Sets
        set_partial_rule("Entropy -- PointClicker (Mission)", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")
        set_partial_rule("Entropy -- The famous counter-hack", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")
        set_partial_rule("Entropy -- Back to School", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")
        set_partial_rule("Entropy -- X-C Project", "Entropy -- Welcome", 1,
                         "FTPBounce", "SSHCrack")

        # Entropy - eOS Intro
        set_partial_rule("Entropy -- eOS Device Scanning", "Entropy -- Back to School", 1,
                         "eosDeviceScan")
        # This one below will implicitly check for faction access and eosDeviceScan, so it can be basic
        set_basic_rule("Entropy -- Smash N' Grab", "Entropy -- eOS Device Scanning")

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
                     lambda state: player_can_reach_locations(state, entropy_missions))

        set_rule(multiworld.get_location("Entropy -- Naix", player),
                 lambda state: ((
                                       (state.has("FTPBounce", player) or state.has("FTPSprint", player)) and
                                       (state.has("WebServerWorm", player) and state.has("SMTPOverflow", player))
                               ) or
                               dont_shuffle_execs) and
                               multiworld.get_location("Entropy -- Smash N' Grab", player).can_reach(state)
                 )

        # /el Sec
        # IIRC, only Polar Star needs to be completed in /el...
        set_partial_rule("Naix -- Deface Nortron Website", "Entropy -- Naix",
                         1, "WebServerWorm", "SMTPOverflow")
        set_partial_rule("Naix -- Nortron Security Mainframe", "Naix -- Deface Nortron Website",
                         1, "FTPBounce", "SSHCrack")
        # From here on out, it's assumed the player has the base 4 executables (ftp, ssh, web, smtp)
        set_basic_rule("/el -- Head of Polar Star (Download Files)", "Naix -- Nortron Security Mainframe")

        # CSEC Intro
        set_basic_rule("CSEC -- CFC Herbs & Spices", "/el -- Head of Polar Star (Download Files)")

        # Set Labyrinths rules (if applicable)
        set_labyrinths_mission_rules()

        if shuffle_labs:
            set_partial_rule("Join CSEC", "Labyrinths -- Altitude Loss", 3, "SQL_MemCorrupt")
            set_basic_rule("CSEC -- Subvert Psylance Investigation", "Join CSEC")
        else:
            set_partial_rule("Join CSEC", "CSEC -- CFC Herbs & Spices", 2, "SQL_MemCorrupt")

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
        set_basic_rule("CSEC -- Track an Encrypted File", "CSEC -- Locate or Create Decryption Software")

        # Junebug
        if not exclude_junebug:
            set_exec_rule_with_loc("CSEC -- Project Junebug",
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
                     lambda state: player_can_reach_locations(state, csec_missions))

        # CSEC -> Bit
        bit_prev_loc = "CSEC -- Project Junebug"
        if exclude_junebug: bit_prev_loc = "CSEC -- Locate or Create Decryption Software"
        set_basic_rule("CSEC -- Investigate a CSEC member's disappearance", bit_prev_loc)

        # Finale
        # NO MORE EXECUTABLES ARE REQUIRED! HALLELUIJAH
        set_basic_rule("Bit -- Foundation", "CSEC -- Investigate a CSEC member's disappearance")
        set_basic_rule("Bit -- Substantiation", "Bit -- Foundation")
        set_basic_rule("Bit -- Investigation", "Bit -- Substantiation")
        set_basic_rule("Bit -- Propagation", "Bit -- Investigation")
        set_basic_rule("Bit -- Termination", "Bit -- Propagation")

        if player_goal in (1, 5):
            set_basic_rule("Stop PortHack.Heart", "Bit -- Termination")

        forbid_items(multiworld.get_location("Bit -- Propagation", player), {"Tracekill", "Mission Skip",
                                                                             "ForceHack"})
        forbid_items(multiworld.get_location("Bit -- Termination", player), {"Tracekill", "Mission Skip",
                                                                             "ForceHack"})

        if shuffle_achievements:
            set_achievement_rules()

        visualize_regions(multiworld.get_region("Menu", player), "hacknet_test.puml")

    def set_labyrinths_mission_rules() -> None:
        if not shuffle_labs:
            return

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

        if player_goal in (2, 5):
            set_basic_rule("Watched Labyrinths Credits", "Labyrinths -- Altitude Loss")

        if player_goal in (3, 5):
            set_full_rule("Broke Into The Gibson", "Labyrinths -- Altitude Loss", 2,
                          10, 10, "FTPBounce", "SSHCrack", "WebServerWorm",
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
        tens_needed, hundreds_needed, thousands_needed = decompose_number(target_rate)

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
                 lambda state: (state.has("PointClicker Passive*10", tens_needed)) and
                               (state.has("PointClicker Passive*100", hundreds_needed)) and
                               (state.has("PointClicker Passive*1000", thousands_needed)) and
                               (state.has("PointClicker +100pt./s", static_hundreds)) and
                               (state.has("PointClicker +1000pt./s", static_thousands)))

    def set_pointclicker_rules():
        # Does PointClicker even need rules...?
        if shuffle_ptc == 3:
            return

        set_basic_rule("PointClicker -- Click Me!", "Entropy -- PointClicker (Mission)")
        set_basic_rule("PointClicker -- Autoclicker v1", "PointClicker -- Click Me!")
        set_basic_rule("PointClicker -- Autoclicker v2", "PointClicker -- AutoClicker v1")
        set_basic_rule("PointClicker -- Pointereiellion", "PointClicker -- Autoclicker v2")
        set_basic_rule("PointClicker -- Upgrade 4", "PointClicker -- Pointereiellion")

        for x in range(5, 51):
            set_basic_rule(f"PointClicker -- Upgrade {x}", f"PointClicker -- Upgrade {x - 1}")

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
        set_exec_rule("Achievement -- Makeover!", "ThemeChanger")
        set_exec_rule("Achievement -- TRUE ULTIMATE POWER!", "ClockEXE")
        set_basic_rule("Achievement -- Join Entropy", "Entropy -- Confirmation Mission")
        set_basic_rule("Achievement -- Join CSEC", "Join CSEC")
        set_basic_rule("Achievement -- Rude//el Sec Champion", "/el -- Head of Polar Star (Download Files)")
        set_basic_rule("Achievement -- PointClicker", "Entropy -- PointClicker (Mission)")
        set_basic_rule("Achievement -- You better not have clicked for those...", "Entropy -- PointClicker (Mission)")
        pass

    def set_node_rules(): # this one is gonna be the most annoying :/
        pass

    set_mission_rules()