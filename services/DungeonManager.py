"""
GPL 3 file header
"""
import json

from PyQt5 import QtCore
from buildurl import BuildURL
from functools import partial

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

	loginKey = None

	def isValidLoginData(self, serverURL, username, password):
		return len(serverURL) != 0 and len(username) != 0 and len(password) != 0

	def login(self, username, password, callback):
		url = ServicesManager.getConfigManager().getValue(Constants.Login_Url, 'URL')
		if self.isValidLoginData(url, username, password):
			request = RequestData(Constants.Login_Request)
			request.username = username
			request.password = password
			dataResponse = DataRequesterResponse(callback)
			dataResponse.onSuccess = partial(self.handleSuccessfulLogin, dataResponse)
			dataResponse.onFailure = partial(self.handleFailedLogin, dataResponse)
			AsyncJsonData(url, request, dataResponse)
		else:
			callback.onFailure(None)
		pass

	@QtCore.pyqtSlot(DataRequesterResponse)
	def handleSuccessfulLogin(self, dataRequestResponse):
		loginResponse = json.loads(dataRequestResponse.data.text)
		if loginResponse['token'] == 0 or loginResponse['error'] != 0:
			self.handleFailedLogin(dataRequestResponse)
			return
		self.loginKey = loginResponse['token']
		dataRequestResponse.userCallback.onSuccess(dataRequestResponse.data.text)
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, True)
		dataRequestResponse.cleanUp()
		pass

	@QtCore.pyqtSlot(DataRequesterResponse)
	def handleFailedLogin(self, dataRequestResponse):
		dataRequestResponse.userCallback.onFailure(dataRequestResponse.data.text)
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, False)
		dataRequestResponse.cleanUp()
		pass
