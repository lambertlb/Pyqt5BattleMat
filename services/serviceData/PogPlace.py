"""
GPL 3 file header
"""


class PogPlace:
    """
    Manage the places a Pog can reside

    Ended up treating these as constants instead of as an enum.
    This is because I had a lot of issues with enums in json data
    and this turned out to be a lot easier.
    """
    DisplayNames = {
        0: 'Dungeon Level',
        1: 'Session Level',
        2: 'Player Location',
        3: 'Common Resource'
    }

    DUNGEON_LEVEL = 0
    SESSION_LEVEL = 1
    SESSION_RESOURCE = 2
    COMMON_RESOURCE = 3

    @staticmethod
    def displayName(value):
        return PogPlace.DisplayNames[value]

    @staticmethod
    def getKey(value):
        for x in PogPlace.DisplayNames.keys():
            if PogPlace.DisplayNames[x] == value:
                return x
        return 0
