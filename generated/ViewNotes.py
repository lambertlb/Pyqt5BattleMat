# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ViewNotes.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_PogNotesDialog(object):
    def setupUi(self, PogNotesDialog):
        if not PogNotesDialog.objectName():
            PogNotesDialog.setObjectName(u"PogNotesDialog")
        PogNotesDialog.resize(400, 300)
        self.gridLayout = QGridLayout(PogNotesDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(PogNotesDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.notesTab = QWidget()
        self.notesTab.setObjectName(u"notesTab")
        self.gridLayout_2 = QGridLayout(self.notesTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.notesTextEdit = QTextEdit(self.notesTab)
        self.notesTextEdit.setObjectName(u"notesTextEdit")

        self.gridLayout_2.addWidget(self.notesTextEdit, 0, 0, 1, 1)

        self.tabWidget.addTab(self.notesTab, "")
        self.dmNotesTab = QWidget()
        self.dmNotesTab.setObjectName(u"dmNotesTab")
        self.gridLayout_3 = QGridLayout(self.dmNotesTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.dmNotesTextEdit = QTextEdit(self.dmNotesTab)
        self.dmNotesTextEdit.setObjectName(u"dmNotesTextEdit")

        self.gridLayout_3.addWidget(self.dmNotesTextEdit, 0, 0, 1, 1)

        self.tabWidget.addTab(self.dmNotesTab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fontSizeControl = QSpinBox(PogNotesDialog)
        self.fontSizeControl.setObjectName(u"fontSizeControl")

        self.horizontalLayout.addWidget(self.fontSizeControl)

        self.buttonBox = QDialogButtonBox(PogNotesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(PogNotesDialog)
        self.buttonBox.accepted.connect(PogNotesDialog.accept)
        self.buttonBox.rejected.connect(PogNotesDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PogNotesDialog)
    # setupUi

    def retranslateUi(self, PogNotesDialog):
        PogNotesDialog.setWindowTitle(QCoreApplication.translate("PogNotesDialog", u"Dialog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.notesTab), QCoreApplication.translate("PogNotesDialog", u"Notes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dmNotesTab), QCoreApplication.translate("PogNotesDialog", u"DM Notes", None))
    # retranslateUi

