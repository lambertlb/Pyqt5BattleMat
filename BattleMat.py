"""
GPL 3 file header
"""
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from services.DungeonManager import DungeonManager
from services.EventManager import EventManager
from services.ReasonForEvent import ReasonForEvent
from services.ServicesManager import ServicesManager
from services.Utilities import MyConfigManager
from views.AssetManagement import AssetManagement
from views.BattleMatScene import BattleMatScene
from views.LoginDialog import LoginDialog
from views.RibbonBar import RibbonBar


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.resize(800, 600)
		self.centralWidget = QtWidgets.QWidget()
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
		self.windowFrame = QtWidgets.QFrame(self.centralWidget)
		self.windowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.windowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.gridLayout = QtWidgets.QGridLayout(self.windowFrame)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.ribbonBar = RibbonBar(self.windowFrame)
		self.splitter = QtWidgets.QSplitter(self.windowFrame)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		self.scene = BattleMatScene(self.splitter)
		self.gridLayout.addLayout(self.ribbonBar, 0, 0, 1, 1)
		self.assetHolder = AssetManagement(self.splitter)
		self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
		self.gridLayout_2.addWidget(self.windowFrame, 0, 0, 1, 1)
		self.setCentralWidget(self.centralWidget)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.setStatusBar(self.statusbar)

		self.splitter.setSizes([600, 200])
		self.localize()
		self.loginDialog = LoginDialog()
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle("MainWindow")

	def mouseDoubleClickEvent(self, event):
		self.scene.computeInitialZoom()

	def show(self):
		super(MainWindow, self).show()

	def appStarted(self):
		self.loginDialog.show()

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForEvent.LOGGED_IN:
			self.loggedIn()

	def loggedIn(self):
		self.scene.loadImage('image/level1.jpg')
		self.scene.addButtonToScene(100, 100)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	ServicesManager.setEventManager(EventManager())
	ServicesManager.setConfigManager(MyConfigManager())
	ServicesManager.setDungeonManager(DungeonManager())
	app.mainWindow = MainWindow()
	app.mainWindow.show()
	app.mainWindow.appStarted()
	sys.exit(app.exec_())
