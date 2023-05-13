"""
GPL 3 file header
"""
from services.serviceData.PogList import PogList


class DungeonSessionLevel:

	def __init__(self):
		self.fogOfWarVersion = 0
		self.fogOfWar = None  # deprecated used to support old format
		self.fogOfWarData = None
		self.bitsPerColumn = 0
		self.monsters = None
		self.roomObjects = None

	def construct(self):
		dl = DungeonSessionLevel()
		self.cloneData(dl)
		return dl

	def cloneData(self, dl):
		if 'fogOfWarVersion' in locals():
			dl.fogOfWarVersion = self.fogOfWarVersion
		else:
			dl.fogOfWarVersion = None
		if 'bitsPerColumn' in locals():
			dl.bitsPerColumn = self.bitsPerColumn
		else:
			dl.fogOfWarVersion = 0
		if 'fogOfWarVersion' in locals():
			dl.fogOfWar = self.fogOfWar
		else:
			dl.fogOfWar = None
		if 'fogOfWarData' in locals():
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
		arrayIndex = bitIndex / 32
		bitShift = bitIndex % 32
		bitMask = 1 << bitShift
		if value:
			self.fogOfWarData[arrayIndex] |= bitMask
		else:
			self.fogOfWarData[arrayIndex] &= ~bitMask

	def isFowSet(self, column, row):
		if self.fogOfWarData is None:
			return
		bitIndex = (row * self.bitsPerColumn) + column
		arrayIndex = bitIndex / 32
		bitShift = bitIndex % 32
		bitMask = 1 << bitShift
		return (self.fogOfWarData[arrayIndex] & bitMask) != 0

	def migrateSession(self, dungeonLevel):
		self.bitsPerColumn = dungeonLevel.rows
		oldData = self.fogOfWar
		if oldData is None:
			return False
		newData = self.createNewFOWData(dungeonLevel.rows)
		for row in range(dungeonLevel.rows):
			for column in range(dungeonLevel.columns):
				bitIndex = (row * self.bitsPerColumn) + column
				arrayIndex = bitIndex / 32
				bitShift = bitIndex % 32
				bitMask = 1 << bitShift
				if oldData[column][row]:
					newData[arrayIndex] |= bitMask
				else:
					newData[arrayIndex] &= ~bitMask
		self.fogOfWarData = newData
		self.fogOfWar = None
		return True

	# noinspection PyMethodMayBeStatic
	def createNewFOWData(self, rows):
		return [rows]
