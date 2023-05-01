"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from views.DragButton import DragButton


class RibbonBar(QtWidgets.QHBoxLayout):

	def	__init__(self, windowFrame, *args):
		super(RibbonBar, self).__init__(*args)
		self.windowFrame = windowFrame
		self.button3 = DragButton('http://static4.paizo.com/image/content/PathfinderTales/PZO8500-CrisisOfFaith-Corogan.jpg',
								self.windowFrame)
		self.button3.setObjectName("button3")
		self.addWidget(self.button3)
		self.button2 = DragButton('image/FallPanorama.jpg', self.windowFrame)
		self.button2.setObjectName("button2")
		self.addWidget(self.button2)
		self.button1 = DragButton('image/level1.jpg', self.windowFrame)
		self.button1.setObjectName("button1")
		self.addWidget(self.button1)
		self.localize()

	def localize(self):
		_translate = QtCore.QCoreApplication.translate
		self.button3.setText("PushButton")
		self.button2.setText("PushButton")
		self.button1.setText("PushButton")
