import json

from Server.ServerDataManager import ServerDataManager
from services.serviceData.FogOfWarData import FogOfWarData


class UpdateFOWHandler:
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		sessionUUID = parameters.get('sessionUUID')[0]
		currentLevel = int(parameters.get('currentLevel')[0])
		fogOfWarData = FogOfWarData()
		fogOfWarData.__dict__ = json.loads(data.decode())
		ServerDataManager.updateFOW(server, sessionUUID, currentLevel, fogOfWarData.fogOfWar)
		return ''
