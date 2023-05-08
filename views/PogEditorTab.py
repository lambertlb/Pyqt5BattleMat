"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore


class PogEditorTab(QtWidgets.QWidget):

	def __init__(self, *args):
		super(PogEditorTab, self).__init__(*args)
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
