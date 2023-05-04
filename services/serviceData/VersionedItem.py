"""
GPL 3 file header
"""
from enum import Enum, auto


class VersionedItem(Enum):
	COMMON_RESOURCE_MONSTERS = auto()
	COMMON_RESOURCE_ROOMOBECTS = auto()
	DUNGEON_LEVEL_MONSTERS = auto()
	DUNGEON_LEVEL_ROOMOBJECTS = auto()
	SESSION_LEVEL_MONSTERS = auto()
	SESSION_LEVEL_ROOMOBJECTS = auto()
	SESSION_RESOURCE_PLAYERS = auto()
	FOG_OF_WAR = auto()
	LAST_VERSIONED_ITEM = auto()
