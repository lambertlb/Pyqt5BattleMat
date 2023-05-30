import json

from Server.ServerDataManager import ServerDataManager


class FileListResponse:
	def __init__(self, filePath):
		self.filePath = filePath
		self.fileNames = []


class FileLister:

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		folder = parameters.get('folder')[0]
		response = FileListResponse(folder)
		response.fileNames = ServerDataManager.getFilenamesInPath(server, folder)
		return json.dumps(response, default=vars)
