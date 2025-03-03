/*
 * Copyright (C) 2019 Leon Lambert.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package per.lambert.ebattleMat.client.interfaces;

import java.util.List;
import java.util.Map;

import per.lambert.ebattleMat.client.services.serviceData.DataVersions;
import per.lambert.ebattleMat.client.services.serviceData.DungeonLevel;
import per.lambert.ebattleMat.client.services.serviceData.PogData;
import per.lambert.ebattleMat.client.services.serviceData.SessionListData;

/**
 * @author LLambert Interface to dungeon management services
 */
public interface IDungeonManager extends IPogManager {
	/**
	 * get last error that occurred.
	 * 
	 * @return last error
	 */
	DungeonServerError getLastError();

	/**
	 * Log in user.
	 * 
	 * @param username user name.
	 * @param password of user
	 * @param callback when complete
	 */
	void login(String username, String password, IUserCallback callback);

	/**
	 * Is logged in as dungeon master.
	 * 
	 * @return true if dungeon master.
	 */
	boolean isDungeonMaster();

	/**
	 * Is current dungeon in edit mode.
	 * 
	 * @return true if in edit mode.
	 */
	boolean isEditMode();

	/**
	 * Edit the selected dungeon based on selected UUID.
	 * 
	 * @param selectedDungeonUUID UUID of dungeon to edit.
	 */
	void editSelectedDungeonUUID(String selectedDungeonUUID);

	/**
	 * Get map of dungeon names to UUIDs.
	 * 
	 * @return map of dungeon names to UUIDs.
	 */
	Map<String, String> getDungeonToUUIDMap();

	/**
	 * get current level of selected dungeon.
	 * 
	 * @return current level
	 */
	int getCurrentLevelIndex();

	/**
	 * Set current level for selected dungeon.
	 * 
	 * @param currentLevel for selected dungeon
	 */
	void setCurrentLevel(int currentLevel);

	/**
	 * get dungeon data for current level.
	 * 
	 * @return dungeon data for current level.
	 */
	DungeonLevel getCurrentDungeonLevelData();

	/**
	 * Save dungeon data to server.
	 */
	void saveDungeonData();

	/**
	 * Set session level size in columns and rows.
	 * 
	 * @param columns in session level
	 * @param rows in session level
	 */
	void setSessionLevelSize(int columns, int rows);

	/**
	 * Save fog of war to server.
	 */
	void saveFow();

	/**
	 * Is fog of war set for this cell?
	 * 
	 * @param column of cell
	 * @param row of cell
	 * @return true if set
	 */
	boolean isFowSet(int column, int row);

	/**
	 * Set fog of war for this cell.
	 * 
	 * @param column of cell
	 * @param row of cell
	 * @param value true if set
	 */
	void setFow(int column, int row, boolean value);

	/**
	 * get toggle for fog of war.
	 * 
	 * @return true if we are changing fog of war.
	 */
	boolean getFowToggle();

	/**
	 * Set toggle for fog of war.
	 * 
	 * @param fowToggle true if changing.
	 */
	void setFowToggle(boolean fowToggle);

	/**
	 * Create a new dungeon based on template dungeon.
	 * 
	 * @param newDungeonName new dungeon name
	 */
	void createNewDungeon(String newDungeonName);

	/**
	 * Get URL to this dungeon specific resource item.
	 * 
	 * @param resourceItem needing URL
	 * @return URL to resource
	 */
	String getUrlToDungeonResource(String resourceItem);

	/**
	 * Is it ok to delete this template dungeon.
	 * 
	 * The master template dungeon is not ok to delete.
	 * 
	 * @param dungeonUUID to test.
	 * @return true if ok to delete
	 */
	boolean okToDeleteThisTemplate(String dungeonUUID);

	/**
	 * Delete this dungeon.
	 * 
	 * @param dungeonUUID of dungeon to delete
	 */
	void deleteTemplate(String dungeonUUID);

	/**
	 * Get the list of session for this dungeon.
	 * 
	 * @return list of sessions.
	 */
	SessionListData getSessionListData();

	/**
	 * get session list for dungeon from server.
	 * 
	 * @param dungeonUUID UUID of dungeon
	 */
	void getSessionList(String dungeonUUID);

	/**
	 * Is this a valid session name?
	 * 
	 * @param newSessionName name to check
	 * @return true if valid
	 */
	boolean isNameValidForNewSession(String newSessionName);

	/**
	 * Create a new session for this dungeon.
	 * 
	 * @param dungeonUUID dungeon needing session
	 * @param newSessionName new session name
	 */
	void createNewSession(String dungeonUUID, String newSessionName);

	/**
	 * Join this session as a player.
	 * 
	 * @param sessionUUID UUID of session
	 * @param selectedDungeonUUID uuid of dungeon for session
	 */
	void joinSession(String selectedDungeonUUID, String sessionUUID);

	/**
	 * DM this session as a dungeon master.
	 * 
	 * @param sessionUUID UUID of session
	 * @param selectedDungeonUUID uuid of dungeon for session
	 */
	void dmSession(String selectedDungeonUUID, String sessionUUID);

	/**
	 * Delete the specified session in the dungeon.
	 * 
	 * @param dungeonUUID with sessions
	 * @param sessionUUID to delete
	 */
	void deleteSession(String dungeonUUID, String sessionUUID);

