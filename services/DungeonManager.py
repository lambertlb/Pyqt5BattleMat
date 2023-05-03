"""
GPL 3 file header
"""
import json

from services.AsyncTasks import AsyncJsonData
from services.Constants import Constants
from services.ReasonForEvent import ReasonForEvent
from services.ServicesManager import ServicesManager
from services.serviceData.DataRequesterResponse import DataRequesterResponse
from services.serviceData.DungeonListData import DungeonListData
from services.serviceData.RequestData import RequestData
from services.serviceData.SessionListData import SessionListData


class DungeonManager:
	"""
	This will manage all dungeon related data
	"""
	baseURL = None
	dungeonToUUIDMap = dict()
	uuidTemplatePathMap = dict()
	uuidOfMasterTemplate = 'template-dungeon'
	sessionListData = None

	def isValidLoginData(self, serverURL, username, password):
		return len(serverURL) != 0 and len(username) != 0 and len(password) != 0

	def getDungeonToUUIDMap(self):
		return self.dungeonToUUIDMap

	def getSessionListData(self):
		return self.sessionListData

	def okToDeleteThisTemplate(self, uuid):
		return uuid != self.uuidOfMasterTemplate

	def makeURL(self, additions):
		if self.baseURL is None:
			self.baseURL = ServicesManager.getConfigManager().getValue(Constants.Login_Url, 'URL')
		return self.baseURL + additions

	def login(self, username, password, onSuccess, onFailure):
		url = self.makeURL(Constants.ServicePath)
		if self.isValidLoginData(url, username, password):
			request = RequestData(Constants.LoginRequest)
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
		self.getDungeonList(dataRequestResponse.userOnSuccess, dataRequestResponse.userOnFailure)
		pass

	def handleFailedLogin(self, dataRequestResponse):
		dataRequestResponse.userOnFailure('')
		pass

	def getDungeonList(self, onSuccess, onFailure):
		request = RequestData(Constants.DungeonListRequest)
		dataResponse = DataRequesterResponse()
		dataResponse.onSuccess = self.handleSuccessfulDungeonList
		dataResponse.onFailure = self.handleFailedDungeonList
		dataResponse.userOnSuccess = onSuccess
		dataResponse.userOnFailure = onFailure
		AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

	def handleSuccessfulDungeonList(self, dataRequestResponse):
		data = DungeonListData()
		data.__dict__ = json.loads(dataRequestResponse.data.text)
		self.dungeonToUUIDMap.clear()
		self.uuidTemplatePathMap.clear()
		self.uuidOfMasterTemplate = None
		amountInList = len(data.dungeonNames)
		for i in range(amountInList):
			self.dungeonToUUIDMap[data.dungeonNames[i]] = data.dungeonUUIDS[i]
			self.uuidTemplatePathMap[data.dungeonUUIDS[i]] = data.dungeonDirectories[i]

		dataRequestResponse.userOnSuccess('')
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOGGED_IN, True)
		pass

	def handleFailedDungeonList(self, dataRequestResponse):
		pass

	def getSessionList(self, uuid):
		request = RequestData(Constants.SessionListRequest)
		request.dungeonUUID = uuid
		dataResponse = DataRequesterResponse()
		dataResponse.onSuccess = self.handleSuccessfulSessionList
		dataResponse.onFailure = self.handleFailedSessionList
		AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

	def handleSuccessfulSessionList(self, dataRequestResponse):
		self.sessionListData = SessionListData()
		self.sessionListData.__dict__ = json.loads(dataRequestResponse.data.text)
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.SessionListChanged, None)
		pass

	def handleFailedSessionList(self, dataRequestResponse):
		pass
