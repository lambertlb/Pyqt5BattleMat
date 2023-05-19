"""
GPL 3 file header
"""
import json

from PyQt5 import QtWidgets, QtCore

from services.Constants import Constants
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager


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
		self.verticalLayout_3.addWidget(self.treeWidget)
		self.graphicsView = QtWidgets.QGraphicsView(self.artAssetsTab)
		self.graphicsView.setMaximumSize(QtCore.QSize(50, 50))
		self.verticalLayout_3.addWidget(self.graphicsView)

		self.localize()
		self.treeWidget.setColumnCount(1)
		self.treeWidget.setHeaderHidden(True)
		self.dungeonAssets = QtWidgets.QTreeWidgetItem(['Dungeon Assets'])
		self.treeWidget.addTopLevelItem(self.dungeonAssets)
		self.monsterAssets = QtWidgets.QTreeWidgetItem(['Global Monster Assets'])
		self.treeWidget.addTopLevelItem(self.monsterAssets)
		self.roomAssets = QtWidgets.QTreeWidgetItem(['Global Room Assets'])
		self.treeWidget.addTopLevelItem(self.roomAssets)
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)


	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.downLoadAssetButton.setText(_translate("MainWindow", "Download Asset"))
		self.upLoadButton.setText(_translate("MainWindow", "Upload Asset"))
		self.deleteAssetButton.setText(_translate("MainWindow", "Delete Asset"))

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForAction.DungeonDataLoaded:
			self.loadFiles()
		elif eventData.eventReason == ReasonForAction.SessionDataSaved:
			self.loadFiles()

	def loadFiles(self):
		self.disableButtons()
		dm = ServicesManager.getDungeonManager()
		dm.getFileList(dm.getDirectoryForCurrentDungeon(), self.onSuccessGetFilelist, self.onFailedGetFilelist)
		dm.getFileList(Constants.DungeonData + Constants.Monsters, self.onSuccessGetFilelist, self.onFailedGetFilelist)
		dm.getFileList(Constants.DungeonData + Constants.RoomObjects, self.onSuccessGetFilelist, self.onFailedGetFilelist)

	def onSuccessGetFilelist(self, data):
		fileList = json.loads(data)
		self.buildTreeOfAssets(fileList)
		pass

	def onFailedGetFilelist(self):
		pass

	def buildTreeOfAssets(self, fileList):
		filePath = fileList['filePath']
		if not 'fileNames' in fileList:
			return
		fileNames = fileList['fileNames']
		itemToPopulate = None
		if 'dungeons' in filePath:
			itemToPopulate = self.dungeonAssets
		elif 'monsters' in filePath:
			itemToPopulate = self.monsterAssets
		else:
			itemToPopulate = self.roomAssets
		for i in range(itemToPopulate.childCount()):
			itemToPopulate.removeChild(itemToPopulate.child(0))
		itemToPopulate.setData(1, QtCore.Qt.EditRole, filePath)
		for fileName in fileNames:
			treeItem = QtWidgets.QTreeWidgetItem([fileName])
			itemToPopulate.addChild(treeItem)
			treeItem.setData(1, QtCore.Qt.EditRole, fileName)
		pass

	def disableButtons(self):
		pass
