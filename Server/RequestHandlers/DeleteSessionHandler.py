"""
GPL 3 file header
"""
from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class DeleteSessionHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the DELETESESSION request.
	"""

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = parameters.get('dungeonUUID')[0]
		sessionUUID = parameters.get('sessionUUID')[0]
		ServerDataManager.deleteSession(server, dungeonUUID, sessionUUID)
		return ''

	def serviceName(self):
		return 'DELETESESSION'
