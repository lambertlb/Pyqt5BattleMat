"""
GPL 3 file header
"""

from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class LoadJsonDataHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the LOADJSONFILE request.
	"""

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

	def serviceName(self):
		return 'LOADJSONFILE'
