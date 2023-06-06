"""
GPL 3 file header
"""
import socket
import traceback
import urllib
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Timer
from urllib import parse

from Server.RequestHandlers.AddOrUpdatePogHandler import AddOrUpdatePogHandler
from Server.RequestHandlers.CreateNewDungeonHandler import CreateNewDungeonHandler
from Server.RequestHandlers.CreateNewSessionHandler import CreateNewSessionHandler
from Server.RequestHandlers.DeleteDungeonHandler import DeleteDungeonHandler
from Server.RequestHandlers.DeleteFileHandler import DeleteFileHandler
from Server.RequestHandlers.DeletePogHandler import DeletePogHandler
from Server.RequestHandlers.DeleteSessionHandler import DeleteSessionHandler
from Server.RequestHandlers.DungeonListHandler import DungeonListHandler
from Server.RequestHandlers.FileListerHandler import FileListerHandler
from Server.RequestHandlers.FileUploadHandler import FileUploadHandler
from Server.RequestHandlers.LoadJsonDataHandler import LoadJsonDataHandler
from Server.RequestHandlers.LoadSessionHandler import LoadSessionHandler
from Server.RequestHandlers.LoginRequestHandler import LoginRequestHandler
from Server.RequestHandlers.SaveJsonDataHandler import SaveJsonDataHandler
from Server.RequestHandlers.SessionListHandler import SessionListHandler
from Server.RequestHandlers.UpdateFOWHandler import UpdateFOWHandler
from Server.ServerDataManager import ServerDataManager


class BattleMatServer(SimpleHTTPRequestHandler):
    """
    This class manages a web service
    """

    # Following is a list of all services and their corresponding handler
    # noinspection SpellCheckingInspection
    handler = {
        'LOGIN': LoginRequestHandler(),
        'GETDUNGEONLIST': DungeonListHandler(),
        'GETSESSIONLIST': SessionListHandler(),
        'LOADJSONFILE': LoadJsonDataHandler(),
        'FILELISTER': FileListerHandler(),
        'CREATENEWDUNGEON': CreateNewDungeonHandler(),
        'DELETEDUNGEON': DeleteDungeonHandler(),
        'SAVEJSONFILE': SaveJsonDataHandler(),
        'DELETEFILE': DeleteFileHandler(),
        'FILEUPLOAD': FileUploadHandler(),
        'CREATENEWSESSION': CreateNewSessionHandler(),
        'DELETESESSION': DeleteSessionHandler(),
        'LOADSESSION': LoadSessionHandler(),
        'UPDATEFOW': UpdateFOWHandler(),
        'ADDORUPDATEPOG': AddOrUpdatePogHandler(),
        'DELETEPOG': DeletePogHandler()
    }

    webAppDirectory = None
    topDirectory = './webApp/'  # path to top of file tree

    def __init__(self, *args, **kwargs):
        super(BattleMatServer, self).__init__(*args, directory=BattleMatServer.webAppDirectory, **kwargs)

    def do_GET(self):
        super(BattleMatServer, self).do_GET()

    def do_POST(self):
        """
        Handle POST requests.
        This expects a request and it parameters to be included in the parts.
        It will use the request data to look up the proper handler
        """
        self.topDirectory = BattleMatServer.topDirectory
        urlParts = urllib.parse.urlsplit(self.path)
        parameters = urllib.parse.parse_qs(urlParts.query)

        returnCode = 200
        returnData = ''
        rawData = ''
        try:
            content_type = self.headers['content-type']
            if 'multi' not in content_type: # if not multipart then just read the data for the handlers
                content_length = int(self.headers["Content-Length"])
                rawData = self.rfile.read(content_length)
            requestType = parameters['request'][0]
            # look up proper handler for request
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

    @staticmethod
    def startTimer():
        """
        Run a periodic timer to handle time based tasks.
        This can include saving dirty data or flushing stale caches
        """
        t = Timer(5.0, BattleMatServer.periodicTimer)
        t.start()

    @staticmethod
    def periodicTimer():
        ServerDataManager.periodicTimer()
        BattleMatServer.startTimer()


def run(server_class=HTTPServer, handler_class=BattleMatServer, host=None, port=8080, hostDirectory='./webApp'):
    if not host:
        host = socket.gethostbyname(socket.gethostname())
    server_address = (host, port)
    BattleMatServer.webAppDirectory = hostDirectory
    httpd = server_class(server_address, handler_class)
    print(f'Starting battle mat server http://{host}:{port}')
    BattleMatServer.startTimer()
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
