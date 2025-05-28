from BaseClasses import MultiWorld, CollectionState

from worlds.generic.Rules import set_rule

from .Options import HacknetOptions
from .Items import exec_is_in_pack

class HacknetRuleSetter:
    def __init__(self, multiworld: MultiWorld,
                 options: HacknetOptions,
                 player: int):
        self.multiworld = multiworld
        self.options = options
        self.player = player
        self.shuffle_execs = int(options.shuffle_execs)
        self.shuffle_labs = bool(options.shuffle_labs)
        self.shuffle_achievements = bool(options.shuffle_achvs)
        self.shuffle_nodes = bool(options.shuffle_nodes)
        self.shuffle_ptc = int(options.shuffle_ptc)
        self.shuffle_limits = int(options.enable_limits)
        self.exclude_junebug = bool(options.exclude_junebug)
        self.faction_access = int(options.faction_access)
        self.player_goal = int(options.player_goal)
        self.sprint_replaces_bounce = bool(options.sprint_replaces_bounce)
        self.exec_grouping = int(options.exec_grouping)

        self.exec_packs_added: set[str] = set()

    def set_basic_rule(self, loc_name: str, prev_loc: str):
        """
        Sets a "basic" rule - basically, can the player reach this previous location?
        """
        set_rule(self.multiworld.get_location(loc_name, self.player),
                 lambda state: self.multiworld.get_location(prev_loc, self.player).can_reach(state))

    def player_can_reach_locations(self, state: CollectionState, locs: set[str]) -> bool:
        can_reach: bool = True
        for loc in locs:
            if not can_reach:
                break
            real_loc = self.multiworld.get_location(loc, self.player)
            can_reach = real_loc.can_reach(state)
        return can_reach

    def set_exec_rule(self, loc_name: str, *execs: str):
        """
        Sets an "executable" rule - does the player have all these executables?
        """
        if self.shuffle_execs == 4 or len(execs) == 0:
            return
        for exec_name in execs:
            real_name = exec_name
            if exec_name == "FTPBounce" and self.sprint_replaces_bounce:
                real_name = "FTPSprint"

            if exec_name == "FTPBounce" and self.exec_grouping == 1:
                set_rule(self.multiworld.get_location(loc_name, self.player),
                         lambda state: state.has("FTPBounce") or state.has("FTPSprint"))
            elif self.exec_grouping == 1:
                set_rule(self.multiworld.get_location(loc_name, self.player),
                         lambda state: state.has(real_name, self.player))
            elif self.exec_grouping in (2, 3):
                exec_pack = exec_is_in_pack(exec_name, self.exec_grouping == 2)
                if exec_pack in self.exec_packs_added:
                    continue
                set_rule(self.multiworld.get_location(loc_name, self.player),
                         lambda state: state.has(exec_pack, self.player))
                self.exec_packs_added.add(exec_pack)

    def set_any_exec_rule(self, state: CollectionState, amount_needed: int, *execs: str) -> bool:
        """
        Same as above, but checks if player has any of the executables
        This is really only used for the intro
        """
        amount_needed = 1 if amount_needed is None else amount_needed
        has_amount_of_execs: int = 0

        for exec_name in execs:
            real_name = exec_name
            if exec_name == "FTPBounce" and self.sprint_replaces_bounce:
                real_name = "FTPSprint"

            if self.exec_grouping == 1 and exec_name == "FTPBounce":
                if state.has("FTPBounce", self.player) or state.has("FTPSprint", self.player):
                    has_amount_of_execs += 1
            elif self.exec_grouping == 1:
                if state.has(real_name, self.player):
                    has_amount_of_execs += 1
            elif self.exec_grouping in (2, 3):
                exec_pack = exec_is_in_pack(exec_name, self.exec_grouping == 2)
                if state.has(exec_pack, self.player):
                    has_amount_of_execs += 1

        return has_amount_of_execs >= amount_needed

    def set_faction_access_rule(self, loc_name: str, amount_needed: int):
        """
        Does what it says on the tin. Self-explanatory.
        1 - Entropy
        2 - Kaguya Trials
        3 - CSEC
        """
        if self.faction_access == 3:
            return
        if self.shuffle_labs == False and amount_needed == 3:
            amount_needed = 2
        set_rule(self.multiworld.get_location(loc_name, self.player),
                 lambda state: state.has("Progressive Faction Access", self.player, amount_needed))

    def set_limits_rule(self, loc_name: str, shells_needed: int, ram_upgrades_needed: int):
        """
        This is only used for finale nodes, really.
        Altitude Loss and EnTech Backups logically require ~5 shells and maximum RAM.
        Gibson logically requires maximum shells and maximum RAM.
        """
        if self.shuffle_limits == 5:
            return

        has_shell_limits = self.shuffle_limits in (1, 2, 3)
        has_ram_limits = self.shuffle_limits in (1, 4)

        set_rule(self.multiworld.get_location(loc_name, self.player),
                 lambda state: ((has_shell_limits == False) or
                                state.has("Progressive Shell Limit", self.player, shells_needed)) and
                               ((has_ram_limits == False) or state.has("Progressive RAM", self.player, ram_upgrades_needed))
                 )

    def set_exec_rule_with_loc(self, loc_name: str, prev_loc: str, *execs: str):
        self.set_basic_rule(loc_name, prev_loc)
        self.set_exec_rule(loc_name, *execs)

    def set_partial_rule(self, loc_name: str, prev_loc: str, faction_access_needed: int,
                         *execs: str):
        """
        Same thing as below, but without limit requirements. For early nodes.
        """
        self.set_basic_rule(loc_name, prev_loc)
        self.set_exec_rule(loc_name, *execs)
        self.set_faction_access_rule(loc_name, faction_access_needed)

    def set_full_rule(self, loc_name: str, prev_loc: str, faction_access_needed: int,
                      shells_needed: int, ram_upgrades_needed: int, *execs: str):
        """
        The amalgamation of everything above. The full package. Oh, yeah, baby.
        """
        self.set_basic_rule(loc_name, prev_loc)
        self.set_exec_rule(loc_name, *execs)
        self.set_faction_access_rule(loc_name, faction_access_needed)
        self.set_limits_rule(loc_name, shells_needed, ram_upgrades_needed)

    def has_amount_of_req_execs(self, state: CollectionState, amount_required: int,
                                *execs: str) -> bool:
        meets_requirement: bool = False
        has_amount: int = 0
        for exec_name in execs:
            if has_amount >= amount_required:
                meets_requirement = True
                break

            if self.exec_grouping in (2, 3) and self.shuffle_execs < 4:
                pack_name: str = exec_is_in_pack(exec_name, self.exec_grouping == 2)
                if state.has(pack_name, self.player):
                    has_amount += 1
            elif self.shuffle_execs < 4:
                if exec_name == "FTPBounce":
                    has_ftp_cracker = state.has("FTPBounce", self.player) or state.has("FTPSprint", self.player)
                    if has_ftp_cracker:
                        has_amount += 1
                        continue
                if state.has(exec_name, self.player):
                    has_amount += 1

        return has_amount >= amount_required or meets_requirement