"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager


class DungeonEditorTab(QtWidgets.QWidget):

	def __init__(self, *args):
		super(DungeonEditorTab, self).__init__(*args)
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
		self.graphicsView_2 = QtWidgets.QGraphicsView(self.monsterEditorTab)
		self.gridLayout_5.addWidget(self.graphicsView_2, 7, 0, 1, 4)
		self.verticalLayout_4.addLayout(self.gridLayout_5)

		self.setupEvents()
		self.localize()

	def localize(self):
		_translate = QtCore.QCoreApplication.translate

		self.newLevelButton.setText(_translate("MainWindow", "New Level"))
		self.manageDungeonsButton.setText(_translate("MainWindow", "Manage Dungeons"))
		self.deleteLevelButton.setText(_translate("MainWindow", "DELETE Level"))
		self.levelNameLabel.setText(_translate("MainWindow", "Level Name"))
		self.showGridCheckBox.setText(_translate("MainWindow", "Show Grid"))
		self.gridSizeButton.setText(_translate("MainWindow", "Grid Size"))
		self.gridSizeEdit.setText(_translate("MainWindow", "30"))
		self.offsetXLabel.setText(_translate("MainWindow", "Offset X"))
		self.offsetXEdit.setText(_translate("MainWindow", "0"))
		self.offsetYLabel.setText(_translate("MainWindow", "Offset Y"))
		self.offsetYEdit.setText(_translate("MainWindow", "0"))
		self.useSelectedPictureButton.setText(_translate("MainWindow", "Use Selected\n"
"Picture Resource"))
		self.saveButton.setText(_translate("MainWindow", "Save"))
		self.cancelButton.setText(_translate("MainWindow", "Cancel"))

	def setupEvents(self):
		self.manageDungeonsButton.clicked.connect(self.manageDungeons)
		pass

	# noinspection PyMethodMayBeStatic
	def manageDungeons(self):
		ServicesManager.getEventManager().fireEvent(ReasonForAction.LOGGED_IN, True)
