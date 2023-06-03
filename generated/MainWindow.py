# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(832, 644)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.selectPlayer_2 = QComboBox(self.frame)
        self.selectPlayer_2.setObjectName(u"selectPlayer_2")

        self.gridLayout_2.addWidget(self.selectPlayer_2, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.toggleFOW_2 = QCheckBox(self.frame)
        self.toggleFOW_2.setObjectName(u"toggleFOW_2")

        self.gridLayout_2.addWidget(self.toggleFOW_2, 1, 3, 1, 1)

        self.showSelectedPog_2 = QCheckBox(self.frame)
        self.showSelectedPog_2.setObjectName(u"showSelectedPog_2")

        self.gridLayout_2.addWidget(self.showSelectedPog_2, 0, 2, 1, 1)

        self.hideFOW_2 = QCheckBox(self.frame)
        self.hideFOW_2.setObjectName(u"hideFOW_2")

        self.gridLayout_2.addWidget(self.hideFOW_2, 0, 3, 1, 1)

        self.selectedPogArea_2 = QGraphicsView(self.frame)
        self.selectedPogArea_2.setObjectName(u"selectedPogArea_2")
        self.selectedPogArea_2.setMinimumSize(QSize(50, 50))
        self.selectedPogArea_2.setMaximumSize(QSize(50, 50))

        self.gridLayout_2.addWidget(self.selectedPogArea_2, 0, 0, 2, 1)

        self.selectDungeonLevel_2 = QComboBox(self.frame)
        self.selectDungeonLevel_2.setObjectName(u"selectDungeonLevel_2")
        self.selectDungeonLevel_2.setMinimumSize(QSize(200, 0))

        self.gridLayout_2.addWidget(self.selectDungeonLevel_2, 0, 1, 1, 1)

        self.showPogNotes_2 = QCheckBox(self.frame)
        self.showPogNotes_2.setObjectName(u"showPogNotes_2")

        self.gridLayout_2.addWidget(self.showPogNotes_2, 1, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter = QSplitter(self.frame)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setMinimumSize(QSize(0, 500))
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(5)
        self.dungeonPictureArea = QGraphicsView(self.splitter)
        self.dungeonPictureArea.setObjectName(u"dungeonPictureArea")
        self.splitter.addWidget(self.dungeonPictureArea)
        self.assetManagementTabs = QTabWidget(self.splitter)
        self.assetManagementTabs.setObjectName(u"assetManagementTabs")
        self.artAssestsTab = QWidget()
        self.artAssestsTab.setObjectName(u"artAssestsTab")
        self.verticalLayout_3 = QVBoxLayout(self.artAssestsTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.downLoadAssetButton = QPushButton(self.artAssestsTab)
        self.downLoadAssetButton.setObjectName(u"downLoadAssetButton")

        self.gridLayout_3.addWidget(self.downLoadAssetButton, 0, 0, 1, 1)

        self.upLoadButton = QPushButton(self.artAssestsTab)
        self.upLoadButton.setObjectName(u"upLoadButton")

        self.gridLayout_3.addWidget(self.upLoadButton, 0, 2, 1, 1)

        self.deleteAssetButton = QPushButton(self.artAssestsTab)
        self.deleteAssetButton.setObjectName(u"deleteAssetButton")

        self.gridLayout_3.addWidget(self.deleteAssetButton, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.treeWidget = QTreeWidget(self.artAssestsTab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_3.addWidget(self.treeWidget)

        self.filePath = QLineEdit(self.artAssestsTab)
        self.filePath.setObjectName(u"filePath")
        self.filePath.setReadOnly(False)

        self.verticalLayout_3.addWidget(self.filePath)

        self.assetManagementTabs.addTab(self.artAssestsTab, "")
        self.monsterEditorTab = QWidget()
        self.monsterEditorTab.setObjectName(u"monsterEditorTab")
        self.verticalLayout_4 = QVBoxLayout(self.monsterEditorTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.newLevelButton = QPushButton(self.monsterEditorTab)
        self.newLevelButton.setObjectName(u"newLevelButton")

        self.gridLayout_4.addWidget(self.newLevelButton, 0, 1, 1, 1)

        self.manageDungeonsButton = QPushButton(self.monsterEditorTab)
        self.manageDungeonsButton.setObjectName(u"manageDungeonsButton")

        self.gridLayout_4.addWidget(self.manageDungeonsButton, 0, 0, 1, 1)

        self.deleteLevelButton = QPushButton(self.monsterEditorTab)
        self.deleteLevelButton.setObjectName(u"deleteLevelButton")

        self.gridLayout_4.addWidget(self.deleteLevelButton, 0, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 4)

        self.levelNameLabel = QLabel(self.monsterEditorTab)
        self.levelNameLabel.setObjectName(u"levelNameLabel")

        self.gridLayout_5.addWidget(self.levelNameLabel, 1, 0, 1, 1)

        self.levelNameEdit = QLineEdit(self.monsterEditorTab)
        self.levelNameEdit.setObjectName(u"levelNameEdit")

        self.gridLayout_5.addWidget(self.levelNameEdit, 1, 1, 1, 3)

        self.showGridCheckBox = QCheckBox(self.monsterEditorTab)
        self.showGridCheckBox.setObjectName(u"showGridCheckBox")

        self.gridLayout_5.addWidget(self.showGridCheckBox, 2, 0, 1, 2)

        self.gridSizeButton = QPushButton(self.monsterEditorTab)
        self.gridSizeButton.setObjectName(u"gridSizeButton")

        self.gridLayout_5.addWidget(self.gridSizeButton, 3, 0, 1, 2)

        self.gridSizeEdit = QLineEdit(self.monsterEditorTab)
        self.gridSizeEdit.setObjectName(u"gridSizeEdit")

        self.gridLayout_5.addWidget(self.gridSizeEdit, 3, 2, 1, 2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.offsetXLabel = QLabel(self.monsterEditorTab)
        self.offsetXLabel.setObjectName(u"offsetXLabel")

        self.horizontalLayout_2.addWidget(self.offsetXLabel)

        self.offsetXEdit = QLineEdit(self.monsterEditorTab)
        self.offsetXEdit.setObjectName(u"offsetXEdit")

        self.horizontalLayout_2.addWidget(self.offsetXEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_2, 4, 0, 1, 3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.offsetYLabel = QLabel(self.monsterEditorTab)
        self.offsetYLabel.setObjectName(u"offsetYLabel")

        self.horizontalLayout_3.addWidget(self.offsetYLabel)

        self.offsetYEdit = QLineEdit(self.monsterEditorTab)
        self.offsetYEdit.setObjectName(u"offsetYEdit")

        self.horizontalLayout_3.addWidget(self.offsetYEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_3, 4, 3, 1, 1)

        self.useSelectedPictureButton = QPushButton(self.monsterEditorTab)
        self.useSelectedPictureButton.setObjectName(u"useSelectedPictureButton")

        self.gridLayout_5.addWidget(self.useSelectedPictureButton, 5, 0, 1, 2)

        self.selectedPictureEdit = QLineEdit(self.monsterEditorTab)
        self.selectedPictureEdit.setObjectName(u"selectedPictureEdit")

        self.gridLayout_5.addWidget(self.selectedPictureEdit, 5, 2, 1, 2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.saveButton = QPushButton(self.monsterEditorTab)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_4.addWidget(self.saveButton)

        self.cancelButton = QPushButton(self.monsterEditorTab)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_4.addWidget(self.cancelButton)


        self.gridLayout_5.addLayout(self.horizontalLayout_4, 6, 0, 1, 3)

        self.graphicsView_2 = QGraphicsView(self.monsterEditorTab)
        self.graphicsView_2.setObjectName(u"graphicsView_2")

        self.gridLayout_5.addWidget(self.graphicsView_2, 7, 0, 1, 4)


        self.verticalLayout_4.addLayout(self.gridLayout_5)

        self.assetManagementTabs.addTab(self.monsterEditorTab, "")
        self.pogEditorTab = QWidget()
        self.pogEditorTab.setObjectName(u"pogEditorTab")
        self.verticalLayout_5 = QVBoxLayout(self.pogEditorTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.sizeComboBox = QComboBox(self.pogEditorTab)
        self.sizeComboBox.setObjectName(u"sizeComboBox")

        self.gridLayout_7.addWidget(self.sizeComboBox, 5, 2, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.createPogButton = QPushButton(self.pogEditorTab)
        self.createPogButton.setObjectName(u"createPogButton")

        self.gridLayout_6.addWidget(self.createPogButton, 0, 0, 1, 1)

        self.deletePogButton = QPushButton(self.pogEditorTab)
        self.deletePogButton.setObjectName(u"deletePogButton")

        self.gridLayout_6.addWidget(self.deletePogButton, 0, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.savePogButton = QPushButton(self.pogEditorTab)
        self.savePogButton.setObjectName(u"savePogButton")

        self.horizontalLayout_5.addWidget(self.savePogButton)

        self.cancelPogButton = QPushButton(self.pogEditorTab)
        self.cancelPogButton.setObjectName(u"cancelPogButton")

        self.horizontalLayout_5.addWidget(self.cancelPogButton)


        self.gridLayout_7.addLayout(self.horizontalLayout_5, 7, 0, 1, 3)

        self.pogNameLabel = QLabel(self.pogEditorTab)
        self.pogNameLabel.setObjectName(u"pogNameLabel")

        self.gridLayout_7.addWidget(self.pogNameLabel, 1, 0, 1, 1)

        self.useSelectedPogPictureButton = QPushButton(self.pogEditorTab)
        self.useSelectedPogPictureButton.setObjectName(u"useSelectedPogPictureButton")

        self.gridLayout_7.addWidget(self.useSelectedPogPictureButton, 4, 0, 1, 2)

        self.pogTypeComboBox = QComboBox(self.pogEditorTab)
        self.pogTypeComboBox.setObjectName(u"pogTypeComboBox")

        self.gridLayout_7.addWidget(self.pogTypeComboBox, 2, 1, 1, 2)

        self.pogLocationLabel = QLabel(self.pogEditorTab)
        self.pogLocationLabel.setObjectName(u"pogLocationLabel")

        self.gridLayout_7.addWidget(self.pogLocationLabel, 3, 0, 1, 1)

        self.treeWidget_2 = QTreeWidget(self.pogEditorTab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.treeWidget_2.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_2.setObjectName(u"treeWidget_2")

        self.gridLayout_7.addWidget(self.treeWidget_2, 8, 0, 1, 3)

        self.pogNameEdit = QLineEdit(self.pogEditorTab)
        self.pogNameEdit.setObjectName(u"pogNameEdit")

        self.gridLayout_7.addWidget(self.pogNameEdit, 1, 1, 1, 2)

        self.useSelectedPogPictureEdit = QLineEdit(self.pogEditorTab)
        self.useSelectedPogPictureEdit.setObjectName(u"useSelectedPogPictureEdit")

        self.gridLayout_7.addWidget(self.useSelectedPogPictureEdit, 4, 2, 1, 1)

        self.pogTypeLabel = QLabel(self.pogEditorTab)
        self.pogTypeLabel.setObjectName(u"pogTypeLabel")

        self.gridLayout_7.addWidget(self.pogTypeLabel, 2, 0, 1, 1)

        self.playerFlagsButton = QPushButton(self.pogEditorTab)
        self.playerFlagsButton.setObjectName(u"playerFlagsButton")

        self.gridLayout_7.addWidget(self.playerFlagsButton, 6, 0, 1, 2)

        self.graphicsView_3 = QGraphicsView(self.pogEditorTab)
        self.graphicsView_3.setObjectName(u"graphicsView_3")
        self.graphicsView_3.setMaximumSize(QSize(50, 50))

        self.gridLayout_7.addWidget(self.graphicsView_3, 9, 0, 1, 1)

        self.editNotesButton = QPushButton(self.pogEditorTab)
        self.editNotesButton.setObjectName(u"editNotesButton")

        self.gridLayout_7.addWidget(self.editNotesButton, 5, 0, 1, 2)

        self.pogLocationComboBox = QComboBox(self.pogEditorTab)
        self.pogLocationComboBox.setObjectName(u"pogLocationComboBox")

        self.gridLayout_7.addWidget(self.pogLocationComboBox, 3, 1, 1, 2)

        self.dmFlagsButton = QPushButton(self.pogEditorTab)
        self.dmFlagsButton.setObjectName(u"dmFlagsButton")

        self.gridLayout_7.addWidget(self.dmFlagsButton, 6, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_7)

        self.assetManagementTabs.addTab(self.pogEditorTab, "")
        self.splitter.addWidget(self.assetManagementTabs)

        self.verticalLayout.addWidget(self.splitter)


        self.verticalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.assetManagementTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toggleFOW_2.setText(QCoreApplication.translate("MainWindow", u"Toggle FOW", None))
        self.showSelectedPog_2.setText(QCoreApplication.translate("MainWindow", u"Show Selected Pog", None))
        self.hideFOW_2.setText(QCoreApplication.translate("MainWindow", u"Hide FOW", None))
        self.showPogNotes_2.setText(QCoreApplication.translate("MainWindow", u"Show Pog Notes", None))
        self.downLoadAssetButton.setText(QCoreApplication.translate("MainWindow", u"Download Asset", None))
        self.upLoadButton.setText(QCoreApplication.translate("MainWindow", u"Upload Asset", None))
        self.deleteAssetButton.setText(QCoreApplication.translate("MainWindow", u"Delete Asset", None))
        self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.artAssestsTab), QCoreApplication.translate("MainWindow", u"Art Assest", None))
        self.newLevelButton.setText(QCoreApplication.translate("MainWindow", u"New Level", None))
        self.manageDungeonsButton.setText(QCoreApplication.translate("MainWindow", u"Manage Dungeons", None))
        self.deleteLevelButton.setText(QCoreApplication.translate("MainWindow", u"DELETE Level", None))
        self.levelNameLabel.setText(QCoreApplication.translate("MainWindow", u"Level Name", None))
        self.showGridCheckBox.setText(QCoreApplication.translate("MainWindow", u"Show Grid", None))
        self.gridSizeButton.setText(QCoreApplication.translate("MainWindow", u"Grid Size", None))
        self.gridSizeEdit.setText(QCoreApplication.translate("MainWindow", u"30", None))
        self.offsetXLabel.setText(QCoreApplication.translate("MainWindow", u"Offset X", None))
        self.offsetXEdit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.offsetYLabel.setText(QCoreApplication.translate("MainWindow", u"Offset Y", None))
        self.offsetYEdit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.useSelectedPictureButton.setText(QCoreApplication.translate("MainWindow", u"Use Selected\n"
"                                                                        Picture Resource\n"
"                                                                    ", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.cancelButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.monsterEditorTab), QCoreApplication.translate("MainWindow", u"Monster Editor", None))
        self.createPogButton.setText(QCoreApplication.translate("MainWindow", u"Create Pog", None))
        self.deletePogButton.setText(QCoreApplication.translate("MainWindow", u"DELETE Pog", None))
        self.savePogButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.cancelPogButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.pogNameLabel.setText(QCoreApplication.translate("MainWindow", u"Pog Name", None))
        self.useSelectedPogPictureButton.setText(QCoreApplication.translate("MainWindow", u"Use Selected\n"
"                                                                        Picture Resource\n"
"                                                                    ", None))
        self.pogLocationLabel.setText(QCoreApplication.translate("MainWindow", u"Pog Location", None))
        self.pogTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Pog Type", None))
        self.playerFlagsButton.setText(QCoreApplication.translate("MainWindow", u"Player Flags", None))
        self.editNotesButton.setText(QCoreApplication.translate("MainWindow", u"Edit Notes", None))
        self.dmFlagsButton.setText(QCoreApplication.translate("MainWindow", u"DM Flags", None))
        self.assetManagementTabs.setTabText(self.assetManagementTabs.indexOf(self.pogEditorTab), QCoreApplication.translate("MainWindow", u"Pog Editor", None))
    # retranslateUi

