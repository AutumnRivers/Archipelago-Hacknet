from typing import Dict, Union

from BaseClasses import MultiWorld

from Options import Option, Choice, Toggle, DefaultOnToggle

class IncludeLabsContent(DefaultOnToggle):
    """
    Whether or not to include Labyrinths DLC content.
    (Missions, Executables, etc.)
    """
    display_name = "Include Labyrinths"

class GoalPost(Choice):
    """
    The ultimate goal for your Archipelago run.

    Heartstopper - Base game, stop PortHack's heart
    AltitudeLoss - Labyrinths, reach the credits (overrides "Include Labyrinths")
    Veteran - Labyrinths, hack into The Gibson (same as above, overrides "Shuffle Postgame")
    Completionist - Heartstopper and Veteran
    """
    display_name = "Goal/Victory Condition"
    option_heartstopper = 1
    option_altitude_loss = 2
    option_veteran = 3
    option_completionist = 4

class ShuffleAchievements(Toggle):
    """
    Whether or not to shuffle achievements into the location pool.
    This doesn't include unaviodable achievements, such as joining Entropy.
    """
    display_name = "Shuffle Achievements"

class ShuffleNodes(Toggle):
    """
    Shuffles secret nodes into the location pool.
    To "check" these nodes, you must gain administrator access to them.
    However you do that, is up to you.
    Respects "shuffle postgame" and "include labyrinths"
    """
    display_name = "Shuffle Nodes"

class DeathLink(Toggle):
    """
    If on: Whenever you get traced back, everyone who is also on Death Link dies.

    The effect of a 'death' in Hacknet is an ETAS Trap.
    """
    display_name = "Death Link"

class ExecutableShuffle(Choice):
    """
    What types of executables to shuffle.

    Shuffle All - (Default, Recommended) Shuffle all executables.
    (Clock, SecurityTracer, etc.)
    Progression + Useful - OpShell, Tracekill, etc.
    Only Progression - FTPBounce, WebServerWorm, etc.
    """
    display_name = "Shuffle Executables"
    option_all = 1
    option_progressive_and_useful = 2
    option_only_progression = 3

class ShufflePostGameMissions(Toggle):
    """
    Whether or not to shuffle post-game missions.
    """
    display_name = "Shuffle Postgame"

hacknet_options: Dict[str, type] = {
    "include_labyrinths": IncludeLabsContent,
    "victory_condition": GoalPost,
    "shuffle_achievements": ShuffleAchievements,
    "shuffle_nodes": ShuffleNodes,
    "death_link": DeathLink,
    "shuffle_executables": ExecutableShuffle,
    "shuffle_postgame": ShufflePostGameMissions
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[bool, int]:
    option = getattr(world, name, None)

    if option is None:
        return 0

    if issubclass(hacknet_options[name], Toggle) or issubclass(hacknet_options[name], DefaultOnToggle):
        return bool(option[player].value)
    return option[player].value
