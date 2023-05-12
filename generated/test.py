from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


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


class MyLabel(QtWidgets.QLabel):

    def __init__(self, imagePath, view, *args):
        super(MyLabel, self).__init__(*args)
        self.image = QtGui.QImage('../image/test.jpg')
        self.pixMap = None
        self.view = view
        self.scaledGridSize = 0
        pass

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        gridSize = self.view.getScaledGridSize()
        if gridSize != self.scaledGridSize:
            self.scaledGridSize = gridSize
            pixMap = QtGui.QPixmap.fromImage(self.image)
            pixmapSize = pixMap.size()
            # pixmapSize.scale(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio)
            self.pixMap = pixMap.scaled(self.scaledGridSize, self.scaledGridSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter = QtGui.QPainter(self)
        painter.begin(self)
        # painter.drawPixmap(0, 0, self.pixMap)
        print(f'Scaled grid size {self.scaledGridSize} w {self.width()} h {self.height()}')
        painter.drawLine(0, 0, self.scaledGridSize, 0)
        painter.drawLine(0, 0, 0, self.scaledGridSize)
        painter.drawLine(self.scaledGridSize, self.scaledGridSize, 0, self.scaledGridSize)
        painter.drawLine(self.scaledGridSize - 1, self.scaledGridSize -1, self.scaledGridSize, 0)
        painter.end()


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

        # img = QtGui.QImage('../image/test.jpg')
        # pix = QtGui.QPixmap.fromImage(img)
        # pix.scaled(50, 50, Qt.KeepAspectRatio)
        # wig = QtWidgets.QLabel()
        wig = MyLabel('../image/test.jpg', self.graphicsView)
        wig.setGeometry(0,0,50,50)
        # wig.setPixmap(pix)
        wig.setAlignment(QtCore.Qt.AlignCenter)
        wig.setScaledContents(True)
        wig.setMinimumSize(1, 1)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(wig)
        self.scene.addItem(proxy)
        proxy.setPos(200, 200)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
