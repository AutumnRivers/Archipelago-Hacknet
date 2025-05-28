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
def set_node_rules(rule_setter: HacknetRuleSetter):
    # Intro
    rule_setter.set_basic_rule("Intro -- Viper-Battlestation", "Intro -- Getting some tools together")
    rule_setter.set_basic_rule("Intro -- Entropy Asset Cache", "Intro -- Viper-Battlestation")
    rule_setter.set_basic_rule("Intro -- Bitwise Test PC", "Intro -- Maiden Flight")
    rule_setter.set_basic_rule("Intro -- P. Anderson's Bedroom PC", "Intro -- Something in return")
    rule_setter.set_basic_rule("Entropy -- Slash-Bot News Network", "Entropy -- Confirmation Mission")

