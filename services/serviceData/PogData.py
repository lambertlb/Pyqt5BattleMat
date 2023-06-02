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
        self.notes = ''
        self.dmNotes = ''
        self.pogNumber = 0
        self.pogPlace = 0

    @property
    def image(self):
        return PogData.images[self.pogImageUrl]

    def isEqual(self, toCompare):
        if toCompare is None:
            return False
        return self.uuid == toCompare.uuid

    def togglePlayerFlag(self, flag):
        if self.isPlayerFlagSet(flag):
            self.clearPlayerFlags(flag)
        else:
            self.setPlayerFlags(flag)

    def toggleDmFlag(self, flag):
        if self.isDmFlagSet(flag):
            self.clearDmFlags(flag)
        else:
            self.setDmFlags(flag)

    def isPlayerFlagSet(self, flagToTest):
        return PogData._IsFlagSet(self.playerFlags, flagToTest)

    def clearPlayerFlags(self, flagToClear):
        self.playerFlags = PogData._ClearFlag(self.playerFlags, flagToClear)

    def setPlayerFlags(self, flagToSet):
        self.playerFlags = PogData._SetFlag(self.playerFlags, flagToSet)

    def isDmFlagSet(self, flagToTest):
        return PogData._IsFlagSet(self.dungeonMasterFlags, flagToTest)

    def clearDmFlags(self, flagToClear):
        self.playerFlags = PogData._ClearFlag(self.dungeonMasterFlags, flagToClear)

    def setDmFlags(self, flagToSet):
        self.playerFlags = PogData._SetFlag(self.dungeonMasterFlags, flagToSet)

    @staticmethod
    def _IsFlagSet(flags, flag):
        return flags & flag != 0

    @staticmethod
    def _ClearFlag(flags, flag):
        flags &= ~flag
        return flags

    @staticmethod
    def _SetFlag(flags, flag):
        flags |= flag
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

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def failedLoad(self, onFailure, asynchReturn):
        onFailure()

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
        if hasattr(withUpdates, 'notes'):
            self.notes = withUpdates.notes
        if hasattr(withUpdates, 'dmNotes'):
            self.dmNotes = withUpdates.dmNotes
        self.pogNumber = withUpdates.pogNumber
        if hasattr(withUpdates, 'pogPlace'):
            self.pogPlace = withUpdates.pogPlace

    @staticmethod
    def load(data):
        pog = PogData()
        pog.__dict__ = data
        if not hasattr(pog, 'pogName'):
            pog.pogName = ''
        if not hasattr(pog, 'pogImageUrl'):
            pog.pogImageUrl = ''
        if not hasattr(pog, 'pogType'):
            pog.pogType = None
        if not hasattr(pog, 'pogSize'):
            pog.pogSize = 1
        if not hasattr(pog, 'pogColumn'):
            pog.pogColumn = -1
        if not hasattr(pog, 'pogRow'):
            pog.pogRow = -1
        if not hasattr(pog, 'uuid'):
            pog.uuid = None
        if not hasattr(pog, 'dungeonLevel'):
            pog.dungeonLevel = 0
        if not hasattr(pog, 'playerFlags'):
            pog.playerFlags = 0
        if not hasattr(pog, 'dungeonMasterFlags'):
            pog.dungeonMasterFlags = 0
        if not hasattr(pog, 'notes'):
            pog.notes = 0
        if not hasattr(pog, 'dmNotes'):
            pog.dmNotes = 0
        if not hasattr(pog, 'pogNumber'):
            pog.pogNumber = 0
        if not hasattr(pog, 'pogPlace'):
            pog.pogPlace = 0
        return pog
