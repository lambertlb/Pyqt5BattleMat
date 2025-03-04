"""
GPL 3 file header
"""
from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class CreateNewSessionHandler(RequestHandler):

	def __init__(self):
		super().__init__()
		
	# noinspection SpellCheckingInspection
	"""
	Handle the CREATENEWSESSION request.
	"""
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		dungeonUUID = parameters.get('dungeonUUID')[0]
		newSessionName = parameters.get('newSessionName')[0]
		ServerDataManager.createSession(server, dungeonUUID, newSessionName)
		return ''

	def serviceName(self):
		return 'CREATENEWSESSION'
