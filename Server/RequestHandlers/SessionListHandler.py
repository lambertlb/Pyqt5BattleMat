import json

from Server.ServerDataManager import ServerDataManager


class SessionListResponseData:
	def __init__(self, sessionListData, dungeonUUID):
		self.dungeonUUID = dungeonUUID
		self.sessionNames = []
		self.sessionUUIDs = []
		for key, value in sessionListData.items():
			self.sessionNames.append(key)
			self.sessionUUIDs.append(value)


class SessionListHandler:

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters, data):
		dungeonUUID = parameters['dungeonUUID'][0]
		sessionMap = ServerDataManager.getSessionListData(server, dungeonUUID)
		response = SessionListResponseData(sessionMap, dungeonUUID)
		return json.dumps(response, default=vars)
