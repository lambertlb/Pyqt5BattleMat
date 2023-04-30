"""
GPL 3 file header
"""
import json

from buildurl import BuildURL
from functools import partial

from services.ReasonForEvent import ReasonForEvent
from services.ServicesManager import ServicesManager

class DungeonManager:
	"""
	This will manage all dungeon related data
	"""

	loginKey = None
	def isValidLoginData(self, serverURL, username, password):
		return len(serverURL) != 0 and len(username) != 0 and len(password) != 0

	def login(self, username, password, callback):
		# if self.isValidLoginData(ServicesManager.getConfigManager().getConfig().get('Login', 'URL'), username, password):
		# 	loginData = RequestData()
		# 	loginData.username = username
		# 	loginData.password = password
		# 	dataRequest = DataRequesterResponse(callback)
		# 	dataRequest.onSuccess = partial(self.handleSuccessfulLogin, dataRequest)
		# 	dataRequest.onFailure = partial(self.handleLailedLogin, dataRequest)
		# 	ServicesManager.getDataRequester().requestData('LOGIN', loginData, "", dataRequest)
		# else:
		# 	callback.onFailure(None)
		pass

	def handleSuccessfulLogin(self, dataRequestResponse):
		# loginResponse = json.loads(dataRequestResponse.returnData.result)
		# if loginResponse['token'] == 0 or loginResponse['error'] != 0:
		# 	self.handleLailedLogin(dataRequestResponse)
		# 	return
		# self.loginKey = loginResponse['token']
		# dataRequestResponse.userCallback.onSuccess(dataRequestResponse.returnData.result)
		# ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, True)
		pass

	def handleLailedLogin(self, dataRequestResponse):
		# dataRequestResponse.userCallback.onFailure(dataRequestResponse.returnData.result)
		# ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, False)
		pass