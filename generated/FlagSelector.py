# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FlagSelector.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FlagSelector(object):
    def setupUi(self, FlagSelector):
        if not FlagSelector.objectName():
            FlagSelector.setObjectName(u"FlagSelector")
        FlagSelector.resize(434, 307)
        self.verticalLayout = QVBoxLayout(FlagSelector)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.flagGrid = QGridLayout()
        self.flagGrid.setObjectName(u"flagGrid")
        self.checkBox_3 = QCheckBox(FlagSelector)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.flagGrid.addWidget(self.checkBox_3, 1, 0, 1, 1)

        self.checkBox_5 = QCheckBox(FlagSelector)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.flagGrid.addWidget(self.checkBox_5, 2, 0, 1, 1)

        self.checkBox_6 = QCheckBox(FlagSelector)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.flagGrid.addWidget(self.checkBox_6, 2, 1, 1, 1)

        self.checkBox_4 = QCheckBox(FlagSelector)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.flagGrid.addWidget(self.checkBox_4, 1, 1, 1, 1)

        self.checkBox_2 = QCheckBox(FlagSelector)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.flagGrid.addWidget(self.checkBox_2, 0, 1, 1, 1)

        self.checkBox = QCheckBox(FlagSelector)
        self.checkBox.setObjectName(u"checkBox")

        self.flagGrid.addWidget(self.checkBox, 0, 0, 1, 1)

        self.checkBox_7 = QCheckBox(FlagSelector)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.flagGrid.addWidget(self.checkBox_7, 3, 0, 1, 1)

        self.checkBox_8 = QCheckBox(FlagSelector)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.flagGrid.addWidget(self.checkBox_8, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.flagGrid)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(FlagSelector)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(FlagSelector)
        self.buttonBox.accepted.connect(FlagSelector.accept)
        self.buttonBox.rejected.connect(FlagSelector.reject)

        QMetaObject.connectSlotsByName(FlagSelector)
    # setupUi

    def retranslateUi(self, FlagSelector):
        FlagSelector.setWindowTitle(QCoreApplication.translate("FlagSelector", u"Dialog", None))
        self.checkBox_3.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox_5.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox_6.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox_4.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox_7.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
        self.checkBox_8.setText(QCoreApplication.translate("FlagSelector", u"CheckBox", None))
    # retranslateUi