	/**
	 * Get list of monsters on current level.
	 * 
	 * if in edit mode this will be list of monster in template else it will be a list of monster in session.
	 * 
	 * @return list of monsters.
	 */
	PogData[] getMonstersForCurrentLevel();

	/**
	 * Get list of players in this session.
	 * 
	 * @return list of players in this session.
	 */
	PogData[] getPlayersForCurrentSession();

	/**
	 * get list of room objects on current level.
	 * 
	 * if in edit mode this will be list of room objects in template else it will be a list of room objects in session.
	 * 
	 * @return list room objects on current level.
	 */
	PogData[] getRoomObjectsForCurrentLevel();

	/**
	 * get list of level names.
	 * 
	 * @return list of level names
	 */
	String[] getDungeonLevelNames();

	/**
	 * Do periodic tasks.
	 */
	void doTimedTasks();

	/**
	 * Download this dungeon related file.
	 * 
	 * @param fileName to download.
	 */
	void downloadDungeonFile(String fileName);

	/**
	 * Download this file.
	 * 
	 * @param url to file
	 * @param fileName to download.
	 */
	void downloadFile(String url, String fileName);

	/**
	 * get URL to dungeon data.
	 * 
	 * @return URL to dungeon data.
	 */
	String getUrlToDungeonData();

	/**
	 * get login token.
	 * 
	 * @return login token.
	 */
	int getToken();

	/**
	 * is this a legal dungeon name?
	 * 
	 * @param nameToCheck name to check.
	 * @return true if legal
	 */
	boolean isLegalDungeonName(String nameToCheck);

	/**
	 * get next available dungeon level number.
	 * 
	 * @return next available dungeon level number.
	 */
	int getNextAvailableLevelNumber();

	/**
	 * Add this new level to dungeon.
	 * 
	 * @param newLevelToAdd new level to add
	 */
	void addNewLevel(DungeonLevel newLevelToAdd);

	/**
	 * remove current level from duingeon.
	 */
	void removeCurrentLevel();

	/**
	 * Find character pog in dungeon.
	 * 
	 * @param uuid of character
	 * @return pog data if found
	 */
	PogData findCharacterPog(String uuid);

	/**
	 * is this valid monster name.
	 * 
	 * @param monsterName to check
	 * @return true if valid
	 */
	boolean isValidNewMonsterName(String monsterName);

	/**
	 * Add or update pog to proper place.
	 * 
	 * @param pog to add
	 * @param place to add
	 */
	void addOrUpdatePog(PogData pog, PogPlace place);

	/**
	 * Compute place pog should go.
	 * 
	 * @param pog to put
	 * @return Pog Place
	 */
	PogPlace computePlace(PogData pog);

	/**
	 * Add or update Pog.
	 * 
	 * @param pog to add
	 */
	void addOrUpdatePog(PogData pog);

	/**
	 * Get directory for the current dungeon.
	 * 
	 * @return directory for the current dungeon.
	 */
	String getDirectoryForCurrentDungeon();

	/**
	 * Set hide FOW.
	 * 
	 * @param hideFOW true if changing.
	 */
	void setHideFOW(boolean hideFOW);

	/**
	 * Is this coordinate in FOW map.
	 * 
	 * @param column to check
	 * @param row to check
	 * @return true if is
	 */
	boolean isInFOWMap(int column, int row);

	/**
	 * Delete selected pog.
	 */
	void deleteSelectedPog();

	/**
	 * Get list of files in path.
	 * 
	 * @param path
	 * @param callback
	 */
	void getFileList(String path, IUserCallback callback);

	/**
	 * Delete this file.
	 * 
	 * @param url to file
	 * @param callback when complete
	 */
	void deleteFile(String url, IUserCallback callback);

	/**
	 * Set asset URL.
	 * 
	 * @param assetURL to set
	 */
	void setAssetURL(String assetURL);

	/**
	 * Get asset URL.
	 * 
	 * @return asset URL
	 */
	String getAssetURL();

	/**
	 * Is this valid url for picture.
	 * 
	 * @param url
	 * @return true if valid
	 */
	boolean isValidPictureURL(String url);

	/**
	 * Get computed Grid width.
	 * 
	 * @return grid width
	 */
	double getComputedGridWidth();

	/**
	 * Set computed grid witdh.
	 * 
	 * @param gridWidth grid width
	 */
	void setComputedGridWidth(double gridWidth);

	/**
	 * Is dungeon grid Visible.
	 * 
	 * @return true if it is
	 */
	boolean isDungeonGridVisible();

	/**
	 * Set is dungeon grid visible.
	 * 
	 * @param isVisible true if visible
	 */
	void setIsDungeonGridVisible(boolean isVisible);

	/**
	 * get a list of sorted pogs from place.
	 * 
	 * @param fromWhere which pogs
	 * @param typeOfPogs type of pogs
	 * @return sorted list
	 */
	List<PogData> getSortedList(PogPlace fromWhere, String typeOfPogs);

	/**
	 * Get version for this item.
	 * 
	 * @param itemToGet
	 * @return version
	 */
	int getItemVersion(VersionedItem itemToGet);

	/**
	 * Get UUID of current dungeon.
	 * 
	 * @return UUID
	 */
	String getCurrentDungeonUUID();

	/**
	 * Get UUID of current dungeon.
	 * 
	 * @return UUID
	 */
	String getCurrentSessionUUID();

	/**
	 * Update to master data versions.
	 * 
	 * @param needsUpdating
	 */
	void updateDataVersion(DataVersions needsUpdating);
}
