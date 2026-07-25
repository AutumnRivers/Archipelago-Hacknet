from BaseClasses import MultiWorld, ItemClassification, CollectionState
from Utils import visualize_regions

from worlds.generic.Rules import set_rule, forbid_items
from worlds.AutoWorld import World

from .Options import HacknetOptions
from .Items import HacknetItem, exec_is_in_pack

from .RuleSetter import HacknetRuleSetter

"""
Admin Access has its own rules file due to how involved it is
It's mainly for organizational purposes, basically
"""
def set_node_rules(rule_setter: HacknetRuleSetter, options: HacknetOptions, multiworld: MultiWorld, player: int):
    shuffle_labs = bool(options.shuffle_labs)
    exclude_junebug = bool(options.exclude_junebug)

    forbid_items(multiworld.get_location("Intro -- Player's PC", player),
        {"ETAS Trap", "ForkBomb", "Fake Connection", "Random Theme"})

    # Intro
    rule_setter.set_basic_rule("Intro -- Viper-Battlestation", "Intro -- Getting some tools together")
    rule_setter.set_any_exec_rule("Intro -- Bitwise Test PC", 1, "FTPBounce", "SSHCrack", "WebServerWorm",
        "SMTPOverflow")
    rule_setter.set_basic_rule("Intro -- Entropy Asset Cache", "Intro -- Bitwise Test PC")
    rule_setter.set_basic_rule("Intro -- Bitwise Test PC", "Intro -- Maiden Flight")
    rule_setter.set_basic_rule("Intro -- P. Anderson's Bedroom PC", "Intro -- Bitwise Test PC")
    rule_setter.set_basic_rule("Entropy -- Slash-Bot News Network", "Entropy -- Confirmation Mission")
    rule_setter.set_basic_rule("Intro -- Entropy test Server", "Intro -- Bitwise Test PC")

    # Entropy
    rule_setter.set_any_exec_rule("Entropy -- PointClicker (Admin Access)", 2, "FTPBounce", "SSHCrack", "WebServerWorm",
        "SMTPOverflow")
    rule_setter.set_any_exec_rule("Entropy -- PP Marketing Inc.", 2, "FTPBounce", "SSHCrack", "WebServerWorm",
        "SMTPOverflow")
    rule_setter.set_exec_rule_with_loc("Entropy -- Jason's PowerBook Plus", "Entropy -- eOS Device Scanning",
        "eosDeviceScan")
    rule_setter.set_basic_rule("Entropy -- Jason's ePhone 4S", "Entropy -- Jason's PowerBook Plus")
    rule_setter.set_basic_rule("Entropy -- JDel Home PC", "Entropy -- Jason's PowerBook Plus")
    rule_setter.set_basic_rule("Entropy -- Jacob's ePhone 4", "Entropy -- Jason's PowerBook Plus")