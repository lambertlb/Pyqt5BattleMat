import json
import os
import re
import shutil
import threading
import uuid

from Server.DungeonData import DungeonData
from Server.SessionInformation import SessionInformation
from services.Constants import Constants
from services.serviceData.DungeonSessionData import DungeonSessionData


class ServerDataManager:
	lock = threading.RLock()
	uuidTemplatePathMap = {}
	dungeonNameToUUIDMap = {}
	sessionCache = {}

	@staticmethod
	def getDungeonListData(server):
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
		path = server.topDirectory + partial
		return path

	@staticmethod
	def getDungeonName(server, folder):
		dungeonData = ServerDataManager.getDungeonData(server, folder)
		dungeonName = dungeonData.dungeonName
		dungeonUUID = dungeonData.uuid
		ServerDataManager.addToDungeonCache(folder, dungeonName, dungeonUUID)
		pass

	@staticmethod
	def getDungeonData(server, folder):
		path = ServerDataManager.getPathToDirectory(server, Constants.Dungeons) + folder
		return ServerDataManager.getDungeonDataFromPath(path)

	@staticmethod
	def getDungeonDataFromPath(folder):
		filePath = folder + '/dungeonData.json'
		jsonData = ServerDataManager.readJsonFile(filePath)
		dungeonData = DungeonData()
		dungeonData.__dict__ = json.loads(jsonData)
		return dungeonData

	@staticmethod
	def readJsonFile(path):
		with open(path) as f:
			return f.read()

	@staticmethod
	def addToDungeonCache(folder, dungeonName, dungeonUUID):
		ServerDataManager.lock.acquire()
		try:
			path = Constants.Dungeons + folder
			ServerDataManager.uuidTemplatePathMap[dungeonUUID] = path
			ServerDataManager.dungeonNameToUUIDMap[dungeonUUID] = dungeonName
		finally:
			ServerDataManager.lock.release()

	@staticmethod
	def getSessionListData(server, dungeonUUID):
		sessionListData = {}
		ServerDataManager.lock.acquire()
		try:
			print(ServerDataManager.uuidTemplatePathMap)
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
		sessionInformation = ServerDataManager.loadSessionInformation(sessionsPath + possibleSession)
		sessionData: DungeonSessionData = sessionInformation.sessionData
		sessionListData[sessionData.sessionName] = sessionData.sessionUUID

	@staticmethod
	def loadSessionInformation(possibleSession):
		possibleSessionInformation = SessionInformation()
		path = possibleSession + "/sessionData.json"
		jsonData = ServerDataManager.readJsonFile(path)
		possibleSessionInformation.load(path, possibleSession, jsonData)
		return possibleSessionInformation

	@staticmethod
	def getFileAsString(server, fileName):
		ServerDataManager.lock.acquire()
		try:
			filePath = ServerDataManager.getPathToDirectory(server, Constants.DungeonData) + fileName
			return ServerDataManager.readJsonFile(filePath)
		finally:
			ServerDataManager.lock.release()

	@staticmethod
	def getDungeonDataAsString(server, dungeonUUID):
		ServerDataManager.lock.acquire()
		try:
			if dungeonUUID not in ServerDataManager.uuidTemplatePathMap:
				return None
			dungeonPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
			filePath = ServerDataManager.getPathToDirectory(server, dungeonPath + './dungeonData.json')
			return ServerDataManager.readJsonFile(filePath)
		finally:
			ServerDataManager.lock.release()

	@staticmethod
	def getFilenamesInPath(server, folder):
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
		ServerDataManager.lock.acquire()
		try:
			dstDirectory = re.sub("[^a-zA-Z0-9]", "_", newDungeonName)
			dungeonPath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID)
			dungeonFullPath = ServerDataManager.getPathToDirectory(server, dungeonPath)
			copyPath = ServerDataManager.getPathToDirectory(server, Constants.Dungeons + dstDirectory)
			shutil.copytree(dungeonFullPath, copyPath)
			ServerDataManager.deleteAnyOldSessions(copyPath)
			dungeonData = ServerDataManager.getDungeonData(server, dstDirectory)
			dungeonData.dungeonName = newDungeonName
			dungeonData.uuid = str(uuid.uuid4())
			ServerDataManager.addToDungeonCache(dstDirectory, newDungeonName, dungeonData.uuid)
			jsonData = json.dumps(dungeonData, default=vars)
			ServerDataManager.saveDungeonData(server, jsonData, dungeonData.uuid)
			pass
		finally:
			ServerDataManager.lock.release()

	@staticmethod
	def deleteAnyOldSessions(destinationDirectory):
		sessionsPath = destinationDirectory + "/" + Constants.SessionFolder
		ServerDataManager.lock.acquire()
		try:
			if os.path.exists(sessionsPath):
				shutil.rmtree(sessionsPath)
		finally:
			ServerDataManager.lock.release()

	@staticmethod
	def saveDungeonData(server, jsonData, dungeonUUID):
		filePath = ServerDataManager.uuidTemplatePathMap.get(dungeonUUID) + "/dungeonData.json"
		fullPath = ServerDataManager.getPathToDirectory(server, filePath)
		ServerDataManager.saveJsonFile(jsonData, fullPath)

	@staticmethod
	def saveJsonFile(jsonData, fullPath):
		with open(fullPath, "wb") as text_file:
			text_file.write(jsonData)

	@staticmethod
	def deleteDungeon(server, dungeonUUID):
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
		ServerDataManager.uuidTemplatePathMap.clear()
		ServerDataManager.dungeonNameToUUIDMap.clear()
		ServerDataManager.getDungeonListData(server)

	@staticmethod
	def saveSessionData(server, jsonData, dungeonUUID, sessionUUID):
		if not dungeonUUID:
			return
		ServerDataManager.lock.acquire()
		try:
			sessionInformation = ServerDataManager.getSessionInformation(server, dungeonUUID, sessionUUID)
			if sessionInformation:
				sessionInformation.fromJson(jsonData)
				sessionJson = json.dumps(sessionInformation.sessionData, default=vars)
				ServerDataManager.saveJsonFile(sessionJson, sessionInformation.sessionPath);
		finally:
			ServerDataManager.lock.release()

	@staticmethod
	def getSessionInformation(server, dungeonUUID, sessionUUID):
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
