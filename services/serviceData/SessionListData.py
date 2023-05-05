"""
GPL 3 file header
"""


class SessionListData:
	dungeonUUID = None
	sessionNames = []
	sessionUUIDs = []

	def getDungeonUUID(self):
		return self.dungeonUUID

	def getSessionNames(self):
		return self.sessionNames

	def getSessionUUIDs(self):
		return self.sessionUUIDs