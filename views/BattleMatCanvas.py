"""
GPL 3 file header
"""
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QTransform

from services.ServicesManager import ServicesManager


class BattleMatCanvas(QtWidgets.QGraphicsView):
    """
    Override QGraphicsView so we can get at mouse wheel to set scaling
    """

    def __init__(self, scene, parent):
        super(BattleMatCanvas, self).__init__(scene, parent)
        self.zoom = 1
        self.scene = scene
        self.changeRubberBand = False
        self.origin = QtCore.QPoint()
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        if delta > 0:
            self.zoom *= 1.1
        elif delta < 0:
            self.zoom /= 1.1
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

    def mousePressEvent(self, event):
        modifierPressed = QtWidgets.QApplication.keyboardModifiers()
        self.origin = event.pos()
        if (modifierPressed and QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rubberBand.show()
            self.changeRubberBand = True
        QtWidgets.QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
        else:
            QtWidgets.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.changeRubberBand:
            rect = self.rubberBand.geometry()
            if ServicesManager.getDungeonManager().editMode:
                sw = rect.width() / self.zoom
                sh = rect.height() / self.zoom
                gridWidth = (sw + sh) / 2
                ServicesManager.getDungeonManager().computedGridWidth = gridWidth
            else:
                rect_scene = self.mapToScene(rect).boundingRect()
                self.scene.handleFOWSelection(rect_scene)
            self.changeRubberBand = False
            self.rubberBand.hide()
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
