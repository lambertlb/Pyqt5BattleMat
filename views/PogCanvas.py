"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from services.AsyncTasks import AsyncImage
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from views.PopupMenu import PopupMenu


class PogCanvas(QtWidgets.QGraphicsItem):

	popup = None

	def __init__(self, view):
		super(PogCanvas, self).__init__()
		if PogCanvas.popup is None:
			PogCanvas.popup = PopupMenu()
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
		fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
		fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
		fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
		fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations
		self.setFlags(fl)
		self.setAcceptDrops(True)

	def setPogData(self, pogData, fromRibbonBar):
		self.fromRibbonBar = fromRibbonBar
		self.setupWithPogData(pogData)

	def getPogData(self):
		return self.pogData

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
		scaledGridSize = self.getScaledGridSize()
		return QtCore.QRectF(0, 0, scaledGridSize, scaledGridSize)

	def getScaledGridSize(self):
		zoom = self.view.getZoom()
		scaledGridSize = int(zoom * self.gridSize)
		return scaledGridSize

	def paint(self, painter: QtGui.QPainter, *args):
		if not self.imageLoaded:
			return
		scaledGridSize = self.getScaledGridSize()
		if scaledGridSize != self.scaledGridSize:
			self.scaledGridSize = scaledGridSize
			pixMap = QtGui.QPixmap.fromImage(self.image)
			self.pixMap = pixMap.scaled(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio,
										Qt.SmoothTransformation)
		# painter.setPen(QtGui.QPen(Qt.black, 5, Qt.SolidLine))
		painter.setBrush(QtGui.QBrush(Qt.white, Qt.SolidPattern))
		painter.drawRect(0, 0, self.scaledGridSize, self.scaledGridSize)
		painter.drawPixmap(0, 0, self.pixMap)

	def mousePressEvent(self, event):
		# modifiers = QtWidgets.QApplication.keyboardModifiers()
		# if ServicesManager.getDungeonManager().getFowToggle() or modifiers & QtCore.Qt.ShiftModifier:
		# 	ServicesManager.getEventManager().fireEvent(ReasonForAction.MouseDownEventBubble, event)
		# 	return
		# if not ServicesManager.getDungeonManager().isDungeonMaster() and not ServicesManager.getDungeonManager().isEditMode and ServicesManager.getDungeonManager().isFowSet(self.pogData.column, self.pogData.row):
		# 	ServicesManager.getEventManager().fireEvent(ReasonForAction.MouseDownEventBubble, event)
		# 	return
		# if not self.fromRibbonBar:
		# 	ServicesManager.getDungeonManager().setSelectedPog(self.pogData)
			# if event.button() == Qt.RightButton:
			# 	if (popup != null) {
			# 		popup.setPopupPosition(event.getClientX(), event.getClientY());
			# 		popup.setPogData(pogData);
			# 		popup.show();
		pass

	def contextMenuEvent(self, event):
		if not self.fromRibbonBar:
			ServicesManager.getDungeonManager().setSelectedPog(self.pogData)
			PogCanvas.popup.showMe(event.screenPos(), self.pogData)

	def mouseMoveEvent(self, event):
		"""
		Move moved on me so start dragging
		:param event: event
		:return: None
		"""
		if QtCore.QLineF(QtCore.QPointF(event.screenPos()),
				QtCore.QPointF(event.buttonDownScreenPos(Qt.LeftButton))).length() < QtWidgets.QApplication.startDragDistance():
			return

		pixMap = QtGui.QPixmap.fromImage(self.image)
		dragPixMap = pixMap.scaled(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio,
									Qt.SmoothTransformation)
		mapToDrag = QtGui.QPixmap(self.scaledGridSize, self.scaledGridSize)
		canvas = QtGui.QPainter()
		canvas.begin(mapToDrag)
		canvas.fillRect(0, 0, mapToDrag.width(), mapToDrag.height(), QtGui.QBrush(QtGui.QColor(255, 255, 255)))
		canvas.setCompositionMode(QtGui.QPainter.CompositionMode_Multiply)
		canvas.drawImage(0, 0, dragPixMap.toImage())
		canvas.end()

		wig = event.widget()
		wig.proxy = self  # add myself to the dragging widget so target can know me
		drag = QtGui.QDrag(wig)
		mime = QtCore.QMimeData()
		drag.setMimeData(mime)
		drag.setPixmap(mapToDrag)
		drag.exec_()
		self.setCursor(Qt.OpenHandCursor)

	def getProxy(self):
		"""
		:return: proxy else None if not in scene
		"""
		return self
