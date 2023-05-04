"""
GPL 3 file header
"""
from services.ReasonForAction import ReasonForAction
from services.serviceData.PogCollection import PogCollection
from services.serviceData.PogPlace import PogPlace


class PogManager:

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
		pass

	def loadRoomObjectPogs(self):
		pass
