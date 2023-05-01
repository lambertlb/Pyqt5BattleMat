"""
GPL 3 file header
"""


class DataRequesterResponse:

	def __init__(self, userCallback):
		self.userCallback = userCallback
		self.hadException = False
		self.data = None
		self.task = None
		pass

	def getUserCallback(self):
		return self.userCallback

	def getData(self):
		"""
		get data from operation
		:return: data
		"""
		return self.data

	def hadError(self):
		"""
		was there an error
		:return: True if was error
		"""
		return self.hadException

	def cleanUp(self):
		self.task.disconnectAll()
