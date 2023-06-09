"""
GPL 3 file header
"""
from services.serviceData.DungeonLevel import DungeonLevel


class DungeonData:
    """
    This contains all the data for the dungeon with a specific UUID
    """
    def __init__(self):
        self.uuid = ''
        self.dungeonName = ''
        self.dungeonLevels = []
        self.showGrid = False

    def construct(self):
        """
        Take a dungeon that had its data loaded via placing json data into its __dict__
        and construct a new tree with actual constructors
        """
        dl = DungeonData()
        self.cloneData(dl)
        return dl

    def cloneData(self, dl):
        dl.uuid = self.uuid
        dl.dungeonName = self.dungeonName
        dl.showGrid = self.showGrid
        dl.dungeonLevels = []
        if self.dungeonLevels is None:
            return
        for level in self.dungeonLevels:
            ld = DungeonLevel()
            ld.__dict__ = level
            dl.dungeonLevels.append(ld.construct())

    def addDungeonLevel(self, level):
        self.dungeonLevels.append(level)

    def remove(self, index):
        if index < 0 or index >= len(self.dungeonLevels) or len(self.dungeonLevels) == 1:
            return
        self.dungeonLevels.remove(self.dungeonLevels[index])
