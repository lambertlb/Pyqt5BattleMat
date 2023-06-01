"""
GPL 3 file header
"""

from Server.ServerDataManager import ServerDataManager


class LoadJsonDataHandler:

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = None
		dd = parameters.get('dungeonUUID')
		if dd:
			dungeonUUID = dd[0]
		fileName = None
		ff = parameters.get('fileName')
		if ff:
			fileName = ff[0]

		if dungeonUUID:
			data = ServerDataManager.getDungeonDataAsString(server, dungeonUUID)
		else:
			data = ServerDataManager.getFileAsString(server, fileName)
		return data
