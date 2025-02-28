"""
GPL 3 file header
"""

from services.serviceData.DungeonSessionLevel import DungeonSessionLevel


class DungeonLevel(DungeonSessionLevel):
    """
    Manage the data in a level within a dungeon
    """
    def __init__(self):
        super(DungeonLevel, self).__init__()
        self.levelDrawing = ''
        self.levelName = ''
        self.gridSize = 30
        self.gridOffsetX = 0
        self.gridOffsetY = 0
        self.columns = 0
        self.rows = 0

    def construct(self):
        """
         Take a level that had its data loaded via placing json data into its __dict__
         and construct a new tree with actual constructors
         """
        dl = DungeonLevel()
        self.cloneData(dl)
        return dl

    def cloneData(self, dl):
        dl.levelDrawing = self.levelDrawing
        dl.levelName = self.levelName
        dl.gridSize = self.gridSize
        dl.gridOffsetX = self.gridOffsetX
        dl.gridOffsetY = self.gridOffsetY
        dl.columns = self.columns
        dl.rows = self.rows
        super(DungeonLevel, self).cloneData(dl)
