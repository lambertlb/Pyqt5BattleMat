"""
GPL 3 file header
"""
from services.serviceData.PogList import PogList


class DungeonSessionLevel:
    """
    class to manage a level with a session

    Fog of war management is a little strange.
    Normally this would be a straight bitmap with one bit
    per column in the grid. But python does not have true
    integers, it uses bits in the mantissa of a floating number.
    Because of that I constrained my usage to just the first
    32 bits of what would have been a 64-bit integer.
    """
    def __init__(self, dungeonLevel=None):
        self.fogOfWarVersion = 0
        self.fogOfWarData = []
        self.bitsPerColumn = 0
        self.monsters = PogList()
        self.roomObjects = PogList()
        if dungeonLevel:
            self.monsters = dungeonLevel.monsters.clone()
            self.roomObjects = dungeonLevel.roomObjects.clone()
            self.bitsPerColumn = dungeonLevel.columns
            self.fogOfWarData = self.createNewFOWData(dungeonLevel.rows, -1)

    def construct(self):
        """
        Take a session level that had its data loaded via placing json data into its __dict__
        and construct a new tree with actual constructors
        """
        dl = DungeonSessionLevel()
        self.cloneData(dl)
        return dl

    def cloneData(self, dl):
        if hasattr(self, 'fogOfWarVersion'):
            dl.fogOfWarVersion = self.fogOfWarVersion
        else:
            dl.fogOfWarVersion = 0
        if hasattr(self, 'bitsPerColumn'):
            dl.bitsPerColumn = self.bitsPerColumn
        else:
            dl.bitsPerColumn = 0
        if hasattr(self, 'fogOfWar'):
            dl.fogOfWar = self.fogOfWar
        if hasattr(self, 'fogOfWarData'):
            dl.fogOfWarData = self.fogOfWarData
        else:
            dl.fogOfWarData = []
        if hasattr(self, 'monsters'):
            if self.monsters is not None:
                monsters = PogList()
                monsters.__dict__ = self.monsters
                dl.monsters = monsters.construct()
        if hasattr(self, 'roomObjects'):
            if self.roomObjects is not None:
                roomObjects = PogList()
                roomObjects.__dict__ = self.roomObjects
                dl.roomObjects = roomObjects.construct()

    def updateFOW(self, columns, rows, value):
        if self.fogOfWarData is None:
            return
        bitIndex = (rows * self.bitsPerColumn) + columns
        arrayIndex = bitIndex // 32
        bitShift = bitIndex % 32
        bitMask = 1 << bitShift
        word = self.fogOfWarData[arrayIndex] & 0xffffffff
        if value:
            word |= bitMask
        else:
            word &= ~bitMask
        self.fogOfWarData[arrayIndex] = word

    def isFowSet(self, column, row):
        if self.fogOfWarData is None:
            return
        bitIndex = (row * self.bitsPerColumn) + column
        arrayIndex = bitIndex // 32
        bitShift = bitIndex % 32
        bitMask = 1 << bitShift
        ans = self.fogOfWarData[arrayIndex] & bitMask
        return ans != 0

    def migrateSession(self, dungeonLevel):
        self.bitsPerColumn = dungeonLevel.columns
        return False

    def createNewFOWData(self, rows, fillData=0):
        size = int(((self.bitsPerColumn * rows) / 32) + 1)
        data = []
        for _ in range(size):
            data.append(fillData)
        return data

    def setFogOfWar(self, newFogOfWar):
        self.fogOfWarData = newFogOfWar
        self.fogOfWarVersion += 1
