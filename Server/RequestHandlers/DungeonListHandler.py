"""
GPL 3 file header
"""
import json

from Server.ServerDataManager import ServerDataManager
from services.serviceData.DungeonListData import DungeonListData


class DungeonListHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the GETDUNGEONLIST request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters, data):
        ServerDataManager.getDungeonListData(server)
        response = DungeonListData(ServerDataManager.dungeonNameToUUIDMap, ServerDataManager.uuidTemplatePathMap)
        return json.dumps(response, default=vars)
