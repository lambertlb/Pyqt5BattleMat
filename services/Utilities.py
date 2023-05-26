"""
GPL 3 file header
"""
from PySide2.QtCore import QSettings

from services.Constants import Constants


class MyConfigManager:
	"""
	Class to contain application configuration
	"""

	def __init__(self):
		self.config = QSettings("./BattleMat.ini", QSettings.IniFormat)
		self.setDefaultsIfNeeded()

	def setDefaultsIfNeeded(self):
		if not self.config.contains('Login_Url'):
			self.config.setValue(Constants.Login_Url, 'My url')
			self.config.setValue(Constants.Login_USERNAME, 'My Username')
			self.config.setValue(Constants.Login_PASSWORD, 'My Password')

	def setValue(self, key, value):
		self.config.setValue(key, value)

	def getValue(self, key, default):
		return self.config.value(key, default)
