"""
GPL 3 file header
"""
import json
import traceback

from services.Constants import Constants
from services.serviceData.DungeonSessionData import DungeonSessionData
from services.serviceData.DungeonSessionLevel import DungeonSessionLevel


class SessionInformation:
    """
    This class manages a single session with a client.
    """
    def __init__(self, sessionData=None, sessionPath=None, sessionDirectory=None):
        self.dirty = False
        self.sessionDirectory = sessionDirectory
        self.sessionPath = sessionPath
        self.sessionData: DungeonSessionData = sessionData

    def load(self, sessionPath, sessionDirectory, jsonData):
        """
        Load in session data
        """
        self.sessionPath = sessionPath
        self.sessionDirectory = sessionDirectory
        self.fromJson(jsonData)

    def fromJson(self, jsonData):
        """
        return session data from a json file
        """
        self.sessionData = None
        if jsonData is not None and jsonData:
            sessionData = DungeonSessionData()
            sessionData.__dict__ = json.loads(jsonData)
            self.sessionData = sessionData.construct()

    def toJson(self):
        return json.dumps(self.sessionData, default=vars)

    def getUUID(self):
        if self.sessionData:
            return self.sessionData.sessionUUID
        return None

    def save(self):
        """
        Save session data to json file
        """
        sessionJson = json.dumps(self.sessionData, default=vars)
        with open(self.sessionPath, "wb") as text_file:
            text_file.write(sessionJson.encode())
        self.dirty = False

    def getSessionLevel(self, currentLevel):
        """
        get data for this level in a session
        """
        if currentLevel < 0 or currentLevel >= len(self.sessionData.sessionLevels):
            return None
        return self.sessionData.sessionLevels[currentLevel]

    def updateFOW(self, fowData, currentLevel):
        """
        Up data fog of war in this session level
        """
        sessionLevel = self.getSessionLevel(currentLevel)
        if not sessionLevel:
            return None
        sessionLevel.setFogOfWar(fowData)
        self.sessionData.incrementVersion()
        self.dirty = True

    def addOrUpdatePog(self, pogData, currentLevel):
        """
        Add or update this pog in a session level
        """
        sessionLevel: DungeonSessionLevel = self.getSessionLevel(currentLevel)
        if pogData.pogType == Constants.POG_TYPE_MONSTER:
            sessionLevel.monsters.addOrUpdate(pogData)
        elif pogData.pogType == Constants.POG_TYPE_ROOMOBJECT:
            sessionLevel.roomObjects.addOrUpdate(pogData)
        elif pogData.pogType == Constants.POG_TYPE_PLAYER:
            self.sessionData.players.addOrUpdate(pogData)
        self.sessionData.incrementVersion()
        self.dirty = True

    def saveIfDirty(self):
        if self.dirty:
            try:
                self.save()
            except (Exception,):
                traceback.print_exc()
        self.dirty = False

    def removePog(self, pogData, level):
        """
        remove this pog from a session level
        """
        sessionLevel: DungeonSessionLevel = self.getSessionLevel(level)
        if pogData.pogType == Constants.POG_TYPE_MONSTER:
            sessionLevel.monsters.remove(pogData)
        elif pogData.pogType == Constants.POG_TYPE_ROOMOBJECT:
            sessionLevel.roomObjects.remove(pogData)
        elif pogData.pogType == Constants.POG_TYPE_PLAYER:
            self.sessionData.players.remove(pogData)
        self.sessionData.incrementVersion()
        self.dirty = True
