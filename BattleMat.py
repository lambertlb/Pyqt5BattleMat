"""
GPL 3 file header
"""
import sys

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QMainWindow

from services.DungeonManager import DungeonManager
from services.EventManager import EventManager
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.ConfigurationManager import ConfigManager
from views.ArtAssetsTab import ArtAssetsTab
from views.BattleMatScene import BattleMatScene
from views.DungeonEditorTab import DungeonEditorTab
from views.DungeonManagerDialog import DungeonManagerDialog
from views.LoginDialog import LoginDialog
from views.PogEditorTab import PogEditorTab
from views.RibbonBar import RibbonBar


class MainWindow(QMainWindow):
    """
    This is the main window for the application.
    It was originally generated from builder/MainWindow.ui
    I edited it so that I could split oot the various parts
    of the window into separate components line RibbonBar,
    BattMatArea, and one component for each tab in the
    tabbed panel
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.dungeonManagerDialog = None
        self.loginDialog = None
        self.timer = None

        self.resize(2000, 1200)
        self.centralWidget = QtWidgets.QWidget(self)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.gridLayout_2 = RibbonBar(self.frame)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.splitter = QtWidgets.QSplitter(self.frame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(5)
        self.scene = BattleMatScene(self.splitter)

        self.assetManagementTabs = QtWidgets.QTabWidget(self.splitter)
        self.artAssetsTab = ArtAssetsTab()
        self.assetManagementTabs.addTab(self.artAssetsTab, "")

        self.monsterEditorTab = DungeonEditorTab()
        self.assetManagementTabs.addTab(self.monsterEditorTab, "")

        self.pogEditorTab = PogEditorTab()
        self.assetManagementTabs.addTab(self.pogEditorTab, "")

        self.verticalLayout.addWidget(self.splitter)
        self.verticalLayout_2.addWidget(self.frame)
        self.setCentralWidget(self.centralWidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.splitter.setSizes([600, 200])

        self.localize()
        self.assetManagementTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        ServicesManager.getEventManager().subscribeToEvent(self.eventFired)

    def localize(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("MainWindow")
        self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.artAssetsTab), "Art Assets")
        self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.monsterEditorTab), "Dungeon Editor")
        self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.pogEditorTab), "Pog Editor")

    def mouseDoubleClickEvent(self, event):
        self.scene.computeInitialZoom()

    def show(self):
        super(MainWindow, self).show()

    def appStarted(self):
        """
        Application has start so start up time based tasks
        and bring up the login window
        """
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.doTimeBasedTasks)
        self.timer.start(1000)
        self.loginDialog = LoginDialog()
        self.loginDialog.show()
        self.dungeonManagerDialog = DungeonManagerDialog(False)

    def eventFired(self, eventData):
        """
        Handle event bus signals
        """
        if eventData.eventReason == ReasonForAction.LOGGED_IN:
            self.loggedIn(eventData.eventData)
        elif eventData.eventReason == ReasonForAction.DungeonDataReadyToEdit:
            self.dungeonDataChanged()
        elif eventData.eventReason == ReasonForAction.DungeonDataReadyToJoin:
            self.dungeonDataChanged()
        elif eventData.eventReason == ReasonForAction.DungeonDataSaved:
            self.dungeonDataChanged()

    def dungeonDataChanged(self):
        isDM = ServicesManager.getDungeonManager().isDungeonMaster
        # hide the splitter if not dm
        if isDM:
            panel1Width = int(self.width() * .75)
            panel2Width = int(self.width() * .25)
        else:
            panel1Width = self.width()
            panel2Width = 0
        self.splitter.setSizes([panel1Width, panel2Width])

    # noinspection PyUnusedLocal
    def loggedIn(self, succeeded):
        """
        We successfully logged in so select a dungeon
        """
        self.loginDialog = None
        self.dungeonManagerDialog.show()

    # noinspection PyMethodMayBeStatic
    def doTimeBasedTasks(self):
        ServicesManager.getDungeonManager().doTimeBasedTasks()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # add various managers to the Services manager
    # I find doing this easier that doing dependency injection
    # everywhere in the application
    ServicesManager.setEventManager(EventManager())
    ServicesManager.setConfigManager(ConfigManager())
    ServicesManager.setDungeonManager(DungeonManager())
    app.mainWindow = MainWindow()
    app.mainWindow.show()
    app.mainWindow.appStarted()
    sys.exit(app.exec())
