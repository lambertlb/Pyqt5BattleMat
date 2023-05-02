"""
GPL 3 file header
"""


class RequestData:
	"""
	This class is used to hold the parameters needed to request data from the server.
	Variables will be added dynamically that represent the details for the request
	"""

	token = 0  # token received from login

	def	__init__(self, request):
		self.request = request
		self.token = RequestData.token
	pass

	@staticmethod
	def setToken(newToken):
		RequestData.token = newToken