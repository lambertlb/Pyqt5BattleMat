"""
GPL 3 file header
"""


class DungeonListData:

	def __init__(self, dungeonListData=None, dungeonDirectoryData=None):
		self.dungeonNames = []
		self.dungeonUUIDS = []
		self.dungeonDirectories = []
		if dungeonListData is None:
			return
		for key, value in dungeonListData.items():
			self.dungeonNames.append(value)
			self.dungeonUUIDS.append(key)
		for key, value in dungeonDirectoryData.items():
			self.dungeonDirectories.append(value)
