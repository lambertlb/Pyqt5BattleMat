"""
GPL 3 file header
"""
import json

from services.AsyncTasks import AsyncJsonData
from services.Constants import Constants
from services.ReasonForEvent import ReasonForEvent
from services.ServicesManager import ServicesManager
from services.serviceData.DataRequesterResponse import DataRequesterResponse
from services.serviceData.RequestData import RequestData


class DungeonManager:
	"""
	This will manage all dungeon related data
	"""

	def isValidLoginData(self, serverURL, username, password):
		return len(serverURL) != 0 and len(username) != 0 and len(password) != 0

	def login(self, username, password, onSuccess, onFailure):
		url = ServicesManager.getConfigManager().getValue(Constants.Login_Url, 'URL')
		if self.isValidLoginData(url, username, password):
			request = RequestData(Constants.Login_Request)
			request.username = username
			request.password = password
			dataResponse = DataRequesterResponse()
			dataResponse.onSuccess = self.handleSuccessfulLogin
			dataResponse.onFailure = self.handleFailedLogin
			dataResponse.userOnSuccess = onSuccess
			dataResponse.userOnFailure = onFailure
			AsyncJsonData(url, request, dataResponse, None).submit()
		else:
			onFailure(None)
		pass

	def handleSuccessfulLogin(self, dataRequestResponse):
		loginResponse = json.loads(dataRequestResponse.data.text)
		if loginResponse['token'] == 0 or loginResponse['error'] != 0:
			self.handleFailedLogin(dataRequestResponse)
			return
		RequestData.setToken(int(loginResponse['token']))
		dataRequestResponse.userOnSuccess('')
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, True)
		pass

	def handleFailedLogin(self, dataRequestResponse):
		dataRequestResponse.userOnFailure('')
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, False)
		pass
