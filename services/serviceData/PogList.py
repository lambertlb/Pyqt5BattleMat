"""
GPL 3 file header
"""
from services.serviceData.PogData import PogData


class PogList:
	pogList = []
	listVersion = 0

	def construct(self):
		dl = PogList()
		self.cloneData(dl)
		return dl

	def cloneData(self, dl):
		dl.listVersion = self.listVersion
		if self.pogList is None:
			return
		for pog in self.pogList:
			pd = PogData()
			pd.__dict__ = pog
			dl.pogList.append(pd)
			pass

	def getListVersion(self):
		return self.listVersion
