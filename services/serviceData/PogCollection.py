"""
GPL 3 file header
"""
import json

from services.AsyncTasks import AsyncJsonData
from services.Constants import Constants
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.DataRequesterResponse import DataRequesterResponse
from services.serviceData.PogList import PogList
from services.serviceData.RequestData import RequestData


class PogCollection:

	def __init__(self, loadEvent, pogPlace):
		self.loadEvent = loadEvent
		self.pogPlace = pogPlace
		self.pogList = None
		self.loadEvent = None
		self.pogPlace = None
		self.pogMap = dict()

	def setPogList(self, pogList):
		self.pogList = pogList
		self.rebuildCollections()

	def rebuildCollections(self):
		self.clear()
		for pogTemplate in self.pogList.pogList:
			pogTemplate.pogPlace = self.pogPlace
			self.addToCollections(pogTemplate)
		if self.loadEvent != ReasonForAction.LastReason:
			ServicesManager.getEventManager().fireEvent(self.loadEvent, None)

	def addToCollections(self, pogToAdd):
		self.pogMap[pogToAdd.uuid] = pogToAdd

	def getPogListVersion(self):
		if self.pogList is None:
			return -1
		return self.pogList.getListVersion()

	def clear(self):
		self.pogMap.clear()

	def loadFromServer(self, urlToService, typeToLoad):
		self.clear()
		request = RequestData(Constants.LoadJsonFileRequest)
		request.fileName = typeToLoad + "pogs.json"
		dataResponse = DataRequesterResponse()
		dataResponse.onSuccess = self.onSuccess
		dataResponse.onFailure = self.onFailure
		AsyncJsonData(urlToService, request, dataResponse, None).submit()

	def onSuccess(self, dataRequestResponse):
		pl = PogList()
		pl.__dict__ = json.loads(dataRequestResponse.data.text)
		self.setPogList(pl.construct())

	def onFailure(self, dataRequestResponse):
		pass

	def updateCollection(self, updateList):
		if self.pogList is None:
			self.setPogList(updateList)
			return

		toRemove = self.pogList.pogList.copy()
		toAdd = []
		for pd in updateList.pogList:
			pd.setPogPlace(self.pogPlace)
			found = self.pogMap.get(pd.uuid)
			if found is not None:
				found.fullUpdate(pd)
				toRemove.remove(found)
				continue
			toAdd.append(pd)
		for pg in toRemove:
			self.remove(pg)
		for pg in toAdd:
			self.addPog(pg)

	def addPog(self, pog):
		pog.pogPlace = self.pogPlace
		self.pogList.addPog(pog)
		self.addToCollections(pog)

	def remove(self, pog):
		if self.findPog(pog.uuid) is None:
			return
		self.pogList.remove(pog)
		self.pogMap.pop(pog.uuid)

	def findPog(self, pogUUID):
		return self.pogMap.get(pogUUID)

	def getPogList(self):
		return self.pogList.pogList

	def addOrUpdatePogCollection(self, pog):
		existing = self.findPog(pog.uuid)
		if existing is None:
			self.addPog(pog)
		else:
			self.pogList.update(pog, existing)
