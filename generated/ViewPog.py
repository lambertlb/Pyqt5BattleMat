# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ViewPog.ui'
#
# Created by: PySide2 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_PogDialog(object):
    def setupUi(self, PogDialog):
        PogDialog.setObjectName("PogDialog")
        PogDialog.resize(458, 522)
        self.gridLayout = QtWidgets.QGridLayout(PogDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWidgets.QGraphicsView(PogDialog)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)

        self.retranslateUi(PogDialog)
        QtCore.QMetaObject.connectSlotsByName(PogDialog)

    def retranslateUi(self, PogDialog):
        _translate = QtCore.QCoreApplication.translate
        PogDialog.setWindowTitle(_translate("PogDialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PogDialog = QtWidgets.QDialog()
    ui = Ui_PogDialog()
    ui.setupUi(PogDialog)
    PogDialog.show()
    sys.exit(app.exec_())