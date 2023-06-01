"""
GPL 3 file header
"""
import copy
import uuid

from services.serviceData.PogData import PogData


class PogList:

	def __init__(self):
		self.pogList = []
		self.listVersion = 0

	def construct(self):
		dl = PogList()
		self.cloneData(dl)
		return dl

	def clone(self):
		pl = PogList()
		pl.listVersion = self.listVersion
		for pog in self.pogList:
			np = copy.copy(pog)
			np.uuid = str(uuid.uuid4())
			pl.pogList.append(np)
		return pl

	def cloneData(self, dl):
		if 'listVersion' in locals():
			dl.listVersion = self.listVersion
		else:
			dl.listVersion = 0
		if self.pogList is None:
			return
		for pog in self.pogList:
			pd = PogData.load(pog)
			pd1 = PogData()
			pd1.fullUpdate(pd)
			pd1.uuid = pd.uuid
			dl.pogList.append(pd1)

	def getListVersion(self):
		return self.listVersion

	def remove(self, pog):
		oldList = self.pogList
		self.pogList = []
		for pogInList in oldList:
			if not pogInList.isEqual(pog):
				self.pogList.append(pogInList)
		self.listVersion = self.listVersion + 1

	def addPog(self, pogToAdd):
		self.pogList.append(pogToAdd)
		self.listVersion += 1

	def update(self, src, dst):
		dst.fullUpdate(src)
		self.listVersion = self.listVersion + 1

	def addOrUpdate(self, pog):
		for pogInList in self.pogList:
			if pogInList.isEqual(pog):
				pogInList.fullUpdate(pog)
				self.listVersion += 1
				return
		self.addPog(pog)
