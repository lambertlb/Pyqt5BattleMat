import json
import os
import threading

from Server.DungeonData import DungeonData
from services.Constants import Constants


class ServerDataManager:
	lock = threading.RLock()
	uuidTemplatePathMap = {}
	dungeonNameToUUIDMap = {}

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
	def	getPathToDirectory(server, partial):
		path = server.topDirectory + partial
		return path

	@staticmethod
	def getDungeonName(server, folder):
		dungeonData = ServerDataManager.getDungeonData(server, folder)
		dungeonName = dungeonData.dungeonName
		uuid = dungeonData.uuid
		ServerDataManager.addToDungeonCache(server, folder, dungeonName, uuid)
		pass

	@staticmethod
	def getDungeonData(server, folder):
		path = ServerDataManager.getPathToDirectory(server, Constants.Dungeons) + folder
		return ServerDataManager.getDungeonDataFromPath(server, path)

	@staticmethod
	def getDungeonDataFromPath(server, folder):
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
	def addToDungeonCache(server, folder, dungeonName, uuid):
		ServerDataManager.lock.acquire()
		try:
			path = ServerDataManager.getPathToDirectory(server, Constants.Dungeons) + folder
			ServerDataManager.uuidTemplatePathMap[uuid] = path
			ServerDataManager.dungeonNameToUUIDMap[uuid] = dungeonName
		finally:
			ServerDataManager.lock.release()
