"""
GPL 3 file header
"""
from enum import Enum
from enum import auto


class ReasonForAction(Enum):
    """
    Enumeration of reasons for all global events
    """
    LOGGED_IN = auto()
    LOAD_IMAGE = auto()

    DungeonDataDeleted = auto()
    DungeonDataLoaded = auto()
    DungeonDataCreated = auto()
    DungeonDataSaved = auto()
    DungeonSelected = auto()
    DungeonDataReadyToEdit = auto()
    DungeonDataReadyToJoin = auto()
    DungeonSelectedLevelChanged = auto()

    SessionListChanged = auto()
    SessionDataChanged = auto()
    SessionDataSaved = auto()

    DMStateChange = auto()
    MonsterPogsLoaded = auto()
    RoomObjectPogsLoaded = auto()

    PogDataChanged = auto()
    PogWasSelected = auto()

    MouseDownEventBubble = auto()

    LastReason = auto()
