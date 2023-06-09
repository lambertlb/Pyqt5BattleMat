"""
GPL 3 file header
"""
import sys

from services.serviceData.DungeonSessionLevel import DungeonSessionLevel
from services.serviceData.PogList import PogList


class DungeonSessionData:
    """
    data for a session with a dungeon
    """
    def __init__(self, newSessionName='', dungeonUUID='', sessionUUID=''):
        self.version = 1
        self.sessionName = newSessionName
        self.dungeonUUID = dungeonUUID
        self.sessionUUID = sessionUUID
        self.players = PogList()
        self.sessionLevels = []
        self.bitsPerColumn = 32

    def construct(self):
        """
        Take a session that had its data loaded via placing json data into its __dict__
        and construct a new tree with actual constructors
        """
        ds = DungeonSessionData()
        self.cloneData(ds)
        return ds

    def cloneData(self, ds):
        ds.version = self.version
        ds.sessionName = self.sessionName
        ds.dungeonUUID = self.dungeonUUID
        ds.sessionUUID = self.sessionUUID

        players = PogList()
        players.__dict__ = self.players
        ds.players = players.construct()

        for level in self.sessionLevels:
            ld = DungeonSessionLevel()
            ld.__dict__ = level
            ds.sessionLevels.append(ld.construct())

    def setSessionLevels(self, sessionLevels):
        self.sessionLevels = sessionLevels

    def incrementVersion(self):
        self.version += 1
        if self.version == sys.maxsize:
            self.version = 1
