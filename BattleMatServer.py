import traceback
import urllib
from urllib import parse
from http.server import SimpleHTTPRequestHandler, HTTPServer

from Server.RequestHandlers.DeleteFileHandler import DeleteFileHandler
from Server.RequestHandlers.FileListerHandler import FileListerHandler
from Server.RequestHandlers.CreateNewDungeonHandler import CreateNewDungeonHandler
from Server.RequestHandlers.DeleteDungeonHandler import DeleteDungeonHandler
from Server.RequestHandlers.DungeonListHandler import DungeonListHandler
from Server.RequestHandlers.LoadJsonDataHandler import LoadJsonDataHandler
from Server.RequestHandlers.LoginRequestHandler import LoginRequestHandler
from Server.RequestHandlers.SaveJsonDataHandler import SaveJsonDataHandler
from Server.RequestHandlers.SessionListHandler import SessionListHandler

"""
		webServices.put("CREATENEWSESSION", new CreateNewSessionHandler());
		webServices.put("DELETESESSION", new DeleteSessionHandler());
		webServices.put("LOADSESSION", new LoadSessionHandler());
		webServices.put("UPDATEFOW", new UpdateFOWHander());
		webServices.put("FILEUPLOAD", new FileUploadHandler());
		webServices.put("ADDORUPDATEPOG", new AddOrUpdatePogHandler());
		webServices.put("DELETEPOG", new DeletePogHandler());
		webServices.put("DELETEFILE", new DeleteFile());
"""


class BattleMatServer(SimpleHTTPRequestHandler):
	handler = {
		'LOGIN': LoginRequestHandler(),
		'GETDUNGEONLIST': DungeonListHandler(),
		'GETSESSIONLIST': SessionListHandler(),
		'LOADJSONFILE': LoadJsonDataHandler(),
		'FILELISTER': FileListerHandler(),
		'CREATENEWDUNGEON': CreateNewDungeonHandler(),
		'DELETEDUNGEON': DeleteDungeonHandler(),
		'SAVEJSONFILE': SaveJsonDataHandler(),
		'DELETEFILE': DeleteFileHandler()

	}

	webAppDirectory = None
	topDirectory = './webApp/'

	def __init__(self,  *args, **kwargs):
		super(BattleMatServer, self).__init__(*args, directory=BattleMatServer.webAppDirectory, **kwargs)

	def do_GET(self):
		super(BattleMatServer, self).do_GET()

	def do_POST(self):
		self.topDirectory = BattleMatServer.topDirectory
		urlParts = urllib.parse.urlsplit(self.path)
		parameters = urllib.parse.parse_qs(urlParts.query)

		returnCode = 200
		returnData = ''
		try:
			content_length = int(self.headers["Content-Length"])
			rawData = self.rfile.read(content_length)
			requestType = parameters['request'][0]
			requestHandler = BattleMatServer.handler.get(requestType)
			if requestHandler is not None:
				returnData = requestHandler.handleRequest(self, parameters, rawData)
			else:
				print(f'need handler {requestType}')
				returnData = 'Bad request'
		except (Exception,):
			traceback.print_exc()
			returnCode = 400
		self.send_response(returnCode)
		self.end_headers()
		self.wfile.write(bytes(returnData, 'utf-8'))


def run(server_class=HTTPServer, handler_class=BattleMatServer, host='localhost', port=8080, hostDirectory='./webApp'):
	server_address = (host, port)
	BattleMatServer.webAppDirectory = hostDirectory
	httpd = server_class(server_address, handler_class)
	print('Starting httpd...')
	httpd.serve_forever()


if __name__ == "__main__":
	from sys import argv

if len(argv) == 2:
	run(port=int(argv[1]))
else:
	run()
