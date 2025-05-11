from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Toggle, DefaultOnToggle, Range, Visibility

class GoalPost(Choice):
    """
    What the player should achieve to reach their goal.
    Heartstopper: Vanilla ending, fulfill Bit's final request
    Altitude Loss: Labyrinths ending, any
    Veteran: Break into a super secret node
    VIP: Complete every Entropy and CSEC mission
    Completionist: All of the above. Recommended for asyncs
    """

    display_name = "Player Goal"
    option_heartstopper = 1
    option_altitude_loss = 2
    option_veteran = 3
    option_vip = 4
    option_completionist = 5
    default = 1

class ExcludeJunebug(Toggle):
    """
    If enabled, Project Junebug will not be marked as a location.
    If "Admin Access as Checks" is enabled, this will also not mark Project Junebug nodes.
    Recommended for those easily triggered by sensitive topics.
    If enabled while Shuffle Executables is disabled, KBTPortTest can be found in finale nodes.
    """

    display_name = "Exclude Project Junebug"

class EnableLabyrinths(Toggle):
    """
    Whether or not to shuffle Labyrinths content (missions, executables, etc.)
    If player goal is set to Altitude Loss, Veteran, or Completionist, generation will throw an error if this is disabled.
    """

    display_name = "Shuffle Labyrinths"

class EnableLimits(Choice):
    """
    Whether or not to set limits on in-game mechanics, shuffling progressive limits into the item pool.
    Enable All: Set limits for shells (defaults to 1) and RAM.
    Shells: Restricts how many shells you can have open at once. (Defaults to 1)
    Shells Zero: Same as shells, but defaults to 0 instead of 1 shell. (Meaning, you can't open ANY shells from the start)
    RAM: Restricts your RAM to 300mb from the get-go. Progressive RAM adds 50mb each time it's received.
    Disabled: (Default) Don't set any limits.
    """
    
    display_name = "Shuffle Limits"
    option_enable_all = 1
    option_shells = 2
    option_shells_zero = 3
    option_ram = 4
    option_disabled = 5
    default = 5

class EnableAchievements(Toggle):
    """
    If enabled, actions that usually unlock Steam achievements will be added as location checks.
    ("Rude" is excluded, as the player is automatically put onto the /el Sec path after defeating Naix.)
    (If the player misses Quickdraw, they can get it again by starting a new save file.)
    """
    
    display_name = "Shuffle Steam Achievements"

class ShuffleAdminAccess(Toggle):
    """
    Adds admin access for EVERY ACCESSIBLE NODE as a check. This adds a LOT of locations. (~140 with DLC enabled) Recommended for asyncs.
    Respects "Shuffle Labyrinths"

    (Not yet implemented.)
    """

    display_name = "Admin Access as Checks"

class ShufflePointClicker(Choice):
    """
    Adds PointClicker upgrades as checks and items.
    PointClicker upgrades only send a check the first time they're bought.
    This adds ~51 location checks.

    Checks + Items: Every PointClicker upgrade is a check, but won't do anything when the player buys it.
    This forces the player to rely on PointClicker Passive items being sent to them.*
    Only Checks: Every PointClicker upgrade is a check, and will actually upgrade when the player buys it.
    Disabled: (Default) Don't shuffle PointClicker, at all.

    * = not yet implemented
    """

    display_name = "Shuffle PointClicker Upgrades"
    option_checks_and_items = 1
    option_only_checks = 2
    option_disabled = 3
    default = 3

class ShuffleExecutables(Choice):
    """
    Shuffles executables into the item pool. The player can't do ANYTHING without these, pretty much.
    Any executable not shuffled can be found and downloaded in its vanilla location.

    Shuffle All: Shuffle EVERY executable. Even the useless ones.
    Progression And Useful: Only shuffle progression and useful executables. (e.g., OpShell, ThemeChanger)
    Progression Only: Only shuffle progression executables. (e.g., FTPBounce, WebServerWorm)
    Disabled: Don't shuffle executables.

    The finale sequencer executable is never shuffled.
    """

    display_name = "Shuffle Executables"
    option_shuffle_all = 1
    option_progression_and_useful = 2
    option_progression_only = 3
    option_disabled = 4
    default = 1

class ExecutableGrouping(Choice):
    """
    When shuffling executables, how should they be grouped?
    Currently, doesn't work (its rules aren't implemented), but will before beta

    Individually: (Default) Every executable is its own item.
    Regional: Executables are grouped by region. (e.g., "Labyrinths Executables" is TorrentStreamInjector, SSLTrojan, etc.)
    Practicality: Executables are grouped by what they're used for. (e.g., Portcrushers, Aesthetics, etc.) Good for quick syncs.
    """

    visibility = Visibility.template
    display_name = "Executable Grouping"
    option_individually = 1
    option_regional = 2
    option_practicality = 3
    default = 1

