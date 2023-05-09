"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui

from services.AsyncTasks import AsyncImage
from services.ServicesManager import ServicesManager


class PogCanvas(QtWidgets.QLabel):
	fromRibbonBar = False
	pogData = None
	badURL = False
	showImage = False
	currentPictureUrl = None
	imageLoaded = False
	proxy = None

	def __init__(self):
		super(PogCanvas, self).__init__()

	def setPogData(self, pogData, fromRibbonBar):
		self.fromRibbonBar = fromRibbonBar
		self.setupWithPogData(pogData)

	def setupWithPogData(self, pogData):
		self.pogData = pogData
		self.badURL = False
		if pogData.pogImageUrl != '':
			self.setPogImageUrl(pogData.pogImageUrl)
		else:
			self.showImage = False

	def setPogImageUrl(self, pogImageUrl):
		self.currentPictureUrl = pogImageUrl
		self.imageLoaded = False
		self.pogData.pogImageUrl = pogImageUrl
		imageUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(pogImageUrl)
		AsyncImage(imageUrl, self.successfulLoaded, self.failedLoad).submit()

	def successfulLoaded(self, asynchReturn):
		"""
		Callback from background task when image loaded
		:param asynchReturn: Image that was loaded
		:return: None
		"""
		image = asynchReturn.getData()
		self.setPixmap(QtGui.QPixmap.fromImage(image))
		self.setScaledContents(True)

	def failedLoad(self, asynchReturn):
		"""
		Image loading failed
		:param asynchReturn: return data from task
		:return: None
		"""
		pass

	def setProxy(self, proxy):
		"""
		Set scene proxy if in a scene
		:param proxy:
		:return:
		"""
		self.proxy = proxy

	def getProxy(self):
		"""
		:return: proxy else None if not in scene
		"""
		return self.proxy

	def setGridSize(self, size):
		self.setGeometry(0, 0, int(size), int(size))

	def paintEvent(self, event):
		super(PogCanvas, self).paintEvent(event)
		pass
