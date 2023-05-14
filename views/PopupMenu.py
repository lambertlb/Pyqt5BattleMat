"""
GPL 3 file header
"""
from functools import partial

from PyQt5 import QtWidgets

from services.DungeonMasterFlag import DungeonMasterFlag
from services.PlayerFlags import PlayerFlag
from services.ServicesManager import ServicesManager


class PopupMenu(QtWidgets.QMenu):

	def __init__(self, *args):
		super(PopupMenu, self).__init__(*args)
		self.playerFlagsMenu = self.addMenu('Player Flags')

		self.deadToggleAction = self.playerFlagsMenu.addAction('Dead Toggle')
		self.deadToggleAction.triggered.connect(partial(self.toggleDead, self.deadToggleAction))
		self.deadToggleAction.setCheckable(True)

		self.invisibleToggleAction = self.playerFlagsMenu.addAction('Invisible Toggle')
		self.invisibleToggleAction.triggered.connect(partial(self.toggleInvisible, self.invisibleToggleAction))
		self.invisibleToggleAction.setCheckable(True)

		self.dmFlagsMenu = self.addMenu('Player Flags')

		self.invisibleToPlayerToggleAction = self.dmFlagsMenu.addAction('Invisible Toggle')
		self.invisibleToPlayerToggleAction.triggered.connect(partial(self.toggleInvisibleToPlayer, self.invisibleToPlayerToggleAction))
		self.invisibleToPlayerToggleAction.setCheckable(True)

	# noinspection PyMethodMayBeStatic
	# noinspection PyUnusedLocal
	def toggleDead(self, action, state):
		ServicesManager.getDungeonManager().toggleFlagOfSelectedPog(PlayerFlag.DEAD)

	# noinspection PyMethodMayBeStatic
	# noinspection PyUnusedLocal
	def toggleInvisible(self, action, state):
		ServicesManager.getDungeonManager().toggleFlagOfSelectedPog(PlayerFlag.INVISIBLE)

	# noinspection PyMethodMayBeStatic
	# noinspection PyUnusedLocal
	def toggleInvisibleToPlayer(self, action, state):
		ServicesManager.getDungeonManager().toggleFlagOfSelectedPog(DungeonMasterFlag.INVISIBLE_FROM_PLAYER)

	def showMe(self, pos):
		self.exec_(pos)
