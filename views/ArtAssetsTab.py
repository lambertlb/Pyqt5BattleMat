"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore


class ArtAssetsTab(QtWidgets.QWidget):

	def __init__(self, *args):
		super(ArtAssetsTab, self).__init__(*args)
		self.artAssetsTab = self
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.artAssetsTab)
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.downLoadAssetButton = QtWidgets.QPushButton(self.artAssetsTab)
		self.gridLayout_3.addWidget(self.downLoadAssetButton, 0, 0, 1, 1)
		self.upLoadButton = QtWidgets.QPushButton(self.artAssetsTab)
		self.gridLayout_3.addWidget(self.upLoadButton, 0, 2, 1, 1)
		self.deleteAssetButton = QtWidgets.QPushButton(self.artAssetsTab)
		self.gridLayout_3.addWidget(self.deleteAssetButton, 0, 1, 1, 1)
		self.verticalLayout_3.addLayout(self.gridLayout_3)
		self.treeWidget = QtWidgets.QTreeWidget(self.artAssetsTab)
		self.treeWidget.headerItem().setText(0, "1")
		self.verticalLayout_3.addWidget(self.treeWidget)
		self.graphicsView = QtWidgets.QGraphicsView(self.artAssetsTab)
		self.graphicsView.setMaximumSize(QtCore.QSize(50, 50))
		self.verticalLayout_3.addWidget(self.graphicsView)

		self.localize()

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.downLoadAssetButton.setText(_translate("MainWindow", "Download Asset"))
		self.upLoadButton.setText(_translate("MainWindow", "Upload Asset"))
		self.deleteAssetButton.setText(_translate("MainWindow", "Delete Asset"))
