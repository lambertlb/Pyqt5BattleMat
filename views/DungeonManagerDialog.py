"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from generated.dungeonManagerDialog import Ui_DungeonSelectDialog
from services.ReasonForEvent import ReasonForEvent
from services.ServicesManager import ServicesManager


class DungeonManagerDialog(QtWidgets.QDialog, Ui_DungeonSelectDialog):
	isDM = False
	isOkToCreateDungeon = False
	isTemplateSelected = False
	isOkToDelete = False
	isOkToCreateSession = False
	isOkToDeleteSession = False
	isOkToDMSession = False
	isOkToJoinSession = False
	isValidDungeonForSessions = False
	isSessionSelected = False
	selectedDungeonUUID = ''

	def __init__(self, *args):
		super(DungeonManagerDialog, self).__init__(*args)
		self.setupUi(self)
		self.setupEventHandling()

	def setupEventHandling(self):
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)
		self.iAmDungeonMaster.clicked.connect(self.iAmDMChanged)
		self.editDungeonButton.clicked.connect(self.editDungeon)
		self.deleteDungeonButton.clicked.connect(self.deleteDungeon)
		self.deleteSessionButton.clicked.connect(self.deleteSession)
		self.createDungeonButton.clicked.connect(self.createDungeon)
		self.createSessionButton.clicked.connect(self.createSession)
		self.dmSessionButton.clicked.connect(self.dmSession)
		self.templateList.currentTextChanged.connect(self.templateSelected)
		self.newDungeonName.textChanged[str].connect(self.newDungeonNameText)
		self.sessionList.currentTextChanged.connect(self.sessionSelected)
		self.newSessionName.textChanged[str].connect(self.newSessionNameText)
		pass

	def show(self):
		self.intialize()
		self.refreshView()
		super(DungeonManagerDialog, self).show()

	def intialize(self):
		_translate = QtCore.QCoreApplication.translate
		self.newDungeonName.setText(_translate("DungeonSelectDialog", "Enter Dungeon Name"))
		self.newSessionName.setText(_translate("DungeonSelectDialog", "Enter Session Name"))
		self.hideItem(self.deleteSessionButton)
		self.hideItem(self.createSessionButton)
		self.hideItem(self.newSessionName)
		self.hideItem(self.label_2)
		self.hideItem(self.deleteDungeonButton)
		self.hideItem(self.editDungeonButton)
		self.hideItem(self.createDungeonButton)
		self.hideItem(self.newDungeonName)
		if self.isDM:
			self.dmSessionButton.setText(_translate("DungeonSelectDialog", "DM the Session"))
		else:
			self.dmSessionButton.setText(_translate("DungeonSelectDialog", "Join the Session"))
		self.setStates()

	def setStates(self):
		self.newDungeonName.setDisabled(False)
		self.deleteDungeonButton.setDisabled(not self.isOkToDelete)
		self.editDungeonButton.setDisabled(not self.isTemplateSelected)
		self.createDungeonButton.setDisabled(not self.isOkToCreateDungeon)
		self.setSessionStates()

	def setSessionStates(self):
		self.deleteSessionButton.setDisabled(not self.isOkToDeleteSession)
		self.createSessionButton.setDisabled(not self.isOkToCreateSession)
		self.sessionList.setDisabled(not self.isOkToShowSessions())
		self.dmSessionButton.setDisabled(not self.isOkToDMSession)
		self.newSessionName.setDisabled(not self.isOkToDelete)
		if self.isOkToDelete:
			self.newSessionName.setText('Enter Session Name')

	def hideItem(self, item):
		if self.isDM:
			item.show()
		else:
			item.hide()

	def iAmDMChanged(self, state):
		self.isDM = state
		self.intialize()

	def editDungeon(self):
		pass

	def deleteDungeon(self):
		pass

	def deleteSession(self):
		pass

	def createDungeon(self):
		pass

	def createSession(self):
		pass

	def dmSession(self):
		pass

	def templateSelected(self, selectedText):
		self.resetSessionLogic()
		self.resetDungeonLogic()
		self.isTemplateSelected = not selectedText.startswith('Select ')
		if self.isTemplateSelected:
			self.selectedDungeonUUID = ServicesManager.getDungeonManager().getDungeonToUUIDMap()[selectedText]
			self.isOkToDelete = ServicesManager.getDungeonManager().okToDeleteThisTemplate(self.selectedDungeonUUID)
			self.isValidDungeonTemplateForSessions(selectedText)
		if self.isValidDungeonForSessions:
			ServicesManager.getDungeonManager().getSessionList(self.selectedDungeonUUID)
		self.setStates()
		pass

	def isValidDungeonTemplateForSessions(self, dungeonName):
		self.isValidDungeonForSessions = not dungeonName.startswith("Select ") and not dungeonName.startswith("Template ")

	def newDungeonNameText(self, newName):
		pass

	def sessionSelected(self, selectedText):
		pass

	def newSessionNameText(self, newSession):
		pass

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForEvent.DungeonDataDeleted:
			self.refreshView()
		elif eventData.eventReason == ReasonForEvent.DungeonDataLoaded:
			self.refreshView()
		elif eventData.eventReason == ReasonForEvent.DungeonDataCreated:
			self.refreshView()
		elif eventData.eventReason == ReasonForEvent.SessionListChanged:
			self.refreshSessionData()

	def refreshView(self):
		self.resetDungeonLogic()
		self.loadDungeonList()
		self.setStates()
		self.refreshSession()
		pass

	def resetDungeonLogic(self):
		self.isOkToCreateDungeon = False
		self.isOkToDelete = False
		self.isTemplateSelected = False
		self.selectedDungeonUUID = ''

	def loadDungeonList(self):
		self.templateList.clear()
		self.templateList.addItem('Select a Dungeon for Operations')
		uuidMap = ServicesManager.getDungeonManager().getDungeonToUUIDMap()
		sortedMap = sorted(uuidMap.keys())
		for dungeonName in sortedMap:
			self.templateList.addItem(dungeonName)

	def refreshSession(self):
		self.resetSessionLogic()
		self.refreshSessionData()

	def resetSessionLogic(self):
		self.isValidDungeonForSessions = False
		self.isOkToCreateSession = False
		self.isSessionSelected = False
		self.isOkToDeleteSession = False
		self.isOkToDMSession = False
		self.isOkToJoinSession = False

	def refreshSessionData(self):
		self.setSessionStates()
		self.sessionList.clear()
		if self.isDM:
			self.sessionList.addItem('Select a Session to DM')
		else:
			self.sessionList.addItem('Select a Session to Join')
		if not self.isOkToShowSessions():
			return
		sessionListData = ServicesManager.getDungeonManager().getSessionListData()
		amount = len(sessionListData.sessionNames)
		for i in range(amount):
			sessionName = sessionListData.sessionNames[i]
			sessionUUID = sessionListData.sessionUUIDs[i]
			self.sessionList.addItem(sessionName, sessionUUID)

	def isOkToShowSessions(self):
		return self.isValidDungeonForSessions and ServicesManager.getDungeonManager().getSessionListData() is not None
