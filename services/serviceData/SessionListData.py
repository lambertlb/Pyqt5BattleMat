"""
GPL 3 file header
"""


class SessionListData:

    def __init__(self, sessionListData=None, dungeonUUID=None):
        self.dungeonUUID = dungeonUUID
        self.sessionNames = []
        self.sessionUUIDs = []
        if sessionListData is None:
            return
        for key, value in sessionListData.items():
            self.sessionNames.append(key)
            self.sessionUUIDs.append(value)

    def getDungeonUUID(self):
        return self.dungeonUUID

    def getSessionNames(self):
        return self.sessionNames

    def getSessionUUIDs(self):
        return self.sessionUUIDs
