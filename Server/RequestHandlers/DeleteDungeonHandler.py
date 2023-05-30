from Server.ServerDataManager import ServerDataManager


class DeleteDungeonHandler:
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = parameters.get('dungeonUUID')[0]
		ServerDataManager.deleteDungeon(server, dungeonUUID)
		return ''
