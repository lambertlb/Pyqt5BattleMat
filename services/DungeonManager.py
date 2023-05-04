"""
GPL 3 file header
"""
import json

from services.AsyncTasks import AsyncJsonData
from services.Constants import Constants
from services.PogManager import PogManager
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.DataRequesterResponse import DataRequesterResponse
from services.serviceData.DataVersions import DataVersions
from services.serviceData.DungeonData import DungeonData
from services.serviceData.DungeonListData import DungeonListData
from services.serviceData.PogCollection import PogCollection
from services.serviceData.PogPlace import PogPlace
from services.serviceData.RequestData import RequestData
from services.serviceData.SessionListData import SessionListData
from services.serviceData.VersionedItem import VersionedItem


class DungeonManager(PogManager):
	"""
	This will manage all dungeon related data
	"""
	baseURL = None
	dungeonToUUIDMap = dict()
	uuidTemplatePathMap = dict()
	uuidOfMasterTemplate = 'template-dungeon'
	sessionListData = None
	isDungeonMaster = False
	selectedDungeonUUID = None
	selectedSessionUUID = None
	editMode = False
	selectedDungeon = None
	currentLevelIndex = 0
	selectedSession = None
	fowToggle = False

	dungeonLevelMonsters = PogCollection(ReasonForAction.LastReason, PogPlace.DUNGEON_LEVEL)
	dungeonLevelRoomObjects = PogCollection(ReasonForAction.LastReason, PogPlace.DUNGEON_LEVEL)
	sessionLevelMonsters = PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_LEVEL)
	sessionLevelRoomObjects = PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_LEVEL)
	sessionLevelPlayers = PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_RESOURCE)
	dataVersion = DataVersions()

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
		ServicesManager.getEventManager().fireEvent(ReasonForAction.LOGGED_IN, True)
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
		ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionListChanged, None)
		pass

	def handleFailedSessionList(self, dataRequestResponse):
		pass

	def editSelectedDungeonUUID(self, selectedDungeonUUID):
		self.selectedDungeonUUID = selectedDungeonUUID
		self.selectedSessionUUID = None
		self.editMode = True
		self.setDungeonMaster(True)
		self.loadSelectedDungeon()

	def setDungeonMaster(self, isDungeonMaster):
		self.isDungeonMaster = isDungeonMaster
		ServicesManager.getEventManager().fireEvent(ReasonForAction.DMStateChange, None)

	def loadSelectedDungeon(self):
		self.initializeDungeonData()
		self.loadInResourceData()

		request = RequestData(Constants.LoadJsonFileRequest)
		request.dungeonUUID = self.selectedDungeonUUID
		dataResponse = DataRequesterResponse()
		dataResponse.onSuccess = self.handleSuccessfulDungeonLoad
		dataResponse.onFailure = self.handleFailedDungeonLoad
		AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

	def handleSuccessfulDungeonLoad(self, dataRequestResponse):
		dd = DungeonData()
		dd.__dict__ = json.loads(dataRequestResponse.data.text)
		self.selectedDungeon = dd.construct()
		self.loadDungeonData()
		# computedGridWidth = getCurrentDungeonLevelData().getGridSize();
		# ServiceManager.getEventManager().fireEvent(new
		# ReasonForActionEvent(ReasonForAction.DungeonSelected, null));
		# ServiceManager.getEventManager().fireEvent(new
		# ReasonForActionEvent(ReasonForAction.DungeonDataLoaded, null));
		# if (editMode) {
		# ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataReadyToEdit, null));
		# } else {
		# loadSessionData(-1);
		# }
		pass

	def handleFailedDungeonLoad(self, dataRequestResponse):
		pass

	def initializeDungeonData(self):
		self.currentLevelIndex = 0
		self.selectedDungeon = None
		self.selectedSession = None
		self.fowToggle = False
		self.setSelectedPog(None)
		self.setPogBeingDragged(None, False)

	def loadInResourceData(self):
		self.loadMonsterPogs()
		self.loadRoomObjectPogs()

	def loadDungeonData(self):
		dungeonLevel = self.getCurrentDungeonLevelData()
		if dungeonLevel is not None:
			self.dungeonLevelMonsters.setPogList(dungeonLevel.monsters)
			self.dungeonLevelRoomObjects.setPogList(dungeonLevel.roomObjects)
			self.updateDataVersion()

	def updateDataVersion(self):
		self.dataVersion.initialize()
		self.dataVersion.setItemVersion(VersionedItem.COMMON_RESOURCE_MONSTERS,
										self.getMonsterCollection().getPogListVersion())
		self.dataVersion.setItemVersion(VersionedItem.COMMON_RESOURCE_ROOMOBECTS,
										self.getRoomCollection().getPogListVersion())
		dungeonLevel = self.getCurrentDungeonLevelData()
		if dungeonLevel is not None:
			self.dataVersion.setItemVersion(VersionedItem.DUNGEON_LEVEL_MONSTERS,
											self.dungeonLevelMonsters.getPogListVersion())
			self.dataVersion.setItemVersion(VersionedItem.DUNGEON_LEVEL_ROOMOBJECTS,
											self.dungeonLevelRoomObjects.getPogListVersion())
		sessionLevelData = self.getCurrentSessionLevelData()
		# if (sessionLevelData != null) {
		# 	dataVersion.setItemVersion(VersionedItem.SESSION_LEVEL_MONSTERS, sessionLevelMonsters.getPogListVersion());
		# 	dataVersion.setItemVersion(VersionedItem.SESSION_LEVEL_ROOMOBJECTS, sessionLevelRoomObjects.getPogListVersion());
		# 	dataVersion.setItemVersion(VersionedItem.SESSION_RESOURCE_PLAYERS, sessionLevelPlayers.getPogListVersion());
		# 	dataVersion.setItemVersion(VersionedItem.FOG_OF_WAR, sessionLevelData.getFOWVersion());
		pass

	def getCurrentDungeonLevelData(self):
		if self.selectedDungeon is not None and self.currentLevelIndex < len(self.selectedDungeon.dungeonLevels):
			return self.selectedDungeon.dungeonLevels[self.currentLevelIndex]
		return None

	def getCurrentSessionLevelData(self):
		if self.selectedSession is not None and self.currentLevelIndex < len(self.selectedSession.sessionLevels):
			return self.selectedSession.sessionLevels[self.currentLevelIndex]
		return None
