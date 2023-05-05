"""
GPL 3 file header
"""
from services.serviceData.PogList import PogList


class DungeonSessionLevel:
	fogOfWarVersion = 0
	fogOfWar = None		# deprecated used to support old format
	fogOfWarData = None
	bitsPerColumn = 0
	monsters = None
	roomObjects = None

	def construct(self):
		dl = DungeonSessionLevel()
		self.cloneData(dl)
		return dl

	def cloneData(self, dl):
		dl.fogOfWarVersion = self.fogOfWarVersion
		dl.bitsPerColumn = self.bitsPerColumn
		dl.fogOfWar = self.fogOfWar
		dl.fogOfWarData = self.fogOfWarData
		if self.monsters is not None:
			monsters = PogList()
			monsters.__dict__ = self.monsters
			dl.monsters = monsters.construct()
		if self.roomObjects is not None:
			roomObjects = PogList()
			roomObjects.__dict__ = self.monsters
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
			for column  in range( dungeonLevel.columns):
				bitIndex = (row * self.bitsPerColumn) + column
				arrayIndex = bitIndex/ 32
				bitShift = bitIndex % 32
				bitMask = 1 << bitShift
				if oldData[column][row]:
					newData[arrayIndex] |= bitMask
				else:
					newData[arrayIndex] &= ~bitMask
		self.fogOfWarData = newData
		self.fogOfWar = None
		return True
