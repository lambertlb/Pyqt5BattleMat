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
	pogList = None
	loadEvent = None
	pogPlace = None
	pogMap = dict()

	def __init__(self, loadEvent, pogPlace):
		self.loadEvent = loadEvent
		self.pogPlace = pogPlace

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
