from typing import Any, Dict

from .Options import *

hacknet_option_presets: Dict[str, Dict[str, Any]] = {
    # The default run, best for most people
    "Default": {
        "player_goal": 1,
        "shuffle_labs": True,
        "shuffle_execs": 2
    },
    "The Full Package": {
        "player_goal": 5,
        "shuffle_labs": True,
        "shuffle_execs": 1,
        "shuffle_achvs": True,
        "shuffle_nodes": True,
        "shuffle_ptc": 1
    }
}