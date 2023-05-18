"""
GPL 3 file header
"""
import copy
import uuid
from functools import partial

from services.AsyncTasks import AsyncImage
from services.Constants import Constants
from services.ServicesManager import ServicesManager


class PogData:

	images = dict()

	def __init__(self):
		self.pogName = None
		self.pogImageUrl = None
		self.pogType = None
		self.pogSize = 1
		self.pogColumn = -1
		self.pogRow = -1
		self.uuid = None
		self.dungeonLevel = 0
		self.playerFlags = 0
		self.dungeonMasterFlags = 0
		self.notes = None
		self.dmNotes = None
		self.pogNumber = 0
		self.pogPlace = 0

	@property
	def image(self):
		return PogData.images[self.pogImageUrl]

	def isEqual(self, toCompare):
		if toCompare is None:
			return False
		return self.uuid == toCompare.uuid

	def	togglePlayerFlag(self, flag):
		if self.isPlayerFlagSet(flag):
			self.clearPlayerFlags(flag)
		else:
			self.setPlayerFlags(flag)

	def	toggleDmFlag(self, flag):
		if self.isDmFlagSet(flag):
			self.clearDmFlags(flag)
		else:
			self.setDmFlags(flag)

	def isPlayerFlagSet(self, flagToTest):
		return PogData._IsFlagSet(self.playerFlags, flagToTest)

	def clearPlayerFlags(self, flagToClear):
		self.playerFlags =  PogData._ClearFlag(self.playerFlags, flagToClear)

	def setPlayerFlags(self, flagToSet):
		self.playerFlags =  PogData._SetFlag(self.playerFlags, flagToSet)

	def isDmFlagSet(self, flagToTest):
		return PogData._IsFlagSet(self.dungeonMasterFlags, flagToTest)

	def clearDmFlags(self, flagToClear):
		self.playerFlags =  PogData._ClearFlag(self.dungeonMasterFlags, flagToClear)

	def setDmFlags(self, flagToSet):
		self.playerFlags =  PogData._SetFlag(self.dungeonMasterFlags, flagToSet)

	@staticmethod
	def _IsFlagSet(flags, flag):
		return flags & flag.value != 0

	@staticmethod
	def _ClearFlag(flags, flag):
		flags &= ~flag.value
		return flags

	@staticmethod
	def _SetFlag(flags, flag):
		flags |= flag.value
		return flags

	def setPogNumber(self, pogNumber):
		self.pogNumber = pogNumber

	def loadPogImage(self, onSuccess, onFailure):
		imageUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(self.pogImageUrl)
		if self.pogImageUrl in PogData.images:
			onSuccess()
			return
		AsyncImage(imageUrl, partial(self.successfulLoaded, onSuccess), partial(self.failedLoad, onFailure)).submit()

	def successfulLoaded(self, onSuccess, asynchReturn):
		PogData.images[self.pogImageUrl] = asynchReturn.data
		onSuccess()

	def failedLoad(self, onFailure, asynchReturn):
		onFailure()
		pass

	def setPogPosition(self, column, row):
		self.pogColumn = column
		self.pogRow = row

	def isThisAPlayer(self):
		return self.pogType == Constants.POG_TYPE_PLAYER

	def clone(self):
		theClone = copy.deepcopy(self)
		theClone.uuid = str(uuid.uuid4())
		return theClone

	def fullUpdate(self, pogData):
		self.updatePog(pogData)
		self.playerFlags = pogData.playerFlags
		self.dungeonMasterFlags = pogData.dungeonMasterFlags
		self.pogName = pogData.pogName
		self.pogImageUrl = pogData.pogImageUrl
		self.pogType = pogData.pogType
		self.pogSize = pogData.pogSize

	def updatePog(self, withUpdates):
		self.pogColumn = withUpdates.pogColumn
		self.pogRow = withUpdates.pogRow
		self.dungeonLevel = withUpdates.dungeonLevel
		self.notes = withUpdates.notes
		self.dmNotes = withUpdates.dmNotes
		self.pogNumber = withUpdates.pogNumber
		self.pogPlace = withUpdates.pogPlace
