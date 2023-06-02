"""
GPL 3 file header
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
