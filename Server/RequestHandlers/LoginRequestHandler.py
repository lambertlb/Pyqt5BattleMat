"""
GPL 3 file header
"""
import json
from Server.RequestHandler import RequestHandler


class LoginResponse:

	def __init__(self):
		self.error = 0
		self.token = 0


class LoginRequestHandler(RequestHandler):

	def __init__(self):
		super().__init__()

	# noinspection SpellCheckingInspection
	"""
	Handle the LOGIN request.
	"""

	# noinspection PyUnusedLocal
	# noinspection PyMethodMayBeStatic
	def handleRequest(self, server, parameters, data):
		response = LoginResponse()
		username = parameters.get('username')[0]
		password = parameters.get('password')[0]
		# login authorization not implemented just do parameter check
		if username is None or not username or password is None or not password:
			response.error = 1
		else:
			response.token = 22
		return json.dumps(response, default=vars)

	def serviceName(self):
		return 'LOGIN'
