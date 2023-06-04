"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class CreateNewSessionHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the CREATENEWSESSION request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        dungeonUUID = parameters.get('dungeonUUID')[0]
        newSessionName = parameters.get('newSessionName')[0]
        ServerDataManager.createSession(server, dungeonUUID, newSessionName)
        return ''
