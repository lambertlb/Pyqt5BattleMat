"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from generated.dungeonManagerDialog import Ui_DungeonSelectDialog
from services.ReasonForAction import ReasonForAction
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
	templateListDisabled = False
	sessionListDisabled = False
	dungeonToCreate = ''
	selectedSessionName = None
	selectedSessionUUID = None
	sessionToCreate = None

	def __init__(self, needButtons, *args):
		super(DungeonManagerDialog, self).__init__(*args)
		self.needButtons = needButtons
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
		self.sessionList.currentIndexChanged.connect(self.sessionSelected)
		self.newSessionName.textChanged[str].connect(self.newSessionNameText)
		if not self.needButtons:
			button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
			button.setEnabled(False)
			button = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
			button.setEnabled(False)
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
		if not self.isOkToDelete:
			self.newSessionName.setText('Enter Session Name')

	def hideItem(self, item):
		if self.isDM:
			item.show()
		else:
			item.hide()

	def iAmDMChanged(self, state):
		self.isDM = state
		self.intialize()

	def templateSelected(self, selectedText):
		if self.templateListDisabled:
			return
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

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForAction.DungeonDataDeleted:
			self.refreshView()
		elif eventData.eventReason == ReasonForAction.DungeonDataLoaded:
			self.refreshView()
		elif eventData.eventReason == ReasonForAction.DungeonDataCreated:
			self.refreshView()
		elif eventData.eventReason == ReasonForAction.SessionListChanged:
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
		self.templateListDisabled = True
		self.templateList.clear()
		self.templateList.addItem('Select a Dungeon for Operations')
		uuidMap = ServicesManager.getDungeonManager().getDungeonToUUIDMap()
		sortedMap = sorted(uuidMap.keys())
		for dungeonName in sortedMap:
			self.templateList.addItem(dungeonName)
		self.templateListDisabled = False
		self.templateList.setCurrentIndex(0)

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

	def editDungeon(self):
		ServicesManager.getDungeonManager().editSelectedDungeonUUID(self.selectedDungeonUUID)
		self.done(0)
		pass

	def newDungeonNameText(self, newName):
		self.isOkToCreateDungeon = not newName.startswith("Enter ") and len(newName) > 4
		self.dungeonToCreate = newName
		self.setStates()
		pass

	def createDungeon(self):
		ServicesManager.getDungeonManager().createNewDungeon(self.dungeonToCreate)
		self.newDungeonName.setText("Enter Dungeon Name")
		pass

	def deleteDungeon(self):
		ServicesManager.getDungeonManager().deleteTemplate(self.selectedDungeonUUID)
		pass

	def sessionSelected(self, index):
		if index != 0:
			self.selectedSessionName = self.sessionList.itemText(index)
			self.selectedSessionUUID = self.sessionList.itemData(index)
		self.isOkToDeleteSession = index != 0
		self.isOkToDMSession = self.isOkToDeleteSession
		self.isOkToJoinSession = self.isOkToDeleteSession
		self.setStates()

	def dmSession(self):
		if self.isDM:
			ServicesManager.getDungeonManager().dmSession(self.selectedDungeonUUID, self.selectedSessionUUID)
		else:
			ServicesManager.getDungeonManager().joinSession(self.selectedDungeonUUID, self.selectedSessionUUID)
		self.done(0)
		pass

	def newSessionNameText(self, newSession):
		self.isOkToCreateSession = ServicesManager.getDungeonManager().isNameValidForNewSession(newSession)
		self.sessionToCreate = newSession
		self.setStates()
		pass

	def createSession(self):
		ServicesManager.getDungeonManager().createNewSession(self.selectedDungeonUUID, self.sessionToCreate)
		self.isOkToCreateSession = False
		_translate = QtCore.QCoreApplication.translate
		self.newSessionName.setText(_translate("DungeonSelectDialog", "Enter Session Name"))
		pass

	def deleteSession(self):
		ServicesManager.getDungeonManager().deleteSession(self.selectedDungeonUUID, self.selectedSessionUUID)
		self.isOkToDeleteSession = False
		pass

