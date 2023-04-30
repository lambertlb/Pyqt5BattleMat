"""
GPL 3 file header
"""
from enum import Enum
from enum import auto


class ReasonForEvent(Enum):
	LOGGED_IN = auto()
	LOAD_IMAGE = auto()
