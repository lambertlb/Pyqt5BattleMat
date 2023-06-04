"""
GPL 3 file header
"""
from Server.ServerDataManager import ServerDataManager


class DeleteDungeonHandler:
    # noinspection SpellCheckingInspection
    """
    Handle the DELETEDUNGEON request.
    """

    # noinspection PyUnusedLocal
    # noinspection PyMethodMayBeStatic
    def handleRequest(self, server, parameters: dict, data):
        dungeonUUID = parameters.get('dungeonUUID')[0]
        ServerDataManager.deleteDungeon(server, dungeonUUID)
        return ''
