"""
GPL 3 file header
"""
import json

from Server.ServerDataManager import ServerDataManager
from services.serviceData.SessionListData import SessionListData


class SessionListHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the GETSESSIONLIST request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters, data):
        dungeonUUID = parameters['dungeonUUID'][0]
        sessionMap = ServerDataManager.getSessionListData(server, dungeonUUID)
        response = SessionListData(sessionMap, dungeonUUID)
        return json.dumps(response, default=vars)