class StartWithFTPSSH(DefaultOnToggle):
    """
    When shuffling executables, add FTPBounce and SSHCrack to starting inventory automatically.
    """

    display_name = "Start with FTP & SSH Crushers"

class ReplaceBounceWithSprint(DefaultOnToggle):
    """
    Completely removes FTPBounce from the item pool, replacing it with FTPSprint.
    If disabled, FTPBounce and FTPSprint will be two different items in the item pool.
    This ignores Shuffle Labyrinths.
    If Shuffle Executables is set to Disabled, this does nothing.
    """

    display_name = "FTPSprint Replaces FTPBounce"

class EnableFactionAccess(Choice):
    """
    If enabled, the player must first receive the respective Access for the faction before they can do missions for it. (Entropy, CSEC, Kaguya Trials)
    Good for asyncs!

    Starting Hints: Automatically hints access for each faction from the start of the run. (doesn't work)
    """

    display_name = "Shuffle Faction Access"
    option_enabled = 1
    option_starting_hints = 2
    option_disabled = 3
    default = 3

class TrapPercentage(Range):
    """
    What percentage of filler items should be traps. If set to 0, no traps will be shuffled into the item pool.
    """

    display_name = "Trap Percentage (%)"
    range_start = 0
    range_end = 100
    default = 10

class ShuffleETASTrap(Toggle):
    """
    If traps are enabled, shuffle ETAS traps. Automatically causes an ETAS to trigger.
    These can be REALLY annoying, so they're off by default. Enable them if you like a challenge!
    """

    display_name = "Enable ETAS Traps"

class DeathLink(Toggle):
    """
    If enabled: whenever you are traced back, you abandon a mission, or your in-game computer crashes, a deathlink is sent.
    DeathLinks are not sent for the crash caused by Striker. (But they are for Naix! :3c)

    A DeathLink in Hacknet will crash the player's (in-game) computer. If an ETAS is currently active, then the DeathLink is discarded.
    """

    display_name = "Enable DeathLink"

class MaxMissionSkips(Range):
    """
    The maximum amount of mission skips that should be shuffled into the item pool.
    Mission skips allow you to skip any current mission.
    Mission skips cannot be used on transition missions.
    Mission skips cannot be used on finale missions.
    If set to 0, no mission skips will be shuffled into the item pool.
    """

    display_name = "Max. Amount of Mission Skips"
    range_start = 0
    range_end = 5
    default = 0

class MaxForceHacks(Range):
    """
    The maximum amount of forcehacks that should be shuffled into the item pool.
    ForceHacks allow you to instantly gain admin access to most nodes. (With a few exceptions...)
    If set to 0, no forcehacks will be shuffled into the item pool.
    """

    display_name = "Max. Amount of ForceHacks"
    range_start = 0
    range_end = 10
    default = 0

class AddMcGuffins(Toggle):
    """
    A super secret option you shouldn't be seeing because it's not actually implemented yet

    Adds McGuffin items to the item pool, forcing the player to make even LESS progress until they have more items.
    Why would you do this?
    """

    visibility = Visibility.none
    display_name = "Add McGuffin Items"

class RandomizeNonRandomizedIPs(Toggle):
    """
    A super secret option you shouldn't be seeing because it's not actually implemented yet

    If enabled, static IPs are randomized, making it much more difficult to do skips.
    """

    visibility = Visibility.none
    display_name = "Randomize Static IPs"

@dataclass
class HacknetOptions(PerGameCommonOptions):
    player_goal: GoalPost
    exclude_junebug: ExcludeJunebug
    shuffle_labs: EnableLabyrinths
    enable_limits: EnableLimits
    shuffle_achvs: EnableAchievements
    shuffle_nodes: ShuffleAdminAccess

    shuffle_ptc: ShufflePointClicker

    max_mission_skips: MaxMissionSkips
    max_forcehacks: MaxForceHacks

    shuffle_execs: ShuffleExecutables
    sprint_replaces_bounce: ReplaceBounceWithSprint
    start_with_ftp_and_ssh: StartWithFTPSSH
    exec_grouping: ExecutableGrouping

    faction_access: EnableFactionAccess

    trap_percentage: TrapPercentage
    enable_etas_traps: ShuffleETASTrap

    deathlink: DeathLink

hn_option_groups = [
    OptionGroup(
        "Executable Options",
        [
            ShuffleExecutables,
            ExecutableGrouping,
            StartWithFTPSSH,
            ReplaceBounceWithSprint
        ]
    ),
    OptionGroup(
        "Optional Checks",
        [
            EnableAchievements,
            ShufflePointClicker,
            EnableFactionAccess
        ]
    ),
    OptionGroup(
        "Trap Options",
        [
            TrapPercentage,
            ShuffleETASTrap
        ]
    ),
    OptionGroup(
        "DeathLink Options",
        [
            DeathLink
        ]
    )
]