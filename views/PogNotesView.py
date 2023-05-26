"""
GPL 3 file header
"""
from PyQt5 import QtWidgets, QtCore

from generated.ViewNotes import Ui_PogNotesDialog


class PogNotesViewer(QtWidgets.QDialog, Ui_PogNotesDialog):
	def __init__(self, *args):
		super(PogNotesViewer, self).__init__(*args)
		self.currentFontSize = 8
		self.notes = ''
		self.dmNotes = ''

		self.setupUi(self)
		self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
		self.buttonBox.setVisible(False)
		self.fontSizeControl.setRange(8, 20)
		self.fontSizeControl.setValue(8)
		self.fontSizeControl.valueChanged.connect(self.fontSizeChanged)
		self.setWindowTitle('Pog Notes')

	def setupDisplayWithData(self):
		self.notesTextEdit.setText(self.notes)
		self.dmNotesTextEdit.setText(self.dmNotes)
		self.setFontSize()

	def show(self):
		self.setupDisplayWithData()
		super().show()

	def fontSizeChanged(self, text):
		self.currentFontSize = int(text)
		self.setFontSize()

	def setFontSize(self):
		cursor = self.notesTextEdit.textCursor()
		self.notesTextEdit.selectAll()
		self.notesTextEdit.setFontPointSize(self.currentFontSize)
		self.notesTextEdit.setTextCursor(cursor)

		cursor = self.dmNotesTextEdit.textCursor()
		self.dmNotesTextEdit.selectAll()
		self.dmNotesTextEdit.setFontPointSize(self.currentFontSize)
		self.dmNotesTextEdit.setTextCursor(cursor)

	def setNotes(self, notes):
		self.buttonBox.setVisible(True)
		self.notes = notes
		self.setupDisplayWithData()

	def setDmNotes(self, dmNotes):
		self.buttonBox.setVisible(True)
		self.dmNotes = dmNotes
		self.setupDisplayWithData()

	def getNotes(self):
		return self.notesTextEdit.toPlainText()

	def getDmNotes(self):
		return self.dmNotesTextEdit.toPlainText()
