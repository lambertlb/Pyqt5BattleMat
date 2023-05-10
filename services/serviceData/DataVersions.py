"""
GPL 3 file header
"""
from services.serviceData.VersionedItem import VersionedItem


class DataVersions:

	def __init__(self):
		self.dataVersion = [0 for _ in range(VersionedItem.LAST_VERSIONED_ITEM.value)]

	def initialize(self):
		for i in range(VersionedItem.LAST_VERSIONED_ITEM.value):
			self.dataVersion[i] = -1

	def setItemVersion(self, item, version):
		self.dataVersion[item.value] = version
