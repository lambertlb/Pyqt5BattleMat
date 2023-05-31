"""
GPL 3 file header
"""
from services.serviceData.DungeonSessionLevel import DungeonSessionLevel
from services.serviceData.PogList import PogList


class DungeonSessionData:

	def __init__(self, newSessionName='', dungeonUUID='', sessionUUID=''):
		self.version = 1
		self.sessionName = newSessionName
		self.dungeonUUID = dungeonUUID
		self.sessionUUID = sessionUUID
		self.players = PogList()
		self.sessionLevels = []
		self.bitsPerColumn = 32

	def construct(self):
		ds = DungeonSessionData()
		self.cloneData(ds)
		return ds

	def cloneData(self, ds):
		ds.version = self.version
		ds.sessionName = self.sessionName
		ds.dungeonUUID = self.dungeonUUID
		ds.sessionUUID = self.sessionUUID

		players = PogList()
		players.__dict__ = self.players
		ds.players = players.construct()

		for level in self.sessionLevels:
			ld = DungeonSessionLevel()
			ld.__dict__ = level
			ds.sessionLevels.append(ld.construct())

	def setSessionLevels(self, sessionLevels):
		self.sessionLevels = sessionLevels
