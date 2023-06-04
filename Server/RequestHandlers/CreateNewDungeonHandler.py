"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class CreateNewDungeonHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the CREATENEWDUNGEON request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        dungeonUUID = parameters.get('dungeonUUID')[0]
        newDungeonName = parameters.get("newDungeonName")[0]
        ServerDataManager.copyDungeon(server, dungeonUUID, newDungeonName)
        return ''
