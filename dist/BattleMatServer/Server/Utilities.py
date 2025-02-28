"""
GPL 3 file header
"""
import importlib
import inspect
import os
import re

class ClassLoader:
	"""
	This class will dynamically load classes

	"""
	def __init__(self):
		self.parentClass = None
		pass

	def	loadClasses(self, pathToFolder, parentClass=None):
		self.parentClass = parentClass
		foundScripts = []
		files = os.listdir(pathToFolder)
		for file in files:
			fullPath = pathToFolder + '/' + file
			if os.path.isfile(fullPath):
				fullPath = re.sub("/", ".", fullPath)
				fullPath = re.sub("\.\.", "", fullPath)
				fullPath = re.sub("\.py", "", fullPath)
				foundScripts.append(fullPath)

		classes = {}
		self.getClassesFromScripts(foundScripts, classes)
		return list(classes.values())

	def getClassesFromScripts(self, listOfScripts, classes):
		for script in listOfScripts:
			self.getClassesFromScript(script, classes)

	def getClassesFromScript(self, scriptName, classes):
		module = importlib.import_module(scriptName)
		self.getClassesFromModule(module, classes)

	def getClassesFromModule(self, module, classes):
		members = inspect.getmembers(module)
		for member in members:
			name, item = member
			if inspect.isclass(item):
				if self.parentClass != None and issubclass(item, self.parentClass):
					if not classes.get(name):
						if module.__name__ == item.__module__:
							classes[name] = self.createInstanceFromClass(
								getattr(module, name))

	@staticmethod
	def createInstanceFromClass(classToCreate):
		# magic to create instance of class
		alias = "SomeAlias"
		return eval(alias + '()', {alias: classToCreate})
