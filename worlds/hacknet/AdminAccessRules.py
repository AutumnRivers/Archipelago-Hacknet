from BaseClasses import MultiWorld, ItemClassification, CollectionState
from Utils import visualize_regions

from worlds.generic.Rules import set_rule, forbid_items
from worlds.AutoWorld import World

from .Options import HacknetOptions
from .Items import HacknetItem, exec_is_in_pack

from .Rules import HacknetRuleSetter

"""
Admin Access has its own rules file due to how involved it is
It's mainly for organizational purposes, basically
"""
def set_node_rules(rule_setter: HacknetRuleSetter):
    pass
