"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore, QtGui

from services.AsyncTasks import AsyncImage
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.DataVersions import DataVersions
from views.BattleMatCanvas import BattleMatCanvas
from views.DragButton import DragButton
from views.PogCanvas import PogCanvas


class BattleMatScene(QtWidgets.QGraphicsScene):
	"""
	Subclass QGraphicsScene to manage drag and drop
	"""
	currentDungeonID = None
	currentSessionID = None
	dungeonPicture = None
	currentLevel = -1
	dataVersionsHistory = DataVersions()
	monsterPogs = list()
	roomObjectPogs = list()
	playerPogs = list()
	imageLoaded = False
	selectedPogCanvas = None
	gridOffsetX = 0
	gridOffsetY = 0
	gridSpacing = 50
	showGrid = True
	imageWidth = 100
	imageHeight = 100
	verticalLines = 10
	horizontalLines = 10

	def __init__(self, splitter):
		super(BattleMatScene, self).__init__()
		self.imageLoaded = False
		self.splitter = splitter
		self.pixelMap = QtGui.QPixmap()
		self.pixMapItem = self.addPixmap(self.pixelMap)
		self.view = BattleMatCanvas(self, splitter)
		self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
		self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
		self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)

	def dragEnterEvent(self, e):
		e.acceptProposedAction()

	def dropEvent(self, e):
		"""
		Item was dropped here.
		If is had a proxy it means it was already here so just move it.
		If no proxy then create a new item
		:param e: event
		:return:None
		"""
		src = e.source()
		if src.getProxy() is not None:
			src.getProxy().setPos(e.scenePos())
		else:
			pos = e.scenePos()
			self.addButtonToScene(pos.x(), pos.y())

	def dragMoveEvent(self, e):
		e.acceptProposedAction()

	def computeInitialZoom(self):
		if self.imageLoaded:
			if self.pixelMap.width() > self.pixelMap.height():
				pw = self.pixelMap.width()
				sz = self.splitter.sizes()[0]
			else:
				pw = self.pixelMap.height()
				sz = self.splitter.height()

			newZoom = sz / pw
			self.view.setZoom(newZoom)

	def resetScroll(self):
		self.view.verticalScrollBar().setValue(0)
		self.view.horizontalScrollBar().setValue(0)

	def eventFired(self, eventData):
		# if eventData.eventReason == ReasonForAction.LOAD_IMAGE:
		# 	if eventData.eventData is not None:
		# 		self.loadImage(eventData.eventData)
		if eventData.eventReason == ReasonForAction.PogDataChanged:
			self.checkForDataChanges()
		elif eventData.eventReason == ReasonForAction.DungeonDataReadyToEdit:
			self.checkForDataChanges()
		elif eventData.eventReason == ReasonForAction.DungeonDataReadyToJoin:
			self.checkForDataChanges()
		elif eventData.eventReason == ReasonForAction.SessionDataChanged:
			self.checkForDataChanges()
		elif eventData.eventReason == ReasonForAction.DungeonSelectedLevelChanged:
			self.checkForDataChanges()
		elif eventData.eventReason == ReasonForAction.DungeonDataSaved:
			self.checkForDataChanges()

	def checkForDataChanges(self):
		pass
		dungeonManager = ServicesManager.getDungeonManager()
		if dungeonManager.getCurrentDungeonLevelData() is None:
			return
		initView = False
		if dungeonManager.selectedDungeonUUID != self.currentDungeonID:
			initView = True
		elif dungeonManager.getCurrentSessionUUID() != self.currentSessionID:
			initView = True
		elif dungeonManager.currentLevelIndex != self.currentLevel:
			initView = True
		elif dungeonManager.getCurrentDungeonLevelData().levelDrawing != self.dungeonPicture:
			initView = True

		if initView:
			self.intializeView()
		else:
			self.dungeonDataUpdated()
		self.currentDungeonID = dungeonManager.selectedDungeonUUID
		self.currentSessionID = dungeonManager.getCurrentSessionUUID()
		self.currentLevel = dungeonManager.currentLevelIndex

	def intializeView(self):
		self.dataVersionsHistory.initialize()
		self.monsterPogs.clear()
		self.roomObjectPogs.clear()
		self.playerPogs.clear()
		self.pixMapItem = None
		self.clear()
		dungeonLevel = ServicesManager.getDungeonManager().getCurrentDungeonLevelData()
		if dungeonLevel is None:
			return
		self.dungeonPicture = dungeonLevel.levelDrawing
		imageUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(self.dungeonPicture)
		self.imageLoaded = False
		AsyncImage(imageUrl, self.imageWasLoaded, self.failedLoad).submit()
		pass

	def imageWasLoaded(self, asynchReturn):
		"""
		Callback from background task when image loaded
		:param asynchReturn: Image that was loaded
		:return: None
		"""
		image = asynchReturn.getData()
		self.imageLoaded = True
		self.updateImage(QtGui.QPixmap.fromImage(image))
		self.checkForDataChanges()

	def failedLoad(self, asynchReturn):
		"""
		Image loading failed
		:param asynchReturn: return data from task
		:return: None
		"""
		pass

	def updateImage(self, newPixmap):
		"""
		new image loaded so update old pixel map
		:param newPixmap:
		:return: None
		"""
		if self.pixMapItem is not None:
			self.removeItem(self.pixMapItem)
		self.pixelMap = newPixmap
		self.pixMapItem = self.addPixmap(self.pixelMap)
		self.computeInitialZoom()
		self.resetScroll()
		self.view.setSceneRect(0, 0, self.pixelMap.width(), self.pixelMap.height())
		self.view.fitInView(0, 0, self.pixelMap.width(), self.pixelMap.height(), QtCore.Qt.KeepAspectRatio)
		self.imageWidth = self.pixelMap.width()
		self.imageHeight = self.pixelMap.height()

	def dungeonDataUpdated(self):
		if not self.imageLoaded:
			return
		self.calculateDimensions()
		self.deSelectPog()
		self.updateNeededData()
		self.newSelectedPog()

	def deSelectPog(self):
		if self.selectedPogCanvas is not None:
			# selectedPogCanvas.getElement().getStyle().setBorderColor("grey");
			self.selectedPogCanvas = None

	def updateNeededData(self):
		self.getGridData()
		monsters = ServicesManager.getDungeonManager().getMonstersForCurrentLevel()
		pogData = monsters[0]
		self.addPogToCanvas(pogData)
		pass

	def addPogToCanvas(self, pogData):
		proxy = QtWidgets.QGraphicsProxyWidget()
		pogCanvas = PogCanvas()
		pogCanvas.setPogData(pogData, False)
		pogCanvas.setGridSize(self.gridSpacing)
		proxy.setWidget(pogCanvas)
		pogCanvas.setProxy(proxy)
		self.addItem(proxy)
		proxy.setPos(200, 200)
		proxy.setZValue(100)
		pass

	def drawBackground(self, painter, rect):
		self.drawGrid(painter)
		pass

	def drawForeground(self, painter, rect):
		pass

	def drawGrid(self, painter):
		if not self.imageLoaded:
			return
		self.calculateDimensions()
		if not self.showGrid:
			return
		line = QtCore.QLineF(QtCore.QPointF(self.gridOffsetX, self.gridOffsetY),
							QtCore.QPointF(self.imageWidth, self.gridOffsetY))
		for _ in range(self.horizontalLines):
			painter.drawLine(line)
			line.translate(0, self.gridSpacing)
		line = QtCore.QLineF(QtCore.QPointF(self.gridOffsetX, self.gridOffsetY),
							QtCore.QPointF(self.gridOffsetX, self.imageHeight))
		for _ in range(self.verticalLines):
			painter.drawLine(line)
			line.translate(self.gridSpacing, 0)

	def calculateDimensions(self):
		self.getGridData()
		self.verticalLines = int((self.imageWidth / self.gridSpacing) + 1)
		self.horizontalLines = int((self.imageHeight / self.gridSpacing) + 1)
		ServicesManager.getDungeonManager().setSessionLevelSize(self.verticalLines, self.horizontalLines)

	def getGridData(self):
		self.gridOffsetX = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridOffsetX
		self.gridOffsetY = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridOffsetY
		self.gridSpacing = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridSize
		self.showGrid = ServicesManager.getDungeonManager().isDungeonGridVisible()

	def newSelectedPog(self):
		pass

	def addButtonToScene(self, x, y):
		"""
		add a button to scene
		:param x:
		:param y:
		:return: None
		"""
		pw = QtWidgets.QGraphicsProxyWidget()
		db = DragButton('image/level1.jpg', 'push me')
		pw.setWidget(db)
		db.setProxy(pw)
		self.addItem(pw)
		pw.setPos(x, y)
		pw.setZValue(100)
