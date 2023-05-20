"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

from services.DungeonMasterFlag import DungeonMasterFlag
from services.PlayerFlags import PlayerFlag
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
		self.imageLoaded = False
		self.proxy = None
		self.pixMap = None
		self.scaledGridSize = 0
		self.gridSize = 0
		self.fromRibbonBar = False
		self.wasSelected = False
		self.currentPictureUrl = None
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

	def updatePogData(self, updateData):
		if updateData.pogImageUrl != self.currentPictureUrl:
			self.setupWithPogData(updateData)

	def setupWithPogData(self, pogData):
		self.pogData = pogData
		self.badURL = False
		self.imageLoaded = False
		self.currentPictureUrl = pogData.pogImageUrl

		if pogData.pogNumber != 0:
			self.setToolTip(str(pogData.pogNumber))
		if pogData.pogImageUrl != '':
			self.pogData.loadPogImage(self.successfulLoaded, self.failedLoad)

	def successfulLoaded(self):
		self.image = self.pogData.image
		self.imageLoaded = self.image is not None
		self.update()

	def failedLoad(self, asynchReturn):
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
		invisibleToPlayer = self.pogData.isDmFlagSet(DungeonMasterFlag.INVISIBLE_FROM_PLAYER)
		isDM = ServicesManager.getDungeonManager().isDungeonMaster
		if not isDM and invisibleToPlayer:
			return
		inEdit = ServicesManager.getDungeonManager().editMode
		selected = ServicesManager.getDungeonManager().getSelectedPog()
		isSelected = selected is not None and selected.isEqual(self.pogData)
		scaledGridSize = self.getScaledGridSize()
		if scaledGridSize != self.scaledGridSize:
			self.scaledGridSize = scaledGridSize
			pixMap = QtGui.QPixmap.fromImage(self.image)
			self.pixMap = pixMap.scaled(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio,
										Qt.SmoothTransformation)
		darkInBackground = self.pogData.isDmFlagSet(DungeonMasterFlag.DARK_BACKGROUND)
		transparent = self.pogData.isDmFlagSet(DungeonMasterFlag.TRANSPARENT_BACKGROUND)
		if not inEdit and invisibleToPlayer:
			painter.setOpacity(0.5)
		else:
			painter.setOpacity(1.0)
		if inEdit and darkInBackground:
			painter.setBrush(QtGui.QBrush(Qt.black, Qt.SolidPattern))
		else:
			painter.setBrush(QtGui.QBrush(Qt.white, Qt.SolidPattern))
		if not transparent:
			painter.drawRect(0, 0, self.scaledGridSize, self.scaledGridSize)
		elif inEdit and darkInBackground:
			painter.drawRect(0, 0, self.scaledGridSize, self.scaledGridSize)

		painter.drawPixmap(0, 0, self.pixMap)
		self.drawOverlays(painter)
		if isSelected:
			border = self.computePogBorderWidth()
			inset = int(border / 2)
			length = self.scaledGridSize - inset
			painter.setPen(QtGui.QPen(Qt.black, border, Qt.SolidLine))
			painter.drawLine(inset, inset, length, inset)
			painter.drawLine(inset, inset, inset, length)
			painter.drawLine(length, length, 0, length)
			painter.drawLine(length, length, length, 0)

		self.wasSelected = isSelected

	def drawOverlays(self, painter):
		if self.pogData.isPlayerFlagSet(PlayerFlag.DEAD):
			self.addDeadOverlay(painter)
		pass

	def addDeadOverlay(self, painter):
		size = self.computePogBorderWidth()
		painter.setPen(QtGui.QPen(Qt.red, size, Qt.SolidLine))
		painter.setBrush(QtGui.QBrush())
		painter.drawEllipse(0, 0, self.scaledGridSize, self.scaledGridSize)
		painter.drawLine(0, 0, self.scaledGridSize, self.scaledGridSize)
		pass

	def computePogBorderWidth(self):
		zoom = self.view.getZoom()
		pogBorderWidth = zoom * self.gridSize / 10
		if pogBorderWidth < 3.0:
			pogBorderWidth = 3.0
		if pogBorderWidth * 2 > self.getScaledGridSize():
			pogBorderWidth = 0
		return int(pogBorderWidth)

	def mousePressEvent(self, event):
		modifiers = QtWidgets.QApplication.keyboardModifiers()
		dm = ServicesManager.getDungeonManager()
		em = ServicesManager.getEventManager()
		if dm.getFowToggle() or modifiers & QtCore.Qt.ShiftModifier:
			em.fireEvent(ReasonForAction.MouseDownEventBubble, event)
			return
		if not dm.isDungeonMaster and not dm.editMode and dm.isFowSet(
				self.pogData.column, self.pogData.row):
			em.fireEvent(ReasonForAction.MouseDownEventBubble, event)
			return
		if not self.fromRibbonBar:
			dm.setSelectedPog(self.pogData)

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
						QtCore.QPointF(event.buttonDownScreenPos(
							Qt.LeftButton))).length() < QtWidgets.QApplication.startDragDistance():
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
