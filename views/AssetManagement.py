"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore


class AssetManagement(QtWidgets.QTabWidget):
	def __init__(self, splitter):
		super(AssetManagement, self).__init__(splitter)
		self.splitter = splitter
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.addTab(self.tab_2, "")
		self.localize()

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.setTabText(self.indexOf(self.tab), "Tab 1")
		self.setTabText(self.indexOf(self.tab_2), "Tab 2")
