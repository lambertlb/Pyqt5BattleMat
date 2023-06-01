"""
GPL 3 file header
"""
from PySide2 import QtWidgets, QtCore, QtGui

from services.AsyncTasks import AsyncImage
from services.DungeonManager import DungeonManager
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.DungeonLevel import DungeonLevel


class DungeonEditorTab(QtWidgets.QWidget):

	def __init__(self, *args):
		super(DungeonEditorTab, self).__init__(*args)
		self.isDirty = False
		self.newLevel = False
		self.currentLevel: DungeonLevel | None = None
		self.imageLoaded = False
		self.lastImageUrl = ''
		self.image = None

		self.monsterEditorTab = self
		self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.monsterEditorTab)
		self.gridLayout_5 = QtWidgets.QGridLayout()
		self.gridLayout_4 = QtWidgets.QGridLayout()
		self.newLevelButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.gridLayout_4.addWidget(self.newLevelButton, 0, 1, 1, 1)
		self.manageDungeonsButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.gridLayout_4.addWidget(self.manageDungeonsButton, 0, 0, 1, 1)
		self.deleteLevelButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.gridLayout_4.addWidget(self.deleteLevelButton, 0, 2, 1, 1)
		self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 4)
		self.levelNameLabel = QtWidgets.QLabel(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.levelNameLabel, 1, 0, 1, 1)
		self.levelNameEdit = QtWidgets.QLineEdit(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.levelNameEdit, 1, 1, 1, 3)
		self.showGridCheckBox = QtWidgets.QCheckBox(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.showGridCheckBox, 2, 0, 1, 2)
		self.gridSizeButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.gridSizeButton, 3, 0, 1, 2)
		self.gridSizeEdit = QtWidgets.QLineEdit(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.gridSizeEdit, 3, 2, 1, 2)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.offsetXLabel = QtWidgets.QLabel(self.monsterEditorTab)
		self.horizontalLayout_2.addWidget(self.offsetXLabel)
		self.offsetXEdit = QtWidgets.QLineEdit(self.monsterEditorTab)
		self.horizontalLayout_2.addWidget(self.offsetXEdit)
		self.gridLayout_5.addLayout(self.horizontalLayout_2, 4, 0, 1, 3)
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.offsetYLabel = QtWidgets.QLabel(self.monsterEditorTab)
		self.horizontalLayout_3.addWidget(self.offsetYLabel)
		self.offsetYEdit = QtWidgets.QLineEdit(self.monsterEditorTab)
		self.horizontalLayout_3.addWidget(self.offsetYEdit)
		self.gridLayout_5.addLayout(self.horizontalLayout_3, 4, 3, 1, 1)
		self.useSelectedPictureButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.useSelectedPictureButton, 5, 0, 1, 2)
		self.selectedPictureEdit = QtWidgets.QLineEdit(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.selectedPictureEdit, 5, 2, 1, 2)
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
		self.saveButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.horizontalLayout_4.addWidget(self.saveButton)
		self.cancelButton = QtWidgets.QPushButton(self.monsterEditorTab)
		self.horizontalLayout_4.addWidget(self.cancelButton)
		self.gridLayout_5.addLayout(self.horizontalLayout_4, 6, 0, 1, 3)
		self.scene = QtWidgets.QGraphicsScene(self.monsterEditorTab)
		self.graphicsView_2 = QtWidgets.QGraphicsView(self.scene)
		self.gridLayout_5.addWidget(self.graphicsView_2, 7, 0, 1, 4)
		self.verticalLayout_4.addLayout(self.gridLayout_5)
		self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.graphicsView_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.localize()
		self.setupEvents()

	def localize(self):
		self.newLevelButton.setText("New Level")
		self.manageDungeonsButton.setText("Manage Dungeons")
		self.deleteLevelButton.setText("DELETE Level")
		self.levelNameLabel.setText("Level Name")
		self.showGridCheckBox.setText("Show Grid")
		self.gridSizeButton.setText("Grid Size")
		self.gridSizeEdit.setText("30")
		self.offsetXLabel.setText("Offset X")
		self.offsetXEdit.setText("0")
		self.offsetYLabel.setText("Offset Y")
		self.offsetYEdit.setText("0")
		self.useSelectedPictureButton.setText("Use Selected\n" "Picture Resource")
		self.saveButton.setText("Save")
		self.cancelButton.setText("Cancel")

	def setupEvents(self):
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)
		self.manageDungeonsButton.clicked.connect(self.manageDungeons)
		self.newLevelButton.clicked.connect(self.createNewLevel)
		self.deleteLevelButton.clicked.connect(self.deleteLevel)
		self.levelNameEdit.textChanged.connect(self.dataChanged)
		self.selectedPictureEdit.textChanged.connect(self.dataChanged)
		self.gridSizeEdit.textChanged.connect(self.dataChanged)
		self.offsetXEdit.textChanged.connect(self.dataChanged)
		self.offsetYEdit.textChanged.connect(self.dataChanged)
		self.showGridCheckBox.clicked.connect(self.dataChanged)
		self.cancelButton.clicked.connect(self.gatherData)
		self.saveButton.clicked.connect(self.saveFormData)
		self.useSelectedPictureButton.clicked.connect(self.copyResourceURL)
		self.gridSizeButton.clicked.connect(self.copyGridSize)

	# noinspection PyMethodMayBeStatic
	def manageDungeons(self):
		ServicesManager.getEventManager().fireEvent(ReasonForAction.LOGGED_IN, True)

	def initialize(self):
		self.newLevel = False
		self.gridSizeEdit.setText(str(30))
		self.offsetXEdit.setText(str(0.0))
		self.offsetYEdit.setText(str(0.0))
		self.levelNameEdit.setText("New Level")
		self.selectedPictureEdit.setText("")
		self.validateContent()

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForAction.DungeonDataLoaded:
			self.gatherData()
		elif eventData.eventReason == ReasonForAction.DungeonSelectedLevelChanged:
			self.gatherData()

	def gatherData(self):
		self.currentLevel = ServicesManager.getDungeonManager().getCurrentDungeonLevelData()
		if self.currentLevel is None:
			return
		self.addLevelDataToForm()
		self.validateContent()
		self.saveButton.setDisabled(True)
		self.cancelButton.setDisabled(True)
		self.isDirty = False

	def addLevelDataToForm(self):
		self.showGridCheckBox.setChecked(ServicesManager.getDungeonManager().isDungeonGridVisible())
		self.gridSizeEdit.setText(str(self.currentLevel.gridSize))
		self.offsetXEdit.setText(str(self.currentLevel.gridOffsetX))
		self.offsetYEdit.setText(str(self.currentLevel.gridOffsetY))
		self.levelNameEdit.setText(self.currentLevel.levelName)
		self.selectedPictureEdit.setText(self.currentLevel.levelDrawing)

	def dataChanged(self):
		self.isDirty = True
		self.validateContent()

	def validateContent(self):
		isOK = True
		dm: DungeonManager = ServicesManager.getDungeonManager()
		if not dm.isLegalDungeonName(self.levelNameEdit.text()):
			isOK = False
			self.levelNameLabel.setStyleSheet('color: red')
		else:
			self.levelNameLabel.setStyleSheet('color: black')
		if not dm.isValidPictureURL(self.selectedPictureEdit.text()):
			isOK = False
			self.selectedPictureEdit.setStyleSheet('color: red')
		else:
			self.selectedPictureEdit.setStyleSheet('color: black')
			self.drawPicture()
		isOK = self.checkNumberFromControl(self.gridSizeEdit, 4.0, isOK)
		isOK = self.checkNumberFromControl(self.offsetXEdit, 0, isOK)
		isOK = self.checkNumberFromControl(self.offsetYEdit, 0, isOK)
		self.saveButton.setDisabled(not isOK or not self.isDirty)
		self.cancelButton.setDisabled(not self.isDirty)

	# noinspection PyMethodMayBeStatic
	def checkNumberFromControl(self, control, lowerRange, isOK):
		returnIsOK = isOK
		try:
			numberCheck = float(control.text())
			if numberCheck < lowerRange:
				returnIsOK = False
				control.setStyleSheet('color: red')
			else:
				control.setStyleSheet('color: black')
		except (Exception,):
			returnIsOK = False
			control.setStyleSheet('color: red')
		return returnIsOK

	def saveFormData(self):
		dm: DungeonManager = ServicesManager.getDungeonManager()
		levelData: DungeonLevel = dm.getCurrentDungeonLevelData()
		if levelData is None:
			return
		nextAvailableLevelIndex = dm.getNextAvailableLevelNumber()
		dm.setIsDungeonGridVisible(self.showGridCheckBox.isChecked())
		self.currentLevel.gridSize = float(self.gridSizeEdit.text())
		self.currentLevel.gridOffsetX = float(self.offsetXEdit.text())
		self.currentLevel.gridOffsetY = float(self.offsetYEdit.text())
		self.currentLevel.levelName = self.levelNameEdit.text()
		self.currentLevel.levelDrawing = self.selectedPictureEdit.text()
		if self.newLevel:
			dm.addNewLevel(self.currentLevel)
		dm.saveDungeonData()
		if self.newLevel:
			dm.setCurrentLevel(nextAvailableLevelIndex)
		self.newLevel = False
		self.isDirty = False
		self.validateContent()

	def copyResourceURL(self):
		url = ServicesManager.getDungeonManager().assetURL
		if ServicesManager.getDungeonManager().isValidPictureURL(url):
			self.selectedPictureEdit.setText(url)

	def drawPicture(self):
		self.imageLoaded = False
		url = self.selectedPictureEdit.text()
		fullUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(url)
		if self.lastImageUrl != fullUrl:
			self.lastImageUrl = fullUrl
			AsyncImage(fullUrl, self.onSuccessPictureLoaded, self.onFailurePictureLoaded).submit()

	def onSuccessPictureLoaded(self, data):
		self.imageLoaded = True
		self.image = data.data
		self.showThePicture()

	def showThePicture(self):
		if not self.imageLoaded:
			return
		self.scene.clear()
		gw = self.graphicsView_2.width()
		gh = self.graphicsView_2.height()
		pixMap = QtGui.QPixmap.fromImage(self.image)
		scenePixMap = pixMap.scaled(gw, gh, QtCore.Qt.KeepAspectRatio,
									QtCore.Qt.SmoothTransformation)
		self.scene.addPixmap(scenePixMap)
		self.scene.setSceneRect(0, 0, scenePixMap.width(), scenePixMap.height())

	def onFailurePictureLoaded(self, *args):
		pass

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		self.showThePicture()

	def createNewLevel(self):
		self.initialize()
		self.currentLevel = DungeonLevel()
		self.addLevelDataToForm()
		self.newLevel = True
		self.validateContent()

	# noinspection PyMethodMayBeStatic
	def deleteLevel(self):
		dm: DungeonManager = ServicesManager.getDungeonManager()
		dm.removeCurrentLevel()
		dm.saveDungeonData()
		dm.setCurrentLevel(0)

	def copyGridSize(self):
		self.gridSizeEdit.setText(str(ServicesManager.getDungeonManager().computedGridWidth))
		self.isDirty = True
		self.validateContent()
