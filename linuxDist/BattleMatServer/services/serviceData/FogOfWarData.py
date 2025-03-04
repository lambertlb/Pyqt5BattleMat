"""
GPL 3 file header
"""


class FogOfWarData:
    """
    used for passing Fog of war data back and forth
    between client and server
    """
    def __init__(self, fowData=None):
        self.fogOfWar = fowData
