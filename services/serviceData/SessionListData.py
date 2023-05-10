"""
GPL 3 file header
"""


class SessionListData:

	def __init__(self):
		self.dungeonUUID = None
		self.sessionNames = []
		self.sessionUUIDs = []

	def getDungeonUUID(self):
		return self.dungeonUUID

	def getSessionNames(self):
		return self.sessionNames

	def getSessionUUIDs(self):
		return self.sessionUUIDs
