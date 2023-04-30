"""
GPL 3 file header
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
