"""
GPL 3 file header
"""


class DataRequesterResponse:

	def __init__(self):
		self._hadException = False
		self._data = None
		self._task = None
		self._onSuccess = None
		self._onFailure = None
		self._userOnSuccess = None
		self._userOnFailure = None

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, value):
		self._data = value

	@property
	def hadException(self):
		return self._hadException

	@hadException.setter
	def hadException(self, value):
		self._hadException = value

	@property
	def task(self):
		return self._task

	@task.setter
	def task(self, value):
		self._task = value

	@property
	def userOnSuccess(self):
		return self._userOnSuccess

	@userOnSuccess.setter
	def userOnSuccess(self, value):
		self._userOnSuccess = value

	@property
	def userOnFailure(self):
		return self._userOnFailure

	@userOnFailure.setter
	def userOnFailure(self, value):
		self._userOnFailure = value

	@property
	def onSuccess(self):
		return self._onSuccess

	@onSuccess.setter
	def onSuccess(self, value):
		self._onSuccess = value

	@property
	def onFailure(self):
		return self._onFailure

	@onFailure.setter
	def onFailure(self, value):
		self._onFailure = value

	def hadError(self):
		"""
		was there an error
		:return: True if was error
		"""
		return self._hadException
