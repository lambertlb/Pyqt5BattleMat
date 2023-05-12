"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QTransform


class BattleMatCanvas(QtWidgets.QGraphicsView):
	"""
	Override QGraphicsView so we can get at mouse wheel to set scaling
	"""

	def __init__(self, scene, parent):
		super(BattleMatCanvas, self).__init__(scene, parent)
		self.zoom = 1
		self.scene = scene
		# self.setOptimizationFlags(QtWidgets.QGraphicsView.OptimizationFlags.)
		pass

		# self.setAcceptDrops(True)

	def wheelEvent(self, event):
		delta = event.angleDelta().y() / 120
		if delta > 0:
			self.zoom *= 1.05
		elif delta < 0:
			self.zoom /= 1.05
		self.transform()

	def transform(self):
		self.setTransform(QTransform().scale(self.zoom, self.zoom))

	def zoomReset(self):
		self.zoom = 1
		self.transform()

	def setZoom(self, newZoom):
		self.zoom = newZoom
		self.transform()

	def getZoom(self):
		return self.zoom

	def resizeEvent(self, event):
		self.scene.computeInitialZoom()

	def drawForeground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
		pass

	def drawItems(self, painter, items, options):
		self.saveDraw(painter, items, options)
