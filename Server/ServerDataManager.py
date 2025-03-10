"""
GPL 3 file header
"""
import json
import os
import re
import shutil
import threading
import uuid

from Server.SessionInformation import SessionInformation
from services.Constants import Constants
from services.serviceData.DungeonData import DungeonData
from services.serviceData.DungeonLevel import DungeonLevel
from services.serviceData.DungeonSessionData import DungeonSessionData
from services.serviceData.DungeonSessionLevel import DungeonSessionLevel
from services.serviceData.PogData import PogData
from services.serviceData.PogList import PogList
from services.serviceData.PogPlace import PogPlace


class ServerDataManager:
    """
    This class manages all requests from clients.
    It maintains a couple of caches to help speed up some data access
    """
    lock = threading.RLock()    # lock used to limit access to one client at a time
    uuidTemplatePathMap = {}    # cache of UUIDs to dungeon paths
    dungeonNameToUUIDMap = {}   # cache of Dungeon Names to UUIDs
    sessionCache = {}           # cache of current sessions that are running

    @staticmethod
    def getDungeonListData(server):
        """
        Make sure caches of dungeon information are up to-date
        """
        ServerDataManager.lock.acquire()
        if len(ServerDataManager.uuidTemplatePathMap) != 0:
            ServerDataManager.lock.release()
            return
        try:
            path = ServerDataManager.getPathToDirectory(server, Constants.Dungeons)
            files = os.listdir(path)
            for file in files:
                fullPath = path + file
                if os.path.isdir(fullPath):
                    ServerDataManager.getDungeonName(server, file)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getPathToDirectory(server, partial):
        """
        return full path to this partial path
        """
        path = server.topDirectory + partial
        return path

    @staticmethod
    def getDungeonName(server, folder):
        """
        get the name of the dungeon in this folder
        """
        dungeonData = ServerDataManager.getDungeonData(server, folder)
        if dungeonData is None:
            return
        dungeonName = dungeonData.dungeonName
        dungeonUUID = dungeonData.uuid
        ServerDataManager.addToDungeonCache(folder, dungeonName, dungeonUUID)
        pass

    @staticmethod
    def getDungeonData(server, folder):
        """
        Load in the data for the dungeon in this folder
        """
        path = ServerDataManager.getPathToDirectory(server, Constants.Dungeons) + folder
        return ServerDataManager.getDungeonDataFromPath(path)

    @staticmethod
    def getDungeonDataFromPath(folder):
        """
        Load in json data for this dungeon
        """
        filePath = folder + '/dungeonData.json'
        if not os.path.exists(filePath):
            return None
        jsonData = ServerDataManager.readJsonFile(filePath)
        dungeonData = DungeonData()
        dungeonData.__dict__ = json.loads(jsonData)
        return dungeonData.construct()

    @staticmethod
    def readJsonFile(path):
        with open(path) as f:
            return f.read()

    @staticmethod
    def addToDungeonCache(folder, dungeonName, dungeonUUID):
        """
        add this dungeon to cache
        """
        ServerDataManager.lock.acquire()
        try:
            path = Constants.Dungeons + folder
            ServerDataManager.uuidTemplatePathMap[dungeonUUID] = path
            ServerDataManager.dungeonNameToUUIDMap[dungeonUUID] = dungeonName
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getSessionListData(server, dungeonUUID):
        """
        get the list of session names for this dungeon
        """
        sessionListData = {}
        ServerDataManager.lock.acquire()
        try:
            pt = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
            sessionsPath = pt + Constants.SessionFolder
            directoryPath = ServerDataManager.getPathToDirectory(server, sessionsPath)
            ServerDataManager.makeSureDirectoryExists(directoryPath)
            files = os.listdir(directoryPath)
            for file in files:
                fullPath = directoryPath + '/' + file
                if os.path.isdir(fullPath):
                    ServerDataManager.putSessionNameInCache(directoryPath, file, sessionListData)
        finally:
            ServerDataManager.lock.release()
        return sessionListData

    @staticmethod
    def makeSureDirectoryExists(directoryPath):
        if not os.path.exists(directoryPath):
            os.mkdir(directoryPath)

    @staticmethod
    def putSessionNameInCache(sessionsPath, possibleSession, sessionListData):
        """
        Load in session data and add its name to cache
        """
        sessionInformation = ServerDataManager.loadSessionInformation(sessionsPath + possibleSession)
        sessionData: DungeonSessionData = sessionInformation.sessionData
        sessionListData[sessionData.sessionName] = sessionData.sessionUUID

    @staticmethod
    def loadSessionInformation(possibleSession):
        """
        Load in session data
        """
        possibleSessionInformation = SessionInformation()
        path = possibleSession + "/sessionData.json"
        jsonData = ServerDataManager.readJsonFile(path)
        possibleSessionInformation.load(path, possibleSession, jsonData)
        return possibleSessionInformation

    @staticmethod
    def getFileAsString(server, fileName):
        """
        load in the data for this file
        """
        ServerDataManager.lock.acquire()
        try:
            filePath = ServerDataManager.getPathToDirectory(server, Constants.DungeonData) + fileName
            return ServerDataManager.readJsonFile(filePath)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getDungeonDataAsString(server, dungeonUUID):
        """
        Load in the data for this dungeon
        """
        ServerDataManager.lock.acquire()
        try:
            if dungeonUUID not in ServerDataManager.uuidTemplatePathMap:
                return None
            dungeonPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
            filePath = ServerDataManager.getPathToDirectory(server, dungeonPath + '/dungeonData.json')
            return ServerDataManager.readJsonFile(filePath)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getFilenamesInPath(server, folder):
        """
        get all the filenames in this folder
        """
        foundFiles = []
        directoryPath = ServerDataManager.getPathToDirectory(server, folder)
        files = os.listdir(directoryPath)
        for file in files:
            fullPath = directoryPath + '/' + file
            if not os.path.isdir(fullPath):
                foundFiles.append(file)
        return foundFiles

    @staticmethod
    def copyDungeon(server, dungeonUUID, newDungeonName):
        """
        make a copy of the template dungeon
        """
        ServerDataManager.lock.acquire()
        try:
            dstDirectory = re.sub("[^a-zA-Z0-9]", "_", newDungeonName)
            dungeonPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
            dungeonFullPath = ServerDataManager.getPathToDirectory(server, dungeonPath)
            copyPath = ServerDataManager.getPathToDirectory(server, Constants.Dungeons + dstDirectory)
            shutil.copytree(dungeonFullPath, copyPath)  # copy everything ins the source folder
            ServerDataManager.deleteAnyOldSessions(copyPath)
            dungeonData = ServerDataManager.getDungeonData(server, dstDirectory)
            dungeonData.dungeonName = newDungeonName
            dungeonData.uuid = str(uuid.uuid4())
            ServerDataManager.addToDungeonCache(dstDirectory, newDungeonName, dungeonData.uuid)
            jsonData = json.dumps(dungeonData, default=vars)
            ServerDataManager.saveDungeonData(server, jsonData, dungeonData.uuid)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def deleteAnyOldSessions(destinationDirectory):
        """
        remove all sessions in this directory
        """
        sessionsPath = destinationDirectory + "/" + Constants.SessionFolder
        ServerDataManager.lock.acquire()
        try:
            if os.path.exists(sessionsPath):
                shutil.rmtree(sessionsPath)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def saveDungeonData(server, jsonData, dungeonUUID):
        """
        Save the dungeon data as starting session data
        This is so one session does not change another sessions data
        Each session gets it own copy of the original dungeon's data.
        """
        filePath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID) + "/dungeonData.json"
        fullPath = ServerDataManager.getPathToDirectory(server, filePath)
        ServerDataManager.saveJsonFile(jsonData, fullPath)

    @staticmethod
    def saveJsonFile(jsonData, fullPath):
        with open(fullPath, "wb") as text_file:
            if type(jsonData) is str:
                text_file.write(jsonData.encode())
            else:
                text_file.write(jsonData)

    @staticmethod
    def deleteDungeon(server, dungeonUUID):
        """
        Delete a dungeon
        """
        ServerDataManager.lock.acquire()
        try:
            dungeonPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
            dungeonFullPath = ServerDataManager.getPathToDirectory(server, dungeonPath)
            if os.path.exists(dungeonFullPath):
                shutil.rmtree(dungeonFullPath)
            ServerDataManager.rebuildDungeonList(server)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def rebuildDungeonList(server):
        """
        Clear caches and reload all dungeon data
        """
        ServerDataManager.uuidTemplatePathMap.clear()
        ServerDataManager.dungeonNameToUUIDMap.clear()
        ServerDataManager.getDungeonListData(server)

    @staticmethod
    def saveSessionData(server, jsonData, dungeonUUID, sessionUUID):
        """
        save this sessions data
        """
        if not dungeonUUID:
            return
        ServerDataManager.lock.acquire()
        try:
            sessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID, sessionUUID)
            if sessionInformation:
                sessionInformation.fromJson(jsonData)
                sessionJson = json.dumps(sessionInformation.sessionData, default=vars)
                ServerDataManager.saveJsonFile(sessionJson, sessionInformation.sessionPath)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getSessionInformation(server, dungeonUUID, sessionUUID):
        """
        find and return the session with this UUID
        """
        ServerDataManager.lock.acquire()
        try:
            sessionInformation = ServerDataManager.getSessionFromCache(sessionUUID)
            if sessionInformation:
                return sessionInformation
            sessionsPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID) + Constants.SessionFolder
            directoryPath = ServerDataManager.getPathToDirectory(server, sessionsPath)
            files = os.listdir(directoryPath)
            for file in files:
                fullPath = directoryPath + '/' + file
                if os.path.isdir(fullPath):
                    possibleSessionInformation: SessionInformation = ServerDataManager.loadSessionInformation(fullPath)
                    if possibleSessionInformation.sessionData.sessionUUID == sessionUUID:
                        ServerDataManager.addSessionToCache(possibleSessionInformation)
                        return possibleSessionInformation
        finally:
            ServerDataManager.lock.release()
        return None

    @staticmethod
    def getSessionFromCache(sessionUUID):
        ServerDataManager.lock.acquire()
        try:
            return ServerDataManager.sessionCache.get(sessionUUID)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def addSessionToCache(session):
        ServerDataManager.lock.acquire()
        try:
            if session.getUUID() in ServerDataManager.sessionCache:
                ServerDataManager.sessionCache.pop(session.getUUID())
            ServerDataManager.sessionCache[session.getUUID()] = session
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def deleteFile(server, filePath):
        ServerDataManager.lock.acquire()
        try:
            path = ServerDataManager.getPathToDirectory(server, filePath)
            os.remove(path)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def createSession(server, dungeonUUID, newSessionName):
        """
        Create a new session in the dungeon with this UUID
        """
        ServerDataManager.lock.acquire()
        try:
            dungeonPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
            templateDirectory = ServerDataManager.getPathToDirectory(server, dungeonPath)
            newSessionNameSub = re.sub("[^a-zA-Z0-9]", "_", newSessionName)
            sessionDirectory = templateDirectory + Constants.SessionFolder + newSessionNameSub
            ServerDataManager.makeSureDirectoryExists(sessionDirectory)
            dungeonData = ServerDataManager.getDungeonDataFromUUID(server, dungeonUUID)
            sessionData = ServerDataManager.createSessionData(server, dungeonUUID, newSessionName, dungeonData)
            filePath = sessionDirectory + '/' + 'sessionData.json'
            sessionInformation = SessionInformation(sessionData, filePath, sessionDirectory)
            sessionInformation.save()
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getDungeonDataFromUUID(server, dungeonUUID):
        directoryPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
        return ServerDataManager.getDungeonDataFromPath(ServerDataManager.getPathToDirectory(server, directoryPath))

    # noinspection PyUnusedLocal
    @staticmethod
    def createSessionData(server, dungeonUUID, newSessionName, dungeonData):
        """
        create new session data by copying this dungeon data
        """
        uuidString = str(uuid.uuid4())
        newSessionData = DungeonSessionData(newSessionName, dungeonUUID, uuidString)
        sessionLevels = []
        newSessionData.setSessionLevels(sessionLevels)
        for i in range(len(dungeonData.dungeonLevels)):  # create session level by copying dungeon level
            sessionLevel = DungeonSessionLevel(dungeonData.dungeonLevels[i])
            sessionLevels.append(sessionLevel)
        return newSessionData

    @staticmethod
    def deleteSession(server, dungeonUUID, sessionUUID):
        ServerDataManager.lock.acquire()
        try:
            sessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID, sessionUUID)
            if sessionInformation:
                if sessionUUID in ServerDataManager.sessionCache:
                    ServerDataManager.sessionCache.pop(sessionUUID)
                if os.path.exists(sessionInformation.sessionDirectory):
                    shutil.rmtree(sessionInformation.sessionDirectory)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def getSessionDataAsString(server, dungeonUUID, sessionUUID, version):
        ServerDataManager.lock.acquire()
        try:
            if version != -1:   # if version is -1 the do a full reload else use cached one if it exists
                sessionInformation = ServerDataManager.getSessionFromCache(sessionUUID)
            else:
                sessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID, sessionUUID)
            # only return full json data if version has changed.
            # this is so client can periodically do a check and only incur overhead
            # if the data actually changed
            if sessionInformation and sessionInformation.sessionData.version != version:
                return sessionInformation.toJson()
            return ''
        finally:
            ServerDataManager.lock.release()

    # noinspection PyUnusedLocal
    @staticmethod
    def updateFOW(server, sessionUUID, currentLevel, fogOfWar):
        """
        Update fog of war for this level in a session
        """
        ServerDataManager.lock.acquire()
        try:
            sessionInformation = ServerDataManager.getSessionFromCache(sessionUUID)
            if sessionInformation:
                sessionInformation.updateFOW(fogOfWar, currentLevel)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def savePog(server, dungeonUUID, sessionUUID, level, place, pogJsonData):
        """
        save this pog data to the proper place
        """
        ServerDataManager.lock.acquire()
        try:
            pogData = PogData.load(json.loads(pogJsonData.decode()))
            if place == PogPlace.COMMON_RESOURCE:
                ServerDataManager.addOrUpdatePogToCommonResource(server, pogData)
            elif place == PogPlace.DUNGEON_LEVEL:
                ServerDataManager.addOrUpdatePogToDungeonInstance(server, pogData, dungeonUUID, level)
            elif place == PogPlace.SESSION_RESOURCE:
                ServerDataManager.addOrUpdatePogToSessionResource(server, pogData, dungeonUUID, sessionUUID, level)
            elif place == PogPlace.SESSION_LEVEL:
                ServerDataManager.addOrUpdatePogToSessionInstance(server, pogData, dungeonUUID, sessionUUID, level)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def addOrUpdatePogToCommonResource(server, pogData):
        if pogData.pogType == Constants.POG_TYPE_MONSTER:
            ServerDataManager.addOrUpdatePogToCommon(server, pogData, Constants.Monsters)
        elif pogData.pogType == Constants.POG_TYPE_ROOMOBJECT:
            ServerDataManager.addOrUpdatePogToCommon(server, pogData, Constants.RoomObjects)

    @staticmethod
    def addOrUpdatePogToCommon(server, pogData, folder):
        resourcePath = Constants.DungeonData + folder + "pogs.json"
        filePath = ServerDataManager.getPathToDirectory(server, resourcePath)
        fileData = ServerDataManager.readJsonFile(filePath)
        pl = PogList()
        pl.__dict__ = json.loads(fileData)
        pogList = pl.construct()
        pogList.addOrUpdate(pogData)
        updatedData = json.dumps(pogList, default=vars)
        ServerDataManager.saveJsonFile(updatedData, filePath)

    @staticmethod
    def addOrUpdatePogToDungeonInstance(server, pogData, dungeonUUID, level):
        dungeonData: DungeonData = ServerDataManager.getDungeonDataFromUUID(server, dungeonUUID)
        dungeonLevel: DungeonLevel = dungeonData.dungeonLevels[level]
        if pogData.pogType == Constants.POG_TYPE_MONSTER:
            dungeonLevel.monsters.addOrUpdate(pogData)
        elif pogData.pogType == Constants.POG_TYPE_ROOMOBJECT:
            dungeonLevel.roomObjects.addOrUpdate(pogData)
        jsonData = json.dumps(dungeonData, default=vars)
        ServerDataManager.saveDungeonData(server, jsonData, dungeonUUID)

    @staticmethod
    def addOrUpdatePogToSessionResource(server, pogData, dungeonUUID, sessionUUID, level):
        sessionInformation: SessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID,
                                                                                         sessionUUID)
        if pogData.pogType == Constants.POG_TYPE_PLAYER:
            sessionInformation.addOrUpdatePog(pogData, level)

    @staticmethod
    def addOrUpdatePogToSessionInstance(server, pogData, dungeonUUID, sessionUUID, level):
        sessionInformation: SessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID,
                                                                                         sessionUUID)
        sessionInformation.addOrUpdatePog(pogData, level)

    @staticmethod
    def periodicTimer():
        """
        This run periodically
        It should handle all checks that need to be done occasionally
        """
        ServerDataManager.lock.acquire()
        try:
            ServerDataManager.checkIfTimeToSaveSessionData()
            ServerDataManager.checkIfNeedToPurgeCachedData()
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def checkIfTimeToSaveSessionData():
        """
        see if session data is dirty and needs to be saved to disk
        """
        for sessionInformation in ServerDataManager.sessionCache.values():
            sessionInformation.saveIfDirty()

    @staticmethod
    def checkIfNeedToPurgeCachedData():
        pass  # add code to purge cache after stale time

    @staticmethod
    def deletePog(server, dungeonUUID, sessionUUID, level, place, pogJsonData):
        """
        delete Pog from proper place
        """
        ServerDataManager.lock.acquire()
        try:
            pogData = PogData.load(json.loads(pogJsonData.decode()))
            if place == PogPlace.COMMON_RESOURCE:
                ServerDataManager.deletePogInCommonResource(server, pogData)
            elif place == PogPlace.DUNGEON_LEVEL:
                ServerDataManager.deletePogInDungeonInstance(server, pogData, dungeonUUID, level)
            elif place == PogPlace.SESSION_RESOURCE:
                ServerDataManager.deletePogInSessionResource(server, pogData, dungeonUUID, sessionUUID, level)
            elif place == PogPlace.SESSION_LEVEL:
                ServerDataManager.deletePogInSessionInstance(server, pogData, dungeonUUID, sessionUUID, level)
        finally:
            ServerDataManager.lock.release()

    @staticmethod
    def deletePogInCommonResource(server, pogData):
        if pogData.pogType == Constants.POG_TYPE_MONSTER:
            ServerDataManager.deletePogInCommon(server, pogData, Constants.Monsters)
        elif pogData.pogType == Constants.POG_TYPE_ROOMOBJECT:
            ServerDataManager.deletePogInCommon(server, pogData, Constants.RoomObjects)

    @staticmethod
    def deletePogInCommon(server, pogData, folder):
        resourcePath = Constants.DungeonData + folder + "pogs.json"
        filePath = ServerDataManager.getPathToDirectory(server, resourcePath)
        fileData = ServerDataManager.readJsonFile(filePath)
        pl = PogList()
        pl.__dict__ = json.loads(fileData)
        pogList = pl.construct()
        pogList.remove(pogData)
        updatedData = json.dumps(pogList, default=vars)
        ServerDataManager.saveJsonFile(updatedData, filePath)

    @staticmethod
    def deletePogInDungeonInstance(server, pogData, dungeonUUID, level):
        dungeonData: DungeonData = ServerDataManager.getDungeonDataFromUUID(server, dungeonUUID)
        dungeonLevel: DungeonLevel = dungeonData.dungeonLevels[level]
        if pogData.pogType == Constants.POG_TYPE_MONSTER:
            dungeonLevel.monsters.remove(pogData)
        elif pogData.pogType == Constants.POG_TYPE_ROOMOBJECT:
            dungeonLevel.roomObjects.remove(pogData)
        jsonData = json.dumps(dungeonData, default=vars)
        ServerDataManager.saveDungeonData(server, jsonData, dungeonUUID)

    @staticmethod
    def deletePogInSessionResource(server, pogData, dungeonUUID, sessionUUID, level):
        sessionInformation: SessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID,
                                                                                         sessionUUID)
        if pogData.pogType == Constants.POG_TYPE_PLAYER:
            sessionInformation.removePog(pogData, level)

    @staticmethod
    def deletePogInSessionInstance(server, pogData, dungeonUUID, sessionUUID, level):
        sessionInformation: SessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID,
                                                                                         sessionUUID)
        sessionInformation.removePog(pogData, level)
