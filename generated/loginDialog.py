# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(610, 222)
        Dialog.setModal(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.serverURL = QLineEdit(Dialog)
        self.serverURL.setObjectName(u"serverURL")
        self.serverURL.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.serverURL)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.username = QLineEdit(Dialog)
        self.username.setObjectName(u"username")
        self.username.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.username)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.password = QLineEdit(Dialog)
        self.password.setObjectName(u"password")
        self.password.setFont(font)
        self.password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.password)

        self.failed = QLabel(Dialog)
        self.failed.setObjectName(u"failed")
        self.failed.setEnabled(True)
        palette = QPalette()
        brush = QBrush(QColor(255, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.failed.setPalette(palette)
        font1 = QFont()
        font1.setPointSize(24)
        self.failed.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.failed)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Login", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Server URL:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Username:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Password:", None))
        self.failed.setText(QCoreApplication.translate("Dialog", u"FAILED", None))
    # retranslateUi

