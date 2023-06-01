"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class DeleteSessionHandler:
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = parameters.get('dungeonUUID')[0]
		sessionUUID = parameters.get('sessionUUID')[0]
		ServerDataManager.deleteSession(server, dungeonUUID, sessionUUID)
		return ''
