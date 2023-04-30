"""
MIT License

Copyright (c) 2023 Leon Lambert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class ServicesManager:
	"""
	Central hub for managing all available services.
	THis make a place where dependency injection can happen
	to facilitate unit testing
	"""

	# static singleton of event manager
	_eventManager = None
	# static singleton of Config manager
	_configManager = None
	# static singleton of Dungeon manager
	_dungeonManager = None
	# static singleton of Data Requester
	_dataRequester = None

	@staticmethod
	def getEventManager():
		"""
		Get event manager
		:return: event manager
		"""
		return ServicesManager._eventManager

	@staticmethod
	def setEventManager(eventManager):
		"""
		allow programmer to set their own event manager for things like unit test
		:return: None
		"""
		ServicesManager._eventManager = eventManager

	@staticmethod
	def getConfigManager():
		"""
		Get event manager
		:return: event manager
		"""
		return ServicesManager._configManager

	@staticmethod
	def setConfigManager(configManager):
		"""
		allow programmer to set their own config manager for things like unit test
		:return: None
		"""
		ServicesManager._configManager = configManager

	@staticmethod
	def getDungeonManager():
		"""
		Get event manager
		:return: event manager
		"""
		return ServicesManager._dungeonManager

	@staticmethod
	def setDungeonManager(dungeonManager):
		"""
		allow programmer to set their own Dungeon Manager manager for things like unit test
		:return: None
		"""
		ServicesManager._dungeonManager = dungeonManager

	@staticmethod
	def getDataRequester():
		"""
		Get Data Requester
		:return: Data Requester
		"""
		return ServicesManager._dataRequester

	@staticmethod
	def setDataRequester(dataRequester):
		"""
		allow programmer to set their own Data Requester for things like unit test
		:return: None
		"""
		ServicesManager._dataRequester = dataRequester
