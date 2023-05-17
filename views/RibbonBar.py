"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager


class MyPixmapItem(QtWidgets.QGraphicsPixmapItem):
	def __init__(self, *args):
		super(MyPixmapItem, self).__init__(*args)
		fl = self.flags()
		fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
		fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
		self.setFlags(fl)
	pass

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

		pixMap = self.pixmap()
		mapToDrag = QtGui.QPixmap(70, 70)
		canvas = QtGui.QPainter()
		canvas.begin(mapToDrag)
		canvas.fillRect(0, 0, mapToDrag.width(), mapToDrag.height(), QtGui.QBrush(QtGui.QColor(255, 255, 255)))
		canvas.setCompositionMode(QtGui.QPainter.CompositionMode_Multiply)
		canvas.drawImage(0, 0, pixMap.toImage())
		canvas.end()

		wig = event.widget()
		drag = QtGui.QDrag(wig)
		mime = QtCore.QMimeData()
		drag.setMimeData(mime)
		drag.setPixmap(mapToDrag)
		drag.exec_()


class RibbonBar(QtWidgets.QGridLayout):

	def	__init__(self, frame, *args):
		super(RibbonBar, self).__init__(*args)
		self.selectedPog = None
		self.pogSize = 70
		self.frame = frame
		self.gridLayout_2 = self
		self.selectPlayer_2 = QtWidgets.QComboBox(self.frame)
		self.gridLayout_2.addWidget(self.selectPlayer_2, 1, 1, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout_2.addItem(spacerItem, 1, 4, 1, 1)
		self.toggleFOW_2 = QtWidgets.QCheckBox(self.frame)
		self.gridLayout_2.addWidget(self.toggleFOW_2, 1, 3, 1, 1)
		self.showSelectedPog_2 = QtWidgets.QCheckBox(self.frame)
		self.gridLayout_2.addWidget(self.showSelectedPog_2, 0, 2, 1, 1)
		self.hideFOW_2 = QtWidgets.QCheckBox(self.frame)
		self.gridLayout_2.addWidget(self.hideFOW_2, 0, 3, 1, 1)
		self.scene = QtWidgets.QGraphicsScene(self.frame)
		self.selectedPogArea_2 = QtWidgets.QGraphicsView(self.scene)
		self.selectedPogArea_2.setMinimumSize(QtCore.QSize(self.pogSize, self.pogSize))
		self.selectedPogArea_2.setMaximumSize(QtCore.QSize(self.pogSize, self.pogSize))
		self.scene.setSceneRect(0, 0, self.pogSize, self.pogSize)
		self.selectedPogArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.selectedPogArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.gridLayout_2.addWidget(self.selectedPogArea_2, 0, 0, 2, 1)
		self.selectDungeonLevel_2 = QtWidgets.QComboBox(self.frame)
		self.selectDungeonLevel_2.setMinimumSize(QtCore.QSize(200, 0))
		self.gridLayout_2.addWidget(self.selectDungeonLevel_2, 0, 1, 1, 1)
		self.showPogNotes_2 = QtWidgets.QCheckBox(self.frame)
		self.gridLayout_2.addWidget(self.showPogNotes_2, 1, 2, 1, 1)

		self.localize()
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.toggleFOW_2.setText(_translate("MainWindow", "Toggle FOW"))
		self.showSelectedPog_2.setText(_translate("MainWindow", "Show Selected Pog"))
		self.hideFOW_2.setText(_translate("MainWindow", "Hide FOW"))
		self.showPogNotes_2.setText(_translate("MainWindow", "Show Pog Notes"))

	def eventFired(self, eventData):
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
		elif eventData.eventReason == ReasonForAction.PogWasSelected:
			self.newSelectedPog()

	def checkForDataChanges(self):
		pass

	def newSelectedPog(self):
		selectedPog = ServicesManager.getDungeonManager().getSelectedPog()
		if self.selectedPog is not None:
			if self.selectedPog.isEqual(selectedPog):
				return
		self.selectedPog = selectedPog
		if self.selectedPog is not None:
			self.selectedPog.loafPogImage(self.successfulLoaded, self.failedLoad)
		else:
			self.scene.clear()
		pass

	def successfulLoaded(self):
		self.scene.clear()
		image = self.selectedPog.image
		pixMap = QtGui.QPixmap.fromImage(image)
		scenePixMap = pixMap.scaled(self.pogSize, self.pogSize, QtCore.Qt.KeepAspectRatio,
									QtCore.Qt.SmoothTransformation)
		pm = MyPixmapItem()
		pm.setPixmap(scenePixMap)
		self.scene.addItem(pm)
		pass

	def failedLoad(self, asynchReturn):
		pass
