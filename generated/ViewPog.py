# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ViewPog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_PogDialog(object):
    def setupUi(self, PogDialog):
        if not PogDialog.objectName():
            PogDialog.setObjectName(u"PogDialog")
        PogDialog.resize(458, 522)
        self.gridLayout = QGridLayout(PogDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.graphicsView = QGraphicsView(PogDialog)
        self.graphicsView.setObjectName(u"graphicsView")

        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)


        self.retranslateUi(PogDialog)

        QMetaObject.connectSlotsByName(PogDialog)
    # setupUi

    def retranslateUi(self, PogDialog):
        PogDialog.setWindowTitle(QCoreApplication.translate("PogDialog", u"Dialog", None))
    # retranslateUi

