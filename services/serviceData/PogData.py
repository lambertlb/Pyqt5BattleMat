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
