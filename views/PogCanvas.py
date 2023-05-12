"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from services.AsyncTasks import AsyncImage
from services.ServicesManager import ServicesManager


class PogCanvas(QtWidgets.QGraphicsItem):

	def __init__(self, view):
		super(PogCanvas, self).__init__()
		self.view = view
		self.image = None
		self.pogData = None
		self.badURL = False
		self.currentPictureUrl = None
		self.imageLoaded = False
		self.proxy = None
		self.pixMap = None
		self.scaledGridSize = 0
		self.gridSize = 0
		self.fromRibbonBar = False
		fl = self.flags()
		self.setFlags(fl | QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)

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
		self.image = asynchReturn.data
		self.imageLoaded = True
		self.update()

	def failedLoad(self, asynchReturn):
		"""
		Image loading failed
		:param asynchReturn: return data from task
		:return: None
		"""
		pass

	def setGridSize(self, size):
		self.gridSize = size
		pass

	def boundingRect(self):
		return QtCore.QRectF(0, 0, self.gridSize, self.gridSize)

	def paint(self, painter: QtGui.QPainter, *args):
		if not self.imageLoaded:
			return
		zm = self.view.getZoom()
		gs = int(zm * self.gridSize)
		if gs != self.scaledGridSize:
			self.scaledGridSize = gs
			pixMap = QtGui.QPixmap.fromImage(self.image)
			self.pixMap = pixMap.scaled(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio,
										Qt.SmoothTransformation)
		painter.setPen(QtGui.QPen(Qt.black, 5, Qt.SolidLine))
		painter.setBrush(QtGui.QBrush(Qt.white, Qt.SolidPattern))
		painter.drawRect(0, 0, self.scaledGridSize, self.scaledGridSize)
		painter.drawPixmap(0, 0, self.pixMap)

	# def paintEvent(self, event):
	# 	# super(PogCanvas, self).paintEvent(event)
	# 	if not self.imageLoaded:
	# 		return
	# 	painter = QPainter(self)
	# 	painter.begin(self)
	# 	pixmapSize = self.pixMap.size()
	# 	pixmapSize.scale(self.gridSize, self.gridSize, Qt.KeepAspectRatio)
	# 	pixmapScaled = self.pixMap.scaled(pixmapSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
	# 	painter.drawPixmap(0, 0, pixmapScaled)
	# 	painter.end()
	# 	pass

	def mouseMoveEvent(self, e):
		"""
		Move moved one me so start dragging
		:param e: event
		:return: None
		"""
		# if e.buttons() == QtCore.Qt.LeftButton:
		# 	drag = QtGui.QDrag(self)
		# 	mime = QtCore.QMimeData()
		# 	drag.setMimeData(mime)
		# 	drag.setPixmap(self.grab())
		# 	drag.exec_(QtCore.Qt.MoveAction)
		pass
