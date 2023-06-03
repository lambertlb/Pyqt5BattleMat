# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dungeonManagerDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DungeonSelectDialog(object):
    def setupUi(self, DungeonSelectDialog):
        if not DungeonSelectDialog.objectName():
            DungeonSelectDialog.setObjectName(u"DungeonSelectDialog")
        DungeonSelectDialog.resize(622, 347)
        DungeonSelectDialog.setAutoFillBackground(False)
        DungeonSelectDialog.setModal(True)
        self.gridLayout = QGridLayout(DungeonSelectDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.iAmDungeonMaster = QCheckBox(DungeonSelectDialog)
        self.iAmDungeonMaster.setObjectName(u"iAmDungeonMaster")

        self.gridLayout.addWidget(self.iAmDungeonMaster, 0, 0, 1, 1)

        self.label = QLabel(DungeonSelectDialog)
        self.label.setObjectName(u"label")
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(149, 149, 149, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        brush2 = QBrush(QColor(120, 120, 120, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        brush3 = QBrush(QColor(240, 240, 240, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        self.label.setPalette(palette)
        self.label.setAutoFillBackground(True)
        self.label.setTextFormat(Qt.PlainText)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.templateList = QComboBox(DungeonSelectDialog)
        self.templateList.setObjectName(u"templateList")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.templateList)

        self.createDungeonButton = QPushButton(DungeonSelectDialog)
        self.createDungeonButton.setObjectName(u"createDungeonButton")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.createDungeonButton)

        self.newDungeonName = QLineEdit(DungeonSelectDialog)
        self.newDungeonName.setObjectName(u"newDungeonName")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.newDungeonName)

        self.editDungeonButton = QPushButton(DungeonSelectDialog)
        self.editDungeonButton.setObjectName(u"editDungeonButton")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.editDungeonButton)

        self.deleteDungeonButton = QPushButton(DungeonSelectDialog)
        self.deleteDungeonButton.setObjectName(u"deleteDungeonButton")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.deleteDungeonButton)


        self.gridLayout.addLayout(self.formLayout, 2, 0, 1, 2)

        self.label_2 = QLabel(DungeonSelectDialog)
        self.label_2.setObjectName(u"label_2")
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush3)
        self.label_2.setPalette(palette1)
        self.label_2.setAutoFillBackground(True)
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 2)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.sessionList = QComboBox(DungeonSelectDialog)
        self.sessionList.setObjectName(u"sessionList")

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.sessionList)

        self.dmSessionButton = QPushButton(DungeonSelectDialog)
        self.dmSessionButton.setObjectName(u"dmSessionButton")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.dmSessionButton)

        self.deleteSessionButton = QPushButton(DungeonSelectDialog)
        self.deleteSessionButton.setObjectName(u"deleteSessionButton")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.deleteSessionButton)

        self.createSessionButton = QPushButton(DungeonSelectDialog)
        self.createSessionButton.setObjectName(u"createSessionButton")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.createSessionButton)

        self.newSessionName = QLineEdit(DungeonSelectDialog)
        self.newSessionName.setObjectName(u"newSessionName")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.newSessionName)


        self.gridLayout.addLayout(self.formLayout_2, 4, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(DungeonSelectDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)


        self.retranslateUi(DungeonSelectDialog)
        self.buttonBox.accepted.connect(DungeonSelectDialog.accept)
        self.buttonBox.rejected.connect(DungeonSelectDialog.reject)

        QMetaObject.connectSlotsByName(DungeonSelectDialog)
    # setupUi

    def retranslateUi(self, DungeonSelectDialog):
        DungeonSelectDialog.setWindowTitle(QCoreApplication.translate("DungeonSelectDialog", u"Dungeon Select", None))
        self.iAmDungeonMaster.setText(QCoreApplication.translate("DungeonSelectDialog", u"I am DM", None))
        self.label.setText(QCoreApplication.translate("DungeonSelectDialog", u"Template Management", None))
        self.templateList.setCurrentText("")
        self.createDungeonButton.setText(QCoreApplication.translate("DungeonSelectDialog", u"Create New Dungeon ->", None))
        self.newDungeonName.setText(QCoreApplication.translate("DungeonSelectDialog", u"Enter Dungeon Name", None))
        self.editDungeonButton.setText(QCoreApplication.translate("DungeonSelectDialog", u"Edit Dungeon", None))
        self.deleteDungeonButton.setText(QCoreApplication.translate("DungeonSelectDialog", u"Delete Dungeon", None))
        self.label_2.setText(QCoreApplication.translate("DungeonSelectDialog", u"Session Management", None))
        self.dmSessionButton.setText(QCoreApplication.translate("DungeonSelectDialog", u"DM the Session", None))
        self.deleteSessionButton.setText(QCoreApplication.translate("DungeonSelectDialog", u"Delete Session", None))
        self.createSessionButton.setText(QCoreApplication.translate("DungeonSelectDialog", u"Create Session ->", None))
        self.newSessionName.setText(QCoreApplication.translate("DungeonSelectDialog", u"Enter Session Name", None))
    # retranslateUi

