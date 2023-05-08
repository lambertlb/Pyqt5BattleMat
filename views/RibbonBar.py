"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from views.DragButton import DragButton


class RibbonBar(QtWidgets.QGridLayout):

	def	__init__(self, frame, *args):
		super(RibbonBar, self).__init__(*args)
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
		self.selectedPogArea_2 = QtWidgets.QGraphicsView(self.frame)
		self.selectedPogArea_2.setMinimumSize(QtCore.QSize(50, 50))
		self.selectedPogArea_2.setMaximumSize(QtCore.QSize(50, 50))
		self.gridLayout_2.addWidget(self.selectedPogArea_2, 0, 0, 2, 1)
		self.selectDungeonLevel_2 = QtWidgets.QComboBox(self.frame)
		self.selectDungeonLevel_2.setMinimumSize(QtCore.QSize(200, 0))
		self.gridLayout_2.addWidget(self.selectDungeonLevel_2, 0, 1, 1, 1)
		self.showPogNotes_2 = QtWidgets.QCheckBox(self.frame)
		self.gridLayout_2.addWidget(self.showPogNotes_2, 1, 2, 1, 1)

		self.localize()

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.toggleFOW_2.setText(_translate("MainWindow", "Toggle FOW"))
		self.showSelectedPog_2.setText(_translate("MainWindow", "Show Selected Pog"))
		self.hideFOW_2.setText(_translate("MainWindow", "Hide FOW"))
		self.showPogNotes_2.setText(_translate("MainWindow", "Show Pog Notes"))
