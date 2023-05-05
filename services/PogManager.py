"""
GPL 3 file header
"""
from services.Constants import Constants
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.PogCollection import PogCollection
from services.serviceData.PogPlace import PogPlace


class PogManager:

	baseURL = None
	monsterCollection = PogCollection(ReasonForAction.MonsterPogsLoaded, PogPlace.COMMON_RESOURCE)
	roomCollection = PogCollection(ReasonForAction.RoomObjectPogsLoaded, PogPlace.COMMON_RESOURCE)

	def getMonsterCollection(self):
		return self.monsterCollection

	def getRoomCollection(self):
		return self.roomCollection

	def setSelectedPog(self, pogData):
		pass

	def setPogBeingDragged(self, pogData, fromRibbonBar):
		pass

	def loadMonsterPogs(self):
		self.monsterCollection.loadFromServer(self.makeURL(Constants.ServicePath), Constants.Monsters)
		pass

	def loadRoomObjectPogs(self):
		self.monsterCollection.loadFromServer(self.makeURL(Constants.ServicePath), Constants.RoomObjects)
		pass

	def makeURL(self, additions):
		if self.baseURL is None:
			self.baseURL = ServicesManager.getConfigManager().getValue(Constants.Login_Url, 'URL')
		return self.baseURL + additions

