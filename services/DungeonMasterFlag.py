"""
GPL 3 file header
"""
import enum
from enum import Flag, auto


class DungeonMasterEnumMeta(enum.EnumMeta):
	def __new__(mcs, name, bases, attrs):
		next_value = 0
		obj = super().__new__(mcs, name, bases, attrs)
		obj._value2member_map_ = {}
		for m in obj:
			value, display_string = m.value
			m._value_ = next_value
			m.display_string = display_string
			obj._value2member_map_[next_value] = m
			next_value = DungeonMasterEnumMeta.getNextValue(next_value)
		return obj

	@staticmethod
	def getNextValue(value):
		if value == 0:
			return 1
		return value << 1


class DungeonMasterFlag(Flag, metaclass=DungeonMasterEnumMeta):
	NONE = auto(), 'None'
	INVISIBLE_FROM_PLAYER = auto(), 'Invisible to Player'
	TRANSPARENT_BACKGROUND = auto(), 'Transparent Background'
	SHIFT_RIGHT = auto(), 'Shifted to Right'
	SHIFT_TOP = auto(), 'Shifted to Top'
	DARK_BACKGROUND = auto(), 'Dark background in edit mode'
