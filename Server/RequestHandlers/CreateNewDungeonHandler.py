"""
GPL 3 file header
"""
from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class CreateNewDungeonHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the CREATENEWDUNGEON request.
	"""

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = parameters.get('dungeonUUID')[0]
		newDungeonName = parameters.get("newDungeonName")[0]
		ServerDataManager.copyDungeon(server, dungeonUUID, newDungeonName)
		return ''

	def serviceName(self):
		return 'CREATENEWDUNGEON'
