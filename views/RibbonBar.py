"""
GPL 3 file header
"""
import webbrowser

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

from services.Constants import Constants
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.PogData import PogData
from views.PogNotesView import PogNotesViewer
from views.PogViewer import PogViewer


class MyPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, *args):
        super(MyPixmapItem, self).__init__(*args)
        fl = self.flags()
        fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        fl |= QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        self.setFlags(fl)
        self.doNotDrag = False

    def mouseMoveEvent(self, event):
        """
        Move moved on me so start dragging
        :param event: event
        :return: None
        """
        if self.doNotDrag:
            return

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

    def __init__(self, frame, *args):
        super(RibbonBar, self).__init__(*args)
        self.selectedPog: PogData | None = None
        self.pogSize = 70
        self.pogDialog = None
        self.pogNotesDialog: PogNotesViewer | None = None

        self.frame = frame
        self.gridLayout_2 = self
        self.selectPlayer_2 = QtWidgets.QComboBox(self.frame)
        self.selectPlayer_2.activated[str].connect(self.onPlayerChanged)
        self.gridLayout_2.addWidget(self.selectPlayer_2, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 5, 1, 1)
        self.toggleFOW_2 = QtWidgets.QCheckBox(self.frame)
        self.gridLayout_2.addWidget(self.toggleFOW_2, 1, 3, 1, 1)
        self.showSelectedPog_2 = QtWidgets.QCheckBox(self.frame)
        self.showSelectedPog_2.stateChanged.connect(self.handleSelectedPog)
        self.gridLayout_2.addWidget(self.showSelectedPog_2, 0, 2, 1, 1)
        self.hideFOW_2 = QtWidgets.QCheckBox(self.frame)
        self.gridLayout_2.addWidget(self.hideFOW_2, 0, 3, 1, 1)
        self.hideFOW_2.stateChanged.connect(self.toggleFOW)
        self.scene = QtWidgets.QGraphicsScene(self.frame)
        self.selectedPogArea_2 = QtWidgets.QGraphicsView(self.scene)
        self.selectedPogArea_2.setMinimumSize(QtCore.QSize(self.pogSize, self.pogSize))
        self.selectedPogArea_2.setMaximumSize(QtCore.QSize(self.pogSize, self.pogSize))
        self.scene.setSceneRect(0, 0, self.pogSize, self.pogSize)
        self.selectedPogArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.selectedPogArea_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gridLayout_2.addWidget(self.selectedPogArea_2, 0, 0, 2, 1)
        self.selectDungeonLevel_2 = QtWidgets.QComboBox(self.frame)
        self.selectDungeonLevel_2.setMinimumSize(QtCore.QSize(400, 0))
        self.selectDungeonLevel_2.activated[str].connect(self.onLevelChanged)
        self.gridLayout_2.addWidget(self.selectDungeonLevel_2, 0, 1, 1, 1)
        self.showPogNotes_2 = QtWidgets.QCheckBox(self.frame)
        self.showPogNotes_2.stateChanged.connect(self.handleSelectedPogNotes)
        self.gridLayout_2.addWidget(self.showPogNotes_2, 1, 2, 1, 1)
        self.helpButton = QtWidgets.QPushButton(self.frame)
        self.gridLayout_2.addWidget(self.helpButton, 0, 4, 1, 1)
        self.helpButton.clicked.connect(self.helpMe)

        self.localize()
        ServicesManager.getEventManager().subscribeToEvent(self.eventFired)

    def localize(self):
        self.toggleFOW_2.setText("Toggle FOW")
        self.showSelectedPog_2.setText("Show Selected Pog")
        self.hideFOW_2.setText("Hide FOW")
        self.showPogNotes_2.setText("Show Pog Notes")
        self.helpButton.setText("Help")

    def eventFired(self, eventData):
        if eventData.eventReason == ReasonForAction.DMStateChange:
            self.setupView()
        elif eventData.eventReason == ReasonForAction.DungeonDataLoaded:
            self.dungeonDataLoaded()
        elif eventData.eventReason == ReasonForAction.DungeonDataSaved:
            self.dungeonDataLoaded()
        elif eventData.eventReason == ReasonForAction.SessionDataChanged:
            self.characterPogsLoaded()
        elif eventData.eventReason == ReasonForAction.DungeonDataReadyToJoin:
            self.characterPogsLoaded()
        elif eventData.eventReason == ReasonForAction.PogWasSelected:
            self.pogSelection()

    def pogSelection(self):
        selectedPog: PogData = ServicesManager.getDungeonManager().getSelectedPog()
        if self.selectedPog is not None:
            if self.selectedPog.isEqual(selectedPog):
                return
        self.selectedPog = selectedPog
        if self.selectedPog is not None:
            self.selectedPog.loadPogImage(self.successfulLoaded, self.failedLoad)
        else:
            self.scene.clear()
        if self.pogNotesDialog is not None:
            if self.selectedPog is not None:
                self.pogNotesDialog.setNotes(self.selectedPog.notes)
                self.pogNotesDialog.setDmNotes(self.selectedPog.dmNotes)
            else:
                self.pogNotesDialog.setNotes('')
                self.pogNotesDialog.setDmNotes('')

    def successfulLoaded(self):
        self.scene.clear()
        image = self.selectedPog.image
        pixMap = QtGui.QPixmap.fromImage(image)
        scenePixMap = pixMap.scaled(self.pogSize, self.pogSize, QtCore.Qt.KeepAspectRatio,
                                    QtCore.Qt.SmoothTransformation)
        pm = MyPixmapItem()
        pm.setPixmap(scenePixMap)
        self.scene.addItem(pm)

    def failedLoad(self):
        pass

    def setupView(self):
        editMode = ServicesManager.getDungeonManager().editMode
        isDM = ServicesManager.getDungeonManager().isDungeonMaster
        self.selectPlayer_2.setVisible(not editMode)
        self.toggleFOW_2.setVisible(False)
        # self.toggleFOW_2.setVisible(not editMode and isDM)
        self.hideFOW_2.setVisible(not editMode and isDM)

    def dungeonDataLoaded(self):
        self.selectDungeonLevel_2.clear()
        levelNames = ServicesManager.getDungeonManager().getDungeonLevelNames()
        for levelName in levelNames:
            self.selectDungeonLevel_2.addItem(levelName)
        self.selectDungeonLevel_2.setCurrentIndex(ServicesManager.getDungeonManager().currentLevelIndex)

    def characterPogsLoaded(self):
        self.selectPlayer_2.clear()
        self.selectPlayer_2.addItem("Select Character Pog", "")
        players = ServicesManager.getDungeonManager().getPlayersForCurrentSession()
        if players is None:
            return
        for pogData in players:
            self.selectPlayer_2.addItem(pogData.pogName, pogData.uuid)

    # noinspection PyUnusedLocal
    def onLevelChanged(self, text):
        ServicesManager.getDungeonManager().currentLevelIndex = self.selectDungeonLevel_2.currentIndex()

    # noinspection PyUnusedLocal
    def onPlayerChanged(self, text):
        uuid = self.selectPlayer_2.currentData()
        if uuid is None or uuid == '':
            return
        characterPog = ServicesManager.getDungeonManager().findCharacterPog(uuid)
        if characterPog is not None:
            ServicesManager.getDungeonManager().setSelectedPog(characterPog)

    def handleSelectedPog(self):
        if self.pogDialog is None:
            mainWindow = QtCore.QCoreApplication.instance().mainWindow
            self.pogDialog = PogViewer(mainWindow)
        if self.showSelectedPog_2.isChecked():
            self.pogDialog.show()
        else:
            self.pogDialog.hide()

    def handleSelectedPogNotes(self):
        if self.pogNotesDialog is None:
            mainWindow = QtCore.QCoreApplication.instance().mainWindow
            self.pogNotesDialog = PogNotesViewer(mainWindow)
            self.pogNotesDialog.showButtons(False)
        if self.showPogNotes_2.isChecked():
            self.pogNotesDialog.show()
        else:
            self.pogNotesDialog.hide()

    def toggleFOW(self):
        ServicesManager.getDungeonManager().setHideFOW(self.hideFOW_2.isChecked())

    # noinspection PyMethodMayBeStatic
    def helpMe(self):
        url = ServicesManager.getConfigManager().getValue(Constants.Login_Url, '')
        url += "/help.html"
        webbrowser.open(url)
