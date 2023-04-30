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


class EventData:
	"""
	This manages data around a single event
	"""
	eventReason = None
	eventData = None

	def __init__(self, reason, data):
		"""
		Create event data with the following properties
		:param reason: reason for event
		:param data: associated data for the event
		"""
		self.eventReason = reason
		self.eventData = data

	def getEventReason(self):
		"""
		what was the reason for the event
		:return: event reason
		"""
		return self.eventReason

	def getEventData(self):
		"""
		get the data associated with the event
		:return: event data
		"""
		return self.eventData
