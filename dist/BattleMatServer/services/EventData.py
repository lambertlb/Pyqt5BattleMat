"""
GPL 3 file header
"""


class EventData:
    """
    This manages data around a single event
    """

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
