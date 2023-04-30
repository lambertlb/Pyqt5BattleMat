"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui, QtCore

from services.ReasonForEvent import ReasonForEvent
from services.ServicesManager import ServicesManager


class DragButton(QtWidgets.QPushButton):
	"""
	Make a draggable button
	"""
	def __init__(self, imageName, *args):
		super(DragButton, self).__init__(*args)
		self.imageName = imageName
		self.proxy = None
		self.clicked.connect(self.pressed)

	def mouseMoveEvent(self, e):
		"""
		Move moved one me so start dragging
		:param e: event
		:return: None
		"""
		if e.buttons() == QtCore.Qt.LeftButton:
			drag = QtGui.QDrag(self)
			mime = QtCore.QMimeData()
			drag.setMimeData(mime)
			drag.setPixmap(self.grab())
			drag.exec_(QtCore.Qt.MoveAction)

	def setProxy(self, proxy):
		"""
		Set scene proxy if in a scene
		:param proxy:
		:return:
		"""
		self.proxy = proxy

	def getProxy(self):
		"""
		:return: proxy else None if not in scene
		"""
		return self.proxy

	def pressed(self):
		ServicesManager.getEventManager().fireEvent(ReasonForEvent.LOAD_IMAGE, self.imageName)