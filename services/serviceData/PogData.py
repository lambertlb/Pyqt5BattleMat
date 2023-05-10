"""
GPL 3 file header
"""


class PogData:

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

	def isEqual(self, toCompare):
		if toCompare is None:
			return False
		return self.uuid == toCompare.uuid
