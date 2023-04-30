"""
GPL 3 file header
"""
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from views.BattleMatScene import BattleMatScene
from views.DragButton import DragButton


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setObjectName("MainWindow")
		self.resize(800, 600)
		self.centralWidget = QtWidgets.QWidget()
		self.centralWidget.setObjectName("centralWidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.windowFrame = QtWidgets.QFrame(self.centralWidget)
		self.windowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.windowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.windowFrame.setObjectName("windowFrame")
		self.gridLayout = QtWidgets.QGridLayout(self.windowFrame)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.ribbonBar = QtWidgets.QHBoxLayout()
		self.ribbonBar.setObjectName("ribbonBar")
		self.splitter = QtWidgets.QSplitter(self.windowFrame)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		self.splitter.setObjectName("splitter")
		self.scene = BattleMatScene(self.splitter)

		self.button3 = DragButton(self.windowFrame)
		self.button3.setObjectName("button3")
		self.button3.clicked.connect(self.scene.loadAnImage)
		self.ribbonBar.addWidget(self.button3)
		self.button2 = DragButton(self.windowFrame)
		self.button2.setObjectName("button2")
		self.button2.clicked.connect(self.scene.loadAnImage)
		self.ribbonBar.addWidget(self.button2)
		self.button1 = DragButton(self.windowFrame)
		self.button1.setObjectName("button1")
		self.button1.clicked.connect(self.scene.loadAnImage)
		self.ribbonBar.addWidget(self.button1)
		self.gridLayout.addLayout(self.ribbonBar, 0, 0, 1, 1)

		self.assetHolder = QtWidgets.QTabWidget(self.splitter)
		self.assetHolder.setObjectName("assetHolder")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.assetHolder.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.assetHolder.addTab(self.tab_2, "")

		self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
		self.gridLayout_2.addWidget(self.windowFrame, 0, 0, 1, 1)
		self.setCentralWidget(self.centralWidget)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)

		self.splitter.setSizes([600, 200])
		self.localize()
		self.scene.loadAnImage()
		self.scene.addButtonToScene(100, 100)

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.setWindowTitle("MainWindow")
		self.button3.setText("PushButton")
		self.button2.setText("PushButton")
		self.button1.setText("PushButton")
		self.assetHolder.setTabText(self.assetHolder.indexOf(self.tab), "Tab 1")
		self.assetHolder.setTabText(self.assetHolder.indexOf(self.tab_2), "Tab 2")

	def keyPressEvent(self, event):
		"""
		Update picture when a key is pressed
		:param event:
		:return:
		"""
		self.scene.loadAnImage()

	def mouseDoubleClickEvent(self, event):
		self.scene.computeInitialZoom()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	app.mainWindow = MainWindow()
	app.mainWindow.show()
	sys.exit(app.exec_())
