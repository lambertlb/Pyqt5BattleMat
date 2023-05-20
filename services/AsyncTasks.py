"""
GPL 3 file header
"""
import json
import traceback

import requests
from PyQt5 import QtCore
from PyQt5.QtCore import QRunnable, QThreadPool, QObject
from PyQt5.QtGui import QImage

from services.serviceData.DataRequesterResponse import DataRequesterResponse


class AsyncSignal(QObject):
	"""
	Small worker class so QRunnable can call signals
	"""
	finished = QtCore.pyqtSignal(DataRequesterResponse)


# global reference to thread pool
asyncPool = None


class AsynchBase(QRunnable):
	"""
	Class to allow long takes to run in thread pool
	"""

	def __init__(self, onSuccess, onFailure, dataResponse):
		super().__init__()
		self._signaler = None  # so we can call signals
		self._onSuccess = onSuccess
		self._onFailure = onFailure
		self._returnData = dataResponse
		self._returnData.task = self
		self._connectToken = None

	@property
	def signaler(self):
		return self._signaler

	@property
	def connectToken(self):
		return self._connectToken

	@property
	def returnData(self):
		return self._returnData

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

	def submit(self):
		self._signaler = AsyncSignal()  # so we can call signals
		self._connectToken = self._signaler.finished.connect(taskDone)
		global asyncPool
		if asyncPool is None:
			asyncPool = QThreadPool.globalInstance()
			asyncPool.setMaxThreadCount(30)
		asyncPool.start(self)

	@QtCore.pyqtSlot()
	def run(self):
		"""
		run the task and handle exception
		:return: None
		"""
		try:
			self.runTask()
		except (Exception,):
			self._returnData.hadException(True)
			traceback.print_exc()
		self._signaler.finished.emit(self._returnData)

	def runTask(self):
		"""
		Subclasses need to override this method to do their work
		:return: None
		"""
		pass

	def hadError(self):
		"""
		Subclasses need to override this method to getting errors
		:return:True if there was an error
		"""
		return self._returnData.hadException()


@QtCore.pyqtSlot(DataRequesterResponse)
def taskDone(dataRequesterResponse):
	"""
	target for signal and is run after task is finished
	"""
	task = dataRequesterResponse.task
	if task.hadError():
		task.onFailure(task.returnData)
	else:
		task.onSuccess(task.returnData)
	task.signaler.finished.disconnect(task.connectToken)


class AsyncImage(AsynchBase):
	"""
	Task to asynchronously load an image.
	if the URL starts with http it assumes a web request
	else if tries to load from file
	"""
	def __init__(self, url,  onSuccess, onFailure):
		self.url = url
		self.reply = None
		super(AsyncImage, self).__init__(onSuccess, onFailure, DataRequesterResponse())

	def runTask(self):
		"""
			Runs in background thread to load image
			:return: None
			"""
		if str(self.url).startswith('http'):    # is this a web request?
			self.reply = requests.get(self.url)
			if self.reply.status_code == 200:
				self._returnData._data = QImage()
				self._returnData._data.loadFromData(self.reply.content)
		else:
			self._returnData._data = QImage(self.url)

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self._returnData.hadError() or self._returnData.data is None or self._returnData.data.isNull()

	def getImage(self):
		"""
		get the image
		:return: QImage
		"""
		return self._returnData.data


class AsyncJsonData(AsynchBase):
	"""
	Task to asynchronously load json.
	"""
	def __init__(self, url, requestData, dataResponse, data):
		self.url = url
		self.requestData = requestData
		self._returnData = dataResponse
		self.reply = None
		self.data = data
		super(AsyncJsonData, self).__init__(dataResponse.onSuccess, dataResponse.onFailure, dataResponse)

	def runTask(self):
		"""
		Runs in background thread to load image
		:return: None
		"""
		headers = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
		sendData = ''
		if self.data is not None:
			sendData = json.dumps(self.data, default=vars)
		self.reply = requests.post(self.url, sendData, headers=headers, params=self.requestData.__dict__)
		if self.reply.status_code == 200:
			self.returnData.data = self.reply

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self.returnData.hadException or self.returnData.data is None

	def getJsonData(self):
		"""
		get the image
		:return: QImage
		"""
		return self.returnData.data


class AsyncDownload(AsynchBase):
	"""
	Task to asynchronously load an image.
	if the URL starts with http it assumes a web request
	else if tries to load from file
	"""
	def __init__(self, url,  onSuccess, onFailure):
		self.url = url
		self.reply = None
		super(AsyncDownload, self).__init__(onSuccess, onFailure, DataRequesterResponse())

	def runTask(self):
		"""
			Runs in background thread to load image
			:return: None
			"""
		self.reply = requests.get(self.url, allow_redirects=True)
		if self.reply.status_code == 200:
			self._returnData._data = self.reply.content

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self._returnData.hadError() or self._returnData.data is None


class AsyncUpload(AsynchBase):
	"""
	Task to asynchronously load an image.
	if the URL starts with http it assumes a web request
	else if tries to load from file
	"""
	def __init__(self, url, filePath, requestData, dataResponse):
		self.url = url
		self.requestData = requestData
		self._returnData = dataResponse
		self.reply = None
		self.filePath = filePath
		super(AsyncUpload, self).__init__(dataResponse.onSuccess, dataResponse.onFailure, dataResponse)

	def runTask(self):
		"""
			Runs in background thread to load image
			:return: None
			"""
		data = open(self.filePath, "rb")
		results = requests.post(self.url, files={"form_field_name": data}, params=self.requestData.__dict__)
		if results.ok:
			self.returnData.data = 'good'
		else:
			self.returnData.data = None

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self._returnData.hadError() or self._returnData.data is None


class AsyncCommand(AsynchBase):
	"""
	Task to asynchronously load an image.
	if the URL starts with http it assumes a web request
	else if tries to load from file
	"""
	def __init__(self, url, requestData, dataResponse):
		self.url = url
		self.requestData = requestData
		self._returnData = dataResponse
		self.reply = None
		super(AsyncCommand, self).__init__(dataResponse.onSuccess, dataResponse.onFailure, dataResponse)

	def runTask(self):
		"""
			Runs in background thread to load image
			:return: None
			"""
		headers = {'Content-type': 'binary', 'Accept': 'binary'}
		results = requests.post(self.url, headers=headers,  params=self.requestData.__dict__)
		if results.ok:
			self.returnData.data = 'good'
		else:
			self.returnData.data = None

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self._returnData.hadError() or self._returnData.data is None
