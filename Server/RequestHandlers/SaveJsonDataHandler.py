"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class SaveJsonDataHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the SAVEJSONFILE request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        dungeonUUID = None
        dd = parameters.get('dungeonUUID')
        if dd:
            dungeonUUID = dd[0]
        sessionUUID = None
        ss = parameters.get('sessionUUID')
        if ss:
            sessionUUID = ss[0]
        if sessionUUID:
            ServerDataManager.saveSessionData(server, data, dungeonUUID, sessionUUID)
        else:
            ServerDataManager.saveDungeonData(server, data, dungeonUUID)
        return ''
