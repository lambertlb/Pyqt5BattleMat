"""
GPL 3 file header
"""
from PyQt5.QtCore import QSettings


class MyConfigManager:
	"""
	Class to contain application configuration
	"""

	def __init__(self):
		self.config = QSettings("./BattleMat.ini", QSettings.IniFormat)
		self.setDefaultsIfNeeded()

	def setDefaultsIfNeeded(self):
		if not self.config.contains('Login_Url'):
			self.config.setValue('Login_Url', 'My url')
			self.config.setValue('Login_USERNAME', 'My Username')
			self.config.setValue('Login_PASSWORD', 'My Password')
		pass

	def setValue(self, key, value):
		self.config.setValue(key, value)

	def getValue(self, key):
		return self.config.value(key)
