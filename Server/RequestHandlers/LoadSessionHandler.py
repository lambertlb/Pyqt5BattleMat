"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class LoadSessionHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the LOADSESSION request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        dungeonUUID = parameters.get('dungeonUUID')[0]
        sessionUUID = parameters.get('sessionUUID')[0]
        version = int(parameters.get('version')[0])
        data = ServerDataManager.getSessionDataAsString(server, dungeonUUID, sessionUUID, version)
        return data
