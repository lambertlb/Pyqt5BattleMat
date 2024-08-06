"""
GPL 3 file header
"""
from PySide6 import QtWidgets, QtCore, QtGui

from services.AsyncTasks import AsyncImage
from services.Constants import Constants
from services.DungeonManager import DungeonManager
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager
from services.serviceData.DataVersions import DataVersions
from services.serviceData.PogPlace import PogPlace
from services.serviceData.VersionedItem import VersionedItem
from services.DungeonMasterFlag import DungeonMasterFlag
from views.BattleMatCanvas import BattleMatCanvas
from views.PogCanvas import PogCanvas


class BattleMatScene(QtWidgets.QGraphicsScene):
    """
    Subclass QGraphicsScene to manage drag and drop
    """

    def __init__(self, splitter):
        super(BattleMatScene, self).__init__()
        self._currentDungeonID = None
        self._currentSessionID = None
        self._dungeonPicture = None
        self._currentLevel = -1
        self._dataVersionsHistory = DataVersions()
        self._monsterPogs = list()
        self._roomObjectPogs = list()
        self._playerPogs = list()
        self._imageLoaded = False
        self._selectedPogCanvas = None
        self._gridOffsetX = 0
        self._gridOffsetY = 0
        self._gridSpacing = 50
        self._showGrid = True
        self._imageWidth = 100
        self._imageHeight = 100
        self._verticalLines = 10
        self._horizontalLines = 10
        self._imageLoaded = False
        self._selectedColumn = 0
        self._selectedRow = 0
        self.selectedPogCanvas = None
        self.toggleFOW = False
        self.clearFOW = False

        self.splitter = splitter
        self.pixelMap = QtGui.QPixmap()
        self.pixMapItem = self.addPixmap(self.pixelMap)
        self.view = BattleMatCanvas(self, splitter)
        self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        ServicesManager.getEventManager().subscribeToEvent(self.eventFired)

    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        """
        Item was dropped here.
        If is had a proxy it means it was already here so just move it.
        If no proxy then create a new item
        :param e: event
        :return:None
        """
        pos = e.scenePos()
        self.computeSelectedColumnAndRow(pos.x(), pos.y())
        if not ServicesManager.getDungeonManager().isDungeonMaster:
            if ServicesManager.getDungeonManager().isFowSet(self._selectedColumn, self._selectedRow):
                return
        src = e.source()
        proxy = None
        if hasattr(src, 'proxy'):
            proxy = src.proxy
        if proxy is not None:
            self.movePogToNewSpot(proxy)
        else:
            self.createPogCanvasForThisCell()

    def movePogToNewSpot(self, proxy):
        x = self.columnToPixel(self._selectedColumn)
        y = self.rowToPixel(self._selectedRow)
        pix = QtCore.QPointF(x, y)
        proxy.setPos(pix)
        self.removeItem(proxy)
        self.addItem(proxy)  # make sure on top
        self.updateDroppedItem(proxy)

    def updateDroppedItem(self, proxy):
        proxy.pogData.setPogPosition(self._selectedColumn, self._selectedRow)
        proxy.pogData.dungeonLevel = ServicesManager.getDungeonManager().currentLevelIndex
        ServicesManager.getDungeonManager().addOrUpdatePogWithoutPlace(proxy.pogData)
        ServicesManager.getDungeonManager().setSelectedPog(proxy.pogData)

    def createPogCanvasForThisCell(self):
        pogBeingDragged = ServicesManager.getDungeonManager().getSelectedPog()
        if pogBeingDragged is None:
            return
        if pogBeingDragged.isThisAPlayer():  # players can only be on once
            existing = self.findPogCanvas(pogBeingDragged)
            if existing is not None:
                self.movePogToNewSpot(existing)
                return
        clone = self.addClonePogToCanvas(pogBeingDragged)
        self.updateDroppedItem(clone)

    def addClonePogToCanvas(self, pogData):
        if pogData.isThisAPlayer():
            clonePog = pogData
        else:
            clonePog = pogData.clone()
            if ServicesManager.getDungeonManager().editMode:
                clonePog.pogPlace = PogPlace.DUNGEON_LEVEL
            else:
                clonePog.pogPlace = PogPlace.SESSION_LEVEL
        clonePog.setPogPosition(self._selectedColumn, self._selectedRow)
        return self.addPogToCanvas(clonePog)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

    def computeInitialZoom(self):
        self.view.setZoom(1)

    def resetScroll(self):
        self.view.verticalScrollBar().setValue(0)
        self.view.horizontalScrollBar().setValue(0)

    def eventFired(self, eventData):
        if eventData.eventReason == ReasonForAction.PogDataChanged:
            self.checkForDataChanges()
        elif eventData.eventReason == ReasonForAction.DungeonDataReadyToEdit:
            self.checkForDataChanges()
        elif eventData.eventReason == ReasonForAction.DungeonDataReadyToJoin:
            self.checkForDataChanges()
        elif eventData.eventReason == ReasonForAction.SessionDataChanged:
            self.checkForDataChanges()
        elif eventData.eventReason == ReasonForAction.DungeonSelectedLevelChanged:
            self.checkForDataChanges()
        elif eventData.eventReason == ReasonForAction.DungeonDataSaved:
            self.checkForDataChanges()
        elif eventData.eventReason == ReasonForAction.MouseDownEventBubble:
            self.mousePressEvent(eventData.eventData)
        elif eventData.eventReason == ReasonForAction.PogWasSelected:
            self.newSelectedPog()

    def checkForDataChanges(self):
        dungeonManager = ServicesManager.getDungeonManager()
        if dungeonManager.getCurrentDungeonLevelData() is None:
            return
        initView = False
        if dungeonManager.selectedDungeonUUID != self._currentDungeonID:
            initView = True
        elif dungeonManager.getCurrentSessionUUID() != self._currentSessionID:
            initView = True
        elif dungeonManager.currentLevelIndex != self._currentLevel:
            initView = True
        elif dungeonManager.getCurrentDungeonLevelData().levelDrawing != self._dungeonPicture:
            initView = True

        self._currentDungeonID = dungeonManager.selectedDungeonUUID
        self._currentSessionID = dungeonManager.getCurrentSessionUUID()
        self._currentLevel = dungeonManager.currentLevelIndex

        if initView:
            self.intializeView()
        else:
            self.dungeonDataUpdated()
        self.update(0, 0, self.width(), self.height())

    def intializeView(self):
        self._dataVersionsHistory.initialize()
        self._monsterPogs.clear()
        self._roomObjectPogs.clear()
        self._playerPogs.clear()
        self.pixMapItem = None
        self.clear()
        dungeonLevel = ServicesManager.getDungeonManager().getCurrentDungeonLevelData()
        if dungeonLevel is None:
            return
        self._dungeonPicture = dungeonLevel.levelDrawing
        imageUrl = ServicesManager.getDungeonManager().getUrlToDungeonResource(self._dungeonPicture)
        self._imageLoaded = False
        AsyncImage(imageUrl, self.imageWasLoaded, self.failedLoad).submit()

    def imageWasLoaded(self, asynchReturn):
        """
        Callback from background task when image loaded
        :param asynchReturn: Image that was loaded
        :return: None
        """
        image = asynchReturn.data
        self._imageLoaded = True
        self.updateImage(QtGui.QPixmap.fromImage(image))
        self.checkForDataChanges()

    def failedLoad(self, asynchReturn):
        """
        Image loading failed
        :param asynchReturn: return data from task
        :return: None
        """
        pass

    def updateImage(self, newPixmap):
        """
        new image loaded so update old pixel map
        :param newPixmap:
        :return: None
        """
        if self.pixMapItem is not None:
            self.removeItem(self.pixMapItem)
        self.pixelMap = newPixmap
        self.pixMapItem = self.addPixmap(self.pixelMap)
        self.computeInitialZoom()
        self.resetScroll()
        self.view.setSceneRect(0, 0, self.pixelMap.width(), self.pixelMap.height())
        self._imageWidth = self.pixelMap.width()
        self._imageHeight = self.pixelMap.height()

    def dungeonDataUpdated(self):
        if not self._imageLoaded:
            return
        self.calculateDimensions()
        self.deSelectPog()
        self.updateNeededData()
        self.newSelectedPog()

    def updateNeededData(self):
        self.getGridData()
        self.updatePogs(VersionedItem.SESSION_RESOURCE_PLAYERS,
                        ServicesManager.getDungeonManager().getPlayersForCurrentSession(),
                        self._playerPogs)
        if ServicesManager.getDungeonManager().editMode:
            self.updatePogs(VersionedItem.DUNGEON_LEVEL_MONSTERS,
                            ServicesManager.getDungeonManager().getMonstersForCurrentLevel(),
                            self._monsterPogs)
            self.updatePogs(VersionedItem.DUNGEON_LEVEL_ROOMOBJECTS,
                            ServicesManager.getDungeonManager().getRoomObjectsForCurrentLevel(),
                            self._roomObjectPogs)

        else:
            self.updatePogs(VersionedItem.SESSION_LEVEL_MONSTERS,
                            ServicesManager.getDungeonManager().getMonstersForCurrentLevel(),
                            self._monsterPogs)
            self.updatePogs(VersionedItem.SESSION_LEVEL_ROOMOBJECTS,
                            ServicesManager.getDungeonManager().getRoomObjectsForCurrentLevel(),
                            self._roomObjectPogs)
        # updateFogOfWar();
        # drawEverything();
        ServicesManager.getDungeonManager().updateVersion(self._dataVersionsHistory)

    def getGridData(self):
        self._gridOffsetX = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridOffsetX
        self._gridOffsetY = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridOffsetY
        self._gridSpacing = ServicesManager.getDungeonManager().getCurrentDungeonLevelData().gridSize
        self._showGrid = ServicesManager.getDungeonManager().isDungeonGridVisible()

    def updatePogs(self, versionedItem, pogs, pogList):
        if pogs is None or ServicesManager.getDungeonManager().getItemVersion(
                versionedItem) == self._dataVersionsHistory.getItemVersion(versionedItem):
            return
        existingPogs = pogList.copy()
        pogsToBeAdded = list()

        self.getPogsThatNeedToBeAddedOrRemoved(pogs, existingPogs, pogsToBeAdded)
        for pog in existingPogs:
            pogList.remove(pog)
            self.removeItem(pog)
        for pog in pogsToBeAdded:
            self.addPogToCanvas(pog)

    # noinspection PyMethodMayBeStatic
    def getPogsThatNeedToBeAddedOrRemoved(self, sourcePogs, existingPogs, pogsToBeAdded):
        for pog in sourcePogs:
            found = False
            for index in range(len(existingPogs)):
                pg = existingPogs[index]
                if pog.isEqual(pg.getPogData()):
                    existingPogs.remove(pg)
                    pg.updatePogData(pog)
                    found = True
                    break
            if not found:
                pogsToBeAdded.append(pog)

    def addPogToCanvas(self, pogData):
        pogCanvas = PogCanvas(self.view)
        pogCanvas.setPogData(pogData, False)
        pogCanvas.setGridSize(self._gridSpacing)
        self.addPogToProperList(pogCanvas)
        self.addItem(pogCanvas)
        where = self.computePogPosition(pogData)
        pogCanvas.setPos(where)
        return pogCanvas

    def adjustedGridSize(self):
        return self._gridSpacing * self.view.getZoom()

    def columnToPixel(self, column):
        return (self._gridSpacing * column) + self._gridOffsetX

    def rowToPixel(self, row):
        return (self._gridSpacing * row) + self._gridOffsetY

    def computePogPosition(self, pogData):
        x = self.columnToPixel(pogData.pogColumn)
        if pogData.isDmFlagSet(DungeonMasterFlag.SHIFT_RIGHT):
            x += self._gridSpacing / 2
        y = self.rowToPixel(pogData.pogRow)
        if pogData.isDmFlagSet(DungeonMasterFlag.SHIFT_TOP):
            y -= self._gridSpacing / 2
        return QtCore.QPointF(x, y)

    def computeSelectedColumnAndRow(self, clientX, clientY):
        self._selectedColumn = int(((clientX - self._gridOffsetX) / self._gridSpacing))
        self._selectedRow = int(((clientY - self._gridOffsetY) / self._gridSpacing))

    def addPogToProperList(self, scalablePog):
        if scalablePog.getPogData().pogType == Constants.POG_TYPE_MONSTER:
            self._monsterPogs.append(scalablePog)
        elif scalablePog.getPogData().pogType == Constants.POG_TYPE_ROOMOBJECT:
            self._roomObjectPogs.append(scalablePog)
        elif scalablePog.getPogData().pogType == Constants.POG_TYPE_PLAYER:
            self._playerPogs.append(scalablePog)

    def newSelectedPog(self):
        self.deSelectPog()
        pog = ServicesManager.getDungeonManager().getSelectedPog()
        if pog is None:
            return
        found = self.findPogCanvas(pog)
        if found is not None:
            self.selectedPogCanvas = found
            self.selectedPogCanvas.update()
        self.update(0, 0, self.width(), self.height())

    def deSelectPog(self):
        if self._selectedPogCanvas is not None:
            self._selectedPogCanvas.update()
            self._selectedPogCanvas = None

    def findPogCanvas(self, pogToFind):
        for pog in self._playerPogs:
            if pog.getPogData().isEqual(pogToFind):
                return pog
        for pog in self._monsterPogs:
            if pog.getPogData().isEqual(pogToFind):
                return pog
        for pog in self._roomObjectPogs:
            if pog.getPogData().isEqual(pogToFind):
                return pog
        return None

    def mousePressEvent(self, event):
        super(BattleMatScene, self).mousePressEvent(event)

    def drawForeground(self, painter, rect):
        if not self._imageLoaded:
            return
        if ServicesManager.getDungeonManager().selectedDungeon is None:
            return
        self.calculateDimensions()
        if not ServicesManager.getDungeonManager().editMode:
            self.drawFOW(painter)
        if self._showGrid:
            self.drawGrid(painter)

    def drawGrid(self, painter):
        painter.setPen(QtGui.QColor(174, 173, 172))
        line = QtCore.QLineF(QtCore.QPointF(self._gridOffsetX, self._gridOffsetY),
                             QtCore.QPointF(self._imageWidth, self._gridOffsetY))
        for _ in range(self._horizontalLines):
            painter.drawLine(line)
            line.translate(0, self._gridSpacing)
        line = QtCore.QLineF(QtCore.QPointF(self._gridOffsetX, self._gridOffsetY),
                             QtCore.QPointF(self._gridOffsetX, self._imageHeight))
        for _ in range(self._verticalLines):
            painter.drawLine(line)
            line.translate(self._gridSpacing, 0)

    def calculateDimensions(self):
        self.getGridData()
        self._verticalLines = int((self._imageWidth / self._gridSpacing) + 1)
        self._horizontalLines = int((self._imageHeight / self._gridSpacing) + 1)
        ServicesManager.getDungeonManager().setSessionLevelSize(self._verticalLines, self._horizontalLines)

    def drawFOW(self, painter):
        dm: DungeonManager = ServicesManager.getDungeonManager()
        isDM = dm.isDungeonMaster
        for x in range(self._verticalLines):
            left = (x * self._gridSpacing) + self._gridOffsetX
            for y in range(self._horizontalLines):
                top = (y * self._gridSpacing) + self._gridOffsetY
                if dm.isFowSet(x, y):
                    if isDM:
                        painter.setOpacity(0.4)
                    else:
                        painter.setOpacity(1.0)
                else:
                    painter.setOpacity(0.0)
                painter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern))
                painter.drawRect(int(left), int(top), int(self._gridSpacing), int(self._gridSpacing))

    def computeColumnAndRow(self, clientX, clientY):
        self._selectedColumn = int((clientX - self._gridOffsetX) / self._gridSpacing)
        self._selectedRow = int((clientY - self._gridOffsetY) / self._gridSpacing)

    def handleFOWSelection(self, rect):
        dm: DungeonManager = ServicesManager.getDungeonManager()
        if not dm.isDungeonMaster or dm.editMode:
            return
        where: QtCore.QRect = rect.normalized()
        if where.left() < 0 or (where.left() + where.width()) > self.width():
            return
        if where.top() < 0 or (where.top() + where.height()) > self.height():
            return
        self.computeColumnAndRow(where.left(), where.top())
        startingColumn = self._selectedColumn
        startingRow = self._selectedRow
        self.computeColumnAndRow(where.left() + where.width(), where.top() + where.height())
        endingColumn = self._selectedColumn
        endingRow = self._selectedRow
        # use top left cell as reference. Toggle what it is currently set to
        self.clearFOW = dm.isFowSet(startingColumn, startingRow)
        self.toggleFOW = True
        for column in range(startingColumn, endingColumn + 1):
            for row in range(startingRow, endingRow + 1):
                self._selectedColumn = column
                self._selectedRow = row
                self.handleProperFOWAtSelectedPosition()
        self.update(0, 0, self.width(), self.height())
        dm.saveFow()

    def handleProperFOWAtSelectedPosition(self):
        currentFOW = ServicesManager.getDungeonManager().isFowSet(self._selectedColumn, self._selectedRow)
        # only adjust if different
        if currentFOW == self.clearFOW:
            ServicesManager.getDungeonManager().setFow(self._selectedColumn, self._selectedRow, not currentFOW)
