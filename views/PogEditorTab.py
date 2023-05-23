"""
GPL 3 file header
"""
import uuid

from PyQt5 import QtWidgets, QtCore

from services.Constants import Constants
from services.DungeonManager import DungeonManager
from services.DungeonMasterFlag import DungeonMasterFlag
from services.PlayerFlags import PlayerFlag
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.PogData import PogData
from services.serviceData.PogPlace import PogPlace
from views.FlagEditor import FlagEditor
from views.PogNotesView import PogNotesViewer


class PogEditorTab(QtWidgets.QWidget):

	def __init__(self, *args):
		super(PogEditorTab, self).__init__(*args)
		self.isDirty = False
		self.pogData: PogData | None = None
		self.notes = ''
		self.dmNotes = ''
		self.notesDialog: PogNotesViewer | None = None
		self.flagEditor = None
		self.playerFlags = None
		self.dmFlags = None

		self.pogEditorTab = self
		self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.pogEditorTab)
		self.gridLayout_7 = QtWidgets.QGridLayout()
		self.sizeComboBox = QtWidgets.QComboBox(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.sizeComboBox, 5, 2, 1, 1)
		self.gridLayout_6 = QtWidgets.QGridLayout()
		self.createPogButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.gridLayout_6.addWidget(self.createPogButton, 0, 0, 1, 1)
		self.deletePogButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.gridLayout_6.addWidget(self.deletePogButton, 0, 1, 1, 1)
		self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 3)
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
		self.savePogButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.horizontalLayout_5.addWidget(self.savePogButton)
		self.cancelPogButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.horizontalLayout_5.addWidget(self.cancelPogButton)
		self.gridLayout_7.addLayout(self.horizontalLayout_5, 7, 0, 1, 3)
		self.pogNameLabel = QtWidgets.QLabel(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.pogNameLabel, 1, 0, 1, 1)
		self.useSelectedPogPictureButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.useSelectedPogPictureButton, 4, 0, 1, 2)
		self.pogTypeComboBox = QtWidgets.QComboBox(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.pogTypeComboBox, 2, 1, 1, 2)
		self.pogLocationLabel = QtWidgets.QLabel(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.pogLocationLabel, 3, 0, 1, 1)
		self.treeWidget_2 = QtWidgets.QTreeWidget(self.pogEditorTab)
		self.treeWidget_2.headerItem().setText(0, "1")
		self.gridLayout_7.addWidget(self.treeWidget_2, 8, 0, 1, 3)
		self.pogNameEdit = QtWidgets.QLineEdit(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.pogNameEdit, 1, 1, 1, 2)
		self.useSelectedPogPictureEdit = QtWidgets.QLineEdit(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.useSelectedPogPictureEdit, 4, 2, 1, 1)
		self.pogTypeLabel = QtWidgets.QLabel(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.pogTypeLabel, 2, 0, 1, 1)
		self.playerFlagsButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.playerFlagsButton, 6, 0, 1, 2)
		self.graphicsView_3 = QtWidgets.QGraphicsView(self.pogEditorTab)
		self.graphicsView_3.setMaximumSize(QtCore.QSize(50, 50))
		self.gridLayout_7.addWidget(self.graphicsView_3, 9, 0, 1, 1)
		self.editNotesButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.editNotesButton, 5, 0, 1, 2)
		self.pogLocationComboBox = QtWidgets.QComboBox(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.pogLocationComboBox, 3, 1, 1, 2)
		self.dmFlagsButton = QtWidgets.QPushButton(self.pogEditorTab)
		self.gridLayout_7.addWidget(self.dmFlagsButton, 6, 2, 1, 1)
		self.verticalLayout_5.addLayout(self.gridLayout_7)

		self.localize()
		self.setupEvents()

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.createPogButton.setText(_translate("MainWindow", "Create Pog"))
		self.deletePogButton.setText(_translate("MainWindow", "DELETE Pog"))
		self.savePogButton.setText(_translate("MainWindow", "Save"))
		self.cancelPogButton.setText(_translate("MainWindow", "Cancel"))
		self.pogNameLabel.setText(_translate("MainWindow", "Pog Name"))
		self.useSelectedPogPictureButton.setText(_translate("MainWindow", "Use Selected\n"
"Picture Resource"))
		self.pogLocationLabel.setText(_translate("MainWindow", "Pog Location"))
		self.pogTypeLabel.setText(_translate("MainWindow", "Pog Type"))
		self.playerFlagsButton.setText(_translate("MainWindow", "Player Flags"))
		self.editNotesButton.setText(_translate("MainWindow", "Edit Notes"))
		self.dmFlagsButton.setText(_translate("MainWindow", "DM Flags"))

	def setupEvents(self):
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)
		self.playerFlagsButton.clicked.connect(self.editPlayerFlags)
		self.dmFlagsButton.clicked.connect(self.editDmFlags)
		self.editNotesButton.clicked.connect(self.editNotes)
		self.pogNameEdit.textChanged.connect(self.dataChanged)
		self.useSelectedPogPictureEdit.textChanged.connect(self.dataChanged)
		self.pogLocationComboBox.currentIndexChanged.connect(self.dataChanged)
		self.pogTypeComboBox.currentIndexChanged.connect(self.dataChanged)

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForAction.DungeonDataLoaded:
			self.dungeonDataLoaded()
		elif eventData.eventReason == ReasonForAction.SessionDataSaved:
			self.dungeonDataLoaded()
		elif eventData.eventReason == ReasonForAction.PogWasSelected:
			self.selectPog()
		elif eventData.eventReason == ReasonForAction.PogDataChanged:
			self.pogDataChanged(eventData.eventData)

	def dataChanged(self):
		self.isDirty = True
		self.validateForm()

	def dungeonDataLoaded(self):
		self.fillInSizes()
		self.fillPogPlaceList()
		self.fillPogTypeList()
		self.selectPog()
		pass

	def fillInSizes(self):
		self.sizeComboBox.clear()
		sizes = ServicesManager.getDungeonManager().getPogSizes()
		for size in sizes:
			self.sizeComboBox.addItem(size)

	def fillPogTypeList(self):
		self.pogTypeComboBox.clear()
		self.pogTypeComboBox.addItem(Constants.POG_TYPE_MONSTER)
		self.pogTypeComboBox.addItem(Constants.POG_TYPE_ROOMOBJECT)
		if not ServicesManager.getDungeonManager().editMode:
			self.pogTypeComboBox.addItem(Constants.POG_TYPE_PLAYER)

	def fillPogPlaceList(self):
		self.pogLocationComboBox.clear()
		inEdit = ServicesManager.getDungeonManager().editMode
		dn = PogPlace.DisplayNames
		for place in dn.values():
			if not inEdit or ('Session' not in place and 'Player' not in place):
				self.pogLocationComboBox.addItem(place)

	def createPog(self):
		self.pogData = ServicesManager.getDungeonManager().createTemplatePog(Constants.POG_TYPE_MONSTER)
		self.setupPogData()
		pass

	def selectPog(self):
		self.isDirty = False
		dm: DungeonManager = ServicesManager.getDungeonManager()
		pog: PogData = dm.getSelectedPog()
		if pog is None:
			self.createPog()
			return
		self.pogData = pog.clone()
		self.pogData.uuid = str(uuid.uuid4())
		self.setupPogData()
		pass

	def setupPogData(self):
		self.pogNameEdit.setText(self.pogData.pogName)
		self.setPogType()
		self.setPogLocation()
		self.useSelectedPogPictureEdit.setText(self.pogData.pogImageUrl)
		self.setNotesData()
		self.setSizeData()
		self.playerFlags = self.pogData.playerFlags
		self.dmFlags = self.pogData.dungeonMasterFlags
		self.validateForm()
		pass

	def setPogType(self):
		pogType = self.pogData.pogType
		if pogType == Constants.POG_TYPE_ROOMOBJECT:
			self.pogTypeComboBox.setCurrentIndex(1)
		elif pogType == Constants.POG_TYPE_PLAYER:
			self.pogTypeComboBox.setCurrentIndex(2)
		else:
			self.pogTypeComboBox.setCurrentIndex(0)

	def setPogLocation(self):
		place = self.pogData.pogPlace
		self.pogLocationComboBox.setCurrentIndex(place)

	def setNotesData(self):
		self.notes = self.pogData.notes
		self.dmNotes = self.pogData.dmNotes
		if self.notesDialog is None:
			mainWindow = QtCore.QCoreApplication.instance().mainWindow
			self.notesDialog = PogNotesViewer(mainWindow)
		self.notesDialog.setNotes(self.notes)
		self.notesDialog.setDmNotes(self.dmNotes)

	def setSizeData(self):
		pogSize = self.pogData.pogSize - 1
		if pogSize < 0:
			pogSize = 0
		self.sizeComboBox.setCurrentIndex(pogSize)

	def editPlayerFlags(self):
		self.checkFlagDialog()
		self.flagEditor.setup(self.playerFlags, PlayerFlag.DisplayNames)
		if self.flagEditor.exec_():
			self.playerFlags = self.flagEditor.getFlags()
			self.isDirty = True
			self.validateForm()

	def checkFlagDialog(self):
		if self.flagEditor is None:
			mainWindow = QtCore.QCoreApplication.instance().mainWindow
			self.flagEditor = FlagEditor(mainWindow)

	def editDmFlags(self):
		self.checkFlagDialog()
		self.flagEditor.setup(self.dmFlags, DungeonMasterFlag.DisplayNames)
		if self.flagEditor.exec_():
			self.dmFlags = self.flagEditor.getFlags()
			self.isDirty = True
			self.validateForm()

	def validateForm(self):
		isOK = True
		dm: DungeonManager = ServicesManager.getDungeonManager()
		if not dm.isValidNewMonsterName(self.pogNameEdit.text()):
			isOK = False
			self.pogNameLabel.setStyleSheet('color: red')
		else:
			self.pogNameLabel.setStyleSheet('color: black')
		self.pogData.pogImageUrl = self.useSelectedPogPictureEdit.text()
		self.setupPicture()
		if not dm.isValidPictureURL(self.pogData.pogImageUrl):
			isOK = False
			self.useSelectedPogPictureEdit.setStyleSheet('color: red')
		else:
			self.useSelectedPogPictureEdit.setStyleSheet('color: black')
		self.savePogButton.setDisabled(not isOK or not self.isDirty)
		self.cancelPogButton.setDisabled(not self.isDirty)
		self.deletePogButton.setDisabled(not isOK)
		self.createPogButton.setDisabled(not self.isDirty)
		# selectedPog.setPreventDrag(!isOK);

	def editNotes(self):
		if self.notesDialog.exec_():
			self.notes = self.notesDialog.getNotes()
			self.dmNotes = self.notesDialog.getDmNotes()
			self.isDirty = True
			self.validateForm()

	def pogDataChanged(self, pog):
		pass

	def setupPicture(self):
		pass
