"""
GPL 3 file header
"""


class PlayerFlag:
	DisplayNames = {
		0: 'None',
		1: 'Dead',
		2: 'Invisible'
	}

	NONE = 0
	DEAD = 1
	INVISIBLE = 2

	@staticmethod
	def displayName(value):
		return PlayerFlag.DisplayNames[value]
