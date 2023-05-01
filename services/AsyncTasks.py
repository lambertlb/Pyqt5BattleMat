"""
GPL 3 file header
"""
import json
import traceback

import requests
from PyQt5 import QtCore
from PyQt5.QtCore import QRunnable, QThreadPool, QObject
from PyQt5.QtGui import QImage
from buildurl import BuildURL

from services.serviceData.DataRequesterResponse import DataRequesterResponse


class AsyncSignal(QObject):
	"""
	Small worker class so QRunnable can call signals
	"""
	success = QtCore.pyqtSignal(DataRequesterResponse)
	failure = QtCore.pyqtSignal(DataRequesterResponse)


# global reference to thread pool
asyncPool = None


class AsynchBase(QRunnable):
	"""
	Class to allow long takes to run in thread pool
	"""
	signaler = None  # so we can call signals
	returnData = None

	def __init__(self, onSuccess, onFailure):
		super().__init__()
		self.onSuccess = onSuccess
		self.onFailure = onFailure
		self.signaler = AsyncSignal()  # so we can call signals
		self.signaler.success.connect(onSuccess)
		self.signaler.failure.connect(onFailure)
		if self.returnData is None:
			self.returnData = DataRequesterResponse(None)
		self.returnData.task = self
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
			self.returnData.hadException = True
			traceback.print_exc()
		self.taskFinished()

	def runTask(self):
		"""
		Subclasses need to override this method to do their work
		:return: None
		"""
		pass

	def taskFinished(self):
		"""
		Subclasses need to override this method to handle things after task is finished
		:return: None
		"""
		pass

	def hadError(self):
		"""
		Subclasses need to override this method to getting errors
		:return:True if there was an error
		"""
		return self.returnData.hadException

	def	disconnectAll(self):
		self.signaler.success.disconnect(self.onSuccess)
		self.signaler.failure.disconnect(self.onFailure)


class AsyncImage(AsynchBase):
	"""
	Task to asynchronously load an image.
	if the URL starts with http it assumes a web request
	else if tries to load from file
	"""
	def __init__(self, url,  onSuccess, onFailure):
		self.url = url
		self.reply = None
		super(AsyncImage, self).__init__(onSuccess, onFailure)

	def runTask(self):
		"""
			Runs in background thread to load image
			:return: None
			"""
		if str(self.url).startswith('http'):    # is this a web request?
			self.reply = requests.get(self.url)
			if self.reply.status_code == 200:
				self.returnData.data = QImage()
				self.returnData.data.loadFromData(self.reply.content)
		else:
			self.returnData.data = QImage(self.url)

	def taskFinished(self):
		"""
		Task is finished need to signal to originator
		:return: None
		"""
		if self.hadError():
			self.signaler.failure.emit(self.returnData)
		else:
			self.signaler.success.emit(self.returnData)

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self.returnData.hadError() or self.returnData.getData() is None or self.returnData.getData().isNull()

	def getImage(self):
		"""
		get the image
		:return: QImage
		"""
		return self.returnData.getData()


class AsyncJsonData(AsynchBase):
	"""
	Task to asynchronously load json.
	"""
	def __init__(self, url, requestData, dataResponse):
		self.url = url
		self.requestData = requestData
		self.returnData = dataResponse
		self.reply = None
		super(AsyncJsonData, self).__init__(dataResponse.onSuccess, dataResponse.onFailure)

	def runTask(self):
		"""
		Runs in background thread to load image
		:return: None
		"""
		url = BuildURL(self.url)
		# if self.token is not None:
		# 	parameters.token = self.token
		url += self.requestData.__dict__
		urlStr = str(url)
		headers = {'Content-type': 'text/plain', 'Accept': 'text/plain'}
		data = data=json.dumps(self.requestData, default=vars)
		self.reply = requests.post(urlStr, '', headers=headers)
		if self.reply.status_code == 200:
			self.returnData.data = self.reply

	def taskFinished(self):
		"""
		Task is finished need to signal to originator
		:return: None
		"""
		if self.hadError():
			self.signaler.failure.emit(self.returnData)
		else:
			self.signaler.success.emit(self.returnData)

	def hadError(self):
		"""
		Was there and error
		:return: True is there was
		"""
		return self.returnData.hadError() or self.returnData.getData() is None

	def getJsonData(self):
		"""
		get the image
		:return: QImage
		"""
		return self.returnData.getData()
