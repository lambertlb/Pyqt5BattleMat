"""
GPL 3 file header
"""


class Constants:
	Login_Url = 'Login_Url'
	Login_USERNAME = 'Login_USERNAME'
	Login_PASSWORD = 'Login_PASSWORD'

# Server Paths
	ServicePath = '/electronicbattlemat/dungeons'
	DungeonData = ServicePath + '/dungeonData'
	Dungeons = DungeonData + '/dungeons/'
	Monsters = DungeonData + '/resources/monsters/'
	RoomObjects = DungeonData + '/resources/roomObjects/'
	SessionFolder = 'sessions/'

# requests to dungeon server
	LoginRequest = 'LOGIN'
	DungeonListRequest = 'GETDUNGEONLIST'
