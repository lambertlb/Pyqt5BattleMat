from Server.ServerDataManager import ServerDataManager
from services.serviceData.PogPlace import PogPlace


class AddOrUpdatePogHandler:
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = None
		dd = parameters.get('dungeonUUID')
		if dd:
			dungeonUUID = dd[0]
		sessionUUID = None
		ss = parameters.get('sessionUUID')
		if ss:
			sessionUUID = ss[0]
		currentLevel = 0
		cl = parameters.get('currentLevel')
		if cl:
			currentLevel = int(cl[0])
		place = PogPlace.getKey(parameters.get('place')[0])
		ServerDataManager.savePog(server, dungeonUUID, sessionUUID, currentLevel, place, data)
		return ''
