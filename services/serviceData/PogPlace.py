"""
GPL 3 file header
"""


class PogPlace:
	DisplayNames = {
		0: 'Dungeon Level',
		1: 'Session Level',
		2: 'Player Location',
		4: 'Common Resource'
	}

	DUNGEON_LEVEL = 0
	SESSION_LEVEL = 1
	SESSION_RESOURCE = 2
	COMMON_RESOURCE = 4

	@staticmethod
	def displayName(value):
		return PogPlace.DisplayNames[value]
