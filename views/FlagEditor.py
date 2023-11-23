"""
GPL 3 file header
"""
from PySide6 import QtWidgets

from generated.FlagSelector import Ui_FlagSelector


class FlagEditor(QtWidgets.QDialog, Ui_FlagSelector):

    def __init__(self, *args):
        super(FlagEditor, self).__init__(*args)
        self.flags = None
        self.flagDictionary = None
        self.checkboxMap = dict()
        self.setupUi(self)
        self.setModal(True)

    def setup(self, flags, flagDictionary):
        self.checkboxMap.clear()
        self.flags = flags
        self.flagDictionary = flagDictionary
        for i in reversed(range(self.flagGrid.count())):
            self.flagGrid.itemAt(i).widget().setParent(None)
        column = 0
        row = 0
        for flag in self.flagDictionary:
            if flag == 0:
                continue
            name = self.flagDictionary[flag]
            wg = QtWidgets.QCheckBox(self)
            wg.setText(name)
            wg.setChecked(self.flags & flag == flag)
            self.checkboxMap[flag] = wg
            self.flagGrid.addWidget(wg, row, column)
            column += 1
            if column == 2:
                row += 1
                column = 0

    def getFlags(self):
        returnFlags = 0
        for flag in self.checkboxMap:
            wg: QtWidgets.QCheckBox = self.checkboxMap[flag]
            if wg.isChecked():
                returnFlags |= flag
        return returnFlags
