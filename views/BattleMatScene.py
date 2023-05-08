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
	imageHasBeenLoaded = False

	def __init__(self, splitter):
		super(BattleMatScene, self).__init__()
		self.pixelMapLoaded = False
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

	def computeInitialZoom(self):
		if self.pixelMapLoaded:
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
		imageUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(self.dungeonPicture);
		self.imageHasBeenLoaded = False
		AsyncImage(imageUrl, self.imageLoaded, self.failedLoad).submit()
		pass

	def imageLoaded(self, asynchReturn):
		"""
		Callback from background task when image loaded
		:param asynchReturn: Image that was loaded
		:return: None
		"""
		image = asynchReturn.getData()
		self.pixelMapLoaded = True
		self.updateImage(QtGui.QPixmap.fromImage(image))

	def failedLoad(self, asynchReturn):
		"""
		Image loading failed
		:param asynchReturn: return data from task
		:return: None
		"""
		pass

	def dungeonDataUpdated(self):
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
