"""
GPL 3 file header
"""
import json
import os
import re
import threading
import traceback

import requests
from PySide2 import QtCore
from PySide2.QtCore import QRunnable, QThreadPool, QObject
from PySide2.QtGui import QImage

from services.serviceData.DataRequesterResponse import DataRequesterResponse


class AsyncSignal(QObject):
    """
    Small worker class so QRunnable can call signals
    """
    finished = QtCore.Signal(DataRequesterResponse)


# global reference to thread pool
asyncPool = None


class AsynchBase(QRunnable):
    """
    Class to allow long tasks to run in thread pool
    This is a base class and only serves as a parent for
    the actual tasks.
    """

    def __init__(self, onSuccess, onFailure, dataResponse):
        super().__init__()
        self._signaler = None  # so we can call signals
        self._onSuccess = onSuccess  # method to call upon success
        self._onFailure = onFailure  # method to call upon failure
        self._returnData = dataResponse  # data to hand back as response to task
        self._returnData.task = self  # reference to self
        self._connectToken = None  # connect token used for disconnecting
        self._executeTask = True  # True if the task is to be actually executed

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

    # noinspection PyUnresolvedReferences
    def submit(self):

        # only execute if true. Some tasks may look up data in a cache
        # and might not actually have to go into execution queue.
        if not self._executeTask:
            return
        self._signaler = AsyncSignal()  # so we can call signals
        self._connectToken = self._signaler.finished.connect(taskDone)
        global asyncPool
        if asyncPool is None:
            asyncPool = QThreadPool.globalInstance()
            asyncPool.setMaxThreadCount(100)  # make sure queue is large enough
        asyncPool.start(self)

    @QtCore.Slot()
    def run(self):
        """
        run the task and handle exception
        :return: None
        """
        try:
            self.runTask()
        except (Exception,):
            self._returnData.hadException = True
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


@QtCore.Slot(DataRequesterResponse)
def taskDone(dataRequesterResponse):
    """
    target for signal and is run after task is finished
    """
    task = dataRequesterResponse.task
    if task.hadError():
        task.onFailure(task.returnData)
    else:
        task.onSuccess(task.returnData)
    task.signaler.finished.disconnect(taskDone)  # disconnect so object can be garbage collected


class AsyncImage(AsynchBase):
    """
    Task to asynchronously load an image.
    if the URL starts with http it assumes a web request
    else if tries to load from file.

    This will keep a cache of previously loaded images and save
    time by reuse if it can.
    """
    lock = threading.RLock()  # lock to serialize access to queue
    imageCache = {}  # cache of images
    imagesBeingLoaded = {}  # cache of images being loaded

    def __init__(self, url, onSuccess, onFailure):
        self.url = re.sub("\\\\", "/", url)
        self.reply = None
        self.pending = []
        self.saveOnSuccess = onSuccess
        self.saveOnFailure = onFailure
        super(AsyncImage, self).__init__(onSuccess, onFailure, DataRequesterResponse())
        AsyncImage.lock.acquire()
        cachedImage = AsyncImage.imageCache.get(self.url)  # is image already loaded?
        try:
            if cachedImage:
                self._executeTask = False
                self._returnData.data = cachedImage
                onSuccess(self._returnData)  # tell client about image
                return
            # see if there is a pending task to load same image
            pendingLoad = AsyncImage.imagesBeingLoaded.get(self.url)
            if pendingLoad:
                self._executeTask = False
                pendingLoad.pending.append(self)  # add myself to the pending task for notification
                return
            AsyncImage.imagesBeingLoaded[self.url] = self
            # override normal callbacks so I can notify other pending tasks
            self.onSuccess = self.hadSuccess
            self.onFailure = self.hadFailure
        finally:
            AsyncImage.lock.release()

    def runTask(self):
        """
            Runs in background thread to load image
            :return: None
            """
        if str(self.url).startswith('http'):  # is this a web request?
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

    # noinspection PyUnusedLocal
    def hadSuccess(self, data):
        """
        Image was successfully load.
        If other tasks where also waiting for load we need to notify them
        """
        AsyncImage.lock.acquire()
        try:
            AsyncImage.imagesBeingLoaded.pop(self.url)
            AsyncImage.imageCache[self.url] = self.getImage()  # add to image cache
        finally:
            AsyncImage.lock.release()
        self.saveOnSuccess(self._returnData)
        for pendingTasks in self.pending:
            pendingTasks.returnData.data = self._returnData.data
            pendingTasks.saveOnSuccess(pendingTasks.returnData)  # notify of load

    # noinspection PyUnusedLocal
    def hadFailure(self, data):
        """
        Image was failed to load.
        If other tasks where also waiting for load we need to notify them
        """

        AsyncImage.lock.acquire()
        try:
            AsyncImage.imagesBeingLoaded.pop(self.url)
        finally:
            AsyncImage.lock.release()
        self.saveOnFailure(self._returnData)
        for pendingTasks in self.pending:
            pendingTasks.saveOnFailure(pendingTasks.returnData)


class AsyncJsonData(AsynchBase):
    """
    Task to asynchronously load json data.
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
        headers = {'Content-type': 'text/plain', 'Accept': 'application/json'}
        sendData = ''
        if self.data is not None:  # anything to send?
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
        get the Json return data
        :return: json
        """
        return self.returnData.data


class AsyncDownload(AsynchBase):
    """
    Task to asynchronously download a file.
    """

    def __init__(self, url, onSuccess, onFailure):
        self.url = url
        self.reply = None
        super(AsyncDownload, self).__init__(onSuccess, onFailure, DataRequesterResponse())

    def runTask(self):
        """
            Runs in background thread to load file data
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
    Task to asynchronously upload a file.
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
            Runs in background thread to upload file
            :return: None
            """
        with open(self.filePath, 'rb') as img:
            name_img = os.path.basename(self.filePath)
            files = {'image': (name_img, img, 'multipart/form-data')}
            with requests.Session() as s:
                results = s.post(self.url, files=files, params=self.requestData.__dict__)
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
    Task to asynchronously execute command on server.
    """

    def __init__(self, url, requestData, dataResponse):
        self.url = url
        self.requestData = requestData
        self._returnData = dataResponse
        self.reply = None
        super(AsyncCommand, self).__init__(dataResponse.onSuccess, dataResponse.onFailure, dataResponse)

    def runTask(self):
        """
            Runs in background thread to execute command on server
            :return: None
            """
        headers = {'Content-type': 'binary', 'Accept': 'binary'}
        results = requests.post(self.url, headers=headers, params=self.requestData.__dict__)
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
