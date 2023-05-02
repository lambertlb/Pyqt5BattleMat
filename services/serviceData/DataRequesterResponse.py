"""
GPL 3 file header
"""


class DataRequesterResponse:

	def __init__(self):
		self.hadException = False
		self.data = None
		self.task = None
		self.userOnSuccess = None
		self.userOnFailure = None
		pass

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
