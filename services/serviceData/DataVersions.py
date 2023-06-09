"""
GPL 3 file header
"""
from services.serviceData.VersionedItem import VersionedItem


class DataVersions:
    """
    class for managing data versions.
    This is used to help the UI know which data has actually changed,
    so it can filter out and just update changed data.
    """
    def __init__(self):
        self.dataVersion = [0 for _ in range(VersionedItem.LAST_VERSIONED_ITEM.value)]

    def initialize(self):
        for i in range(VersionedItem.LAST_VERSIONED_ITEM.value):
            self.dataVersion[i] = -1

    def setItemVersion(self, item, version):
        self.dataVersion[item.value] = version

    def getItemVersion(self, item):
        return self.dataVersion[item.value]

    def updateFrom(self, needsUpdating):
        for i in range(len(self.dataVersion)):
            needsUpdating.dataVersion[i] = self.dataVersion[i]
