"""
GPL 3 file header
"""

from enum import Flag, auto


class PogPlace(Flag):
	DUNGEON_LEVEL = auto()
	SESSION_LEVEL = auto()
	SESSION_RESOURCE = auto()
	COMMON_RESOURCE = auto()
