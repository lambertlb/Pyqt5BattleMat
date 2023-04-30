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
from event_bus import EventBus
from services.EventData import EventData

# global event buss
_eventBus = EventBus()


class EventManager:
	"""
	Event manager is a central place to handle all global events within and application
	"""
	eventName = 'globalEvents'

	def subscribeToEvent(self, callback):
		"""
		allow components to subscribe to events
		:param callback: when event is fired
		:return: None
		"""
		_eventBus.add_event(callback, self.eventName)

	def fireEvent(self, eventReason, eventData):
		"""
		fire off event to interested components
		:param eventReason: reason for event
		:param eventData: data for event (can be None)
		:return: None
		"""
		_eventBus.emit(self.eventName, EventData(eventReason, eventData))
		pass
