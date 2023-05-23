"""
GPL 3 file header
"""


class DungeonMasterFlag:
	DisplayNames = {
		0: 'None',
		1: 'Invisible to Player',
		2: 'Transparent Background',
		4: 'Shifted to Right',
		8: 'Shifted to Top',
		16: 'Dark background in edit mode'
	}

	NONE = 0
	INVISIBLE_FROM_PLAYER = 1
	TRANSPARENT_BACKGROUND = 2
	SHIFT_RIGHT = 4
	SHIFT_TOP = 8
	DARK_BACKGROUND = 16

	@staticmethod
	def displayName(value):
		return DungeonMasterFlag.DisplayNames[value]
