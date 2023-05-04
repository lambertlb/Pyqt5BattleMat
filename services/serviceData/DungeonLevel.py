"""
GPL 3 file header
"""

from services.serviceData.DungeonSessionLevel import DungeonSessionLevel


class DungeonLevel(DungeonSessionLevel):
	levelDrawing = None
	levelName = None
	gridSize = 30
	gridOffsetX = 0
	gridOffsetY = 0
	columns = 0
	rows = 0

	def construct(self):
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
