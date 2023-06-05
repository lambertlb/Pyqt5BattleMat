"""
GPL 3 file header
"""


class PlayerFlag:
    """
    Manage the player flags for a pog
    These are used as a bitmask

    Ended up treating these as constants instead of as an enum.
    This is because I had a lot of issues with enums in json data
    and this turned out to be a lot easier.
    """
    DisplayNames = {
        0: 'None',
        1: 'Dead',
        2: 'Invisible'
    }

    NONE = 0
    DEAD = 1
    INVISIBLE = 2

    @staticmethod
    def displayName(value):
        return PlayerFlag.DisplayNames[value]
