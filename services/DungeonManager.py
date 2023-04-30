"""
MIT License

Copyright (c) 2023 Leon Lambert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json

from buildurl import BuildURL
from functools import partial

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
		if self.isValidLoginData(ServicesManager.getConfigManager().getConfig().get('Login', 'URL'), username, password):
			loginData = RequestData()
			loginData.username = username
			loginData.password = password
			dataRequest = DataRequesterResponse(callback)
			dataRequest.onSuccess = partial(self.handleSuccessfulLogin, dataRequest)
			dataRequest.onFailure = partial(self.handleLailedLogin, dataRequest)
			ServicesManager.getDataRequester().requestData('LOGIN', loginData, "", dataRequest)
		else:
			callback.onFailure(None)

	def handleSuccessfulLogin(self, dataRequestResponse):
		loginResponse = json.loads(dataRequestResponse.returnData.result)
		if loginResponse['token'] == 0 or loginResponse['error'] != 0:
			self.handleLailedLogin(dataRequestResponse)
			return
		self.loginKey = loginResponse['token']
		dataRequestResponse.userCallback.onSuccess(dataRequestResponse.returnData.result)
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, True)

	def handleLailedLogin(self, dataRequestResponse):
		dataRequestResponse.userCallback.onFailure(dataRequestResponse.returnData.result)
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, False)
