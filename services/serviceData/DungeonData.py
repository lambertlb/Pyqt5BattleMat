"""
GPL 3 file header
"""
from services.serviceData.DungeonLevel import DungeonLevel


class DungeonData:
	uuid = None
	dungeonName = None
	dungeonLevels = None
	showGrid = False

	def construct(self):
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
			pass