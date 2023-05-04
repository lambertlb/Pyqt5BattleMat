"""
GPL 3 file header
"""


class PogCollection:
	pogList = None
	loadEvent = None
	pogPlace = None

	def __init__(self, loadEvent, pogPlace):
		self.loadEvent = loadEvent
		self.pogPlace = pogPlace

	def setPogList(self, pogList):
		self.pogList = pogList
		self.rebuildCollections()

	def rebuildCollections(self):
		pass

	def getPogListVersion(self):
		if self.pogList is None:
			return -1
		return self.pogList.getListVersion()
