"""
GPL 3 file header
"""
from PyQt5 import QtWidgets

from generated.dungeonManagerDialog import Ui_DungeonSelectDialog


class DungeonManagerDialog(QtWidgets.QDialog, Ui_DungeonSelectDialog):
	def __init__(self, *args):
		super(DungeonManagerDialog, self).__init__(*args)
		self.setupUi(self)
