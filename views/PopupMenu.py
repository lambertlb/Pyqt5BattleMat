"""
GPL 3 file header
"""
from functools import partial

from PySide2 import QtWidgets

from services.DungeonMasterFlag import DungeonMasterFlag
from services.PlayerFlags import PlayerFlag
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager


class PopupMenu(QtWidgets.QMenu):

    def __init__(self, *args):
        super(PopupMenu, self).__init__(*args)
        self.pogData = None
        self.addPlayerFlags()
        self.addDmFlags()
        self.addPogNumbers()
        self.addUtilities()

    # noinspection PyAttributeOutsideInit
    def addDmFlags(self):
        self.dmFlagsMenu = self.addMenu('DM Flags')
        self.invisibleToPlayerToggleAction = self.dmFlagsMenu.addAction('Invisible Toggle')
        self.invisibleToPlayerToggleAction.triggered.connect(partial(self.toggleDMFlag,
                                                                     DungeonMasterFlag.INVISIBLE_FROM_PLAYER))
        self.invisibleToPlayerToggleAction.setCheckable(True)

        self.transparentBackgroundToggleAction = self.dmFlagsMenu.addAction('Transparent Toggle')
        self.transparentBackgroundToggleAction.triggered.connect(partial(self.toggleDMFlag,
                                                                         DungeonMasterFlag.TRANSPARENT_BACKGROUND))
        self.transparentBackgroundToggleAction.setCheckable(True)
        self.shiftRightToggleAction = self.dmFlagsMenu.addAction('Shift Right Toggle')
        self.shiftRightToggleAction.triggered.connect(partial(self.toggleDMFlag,
                                                              DungeonMasterFlag.SHIFT_RIGHT))
        self.shiftRightToggleAction.setCheckable(True)
        self.shiftTopToggleAction = self.dmFlagsMenu.addAction('Shift Top Toggle')
        self.shiftTopToggleAction.triggered.connect(partial(self.toggleDMFlag,
                                                            DungeonMasterFlag.SHIFT_TOP))
        self.shiftTopToggleAction.setCheckable(True)
        self.darkBackgroundToggleAction = self.dmFlagsMenu.addAction('Dark Background Toggle')
        self.darkBackgroundToggleAction.triggered.connect(partial(self.toggleDMFlag,
                                                                  DungeonMasterFlag.DARK_BACKGROUND))
        self.darkBackgroundToggleAction.setCheckable(True)

    # noinspection PyAttributeOutsideInit
    def addPlayerFlags(self):
        self.playerFlagsMenu = self.addMenu('Player Flags')
        self.deadToggleAction = self.playerFlagsMenu.addAction('Dead Toggle')
        self.deadToggleAction.triggered.connect(partial(self.toggleFlag, PlayerFlag.DEAD))
        self.deadToggleAction.setCheckable(True)
        self.invisibleToggleAction = self.playerFlagsMenu.addAction('Invisible Toggle')
        self.invisibleToggleAction.triggered.connect(partial(self.toggleFlag, PlayerFlag.INVISIBLE))
        self.invisibleToggleAction.setCheckable(True)

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def toggleFlag(self, flag, state):
        ServicesManager.getDungeonManager().togglePlayerFlagOfSelectedPog(flag)

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def toggleDMFlag(self, flag, state):
        ServicesManager.getDungeonManager().toggleDmFlagOfSelectedPog(PlayerFlag.INVISIBLE)

    def setupMenuData(self, pogData):
        self.setupPlayerFlagMenus(pogData)
        self.setupDmFlagMenus(pogData)

    def setupDmFlagMenus(self, pogData):
        self.invisibleToPlayerToggleAction.setChecked(pogData.isDmFlagSet(DungeonMasterFlag.INVISIBLE_FROM_PLAYER))
        self.transparentBackgroundToggleAction.setChecked(pogData.isDmFlagSet(DungeonMasterFlag.TRANSPARENT_BACKGROUND))
        self.shiftRightToggleAction.setChecked(pogData.isDmFlagSet(DungeonMasterFlag.SHIFT_RIGHT))
        self.shiftTopToggleAction.setChecked(pogData.isDmFlagSet(DungeonMasterFlag.SHIFT_TOP))
        self.darkBackgroundToggleAction.setChecked(pogData.isDmFlagSet(DungeonMasterFlag.DARK_BACKGROUND))

    def setupPlayerFlagMenus(self, pogData):
        self.deadToggleAction.setChecked(pogData.isPlayerFlagSet(PlayerFlag.DEAD))
        self.invisibleToggleAction.setChecked(pogData.isPlayerFlagSet(PlayerFlag.INVISIBLE))

    # noinspection PyAttributeOutsideInit
    def addPogNumbers(self):
        self.pogNumberMenu = self.addMenu('Pog Number')
        for i in range(21):
            self.deadToggleAction = self.pogNumberMenu.addAction(f'{i}')
            self.deadToggleAction.triggered.connect(partial(self.pogNumberAdded, i))

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def pogNumberAdded(self, number, state):
        ServicesManager.getDungeonManager().updateNumberOfSelectedPog(number)

    # noinspection PyAttributeOutsideInit
    def addUtilities(self):
        self.utilitiesMenu = self.addMenu('Utilities')
        self.deletePogAction = self.utilitiesMenu.addAction('Delete Pog')
        self.deletePogAction.triggered.connect(self.deletePog)

    # noinspection PyMethodMayBeStatic
    def deletePog(self):
        ServicesManager.getDungeonManager().deleteSelectedPog()
        ServicesManager.getEventManager().fireEvent(ReasonForAction.SessionDataSaved, None)

    def showMe(self, pos, pogData):
        self.pogData = pogData
        self.setupMenuData(pogData)
        self.exec_(pos)
