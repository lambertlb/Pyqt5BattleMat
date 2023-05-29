import json

from Server.ServerDataManager import ServerDataManager


class DungeonListResponseData:
	def __init__(self, dungeonListData, dungeonDirectoryData):
		print(dungeonListData)
		print(dungeonDirectoryData)
		self.dungeonNames = []
		self.dungeonUUIDS = []
		self.dungeonDirectories = []
		for key, value in dungeonListData.items():
			self.dungeonNames.append(value)
			self.dungeonUUIDS.append(key)
		for key, value in dungeonDirectoryData.items():
			self.dungeonDirectories.append(value)


class DungeonListHandler:
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters, data):
		ServerDataManager.getDungeonListData(server)
		response = DungeonListResponseData(ServerDataManager.dungeonNameToUUIDMap, ServerDataManager.uuidTemplatePathMap)
		return json.dumps(response, default=vars)
