"""
GPL 3 file header
"""
from PyQt5 import QtWidgets

from generated.loginDialog import Ui_Dialog
from services.Constants import Constants
from services.ServicesManager import ServicesManager
from services.UserCallback import UserCallback


class LoginDialog(QtWidgets.QDialog, Ui_Dialog):

	def __init__(self, *args):
		super(LoginDialog, self).__init__(*args)
		self.setupUi(self)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.serverURL.textChanged.connect(self.validate)
		self.username.textChanged.connect(self.validate)
		self.password.textChanged.connect(self.validate)
		self.loadSettings()

	def loadSettings(self):
		config = ServicesManager.getConfigManager()
		self.serverURL.setText(config.getValue(Constants.Login_Url, ''))
		self.username.setText(config.getValue(Constants.Login_USERNAME, ''))
		self.password.setText(config.getValue(Constants.Login_PASSWORD, ''))
		self.failed.setVisible(False)
		pass

	def accept(self):
		config = ServicesManager.getConfigManager()
		config.setValue(Constants.Login_Url, self.serverURL.text())
		config.setValue(Constants.Login_USERNAME, self.username.text())
		config.setValue(Constants.Login_PASSWORD, self.password.text())
		ServicesManager.getDungeonManager().login(self.username.text(), self.password.text(),
												UserCallback(self.onSuccess, self.onFailure))
		pass

	def reject(self):
		self.loadSettings()
		pass

	def validate(self):
		disabled = ServicesManager.getDungeonManager().isValidLoginData(self.serverURL.text(),
																			self.username.text(), self.password.text())
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(disabled)

	def onSuccess(self, data):
		pass

	def onFailure(self, data):
		self.failed.setVisible(True)
		pass