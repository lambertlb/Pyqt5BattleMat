"""
GPL 3 file header
"""
from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class DeleteFileHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the DELETEFILE request.
	"""

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		path = parameters.get('path')[0]
		ServerDataManager.deleteFile(server, path)
		return ''

	def serviceName(self):
		return 'DELETEFILE'
