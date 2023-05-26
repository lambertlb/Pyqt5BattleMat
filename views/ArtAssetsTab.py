"""
GPL 3 file header
"""
import json
import os
from os.path import expanduser

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
		self.downLoadAssetButton.clicked.connect(self.downloadAsset)
		self.gridLayout_3.addWidget(self.downLoadAssetButton, 0, 0, 1, 1)
		self.upLoadButton = QtWidgets.QPushButton(self.artAssetsTab)
		self.upLoadButton.clicked.connect(self.uploadAsset)
		self.gridLayout_3.addWidget(self.upLoadButton, 0, 2, 1, 1)
		self.deleteAssetButton = QtWidgets.QPushButton(self.artAssetsTab)
		self.deleteAssetButton.clicked.connect(self.deleteAsset)
		self.gridLayout_3.addWidget(self.deleteAssetButton, 0, 1, 1, 1)
		self.verticalLayout_3.addLayout(self.gridLayout_3)
		self.treeWidget = QtWidgets.QTreeWidget(self.artAssetsTab)
		self.verticalLayout_3.addWidget(self.treeWidget)
		self.filePath = QtWidgets.QLineEdit(self.artAssetsTab)
		self.filePath.setReadOnly(False)
		self.verticalLayout_3.addWidget(self.filePath)

		self.localize()
		self.treeWidget.setColumnCount(1)
		self.treeWidget.setHeaderHidden(True)
		self.dungeonAssets = QtWidgets.QTreeWidgetItem(['Dungeon Assets'])
		self.treeWidget.addTopLevelItem(self.dungeonAssets)
		self.monsterAssets = QtWidgets.QTreeWidgetItem(['Global Monster Assets'])
		self.treeWidget.addTopLevelItem(self.monsterAssets)
		self.roomAssets = QtWidgets.QTreeWidgetItem(['Global Room Assets'])
		self.treeWidget.addTopLevelItem(self.roomAssets)
		self.treeWidget.selectionModel().selectionChanged.connect(self.treeItemSelected)
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
		self.clearBranches()
		dm = ServicesManager.getDungeonManager()
		dm.getFileList(dm.getDirectoryForCurrentDungeon(), self.onSuccessGetFilelist, self.onFailedGetFilelist)
		dm.getFileList(Constants.DungeonData + Constants.Monsters, self.onSuccessGetFilelist, self.onFailedGetFilelist)
		dm.getFileList(Constants.DungeonData + Constants.RoomObjects, self.onSuccessGetFilelist, self.onFailedGetFilelist)

	def onSuccessGetFilelist(self, data):
		fileList = json.loads(data)
		self.buildTreeOfAssets(fileList)

	def onFailedGetFilelist(self):
		pass

	def buildTreeOfAssets(self, fileList):
		filePath = fileList['filePath']
		if 'fileNames' not in fileList:
			return
		fileNames = fileList['fileNames']
		if 'dungeons' in filePath:
			itemToPopulate = self.dungeonAssets
		elif 'monsters' in filePath:
			itemToPopulate = self.monsterAssets
		else:
			itemToPopulate = self.roomAssets
		itemToPopulate.setData(1, QtCore.Qt.EditRole, filePath)
		for fileName in fileNames:
			treeItem = QtWidgets.QTreeWidgetItem([fileName])
			itemToPopulate.addChild(treeItem)
			treeItem.setData(1, QtCore.Qt.EditRole, fileName)

	def clearBranches(self):
		self.clearBranch(self.dungeonAssets)
		self.clearBranch(self.monsterAssets)
		self.clearBranch(self.roomAssets)

	# noinspection PyMethodMayBeStatic
	def clearBranch(self, branch):
		for i in range(branch.childCount()):
			branch.removeChild(branch.child(0))

	def disableButtons(self):
		self.downLoadAssetButton.setDisabled(True)
		self.upLoadButton.setDisabled(True)
		self.deleteAssetButton.setDisabled(True)

	# noinspection PyUnusedLocal
	def treeItemSelected(self, *args):
		selItem = self.treeWidget.selectedItems()[0]
		data = selItem.data(1, QtCore.Qt.EditRole)
		self.disableButtons()
		if data is None:
			return
		if data.startswith("/"):
			self.upLoadButton.setDisabled(False)
			return
		if data.endswith(".json"):
			self.downLoadAssetButton.setDisabled(False)
			self.upLoadButton.setDisabled(False)
			return

		self.deleteAssetButton.setDisabled(False)
		self.downLoadAssetButton.setDisabled(False)
		self.upLoadButton.setDisabled(False)
		url = self.buildUrlToFilename(data)
		self.filePath.setText(url)
		ServicesManager.getDungeonManager().setAssetURL(url)

	def buildUrlToFilename(self, filename):
		selected = self.treeWidget.selectedItems()[0]
		if "/" not in filename:
			selected = selected.parent()
		i = filename.rfind('/')
		if i == -1:
			i = filename.rfind('\\')
		rtnName = filename
		if i != -1 and (i + 1) < len(filename):
			rtnName = filename[0, i + 1]
		base = selected.data(1, QtCore.Qt.EditRole)
		if not base.endswith('/') and not base.endswith('\\'):
			base = base + '/'
		url = base + rtnName
		return url

	def downloadAsset(self):
		selected = self.treeWidget.selectedItems()[0]
		filename = selected.data(1, QtCore.Qt.EditRole)
		folder = selected.parent().data(1, QtCore.Qt.EditRole)
		dstFolder = QtWidgets.QFileDialog.getExistingDirectory(
			self,
			"Open a folder",
			expanduser("~"),
			QtWidgets.QFileDialog.ShowDirsOnly
		)
		if not dstFolder:
			return
		ServicesManager.getDungeonManager().downloadFile(folder, filename, dstFolder)

	def uploadAsset(self):
		dialog = QtWidgets.QFileDialog(self)
		dialog.setNameFilters(['All Files (*)'])
		dialog.setDefaultSuffix('.jpg')
		filePath, afilter = dialog.getOpenFileName(self, 'Open file')
		if not filePath:
			return
		folder, filename = os.path.split(filePath)
		selected = self.treeWidget.selectedItems()[0]
		whereOnServer = selected.data(1, QtCore.Qt.EditRole)
		if "/" not in whereOnServer:
			selected = selected.parent()
		whereOnServer = selected.data(1, QtCore.Qt.EditRole)
		ServicesManager.getDungeonManager().uploadFile(whereOnServer,
													folder, filename, self.onSuccessfulUpload, self.onFailureUpload)

	def onSuccessfulUpload(self):
		self.loadFiles()

	def onFailureUpload(self):
		pass

	def deleteAsset(self):
		fileItem = self.treeWidget.selectedItems()[0]
		filename = fileItem.data(1, QtCore.Qt.EditRole)
		parentItem = fileItem.parent()
		whereOnServer = parentItem.data(1, QtCore.Qt.EditRole)
		ServicesManager.getDungeonManager().deleteFile(whereOnServer,
													filename, self.onSuccessfulUpload, self.onFailureUpload)
		pass
