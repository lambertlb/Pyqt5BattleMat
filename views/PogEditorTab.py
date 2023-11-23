"""
GPL 3 file header
"""

from PySide6 import QtWidgets, QtCore, QtGui

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
from views.RibbonBar import MyPixmapItem


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
        self.addingData = False
        self.imageLoading = False
        self.pictureDrag = None
        self.justDidSelection = False
        self.previousSelected = None

        self.pogEditorTab = self
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.pogEditorTab)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.pogSizeComboBox = QtWidgets.QComboBox(self.pogEditorTab)
        self.gridLayout_7.addWidget(self.pogSizeComboBox, 5, 2, 1, 1)
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
        self.scene = QtWidgets.QGraphicsScene(self.pogEditorTab)
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.scene)
        self.graphicsView_3.setMaximumSize(QtCore.QSize(50, 50))
        self.gridLayout_7.addWidget(self.graphicsView_3, 9, 0, 1, 1)
        self.editNotesButton = QtWidgets.QPushButton(self.pogEditorTab)
        self.gridLayout_7.addWidget(self.editNotesButton, 5, 0, 1, 2)
        self.pogLocationComboBox = QtWidgets.QComboBox(self.pogEditorTab)
        self.gridLayout_7.addWidget(self.pogLocationComboBox, 3, 1, 1, 2)
        self.dmFlagsButton = QtWidgets.QPushButton(self.pogEditorTab)
        self.gridLayout_7.addWidget(self.dmFlagsButton, 6, 2, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_7)

        self.graphicsView_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.localize()
        self.setupEvents()
        self.setupTree()

    def localize(self):
        self.createPogButton.setText("Create Pog")
        self.deletePogButton.setText("DELETE Pog")
        self.savePogButton.setText("Save")
        self.cancelPogButton.setText("Cancel")
        self.pogNameLabel.setText("Pog Name")
        self.useSelectedPogPictureButton.setText("Use Selected\n" "Picture Resource")
        self.pogLocationLabel.setText("Pog Location")
        self.pogTypeLabel.setText("Pog Type")
        self.playerFlagsButton.setText("Player Flags")
        self.editNotesButton.setText("Edit Notes")
        self.dmFlagsButton.setText("DM Flags")

    def setupEvents(self):
        ServicesManager.getEventManager().subscribeToEvent(self.eventFired)
        self.playerFlagsButton.clicked.connect(self.editPlayerFlags)
        self.dmFlagsButton.clicked.connect(self.editDmFlags)
        self.editNotesButton.clicked.connect(self.editNotes)
        self.pogNameEdit.textChanged.connect(self.dataChanged)
        self.useSelectedPogPictureEdit.textChanged.connect(self.pictureDataChanged)
        self.pogLocationComboBox.currentIndexChanged.connect(self.dataChanged)
        self.pogTypeComboBox.currentIndexChanged.connect(self.dataChanged)
        self.useSelectedPogPictureButton.clicked.connect(self.useSelectedPicture)
        self.cancelPogButton.clicked.connect(self.cancelEdit)
        self.deletePogButton.clicked.connect(self.deletePog)
        self.createPogButton.clicked.connect(self.createPog)
        self.savePogButton.clicked.connect(self.saveFormData)
        self.treeWidget_2.expanded.connect(self.nodeExpanded)
        self.treeWidget_2.selectionModel().selectionChanged.connect(self.treeItemSelected)

    def eventFired(self, eventData):
        if eventData.eventReason == ReasonForAction.DungeonDataLoaded:
            self.dungeonDataLoaded()
        elif eventData.eventReason == ReasonForAction.SessionDataSaved:
            self.dungeonDataLoaded()
        elif eventData.eventReason == ReasonForAction.PogWasSelected:
            self.selectPog()
        elif eventData.eventReason == ReasonForAction.PogDataChanged:
            self.pogDataChanged(eventData.eventData)
        elif eventData.eventReason == ReasonForAction.DungeonSelectedLevelChanged:
            self.fillTrees()

    def dataChanged(self):
        self.isDirty = True
        self.validateForm()

    def dungeonDataLoaded(self):
        self.fillInSizes()
        self.fillPogPlaceList()
        self.fillPogTypeList()
        self.selectPog()
        self.fillTrees()

    def fillInSizes(self):
        self.pogSizeComboBox.clear()
        sizes = ServicesManager.getDungeonManager().getPogSizes()
        for size in sizes:
            self.pogSizeComboBox.addItem(size)

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

    def selectPog(self):
        self.isDirty = False
        dm: DungeonManager = ServicesManager.getDungeonManager()
        pog: PogData = dm.getSelectedPog()
        if pog is None:
            self.createPog()
            return
        self.pogData = pog.clone()
        self.pogData.uuid = pog.uuid
        self.setupPogData()
        self.setSelectedInTree()

    def setupPogData(self):
        self.addingData = True
        self.pogNameEdit.setText(self.pogData.pogName)
        self.setPogType()
        self.setPogLocation()
        self.scene.clear()
        self.useSelectedPogPictureEdit.setText(self.pogData.pogImageUrl)
        self.setNotesData()
        self.setSizeData()
        self.playerFlags = self.pogData.playerFlags
        self.dmFlags = self.pogData.dungeonMasterFlags
        self.addingData = False
        self.isDirty = False
        self.validateForm()
        self.checkLoadImage()

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
        self.pogSizeComboBox.setCurrentIndex(pogSize)

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
        if self.addingData:
            return
        isOK = True
        dm: DungeonManager = ServicesManager.getDungeonManager()
        if not dm.isValidNewMonsterName(self.pogNameEdit.text()):
            isOK = False
            self.pogNameLabel.setStyleSheet('color: red')
        else:
            self.pogNameLabel.setStyleSheet('color: black')
        self.pogData.pogImageUrl = self.useSelectedPogPictureEdit.text()
        if not dm.isValidPictureURL(self.pogData.pogImageUrl):
            isOK = False
            self.useSelectedPogPictureEdit.setStyleSheet('color: red')
        else:
            self.useSelectedPogPictureEdit.setStyleSheet('color: black')
        self.savePogButton.setDisabled(not isOK or not self.isDirty)
        self.cancelPogButton.setDisabled(not self.isDirty)
        self.deletePogButton.setDisabled(not isOK)
        self.createPogButton.setDisabled(self.isDirty)
        if self.pictureDrag is not None:
            self.pictureDrag.doNotDrag = not isOK or self.isDirty

    def editNotes(self):
        if self.notesDialog.exec_():
            self.notes = self.notesDialog.getNotes()
            self.dmNotes = self.notesDialog.getDmNotes()
            self.isDirty = True
            self.validateForm()

    def useSelectedPicture(self):
        self.copyResourceURL()
        self.dataChanged()

    def copyResourceURL(self):
        dm: DungeonManager = ServicesManager.getDungeonManager()
        url = dm.assetURL
        if dm.isValidPictureURL(url):
            self.useSelectedPogPictureEdit.setText(url)

    def cancelEdit(self):
        self.selectPog()

    def pogDataChanged(self, pog):
        if pog is None:
            return
        if pog.isEqual(self.pogData):
            self.selectPog()

    def pictureDataChanged(self):
        self.dataChanged()
        self.checkLoadImage()

    def checkLoadImage(self):
        if self.imageLoading:
            return
        if ServicesManager.getDungeonManager().isValidPictureURL(self.pogData.pogImageUrl):
            self.imageLoading = True
            self.pogData.loadPogImage(self.successfulLoaded, self.failedLoad)

    def successfulLoaded(self):
        self.imageLoading = False
        self.scene.clear()
        image = self.pogData.image
        gw = self.graphicsView_3.width()
        gh = self.graphicsView_3.height()
        pixMap = QtGui.QPixmap.fromImage(image)
        scenePixMap = pixMap.scaled(gw, gh, QtCore.Qt.KeepAspectRatio,
                                    QtCore.Qt.SmoothTransformation)
        self.pictureDrag = MyPixmapItem()
        self.pictureDrag.doNotDrag = self.isDirty
        self.pictureDrag.setPixmap(scenePixMap)
        self.scene.addItem(self.pictureDrag)
        self.scene.setSceneRect(0, 0, scenePixMap.width(), scenePixMap.height())

    # noinspection PyUnusedLocal
    def failedLoad(self):
        self.imageLoading = False

    # noinspection PyMethodMayBeStatic
    def deletePog(self):
        ServicesManager.getDungeonManager().deleteSelectedPog()

    def saveFormData(self):
        self.isDirty = False
        self.validateForm()
        self.getDialogData()
        pog = self.pogData
        ServicesManager.getDungeonManager().addOrUpdatePog(pog, self.pogLocationComboBox.currentIndex())
        ServicesManager.getDungeonManager().setSelectedPog(pog)

    def getDialogData(self):
        self.pogData.pogName = self.pogNameEdit.text()
        self.pogData.pogType = self.pogTypeComboBox.currentText()
        self.pogData.pogImageUrl = self.useSelectedPogPictureEdit.text()
        self.pogData.pogSize = self.pogSizeComboBox.currentIndex() + 1
        self.pogData.playerFlags = self.playerFlags
        self.pogData.dungeonMasterFlags = self.dmFlags
        self.pogData.notes = self.notes
        self.pogData.dmNotes = self.dmNotes

    # noinspection PyAttributeOutsideInit
    def setupTree(self):
        self.treeWidget_2.setColumnCount(1)
        self.treeWidget_2.setHeaderHidden(True)
        self.treeWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.playersItem = QtWidgets.QTreeWidgetItem(['Players'])
        self.treeWidget_2.addTopLevelItem(self.playersItem)
        self.playersItem.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.commonResources = QtWidgets.QTreeWidgetItem(['Common Pog Resources'])
        self.treeWidget_2.addTopLevelItem(self.commonResources)
        self.monsterResources = QtWidgets.QTreeWidgetItem(['Monsters'])
        self.commonResources.addChild(self.monsterResources)
        self.monsterResources.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.roomResources = QtWidgets.QTreeWidgetItem(['Room Objects'])
        self.commonResources.addChild(self.roomResources)
        self.roomResources.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.dungeonPogs = QtWidgets.QTreeWidgetItem(['Dungeon Level Pogs'])
        self.treeWidget_2.addTopLevelItem(self.dungeonPogs)
        self.dungeonMonsters = QtWidgets.QTreeWidgetItem(['Monsters'])
        self.dungeonPogs.addChild(self.dungeonMonsters)
        self.dungeonMonsters.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.dungeonRooms = QtWidgets.QTreeWidgetItem(['Room Objects'])
        self.dungeonPogs.addChild(self.dungeonRooms)
        self.dungeonRooms.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.sessionPogs = QtWidgets.QTreeWidgetItem(['Session Level Pogs'])
        self.treeWidget_2.addTopLevelItem(self.sessionPogs)
        self.sessionMonsters = QtWidgets.QTreeWidgetItem(['Monsters'])
        self.sessionPogs.addChild(self.sessionMonsters)
        self.sessionMonsters.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.sessionRooms = QtWidgets.QTreeWidgetItem(['Room Objects'])
        self.sessionPogs.addChild(self.sessionRooms)
        self.sessionRooms.addChild(QtWidgets.QTreeWidgetItem(['dummy']))
        self.expandableItems = [
            self.playersItem,
            self.monsterResources,
            self.roomResources,
            self.dungeonMonsters,
            self.dungeonRooms,
            self.sessionMonsters,
            self.sessionRooms
        ]
        self.pogPlaces = [
            PogPlace.SESSION_RESOURCE,
            PogPlace.COMMON_RESOURCE,
            PogPlace.COMMON_RESOURCE,
            PogPlace.DUNGEON_LEVEL,
            PogPlace.DUNGEON_LEVEL,
            PogPlace.SESSION_LEVEL,
            PogPlace.SESSION_LEVEL
        ]
        self.pogTypes = [
            Constants.POG_TYPE_PLAYER,
            Constants.POG_TYPE_MONSTER,
            Constants.POG_TYPE_ROOMOBJECT,
            Constants.POG_TYPE_MONSTER,
            Constants.POG_TYPE_ROOMOBJECT,
            Constants.POG_TYPE_MONSTER,
            Constants.POG_TYPE_ROOMOBJECT
        ]

    def fillTrees(self):
        inEditMode = ServicesManager.getDungeonManager().editMode
        self.playersItem.setHidden(inEditMode)
        self.sessionPogs.setHidden(inEditMode)
        self.previousSelected = None
        index = 0
        for treeItem in self.expandableItems:
            if treeItem.isExpanded():
                self.buildSortedTree(treeItem, ServicesManager.getDungeonManager().getSortedList(self.pogPlaces[index],
                                                                                                 self.pogTypes[index]))
            index += 1

    def buildSortedTree(self, treeItem, pogs):
        if pogs is None:
            return
        self.clearBranch(treeItem)
        for pog in pogs:
            self.addTreeItem(treeItem, pog)

    # noinspection PyMethodMayBeStatic
    def addTreeItem(self, treeItem, pog):
        child = QtWidgets.QTreeWidgetItem([pog.pogName])
        child.setData(1, QtCore.Qt.EditRole, pog)
        treeItem.addChild(child)
        selectedPog = ServicesManager.getDungeonManager().getSelectedPog()
        if pog.isEqual(selectedPog):
            child.setSelected(True)

    # noinspection PyMethodMayBeStatic
    def clearBranch(self, branch):
        for i in range(branch.childCount()):
            branch.removeChild(branch.child(0))

    def nodeExpanded(self, index: QtCore.QModelIndex):
        expandedItem = self.treeWidget_2.itemFromIndex(index)
        self.FillNodeWithChildren(expandedItem)

    def FillNodeWithChildren(self, expandedItem):
        index = 0
        for treeItem in self.expandableItems:
            if treeItem == expandedItem:
                self.buildSortedTree(treeItem, ServicesManager.getDungeonManager().getSortedList(self.pogPlaces[index],
                                                                                                 self.pogTypes[index]))
                break
            index += 1

    # noinspection PyUnusedLocal
    def treeItemSelected(self, *args):
        if len(self.treeWidget_2.selectedItems()) == 0:
            return
        selItem = self.treeWidget_2.selectedItems()[0]
        data = selItem.data(1, QtCore.Qt.EditRole)
        if data is not None:
            ServicesManager.getDungeonManager().setSelectedPog(data)

    def setSelectedInTree(self):
        if self.justDidSelection:
            self.justDidSelection = False
            return
        if self.previousSelected is not None:
            self.previousSelected.setSelected(False)
        index = 0
        for place in self.pogPlaces:
            if place == self.pogData.pogPlace:
                parent: QtWidgets.QTreeWidgetItem = self.expandableItems[index]
                if not parent.isHidden() and parent.isExpanded():
                    for childIndex in range(parent.childCount()):
                        child = parent.child(childIndex)
                        data = child.data(1, QtCore.Qt.EditRole)
                        if self.pogData.isEqual(data):
                            self.justDidSelection = True
                            child.setSelected(True)
                            self.previousSelected = child
                            return
            index += 1
