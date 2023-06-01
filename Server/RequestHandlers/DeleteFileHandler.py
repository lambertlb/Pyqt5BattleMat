"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class DeleteFileHandler:
	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		path = parameters.get('path')[0]
		ServerDataManager.deleteFile(server, path)
		return ''
