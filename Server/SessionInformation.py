import json

from services.serviceData.DungeonSessionData import DungeonSessionData


class SessionInformation:
	def __init__(self, sessionData=None, sessionPath=None, sessionDirectory=None):
		self.dirty = False
		self.sessionDirectory = sessionDirectory
		self.sessionPath = sessionPath
		self.sessionData = sessionData

	def load(self, sessionPath, sessionDirectory, jsonData):
		self.sessionPath = sessionPath
		self.sessionDirectory = sessionDirectory
		self.fromJson(jsonData)

	def fromJson(self, jsonData):
		self.sessionData = None
		if jsonData is not None and jsonData:
			sessionData = DungeonSessionData()
			sessionData.__dict__ = json.loads(jsonData)
			self.sessionData = sessionData.construct()
