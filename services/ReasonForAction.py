"""
GPL 3 file header
"""
from enum import Enum
from enum import auto


class ReasonForAction(Enum):
	LOGGED_IN = auto()
	LOAD_IMAGE = auto()

	DungeonDataDeleted = auto()
	DungeonDataLoaded = auto()
	DungeonDataCreated = auto()
	DungeonSelected = auto()
	DungeonDataReadyToEdit = auto()

	SessionListChanged = auto()
	DMStateChange = auto()
	MonsterPogsLoaded = auto()
	RoomObjectPogsLoaded = auto()

	LastReason = auto()
