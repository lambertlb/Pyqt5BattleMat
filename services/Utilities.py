"""
MIT License

Copyright (c) 2023 Leon Lambert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def findWidgetWithID(starting, propertyName, value):
	"""
	Find a widget based on property content.
	@param starting: starting widget in tree
	@param propertyName: to search for
	@param value: of property
	@return: widget with the property
	"""
	for widget in starting.walk():
		if hasattr(widget, propertyName):
			if getattr(widget, propertyName) == value:
				return widget


def findParentOfType(starting, classType):
	"""
	Look for parent of starting with this type
	:param starting: widget with parent
	:param classType: to look for
	:return: parent of type or None
	"""
	root = starting.get_root_window()
	item = starting
	while item.parent != root:
		if isinstance(item.parent, classType):
			return item.parent
	return None

class   ConfigManager:
	"""
	Class to contain application configuration
	"""
	config = None   # configuration from main app

	def setConfig(self, newConfig):
		"""
		Set configuration
		:param newConfig: to use
		:return: None
		"""
		self.config = newConfig

	def getConfig(self):
		"""
		get application configuration
		:return: application configuration
		"""
		return self.config