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
	Monsters = 'resources/monsters/'
	RoomObjects = 'resources/roomObjects/'
	SessionFolder = 'sessions/'

# requests to dungeon server
	LoginRequest = 'LOGIN'
	DungeonListRequest = 'GETDUNGEONLIST'
	SessionListRequest = 'GETSESSIONLIST'
	LoadJsonFileRequest = 'LOADJSONFILE'
	CreateNewDungeonRequest = 'CREATENEWDUNGEON'
	DeleteDungeonRequest = 'DELETEDUNGEON'
	LoadSessionRequest = 'LOADSESSION'
	UpdateFOWRequest = 'UPDATEFOW'
	CreateNewSessionRequest = 'CREATENEWSESSION'
	DeleteSessionRequest = 'DELETESESSION'
