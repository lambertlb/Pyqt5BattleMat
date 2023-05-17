"""
GPL 3 file header
"""
import enum
from enum import Flag, auto


class PogPlaceEnumMeta(enum.EnumMeta):

	def __new__(mcs, name, bases, attrs):
		next_value = 0
		obj = super().__new__(mcs, name, bases, attrs)
		obj._value2member_map_ = {}
		for m in obj:
			value, displayString = m.value
			m._value_ = next_value
			m.displayString = displayString
			obj._value2member_map_[next_value] = m
			next_value = PogPlaceEnumMeta.getNextValue(next_value)
		return obj

	@staticmethod
	def getNextValue(value):
		if value == 0:
			return 1
		return value << 1


class PogPlace(Flag, metaclass=PogPlaceEnumMeta):
	DUNGEON_LEVEL = auto(), 'Dungeon Level'
	SESSION_LEVEL = auto(), 'Session Level'
	SESSION_RESOURCE = auto(), 'Player Location'
	COMMON_RESOURCE = auto(), 'Common Resource'

	def _get_value(self, **kwargs):
		return self.value
