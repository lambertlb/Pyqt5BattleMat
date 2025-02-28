"""
GPL 3 file header
"""
import json

from Server.RequestHandler import RequestHandler
from Server.ServerDataManager import ServerDataManager


class FileListResponse:
	"""
	response for file list request
	"""
	def __init__(self, filePath):
		self.filePath = filePath
		self.fileNames = []


class FileListerHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the FILELISTER request.
	"""

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters: dict, data):
		folder = parameters.get('folder')[0]
		response = FileListResponse(folder)
		response.fileNames = ServerDataManager.getFilenamesInPath(server, folder)
		return json.dumps(response, default=vars)

	def serviceName(self):
		return 'FILELISTER'
