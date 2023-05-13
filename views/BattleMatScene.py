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

	def __init__(self, splitter):
		super(BattleMatScene, self).__init__()
		self._currentDungeonID = None
		self._currentSessionID = None
		self._dungeonPicture = None
		self._currentLevel = -1
		self._dataVersionsHistory = DataVersions()
		self._monsterPogs = list()
		self._roomObjectPogs = list()
		self._playerPogs = list()
		self._imageLoaded = False
		self._selectedPogCanvas = None
		self._gridOffsetX = 0
		self._gridOffsetY = 0
		self._gridSpacing = 50
		self._showGrid = True
		self._imageWidth = 100
		self._imageHeight = 100
		self._verticalLines = 10
		self._horizontalLines = 10
		self._imageLoaded = False

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
		proxy = None
		if hasattr(src, 'proxy'):
			proxy = src.proxy
		if proxy is not None:
			proxy.setPos(e.scenePos())
		else:
			pos = e.scenePos()
			self.addButtonToScene(pos.x(), pos.y())

	def dragMoveEvent(self, e):
		e.acceptProposedAction()

	def computeInitialZoom(self):
		# if self._imageLoaded:
		# 	if self.pixelMap.width() > self.pixelMap.height():
		# 		pw = self.pixelMap.width()
		# 		sz = self.splitter.sizes()[0]
		# 	else:
		# 		pw = self.pixelMap.height()
		# 		sz = self.splitter.height()
		#
		# 	newZoom = sz / pw
		# 	self.view.setZoom(newZoom)
		self.view.setZoom(1)
		pass

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
		if dungeonManager.selectedDungeonUUID != self._currentDungeonID:
			initView = True
		elif dungeonManager.getCurrentSessionUUID() != self._currentSessionID:
			initView = True
		elif dungeonManager.currentLevelIndex != self._currentLevel:
			initView = True
		elif dungeonManager.getCurrentDungeonLevelData().levelDrawing != self._dungeonPicture:
			initView = True

		if initView:
			self.intializeView()
		else:
			self.dungeonDataUpdated()
		self._currentDungeonID = dungeonManager.selectedDungeonUUID
		self._currentSessionID = dungeonManager.getCurrentSessionUUID()
		self._currentLevel = dungeonManager.currentLevelIndex

	def intializeView(self):
		self._dataVersionsHistory.initialize()
		self._monsterPogs.clear()
		self._roomObjectPogs.clear()
		self._playerPogs.clear()
		self.pixMapItem = None
		self.clear()
		dungeonLevel = ServicesManager.getDungeonManager().getCurrentDungeonLevelData()
		if dungeonLevel is None:
			return
		self._dungeonPicture = dungeonLevel.levelDrawing
		imageUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(self._dungeonPicture)
		self._imageLoaded = False
		AsyncImage(imageUrl, self.imageWasLoaded, self.failedLoad).submit()
		pass

	def imageWasLoaded(self, asynchReturn):
		"""
		Callback from background task when image loaded
		:param asynchReturn: Image that was loaded
		:return: None
		"""
		image = asynchReturn.data
		self._imageLoaded = True
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
		# self.view.fitInView(0, 0, self.pixelMap.width(), self.pixelMap.height(), QtCore.Qt.KeepAspectRatio)
		self._imageWidth = self.pixelMap.width()
		self._imageHeight = self.pixelMap.height()

	def dungeonDataUpdated(self):
		if not self._imageLoaded:
			return
		self.calculateDimensions()
		self.deSelectPog()
		self.updateNeededData()
		self.newSelectedPog()

	def deSelectPog(self):
		if self._selectedPogCanvas is not None:
			# selectedPogCanvas.getElement().getStyle().setBorderColor("grey");
			self._selectedPogCanvas = None

	def updateNeededData(self):
		self.getGridData()
		monsters = ServicesManager.getDungeonManager().getMonstersForCurrentLevel()
		pogData = monsters[0]
		self.addPogToCanvas(pogData)
		pass

	def addPogToCanvas(self, pogData):
		pogCanvas = PogCanvas(self.view)
		pogCanvas.setPogData(pogData, False)
		pogCanvas.setGridSize(self._gridSpacing)
		self.addItem(pogCanvas)
		pogCanvas.setPos(200, 200)
		pogCanvas.setZValue(100)
		pass

	def drawBackground(self, painter, rect):
		self.drawGrid(painter)
		pass

	def drawForeground(self, painter, rect):
		pass

	def drawGrid(self, painter):
		if not self._imageLoaded:
			return
		self.calculateDimensions()
		if not self._showGrid:
			return
		line = QtCore.QLineF(QtCore.QPointF(self._gridOffsetX, self._gridOffsetY),
							QtCore.QPointF(self._imageWidth, self._gridOffsetY))
		for _ in range(self._horizontalLines):
			painter.drawLine(line)
			line.translate(0, self._gridSpacing)
		line = QtCore.QLineF(QtCore.QPointF(self._gridOffsetX, self._gridOffsetY),
							QtCore.QPointF(self._gridOffsetX, self._imageHeight))
		for _ in range(self._verticalLines):
			painter.drawLine(line)
			line.translate(self._gridSpacing, 0)

	def calculateDimensions(self):
		self.getGridData()
		self._verticalLines = int((self._imageWidth / self._gridSpacing) + 1)
		self._horizontalLines = int((self._imageHeight / self._gridSpacing) + 1)
		ServicesManager.getDungeonManager().setSessionLevelSize(self._verticalLines, self._horizontalLines)

	def getGridData(self):
		self._gridOffsetX = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridOffsetX
		self._gridOffsetY = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridOffsetY
		self._gridSpacing = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridSize
		self._showGrid = ServicesManager.getDungeonManager().isDungeonGridVisible()

	def addPixelMap(self, pixelMap):
		pm = pixelMap.scaled(int(self._gridSpacing), int(self._gridSpacing),
							QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
		it = self.addPixmap(pm)
		it.setPos(300, 300)
		pass

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
