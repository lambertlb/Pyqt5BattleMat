"""
GPL 3 file header
"""
from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class DeleteDungeonHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the DELETEDUNGEON request.
	"""

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = parameters.get('dungeonUUID')[0]
		ServerDataManager.deleteDungeon(server, dungeonUUID)
		return ''

	def serviceName(self):
		return 'DELETEDUNGEON'
