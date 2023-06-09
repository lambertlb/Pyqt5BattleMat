"""
GPL 3 file header
"""
import json
from functools import partial

from services.AsyncTasks import AsyncJsonData, AsyncDownload, AsyncUpload, AsyncCommand
from services.Constants import Constants
from services.PogManager import PogManager
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.DataRequesterResponse import DataRequesterResponse
from services.serviceData.DataVersions import DataVersions
from services.serviceData.DungeonData import DungeonData
from services.serviceData.DungeonListData import DungeonListData
from services.serviceData.DungeonSessionData import DungeonSessionData
from services.serviceData.FogOfWarData import FogOfWarData
from services.serviceData.PogCollection import PogCollection
from services.serviceData.PogPlace import PogPlace
from services.serviceData.RequestData import RequestData
from services.serviceData.SessionListData import SessionListData
from services.serviceData.VersionedItem import VersionedItem


class DungeonManager(PogManager):
    """
    This will manage all dungeon related data
    """

    def __init__(self):
        super(DungeonManager, self).__init__()
        self.dungeonToUUIDMap = dict()
        self.uuidTemplatePathMap = dict()
        self.uuidOfMasterTemplate = 'template-dungeon'
        self.sessionListData = None
        self.isDungeonMaster = False
        self.selectedDungeonUUID = None
        self.selectedSessionUUID = None
        self.editMode = False
        self.selectedDungeon: DungeonData | None = None
        self._currentLevelIndex = 0
        self.selectedSession: DungeonSessionData | None = None
        self.fowToggle = False
        self.computedGridWidth = 1.0
        self.fowDirty = False
        self.assetURL = ''
        self.savedFOW = None

        self.dungeonLevelMonsters = PogCollection(ReasonForAction.LastReason, PogPlace.DUNGEON_LEVEL)
        self.dungeonLevelRoomObjects = PogCollection(ReasonForAction.LastReason, PogPlace.DUNGEON_LEVEL)
        self.sessionLevelMonsters = PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_LEVEL)
        self.sessionLevelRoomObjects = PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_LEVEL)
        self.sessionLevelPlayers = PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_RESOURCE)
        self.dataVersion = DataVersions()

    @property
    def currentLevelIndex(self):
        return self._currentLevelIndex

    @currentLevelIndex.setter
    def currentLevelIndex(self, value):
        self._currentLevelIndex = value
        self.updateWithNewDungeonData()
        self.updateWithSessionData()
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonSelectedLevelChanged, None)

    # noinspection PyMethodMayBeStatic
    def isValidLoginData(self, serverURL, username, password):
        return len(serverURL) != 0 and len(username) != 0 and len(password) != 0

    def getDungeonToUUIDMap(self):
        return self.dungeonToUUIDMap

    def getSessionListData(self):
        return self.sessionListData

    def okToDeleteThisTemplate(self, uuid):
        return uuid != self.uuidOfMasterTemplate

    def doTimeBasedTasks(self):
        if self.selectedSession is not None:
            # periodically see if data changed on server
            self.requestLoadSessionData(self.selectedSession.version)

    def getCurrentSessionUUID(self):
        if self.selectedSession is not None:
            return self.selectedSession.sessionUUID
        return None

    def isDungeonGridVisible(self):
        return self.selectedDungeon.showGrid

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

    def handleSuccessfulLogin(self, dataRequestResponse):
        loginResponse = json.loads(dataRequestResponse.data.text)
        if loginResponse['token'] == 0 or loginResponse['error'] != 0:
            self.handleFailedLogin(dataRequestResponse)
            return
        RequestData.setToken(int(loginResponse['token']))
        self.getDungeonList(dataRequestResponse.userOnSuccess, dataRequestResponse.userOnFailure)

    # noinspection PyMethodMayBeStatic
    def handleFailedLogin(self, dataRequestResponse):
        dataRequestResponse.userOnFailure('')

    def getDungeonList(self, onSuccess, onFailure):
        """
        get list of dungeons from server
        """
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
        amountInList = len(data.dungeonNames)
        # fill in caches
        for i in range(amountInList):
            self.dungeonToUUIDMap[data.dungeonNames[i]] = data.dungeonUUIDS[i]
            self.uuidTemplatePathMap[data.dungeonUUIDS[i]] = data.dungeonDirectories[i]

        dataRequestResponse.userOnSuccess('')
        ServicesManager.getEventManager().fireEvent(ReasonForAction.LOGGED_IN, True)

    def handleFailedDungeonList(self, dataRequestResponse):
        pass

    def getSessionList(self, dungeonUUID):
        """
        get list of session for this dungeon UUID
        """
        request = RequestData(Constants.SessionListRequest)
        request.dungeonUUID = dungeonUUID
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulSessionList
        dataResponse.onFailure = self.handleFailedSessionList
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    def handleSuccessfulSessionList(self, dataRequestResponse):
        self.sessionListData = SessionListData()
        self.sessionListData.__dict__ = json.loads(dataRequestResponse.data.text)
        ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionListChanged, None)

    def handleFailedSessionList(self, dataRequestResponse):
        pass

    def editSelectedDungeonUUID(self, selectedDungeonUUID):
        """
        client wants to edit this dungeon
        """
        self.selectedDungeonUUID = selectedDungeonUUID
        self.selectedSessionUUID = None
        self.editMode = True
        self.setDungeonMaster(True)
        self.loadSelectedDungeon()

    def setDungeonMaster(self, isDungeonMaster):
        self.isDungeonMaster = isDungeonMaster
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DMStateChange, None)

    def loadSelectedDungeon(self):
        """
        load in the dungeon data for the selected dungeon UUID
        """
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
        self.updateWithNewDungeonData()
        self.computedGridWidth = self.getCurrentDungeonLevelData().gridSize
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonSelected, None)
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonDataLoaded, None)
        if self.editMode:
            ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonDataReadyToEdit, None)
        else:
            self.requestLoadSessionData(-1)

    def handleFailedDungeonLoad(self, dataRequestResponse):
        pass

    def initializeDungeonData(self):
        self._currentLevelIndex = 0
        self.selectedDungeon = None
        self.selectedSession = None
        self.fowToggle = False
        self.setSelectedPog(None)
        self.setPogBeingDragged(None, False)

    def loadInResourceData(self):
        self.loadMonsterPogs()
        self.loadRoomObjectPogs()

    def updateWithNewDungeonData(self):
        dungeonLevel = self.getCurrentDungeonLevelData()
        if dungeonLevel is not None:
            self.dungeonLevelMonsters.setPogList(dungeonLevel.monsters)
            self.dungeonLevelRoomObjects.setPogList(dungeonLevel.roomObjects)
            self.updateDataVersion()

    def updateDataVersion(self):
        """
        Keep track of versioned data
        """
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
        if sessionLevelData is not None:
            self.dataVersion.setItemVersion(VersionedItem.SESSION_LEVEL_MONSTERS,
                                            self.sessionLevelMonsters.getPogListVersion())
            self.dataVersion.setItemVersion(VersionedItem.SESSION_LEVEL_ROOMOBJECTS,
                                            self.sessionLevelRoomObjects.getPogListVersion())
            self.dataVersion.setItemVersion(VersionedItem.SESSION_RESOURCE_PLAYERS,
                                            self.sessionLevelPlayers.getPogListVersion())
            self.dataVersion.setItemVersion(VersionedItem.FOG_OF_WAR, sessionLevelData.fogOfWarVersion)

    def getCurrentDungeonLevelData(self):
        if self.selectedDungeon is not None and self._currentLevelIndex < len(self.selectedDungeon.dungeonLevels):
            return self.selectedDungeon.dungeonLevels[self._currentLevelIndex]
        return None

    def getCurrentSessionLevelData(self):
        if self.selectedSession is not None and self._currentLevelIndex < len(self.selectedSession.sessionLevels):
            return self.selectedSession.sessionLevels[self._currentLevelIndex]
        return None

    def requestLoadSessionData(self, version):
        """
        get session data from server
        """
        request = RequestData(Constants.LoadSessionRequest)
        request.dungeonUUID = self.selectedDungeonUUID
        request.sessionUUID = self.selectedSessionUUID
        request.version = version
        dataResponse = DataRequesterResponse()
        dataResponse.version = version
        dataResponse.onSuccess = self.handleSuccessfulSessionLoad
        dataResponse.onFailure = self.handleFailedSessionLoad
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    def handleSuccessfulSessionLoad(self, dataRequestResponse):
        """
        if no data returned it means the version has not changed so nothing to do
        """
        if dataRequestResponse.data.text == '':
            return
        dd = DungeonSessionData()
        dd.__dict__ = json.loads(dataRequestResponse.data.text)
        self.selectedSession = dd.construct()
        self.migrateSession()
        self.updateWithSessionData()
        if dataRequestResponse.version == -1:  # if version is -1 means this is first time loaded
            ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonDataReadyToJoin, None)
        else:
            ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionDataChanged, None)

    def handleFailedSessionLoad(self, dataRequestResponse):
        pass

    def updateWithSessionData(self):
        """
        update caches with session data
        """
        if self.getCurrentSessionLevelData() is not None:
            self.sessionLevelMonsters.updateCollection(self.getCurrentSessionLevelData().monsters)
            self.sessionLevelRoomObjects.updateCollection(self.getCurrentSessionLevelData().roomObjects)
            self.sessionLevelPlayers.updateCollection(self.selectedSession.players)
            self.updateDataVersion()

    def migrateSession(self):
        """
        Migrate and old session data
        """
        saveIndex = self._currentLevelIndex
        for i in range(len(self.selectedSession.sessionLevels)):
            sessionLevel = self.selectedSession.sessionLevels[i]
            dungeonLevel = self.selectedDungeon.dungeonLevels[i]
            if sessionLevel.migrateSession(dungeonLevel):  # need to save if data actually migrated
                self._currentLevelIndex = i
                self.fowDirty = True
                self.saveFow()
        self._currentLevelIndex = saveIndex

    def saveFow(self):
        if self.isDungeonMaster and self.fowDirty:
            self.updateFogOfWar()
        self.fowDirty = False

    def updateFogOfWar(self):
        """
        update server with Fog of war data
        """
        if self.selectedDungeon is not None:
            request = RequestData(Constants.UpdateFOWRequest)
            request.sessionUUID = self.selectedSessionUUID
            request.currentLevel = self._currentLevelIndex
            dataResponse = DataRequesterResponse()
            dataResponse.onSuccess = self.handleSuccessfulUpdateFogOfWar
            dataResponse.onFailure = self.handleFailedUpdateFogOfWar
            sessionLevel = self.getCurrentSessionLevelData()
            fow = FogOfWarData(sessionLevel.fogOfWarData)
            AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, fow).submit()
            sessionLevel.fogOfWarVersion = sessionLevel.fogOfWarVersion + 1
            self.dataVersion.setItemVersion(VersionedItem.FOG_OF_WAR, sessionLevel.fogOfWarVersion)

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleSuccessfulUpdateFogOfWar(self, dataRequestResponse):
        ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionDataSaved, None)

    def handleFailedUpdateFogOfWar(self, dataRequestResponse):
        pass

    def createNewDungeon(self, newDungeonName):
        request = RequestData(Constants.CreateNewDungeonRequest)
        request.dungeonUUID = self.uuidOfMasterTemplate
        request.newDungeonName = newDungeonName
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulDungeonCreate
        dataResponse.onFailure = self.handleFailedDungeonCreate
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    # noinspection PyUnusedLocal
    def handleSuccessfulDungeonCreate(self, dataRequestResponse):
        self.getDungeonList(self.gotDungeonList, self.failedDungeonList)

    def handleFailedDungeonCreate(self, dataRequestResponse):
        pass

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def gotDungeonList(self, data):
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonDataCreated, None)

    def failedDungeonList(self, data):
        pass

    def deleteTemplate(self, dungeonUUID):
        """
        delete the dungeon with this UUID from server
        Not allowed to delete template dungeon
        """
        if not self.okToDeleteThisTemplate(dungeonUUID):
            return
        request = RequestData(Constants.DeleteDungeonRequest)
        request.dungeonUUID = dungeonUUID
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulDungeonDelete
        dataResponse.onFailure = self.handleFailedDungeonDelete
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    # noinspection PyUnusedLocal
    def handleSuccessfulDungeonDelete(self, dataRequestResponse):
        self.getDungeonList(self.gotDungeonList2, self.failedDungeonList)

    def handleFailedDungeonDelete(self, dataRequestResponse):
        pass

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def gotDungeonList2(self, data):
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonDataDeleted, None)

    def dmSession(self, selectedDungeonUUID, sessionUUID):
        """
        start DMing the session with this UUID
        """
        self.selectedDungeonUUID = selectedDungeonUUID
        self.selectedSessionUUID = sessionUUID
        self.editMode = False
        self.setDungeonMaster(True)
        self.loadSelectedDungeon()

    def isNameValidForNewSession(self, newSessionName):
        isValidSessionName = not newSessionName.startswith("Enter ") and len(newSessionName) > 4
        isInCurrentSessionNames = False
        isInCurrentSessionDirectories = False
        if isValidSessionName:
            isInCurrentSessionNames = self.isInCurrentSessionNames(newSessionName)
        return isValidSessionName and not isInCurrentSessionNames and not isInCurrentSessionDirectories

    def isInCurrentSessionNames(self, newSessionName):
        for sessionName in self.sessionListData.sessionNames:
            if sessionName == newSessionName:
                return True
        return False

    def createNewSession(self, dungeonUUID, newSessionName):
        """
        tell sever to create a new session with this name
        """
        request = RequestData(Constants.CreateNewSessionRequest)
        request.dungeonUUID = dungeonUUID
        request.newSessionName = newSessionName
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulCreateSession
        dataResponse.onFailure = self.handleFailedCreateSession
        dataResponse.dungeonUUID = dungeonUUID
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    def handleSuccessfulCreateSession(self, dataRequestResponse):
        self.getSessionList(dataRequestResponse.dungeonUUID)

    def handleFailedCreateSession(self, dataRequestResponse):
        pass

    def deleteSession(self, dungeonUUID, sessionUUID):
        """
        tell server to delete the session with this UUID
        """
        request = RequestData(Constants.DeleteSessionRequest)
        request.dungeonUUID = dungeonUUID
        request.sessionUUID = sessionUUID
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulCreateSession
        dataResponse.onFailure = self.handleFailedCreateSession
        dataResponse.dungeonUUID = dungeonUUID
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    def joinSession(self, selectedDungeonUUID, sessionUUID):
        """
        Join the session with this UUID
        """
        self.selectedDungeonUUID = selectedDungeonUUID
        self.selectedSessionUUID = sessionUUID
        self.editMode = False
        self.setDungeonMaster(False)
        self.loadSelectedDungeon()

    def getUrlToDungeonResource(self, resourceItem):
        if '/' in resourceItem or '\\' in resourceItem:
            if resourceItem.startswith('http'):
                return resourceItem
            return self.makeURL(resourceItem)
        resourceUrl = self.getUrlToDungeonData() + resourceItem
        return resourceUrl

    def getUrlToDungeonData(self):
        directoryForDungeon = self.getDirectoryForCurrentDungeon()
        resourceUrl = self.makeURL(directoryForDungeon) + '/'
        return resourceUrl

    def getDirectoryForCurrentDungeon(self):
        return self.uuidTemplatePathMap[self.selectedDungeon.uuid]

    def getMonstersForCurrentLevel(self):
        if self.selectedDungeon is None:
            return None
        if self.editMode:
            return self.dungeonLevelMonsters.getPogList()
        return self.sessionLevelMonsters.getPogList()

    def getRoomObjectsForCurrentLevel(self):
        if self.selectedDungeon is None:
            return None
        if self.editMode:
            return self.dungeonLevelRoomObjects.getPogList()
        return self.sessionLevelRoomObjects.getPogList()

    def setSessionLevelSize(self, columns, rows):
        dungeonLevel = self.getCurrentDungeonLevelData()
        if not self.isDungeonMaster or dungeonLevel is None:
            return
        if dungeonLevel.columns == columns and dungeonLevel.rows == rows:
            return
        dungeonLevel.columns = columns
        dungeonLevel.rows = rows
        self.saveDungeonData()

    def getPlayersForCurrentSession(self):
        if self.editMode or self.selectedDungeon is None or self.selectedSession is None:
            return None
        currentLevel = self._currentLevelIndex
        playersOnLevel = list()
        for player in self.sessionLevelPlayers.getPogList():
            if player.dungeonLevel == currentLevel:
                playersOnLevel.append(player)
        return playersOnLevel

    def getItemVersion(self, itemToGet):
        return self.dataVersion.getItemVersion(itemToGet)

    def updateVersion(self, needsUpdating):
        self.dataVersion.updateFrom(needsUpdating)

    def getFowToggle(self):
        return self.fowToggle

    def isFowSet(self, columns, rows):
        if self.editMode:
            return False
        sessionLevel = self.getCurrentSessionLevelData()
        if sessionLevel is None:
            return False
        return sessionLevel.isFowSet(columns, rows)

    # noinspection PyMethodMayBeStatic
    def computePlace(self, pog):
        return pog.pogPlace

    def getProperCollection(self, fromWhere, typeOfPogs):
        collection = None
        if fromWhere == PogPlace.COMMON_RESOURCE:
            if typeOfPogs == Constants.POG_TYPE_MONSTER:
                collection = self.getMonsterCollection()
            else:
                collection = self.getRoomCollection()
        elif fromWhere == PogPlace.SESSION_LEVEL:
            if typeOfPogs == Constants.POG_TYPE_MONSTER:
                collection = self.sessionLevelMonsters
            else:
                collection = self.sessionLevelRoomObjects
        elif fromWhere == PogPlace.DUNGEON_LEVEL:
            if typeOfPogs == Constants.POG_TYPE_MONSTER:
                collection = self.dungeonLevelMonsters
            else:
                collection = self.dungeonLevelRoomObjects
        elif fromWhere == PogPlace.SESSION_RESOURCE:
            collection = self.sessionLevelPlayers
        return collection

    def addOrUpdatePogWithoutPlace(self, pog):
        self.addOrUpdatePog(pog, self.computePlace(pog))

    def addOrUpdatePog(self, pog, place):
        collection = self.getProperCollection(place, pog.pogType)
        if collection is None:
            return
        collection.addOrUpdatePogCollection(pog)
        self.addOrUpdatePogToServer(pog, place)
        if pog.isEqual(self.getSelectedPog()):
            self.selectedPog = pog
        self.updateDataVersion()
        ServicesManager.getEventManager().fireEvent(ReasonForAction.PogDataChanged, pog)

    def addOrUpdatePogToServer(self, pog, place):
        request = RequestData(Constants.AddOrUpdatePogRequest)
        request.dungeonUUID = self.selectedDungeonUUID
        if self.selectedSession is None:
            request.sessionUUID = ''
        else:
            request.sessionUUID = self.selectedSessionUUID
        request.currentLevel = self._currentLevelIndex
        request.place = PogPlace.displayName(place)
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = partial(self.handleSuccessfulAddOrUpdatePog, pog)
        dataResponse.onFailure = self.handleFailedAddOrUpdatePog
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, pog).submit()

    # noinspection PyUnusedLocal
    def handleSuccessfulAddOrUpdatePog(self, pog, dataRequestResponse):
        if self.editMode:
            ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionDataSaved, None)
        else:
            ServicesManager.getEventManager().fireEvent(ReasonForAction.PogDataChanged, pog)

    def handleFailedAddOrUpdatePog(self, dataRequestResponse):
        pass

    def deleteSelectedPog(self):
        if not self.isDungeonMaster or self.selectedPog is None:
            return
        place = self.computePlace(self.selectedPog)
        request = RequestData(Constants.DeletePogRequest)
        request.dungeonUUID = self.selectedDungeonUUID
        if self.selectedSession is None:
            request.sessionUUID = ''
        else:
            request.sessionUUID = self.selectedSessionUUID
        request.currentLevel = self._currentLevelIndex
        request.place = PogPlace.displayName(place)
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulDeletePog
        dataResponse.onFailure = self.handleFailedDeletePog
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, self.selectedPog).submit()

    # noinspection PyUnusedLocal
    def handleSuccessfulDeletePog(self, dataRequestResponse):
        self.removeThisPog(self.selectedPog, self.selectedPog.pogPlace)
        ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionDataSaved, None)
        ServicesManager.getEventManager().fireEvent(ReasonForAction.PogDataChanged, None)
        self.setSelectedPog(None)

    def handleFailedDeletePog(self, dataRequestResponse):
        pass

    def removeThisPog(self, pog, place):
        collection = self.getProperCollection(place, pog.pogType)
        if collection is None:
            return
        collection.remove(pog)
        self.updateDataVersion()

    def saveDungeonData(self):
        if self.selectedDungeon is None:
            return
        request = RequestData(Constants.SaveJsonFileRequest)
        request.dungeonUUID = self.selectedDungeonUUID
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulSaveDungeon
        dataResponse.onFailure = self.handleFailedSaveDungeon
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, self.selectedDungeon).submit()

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def handleSuccessfulSaveDungeon(self, dataRequestResponse):
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonDataSaved, None)

    def handleFailedSaveDungeon(self, dataRequestResponse):
        pass

    def getDungeonLevelNames(self):
        if self.selectedDungeon is None:
            return []
        levels = self.selectedDungeon.dungeonLevels
        levelNames = []
        for i in range(len(levels)):
            levelNames.append(levels[i].levelName)
        return levelNames

    def findCharacterPog(self, uuid):
        if self.selectedSession is None:
            return None
        return self.sessionLevelPlayers.findPog(uuid)

    def getFileList(self, directory, onSuccess, onFailure):
        if self.selectedDungeon is None:
            return
        request = RequestData(Constants.FileListerRequest)
        request.folder = directory
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulGetFileList
        dataResponse.onFailure = self.handleFailedGetFileList
        dataResponse.userOnSuccess = onSuccess
        dataResponse.userOnFailure = onFailure
        AsyncJsonData(self.makeURL(Constants.ServicePath), request, dataResponse, None).submit()

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def handleSuccessfulGetFileList(self, dataRequestResponse):
        dataRequestResponse.userOnSuccess(dataRequestResponse.data.text)

    # noinspection PyMethodMayBeStatic
    def handleFailedGetFileList(self, dataRequestResponse):
        dataRequestResponse.userOnFailure()

    def setAssetURL(self, assetURL):
        self.assetURL = assetURL

    def downloadFile(self, url, fileName, dstFolder):
        AsyncDownload(self.makeURL(url + '/' + fileName), partial(self.handleSuccessfulDownload,
                                                                  fileName, dstFolder),
                      self.handleFailedGetDownload).submit()

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def handleSuccessfulDownload(self, filename, dstFolder, dataRequestResponse):
        filePath = dstFolder + '/' + filename
        open(filePath, 'wb').write(dataRequestResponse.data)

    # noinspection PyMethodMayBeStatic
    def handleFailedGetDownload(self, dataRequestResponse):
        pass

    def uploadFile(self, url, folder, filename, onSuccess, onFailure):
        request = RequestData(Constants.FileUploadRequest)
        serverPath = url + '/' + filename
        request.filePath = serverPath
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulUpload
        dataResponse.onFailure = self.handleFailedGetUpload
        dataResponse.userOnSuccess = onSuccess
        dataResponse.userOnFailure = onFailure
        filePath = folder + '/' + filename
        AsyncUpload(self.makeURL(Constants.ServicePath), filePath, request, dataResponse).submit()

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def handleSuccessfulUpload(self, dataRequestResponse):
        dataRequestResponse.userOnSuccess()

    # noinspection PyMethodMayBeStatic
    def handleFailedGetUpload(self, dataRequestResponse):
        dataRequestResponse.userOnFailure()

    def deleteFile(self, url, filename, onSuccess, onFailure):
        request = RequestData(Constants.FileDeleteRequest)
        serverPath = url + '/' + filename
        request.path = serverPath
        dataResponse = DataRequesterResponse()
        dataResponse.onSuccess = self.handleSuccessfulDeleteFile
        dataResponse.onFailure = self.handleFailedDeleteFile
        dataResponse.userOnSuccess = onSuccess
        dataResponse.userOnFailure = onFailure
        AsyncCommand(self.makeURL(Constants.ServicePath), request, dataResponse).submit()

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def handleSuccessfulDeleteFile(self, dataRequestResponse):
        dataRequestResponse.userOnSuccess()

    # noinspection PyMethodMayBeStatic
    def handleFailedDeleteFile(self, dataRequestResponse):
        dataRequestResponse.userOnFailure()

    # noinspection PyMethodMayBeStatic
    def isLegalDungeonName(self, nameToCheck):
        if not nameToCheck or len(nameToCheck) < 4:
            return False
        return True

    # noinspection PyMethodMayBeStatic
    def isValidPictureURL(self, url):
        if not url:
            return False
        i = url.rfind('.')
        if i > 0:
            fileExtension = url[i + 1:]
        else:
            fileExtension = ''
        valid = fileExtension == 'jpeg' or fileExtension == 'jpg' or \
            fileExtension == 'png' or fileExtension == 'webp'
        return valid

    def getNextAvailableLevelNumber(self):
        return len(self.selectedDungeon.dungeonLevels)

    def setIsDungeonGridVisible(self, visible):
        self.selectedDungeon.showGrid = visible

    def setCurrentLevel(self, newIndex):
        self.currentLevelIndex = newIndex
        self.updateWithNewDungeonData()
        self.updateWithSessionData()
        self.computedGridWidth = self.getCurrentDungeonLevelData().gridSize
        ServicesManager.getEventManager().fireEvent(ReasonForAction.DungeonSelectedLevelChanged, None)

    def addNewLevel(self, level):
        self.selectedDungeon.addDungeonLevel(level)

    def removeCurrentLevel(self):
        self.selectedDungeon.remove(self.currentLevelIndex)

    # noinspection PyMethodMayBeStatic
    def isValidNewMonsterName(self, monsterName):
        isValid = not monsterName.startswith('Enter ') and len(monsterName) > 3
        return isValid

    def getSortedList(self, fromWhere, typeOfPogs):
        collection = self.getProperCollection(fromWhere, typeOfPogs)
        if collection is not None:
            return collection.getSortedListOfPogs()
        return None

    def setFow(self, columns, rows, value):
        sessionLevel = self.getCurrentSessionLevelData()
        if self.isDungeonMaster and sessionLevel is not None:
            sessionLevel.updateFOW(columns, rows, value)
            self.fowDirty = True

    def setHideFOW(self, doHideFOW):
        if doHideFOW:
            self.hideFOW()
        else:
            self.showSavedFOW()
        self.updateFogOfWar()

    def hideFOW(self):
        self.savedFOW = self.getCurrentSessionLevelData().fogOfWarData
        fogOfWar = self.getCurrentSessionLevelData().createNewFOWData(self.getCurrentDungeonLevelData().rows)
        self.getCurrentSessionLevelData().fogOfWarData = fogOfWar

    def showSavedFOW(self):
        if self.savedFOW is None:
            return
        self.getCurrentSessionLevelData().fogOfWarData = self.savedFOW
        self.savedFOW = None
