"""
GPL 3 file header
"""
from services.serviceData.PogList import PogList


class DungeonSessionLevel:

	def __init__(self):
		self.fogOfWarVersion = 0
		self.fogOfWarData = []
		self.bitsPerColumn = 0
		self.monsters = PogList()
		self.roomObjects = PogList()

	def construct(self):
		dl = DungeonSessionLevel()
		self.cloneData(dl)
		return dl

	def cloneData(self, dl):
		if hasattr(self, 'fogOfWarVersion'):
			dl.fogOfWarVersion = self.fogOfWarVersion
		else:
			dl.fogOfWarVersion = None
		if hasattr(self, 'bitsPerColumn'):
			dl.bitsPerColumn = self.bitsPerColumn
		else:
			dl.bitsPerColumn = 0
		if hasattr(self, 'fogOfWar'):
			dl.fogOfWar = self.fogOfWar
		else:
			dl.fogOfWar = None
		if hasattr(self, 'fogOfWarData'):
			dl.fogOfWarData = self.fogOfWarData
		else:
			dl.fogOfWarData = None
		if self.monsters is not None:
			monsters = PogList()
			monsters.__dict__ = self.monsters
			dl.monsters = monsters.construct()
		if self.roomObjects is not None:
			roomObjects = PogList()
			roomObjects.__dict__ = self.roomObjects
			dl.roomObjects = roomObjects.construct()
		pass

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

	# noinspection PyMethodMayBeStatic
	def createNewFOWData(self, rows):
		return [((self.bitsPerColumn * rows) / 32) + 1]
