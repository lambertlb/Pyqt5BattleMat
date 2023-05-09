"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from services.AsyncTasks import AsyncImage
from services.ServicesManager import ServicesManager


class PogCanvas(QtWidgets.QPushButton):
	fromRibbonBar = False
	pogData = None
	badURL = False
	currentPictureUrl = None
	imageLoaded = False
	proxy = None
	pixMap = None

	def __init__(self):
		super(PogCanvas, self).__init__()
		self.setMouseTracking(True)
		# self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

	def setPogData(self, pogData, fromRibbonBar):
		self.fromRibbonBar = fromRibbonBar
		self.setupWithPogData(pogData)

	def setupWithPogData(self, pogData):
		self.pogData = pogData
		self.badURL = False
		self.imageLoaded = False
		if pogData.pogImageUrl != '':
			self.setPogImageUrl(pogData.pogImageUrl)

	def setPogImageUrl(self, pogImageUrl):
		self.currentPictureUrl = pogImageUrl
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
		self.pixMap = QtGui.QPixmap.fromImage(image)
		self.imageLoaded = True
		self.update()

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
		self.setFixedSize(int(size), int(size))
		pass

	def paintEvent(self, event):
		# super(PogCanvas, self).paintEvent(event)
		if not self.imageLoaded:
			return
		painter = QPainter(self)
		pixmapSize = self.pixMap.size()
		pixmapSize.scale(event.rect().size(), Qt.KeepAspectRatio)
		pixmapScaled = self.pixMap.scaled(pixmapSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		painter.drawPixmap(0, 0, pixmapScaled)
		pass

	def mouseMoveEvent(self, e):
		"""
		Move moved one me so start dragging
		:param e: event
		:return: None
		"""
		if e.buttons() == QtCore.Qt.LeftButton:
			drag = QtGui.QDrag(self)
			mime = QtCore.QMimeData()
			drag.setMimeData(mime)
			drag.setPixmap(self.grab())
			drag.exec_(QtCore.Qt.MoveAction)
