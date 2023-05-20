"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from generated.ViewNotes import Ui_PogNotesDialog
from services.ReasonForAction import ReasonForAction
from services.ServicesManager import ServicesManager


class PogNotesViewer(QtWidgets.QDialog, Ui_PogNotesDialog):
	def __init__(self, *args):
		super(PogNotesViewer, self).__init__(*args)
		self.selectedPog = None
		self.currentFontSize = 8

		self.setupUi(self)
		ServicesManager.getEventManager().subscribeToEvent(self.eventFired)
		self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
		self.buttonBox.setVisible(False)
		self.fontSizeControl.setRange(8, 20)
		self.fontSizeControl.setValue(8)
		self.fontSizeControl.valueChanged.connect(self.fontSizeChanged)

	def eventFired(self, eventData):
		if eventData.eventReason == ReasonForAction.PogWasSelected:
			self.pogSelection()

	def pogSelection(self):
		self.notesTextEdit.clear()
		self.dmNotesTextEdit.clear()
		self.selectedPog = ServicesManager.getDungeonManager().getSelectedPog()
		if self.selectedPog is None:
			return
		self.setWindowTitle(self.selectedPog.pogName)
		self.notesTextEdit.setText(self.selectedPog.notes)
		self.dmNotesTextEdit.setText(self.selectedPog.dmNotes)
		self.setFontSize()
		pass

	def show(self):
		self.pogSelection()
		super().show()

	def fontSizeChanged(self, text):
		self.currentFontSize = int(text)
		self.setFontSize()
		pass

	def setFontSize(self):
		cursor = self.notesTextEdit.textCursor()
		self.notesTextEdit.selectAll()
		self.notesTextEdit.setFontPointSize(self.currentFontSize)
		self.notesTextEdit.setTextCursor(cursor)

		cursor = self.dmNotesTextEdit.textCursor()
		self.dmNotesTextEdit.selectAll()
		self.dmNotesTextEdit.setFontPointSize(self.currentFontSize)
		self.dmNotesTextEdit.setTextCursor(cursor)
