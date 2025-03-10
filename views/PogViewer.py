"""
GPL 3 file header
"""
from PySide6 import QtWidgets, QtGui, QtCore

from generated.ViewPog import Ui_PogDialog
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager


class PogViewer(QtWidgets.QDialog, Ui_PogDialog):
    def __init__(self, *args):
        super(PogViewer, self).__init__(*args)
        self.selectedPog = None

        self.setupUi(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        ServicesManager.getEventManager().subscribeToEvent(self.eventFired)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    def eventFired(self, eventData):
        if eventData.eventReason == ReasonForAction.PogWasSelected:
            self.pogSelection()

    def pogSelection(self):
        self.scene.clear()
        self.selectedPog = ServicesManager.getDungeonManager().getSelectedPog()
        if self.selectedPog is None or self.selectedPog.pogImageUrl is None:
            return
        self.setWindowTitle(self.selectedPog.pogName)
        self.selectedPog.loadPogImage(self.successfulLoaded, self.failedLoad)
        pass

    def successfulLoaded(self):
        self.addImageToScene()
        pass

    def addImageToScene(self):
        self.scene.clear()
        image = self.selectedPog.image
        pixMap = QtGui.QPixmap.fromImage(image)
        scenePixMap = pixMap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio,
                                    QtCore.Qt.SmoothTransformation)
        self.scene.addPixmap(scenePixMap)

    def failedLoad(self):
        pass

    def resizeEvent(self, newSize):
        super().resizeEvent(newSize)
        if self.selectedPog is not None and self.selectedPog.image is not None:
            self.addImageToScene()

    def show(self):
        self.pogSelection()
        super().show()
