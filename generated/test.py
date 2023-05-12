import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class MyQGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args):
        super(MyQGraphicsView, self).__init__(*args)
        self.zoom = 1
        self.gridSize = 50
        pass

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        if delta > 0:
            self.zoom *= 1.05
        elif delta < 0:
            self.zoom /= 1.05
        self.transform()

    def transform(self):
        self.setTransform(QtGui.QTransform().scale(self.zoom, self.zoom))

    def setZoom(self, newZoom):
        self.zoom = newZoom
        self.transform()

    def getScaledGridSize(self):
        return int(self.gridSize * self.zoom)


class MyItem(QtWidgets.QGraphicsItem):

    def __init__(self, imagePath, view, *args):
        super(MyItem, self).__init__(*args)
        self.image = QtGui.QImage(imagePath)
        self.pixMap = None
        self.view = view
        self.scaledGridSize = 0

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 50, 50)

    def paint(self, painter: QtGui.QPainter, option: 'QStyleOptionGraphicsItem',
              widget: typing.Optional[QWidget] = ...) -> None:
        gridSize = self.view.getScaledGridSize()
        if gridSize != self.scaledGridSize:
            self.scaledGridSize = gridSize
            pixMap = QtGui.QPixmap.fromImage(self.image)
            self.pixMap = pixMap.scaled(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio,
                                        Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, self.pixMap)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.scene = QtWidgets.QGraphicsScene(self.centralwidget)
        self.graphicsView = MyQGraphicsView(self.scene)
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView.setSceneRect(0, 0, 2000, 2000)
        self.graphicsView.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        wig = MyItem('../image/test.jpg', self.graphicsView)
        self.scene.addItem(wig)
        wig.setPos(200, 200)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
