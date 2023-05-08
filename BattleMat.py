"""
GPL 3 file header
"""
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from services.DungeonManager import DungeonManager
from services.EventManager import EventManager
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.Utilities import MyConfigManager
from views.DungeonManagerDialog import DungeonManagerDialog
from views.LoginDialog import LoginDialog
from views.ArtAssetsTab import ArtAssetsTab
from views.BattleMatScene import BattleMatScene
from views.DungeonEditorTab import DungeonEditorTab
from views.PogEditorTab import PogEditorTab
from views.RibbonBar import RibbonBar


class MainWindow(QMainWindow):
	dungeonManagerDialog = None
	loginDialog = None
	timer = None

	def __init__(self):
		super(MainWindow, self).__init__()
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
		self.splitter.setMinimumSize(QtCore.QSize(0, 500))
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
		self.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.artAssetsTab),
											_translate("MainWindow", "Art Assets"))
		self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.monsterEditorTab),
											_translate("MainWindow", "Monster Editor"))
		self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.pogEditorTab),
											_translate("MainWindow", "Pog Editor"))

	def mouseDoubleClickEvent(self, event):
		self.scene.computeInitialZoom()

	def show(self):
		super(MainWindow, self).show()

	def appStarted(self):
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.doTimeBasedTasks)
		self.timer.start(1000)
		self.loginDialog = LoginDialog()
		self.loginDialog.show()
		self.dungeonManagerDialog = DungeonManagerDialog()
		pass

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForAction.LOGGED_IN:
			self.loggedIn(eventData.eventData)

	# noinspection PyUnusedLocal
	def loggedIn(self, succeeded):
		self.loginDialog = None
		self.dungeonManagerDialog.show()

	# noinspection PyMethodMayBeStatic
	def doTimeBasedTasks(self):
		ServicesManager.getDungeonManager().doTimeBasedTasks()
		pass


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ServicesManager.setEventManager(EventManager())
	ServicesManager.setConfigManager(MyConfigManager())
	ServicesManager.setDungeonManager(DungeonManager())
	app.mainWindow = MainWindow()
	app.mainWindow.show()
	app.mainWindow.appStarted()
	sys.exit(app.exec_())
