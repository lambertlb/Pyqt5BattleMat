import json
import urllib
from urllib import parse
from http.server import SimpleHTTPRequestHandler, HTTPServer

from RequestHandlers.LoginRequestHandler import LoginRequestHandler


class BattleMatServer(SimpleHTTPRequestHandler):
	handler = {
		'LOGIN': LoginRequestHandler()
	}

	def do_POST(self):
		urlParts = urllib.parse.urlsplit(self.path)
		parameters = urllib.parse.parse_qs(urlParts.query)

		returnCode = 200
		returnData = b''
		try:
			content_length = int(self.headers["Content-Length"])
			rawData = self.rfile.read(content_length)
			if len(rawData) != 0:
				data = json.loads(rawData)
			else:
				data = None
			requestType = parameters['request'][0]
			requestHandler = BattleMatServer.handler.get(requestType)
			if requestHandler is not None:
				returnData = requestHandler.handleRequest(parameters, data)
		except (Exception,):
			returnCode = 400

		self.send_response(returnCode)
		self.end_headers()
		self.wfile.write(bytes(returnData, 'utf-8'))


def run(server_class=HTTPServer, handler_class=BattleMatServer, host='localhost', port=8080):
	server_address = (host, port)
	httpd = server_class(server_address, handler_class)
	print('Starting httpd...')
	httpd.serve_forever()


if __name__ == "__main__":
	from sys import argv

if len(argv) == 2:
	run(port=int(argv[1]))
else:
	run()
