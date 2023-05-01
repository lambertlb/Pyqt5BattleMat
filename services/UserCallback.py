"""
GPL 3 file header
"""

class UserCallback:
	"""
	Use for handling callbacks to user from data requests
	"""
	def __init__(self, onSuccess, onFailure):
		self.onSuccess = onSuccess
		self.onFailure = onFailure
