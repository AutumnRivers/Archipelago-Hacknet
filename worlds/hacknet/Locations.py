from .LocationList import location_table
from .Options import is_option_enabled, get_option_value

from BaseClasses import Location, LocationProgressType, MultiWorld

location_id_offset = 17730000

def hacknet_loc_to_ap_id(index):
    if index is not None:
        return location_id_offset + index
    else:
        return None

def ap_id_to_hacknet_loc(ap_id):
    val = ap_id - location_id_offset

    hn_loc = [location for location in location_table if location_table[location][1] == val]

    if len(hn_loc) > 1:
        raise Exception(f'List returned more than one location')
    elif hn_loc[0] is None:
        raise Exception(f'Location does not exist')
    else:
        return hn_loc[0]

class HacknetLocation(Location):
    game = "Hacknet"

    def __init__(self, player, name, data, region):
        isLabs = data[2]
        isAch = data[3]
        isPriority = data[4]

        if isPriority == True:
            progress_type = LocationProgressType.PRIORITY

        self.index = data[1]
        self.internal = False
        self.disabled = 0
        self.never = False
        self.player = player
        self.name = name

        self.parent_region = region

        if self.index is not None:
            self.address = self.index + location_id_offset
        else:
            self.address = None
    
    def can_fill(self, state, item, check_access=True) -> bool:
        if item.code is None and self.address != None:
            return False
        return super().can_fill(state, item, check_access)

def create_location_descriptions() -> dict:
    location_descriptions = {}

    for locat in location_table:
        real_location = location_table[locat]

        if len(real_location) >= 6:
            location_descriptions[locat] = real_location[5]

    return location_descriptions