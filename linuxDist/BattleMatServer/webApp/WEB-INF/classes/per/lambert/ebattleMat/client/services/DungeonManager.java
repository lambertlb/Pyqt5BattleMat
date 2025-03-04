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
package per.lambert.ebattleMat.client.services;

import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.core.client.JsonUtils;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.DungeonServerError;
import per.lambert.ebattleMat.client.interfaces.IDataRequester;
import per.lambert.ebattleMat.client.interfaces.IDungeonManager;
import per.lambert.ebattleMat.client.interfaces.IErrorInformation;
import per.lambert.ebattleMat.client.interfaces.IUserCallback;
import per.lambert.ebattleMat.client.interfaces.PogPlace;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.interfaces.VersionedItem;
import per.lambert.ebattleMat.client.services.serviceData.DataVersions;
import per.lambert.ebattleMat.client.services.serviceData.DungeonData;
import per.lambert.ebattleMat.client.services.serviceData.DungeonLevel;
import per.lambert.ebattleMat.client.services.serviceData.DungeonListData;
import per.lambert.ebattleMat.client.services.serviceData.DungeonSessionData;
import per.lambert.ebattleMat.client.services.serviceData.DungeonSessionLevel;
import per.lambert.ebattleMat.client.services.serviceData.FileList;
import per.lambert.ebattleMat.client.services.serviceData.FogOfWarData;
import per.lambert.ebattleMat.client.services.serviceData.LoginResponseData;
import per.lambert.ebattleMat.client.services.serviceData.PogData;
import per.lambert.ebattleMat.client.services.serviceData.SessionListData;

/**
 * Manager for handling dungeon data.
 * 
 * @author LLambert
 *
 */
public class DungeonManager extends PogManager implements IDungeonManager {
	/**
	 * Last error from server.
	 */
	private DungeonServerError lastError;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public DungeonServerError getLastError() {
		return (lastError);
	}

	/**
	 * Token from login credentials.
	 */
	private int token;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getToken() {
		return token;
	}

	/**
	 * List of sessions for this dungeon.
	 */
	private SessionListData sessionListData;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public SessionListData getSessionListData() {
		return sessionListData;
	}

	/**
	 * UUID for selected dungeon.
	 */
	private String selectedDungeonUUID;
	/**
	 * UUID for selected session.
	 */
	private String selectedSessionUUID;
	/**
	 * Selected dungeon.
	 */
	private DungeonData selectedDungeon;

	private DungeonData getSelectedDungeon() {
		return selectedDungeon;
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public String getCurrentDungeonUUID() {
		if (selectedDungeon != null) {
			return (selectedDungeon.getUUID());
		}
		return (null);
	}

	/**
	 * selected session.
	 */
	private DungeonSessionData selectedSession;

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public String getCurrentSessionUUID() {
		if (selectedSession != null) {
			return (selectedSession.getSessionUUID());
		}
		return (null);
	}

	/**
	 * Get selected session.
	 * 
	 * @return selected session
	 */
	private DungeonSessionData getSelectedSession() {
		return selectedSession;
	}

	/**
	 * current level index.
	 */
	private int currentLevelIndex;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getCurrentLevelIndex() {
		return currentLevelIndex;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getNextAvailableLevelNumber() {
		return (selectedDungeon.getDungeonlevels().length);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setCurrentLevel(final int currentLevel) {
		this.currentLevelIndex = currentLevel;
		loadDungeonData();
		loadSessionData();
		computedGridWidth = getCurrentDungeonLevelData().getGridSize();
		ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonSelectedLevelChanged, null));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public DungeonLevel getCurrentDungeonLevelData() {
		if (selectedDungeon != null && currentLevelIndex < selectedDungeon.getDungeonlevels().length) {
			return (selectedDungeon.getDungeonlevels()[currentLevelIndex]);
		}
		return null;
	}

	/**
	 * get the session data for the current level index.
	 * 
	 * @return session data for the current level index.
	 */
	private DungeonSessionLevel getCurrentSessionLevelData() {
		if (selectedSession != null && currentLevelIndex < selectedSession.getSessionLevels().length) {
			return (selectedSession.getSessionLevels()[currentLevelIndex]);
		}
		return null;
	}

	/**
	 * is the currently logged in person a dungeon master.
	 */
	private boolean isDungeonMaster;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isDungeonMaster() {
		return isDungeonMaster;
	}

	/**
	 * Set state of dungeon master.
	 * 
	 * @param isDungeonMaster true if DM
	 */
	private void setDungeonMaster(final boolean isDungeonMaster) {
		this.isDungeonMaster = isDungeonMaster;
		ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DMStateChange, null));
	}

	/**
	 * Set state of dungeon master for unit test.
	 * 
	 * @param isDungeonMaster true if DM
	 */
	public void setDungeonMasterForUnitTest(final boolean isDungeonMaster) {
		this.isDungeonMaster = isDungeonMaster;
	}

	/**
	 * Are we in edit mode on the dungeon.
	 */
	private boolean editMode;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isEditMode() {
		return editMode;
	}

	/**
	 * Set edit mode for testing.
	 * 
	 * @param editMode true if in edit mode
	 */
	public void setEditModeForUnitTest(final boolean editMode) {
		this.editMode = editMode;
	}

	/**
	 * Dungeon to uuid map.
	 */
	private Map<String, String> dungeonToUUIDMap = new HashMap<String, String>();

	/**
	 * {@inheritDoc}
	 */
	@Override
	public Map<String, String> getDungeonToUUIDMap() {
		return dungeonToUUIDMap;
	}

	/**
	 * Map of UUIDs to dungeon templates.
	 */
	private Map<String, String> uuidTemplatePathMap = new HashMap<String, String>();

	/**
	 * Map made available for unit test.
	 * 
	 * @return map of uuids to paths
	 */
	public Map<String, String> getUuidTemplatePathMapForUnitTest() {
		return uuidTemplatePathMap;
	}

	/**
	 * UUID of master template.
	 */
	private String uuidOfMasterTemplate;

	/**
	 * Get uuid of master template. Exposed for unit test.
	 * 
	 * @return uuid of master template.
	 */
	public String getUuidOfMasterTemplate() {
		return uuidOfMasterTemplate;
	}

	/**
	 * are we in fog of war toggle mode.
	 */
	private boolean fowToggle;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean getFowToggle() {
		return (fowToggle);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setFowToggle(final boolean fowToggle) {
		this.fowToggle = fowToggle;
		ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.ToggleFowSelected, null));
	}

	/**
	 * Fog of war data is dirty.
	 */
	private boolean fowDirty;

	/**
	 * get is fog of war dirty flag for unit test.
	 * 
	 * @return fog of war dirty
	 */
	public boolean isFowDirty() {
		return fowDirty;
	}

	/**
	 * Current;y selected Asset URL.
	 */
	private String assetURL;

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void setAssetURL(final String assetURL) {
		this.assetURL = assetURL;
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public String getAssetURL() {
		return assetURL;
	}

	/**
	 * Computed grid width.
	 */
	private double computedGridWidth;

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public double getComputedGridWidth() {
		return computedGridWidth;
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void setComputedGridWidth(final double gridWidth) {
		computedGridWidth = gridWidth;
	}

	/**
	 * Collection of dungeon level monster templates.
	 */
	private PogCollection dungeonLevelMonsters = new PogCollection(ReasonForAction.LastReason, PogPlace.DUNGEON_LEVEL);
	/**
	 * Collection of dungeon level monster templates.
	 */
	private PogCollection dungeonLevelRoomObjects = new PogCollection(ReasonForAction.LastReason, PogPlace.DUNGEON_LEVEL);
	/**
	 * Collection of session level monster templates.
	 */
	private PogCollection sessionLevelMonsters = new PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_LEVEL);
	/**
	 * Collection of session level monster templates.
	 */
	private PogCollection sessionLevelRoomObjects = new PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_LEVEL);
	/**
	 * Collection of session level monster templates.
	 */
	private PogCollection sessionLevelPlayers = new PogCollection(ReasonForAction.LastReason, PogPlace.SESSION_RESOURCE);
	/**
	 * Versions of data.
	 */
	private DataVersions dataVersion = new DataVersions();

	/**
	 * construct a dungeon manager.
	 */
	public DungeonManager() {
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void login(final String username, final String password, final IUserCallback callback) {
		lastError = DungeonServerError.Succsess;
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("username", username);
		parameters.put("password", password);
		dataRequester.requestData("", "LOGIN", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				handleSuccessfulLogin(username, callback, data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
				callback.onError(username, error);
			}
		});
	}

	/**
	 * Handle successful login.
	 * 
	 * @param requestData request data
	 * @param callback callback to user
	 * @param data from request
	 */
	private void handleSuccessfulLogin(final Object requestData, final IUserCallback callback, final Object data) {
		LoginResponseData loginResponseData = JsonUtils.<LoginResponseData>safeEval((String) data);
		token = loginResponseData.getToken();
		lastError = DungeonServerError.fromInt(loginResponseData.getError());
		if (lastError == DungeonServerError.Succsess) {
			getDungeonList(requestData, callback);
			return;
		}
		callback.onError(requestData, new IErrorInformation() {
			@Override
			public Throwable getException() {
				return null;
			}

			@Override
			public DungeonServerError getError() {
				return lastError;
			}

			@Override
			public String getErrorMessage() {
				return null;
			}
		});
	}

	/**
	 * get list of dungeon data.
	 * 
	 * @param requestData request data
	 * @param callback user callback
	 */
	private void getDungeonList(final Object requestData, final IUserCallback callback) {
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		Map<String, String> parameters = new HashMap<String, String>();
		dataRequester.requestData("", "GETDUNGEONLIST", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				handleSuccessfulDungeonList("", callback, data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
				callback.onError(requestData, error);
			}
		});
	}

	/**
	 * Handle successful read of dungeon list.
	 * 
	 * @param requestData request data
	 * @param callback user callback
	 * @param data data from response
	 */
	private void handleSuccessfulDungeonList(final Object requestData, final IUserCallback callback, final Object data) {
		dungeonToUUIDMap.clear();
		uuidTemplatePathMap.clear();
		uuidOfMasterTemplate = null;
		DungeonListData dungeonListData = JsonUtils.<DungeonListData>safeEval((String) data);
		for (int i = 0; i < dungeonListData.getDungeonNames().length; ++i) {
			dungeonToUUIDMap.put(dungeonListData.getDungeonNames()[i], dungeonListData.getDungeonUUIDS()[i]);
			uuidTemplatePathMap.put(dungeonListData.getDungeonUUIDS()[i], dungeonListData.getDungeonDirectories()[i]);
			if (dungeonListData.getDungeonUUIDS()[i].equals("template-dungeon")) {
				uuidOfMasterTemplate = dungeonListData.getDungeonUUIDS()[i];
			}
		}
		callback.onSuccess(requestData, null);
	}

	/**
	 * load selected dungeon.
	 */
	private void loadSelectedDungeon() {
		initializeDungeonData();
		loadInResourceData();
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", selectedDungeonUUID);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		dataRequester.requestData("", "LOADJSONFILE", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				selectedDungeon = JsonUtils.<DungeonData>safeEval((String) data);
				loadDungeonData();
				computedGridWidth = getCurrentDungeonLevelData().getGridSize();
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonSelected, null));
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataLoaded, null));
				if (editMode) {
					ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataReadyToEdit, null));
				} else {
					loadSessionData(-1);
				}
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}
		});
	}

	/**
	 * Load in data for dungeon.
	 */
	private void loadDungeonData() {
		DungeonLevel dungeonLevel = getCurrentDungeonLevelData();
		if (dungeonLevel != null) {
			dungeonLevelMonsters.setPogList(dungeonLevel.getMonsters());
			dungeonLevelRoomObjects.setPogList(dungeonLevel.getRoomObjects());
			updateDataVersion();
		}
	}

	/**
	 * initialize dungeon data.
	 */
	private void initializeDungeonData() {
		currentLevelIndex = 0;
		selectedDungeon = null;
		selectedSession = null;
		fowToggle = false;
		setSelectedPog(null);
		setPogBeingDragged(null, false);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void saveDungeonData() {
		if (selectedDungeon != null) {
			Map<String, String> parameters = new HashMap<String, String>();
			parameters.put("dungeonUUID", selectedDungeon.getUUID());
			IDataRequester dataRequester = ServiceManager.getDataRequester();
			String dungeonDataString = JsonUtils.stringify(selectedDungeon);
			dataRequester.requestData(dungeonDataString, "SAVEJSONFILE", parameters, new IUserCallback() {
				@Override
				public void onSuccess(final Object sender, final Object data) {
					ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataSaved, null));
				}

				@Override
				public void onError(final Object sender, final IErrorInformation error) {
					lastError = error.getError();
				}
			});
		}
	}

	/**
	 * Load in resource data.
	 */
	private void loadInResourceData() {
		loadMonsterPogs();
		loadRoomObjectPogs();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void createNewDungeon(final String newDungeonName) {
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", getUuidOfMasterTemplate());
		parameters.put("newDungeonName", newDungeonName);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		dataRequester.requestData("", "CREATENEWDUNGEON", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				handlerNewDungeonCreated(newDungeonName);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * Handle successful new dungeon created callback.
	 * 
	 * @param newDungeonName name of new dungeon
	 */
	private void handlerNewDungeonCreated(final String newDungeonName) {
		getDungeonList(null, new IUserCallback() {
			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}

			@Override
			public void onSuccess(final Object sender, final Object data) {
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataCreated, null));
			}
		});
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean okToDeleteThisTemplate(final String dungeonUUID) {
		return !dungeonUUID.equals(uuidOfMasterTemplate);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void deleteTemplate(final String dungeonUUID) {
		if (!okToDeleteThisTemplate(dungeonUUID)) {
			return;
		}
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", dungeonUUID);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		dataRequester.requestData("", "DELETEDUNGEON", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				handlerDungeonDeleted();
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * handle successful delete dungeon request.
	 */
	private void handlerDungeonDeleted() {
		getDungeonList("", new IUserCallback() {
			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}

			@Override
			public void onSuccess(final Object sender, final Object data) {
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataDeleted, null));
			}
		});
	}

	/**
	 * {@inheritDoc}
	 */
	public void getSessionList(final String dungeonUUID) {
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", dungeonUUID);
		dataRequester.requestData("", "GETSESSIONLIST", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				handleSuccessfulSessionList(data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * handle successful session list request.
	 * 
	 * @param data from response
	 */
	private void handleSuccessfulSessionList(final Object data) {
		sessionListData = JsonUtils.<SessionListData>safeEval((String) data);
		ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.SessionListChanged, null));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void createNewSession(final String dungeonUUID, final String newSessionName) {
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", dungeonUUID);
		parameters.put("newSessionName", newSessionName);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		dataRequester.requestData("", "CREATENEWSESSION", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				getSessionList(dungeonUUID);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void deleteSession(final String dungeonUUID, final String sessionUUID) {
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", dungeonUUID);
		parameters.put("sessionUUID", sessionUUID);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		dataRequester.requestData("", "DELETESESSION", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				getSessionList(dungeonUUID);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * Load in data for session.
	 * 
	 * This will do a version test. If the version hasn't changed then nothing is returned.
	 * 
	 * @param versionToTest see if it is this version.
	 */
	private void loadSessionData(final int versionToTest) {
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", selectedDungeonUUID);
		parameters.put("sessionUUID", selectedSessionUUID);
		parameters.put("version", "" + versionToTest);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		dataRequester.requestData("", "LOADSESSION", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				String jsonData = (String) data;
				if (!jsonData.isEmpty()) {
					selectedSession = JsonUtils.<DungeonSessionData>safeEval(jsonData);
					migrateSession();
					loadSessionData();
					if (versionToTest == -1) { // is this first load?
						ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataReadyToJoin, null));
					} else {
						ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.SessionDataChanged, null));
					}
				}
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}
		});
	}

	/**
	 * Load in session data.
	 */
	private void loadSessionData() {
		if (getCurrentSessionLevelData() != null) {
			sessionLevelMonsters.updateCollection(getCurrentSessionLevelData().getMonsters());
			sessionLevelRoomObjects.updateCollection(getCurrentSessionLevelData().getRoomObjects());
			sessionLevelPlayers.updateCollection(selectedSession.getPlayers());
			updateDataVersion();
		}
	}

	/**
	 * Migrate any needed data.
	 */
	private void migrateSession() {
		int saveIndex = currentLevelIndex;
		for (int i = 0; i < selectedSession.getSessionLevels().length; ++i) {
			DungeonSessionLevel sessionlevel = selectedSession.getSessionLevels()[i];
			DungeonLevel dungeonLevel = selectedDungeon.getDungeonlevels()[i];
			if (sessionlevel.migrateSession(dungeonLevel)) {
				currentLevelIndex = i;
				fowDirty = true;
				saveFow();
			}
		}
		currentLevelIndex = saveIndex;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setSessionLevelSize(final int columns, final int rows) {
		DungeonLevel dungeonLevel = getCurrentDungeonLevelData();
		if (!isDungeonMaster || dungeonLevel == null) {
			return;
		}
		if (dungeonLevel.getColumns() == columns && dungeonLevel.getRows() == rows) {
			return;
		}
		dungeonLevel.setColumns(columns);
		dungeonLevel.setRows(rows);
		saveDungeonData();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setFow(final int columns, final int rows, final boolean value) {
		DungeonSessionLevel sessionLevel = getCurrentSessionLevelData();
		if (isDungeonMaster && sessionLevel != null) {
			sessionLevel.updateFOW(columns, rows, value);
			fowDirty = true;
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isFowSet(final int columns, final int rows) {
		if (editMode) {
			return (false);
		}
		DungeonSessionLevel sessionLevel = getCurrentSessionLevelData();
		if (sessionLevel == null) {
			return (false);
		}
		return (sessionLevel.isFowSet(columns, rows));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void saveFow() {
		if (isDungeonMaster && fowDirty) {
			updateFogOfWar();
		}
		fowDirty = false;
	}

	/**
	 * Get directory for the current dungeon.
	 * 
	 * @return directory for the current dungeon.
	 */
	@Override
	public String getDirectoryForCurrentDungeon() {
		return (uuidTemplatePathMap.get(selectedDungeon.getUUID()));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public String getUrlToDungeonData() {
		String directoryForDungeon = getDirectoryForCurrentDungeon();
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		String resourceUrl = dataRequester.getWebPath() + directoryForDungeon + "/";
		return (resourceUrl);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public String getUrlToDungeonResource(final String resourceItem) {
		if (resourceItem.contains("/") || resourceItem.contains("\\")) {
			if (resourceItem.startsWith("http")) {
				return resourceItem;
			}
			return (ServiceManager.getDataRequester().getWebPath() + resourceItem);
		}
		Date now = new Date(); // append date to make sure not to get cached item. Needed for development where stuff changes a lot.
		String resourceUrl = getUrlToDungeonData() + resourceItem + "?" + now.getTime();
		return (resourceUrl);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isNameValidForNewSession(final String newSessionName) {
		boolean isValidSessionName = !newSessionName.startsWith("Enter ") && newSessionName.length() > 4;
		boolean isInCurrentSessionNames = false;
		boolean isInCurrentSessionDirectories = false;
		if (isValidSessionName) {
			isInCurrentSessionNames = isInCurrentSessionNames(newSessionName);
		}
		return isValidSessionName && !isInCurrentSessionNames && !isInCurrentSessionDirectories;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isValidNewMonsterName(final String monsterName) {
		boolean isValid = !monsterName.startsWith("Enter ") && monsterName.length() > 3;
		return isValid;
	}

	/**
	 * Is this session name in the current list.
	 * 
	 * @param newSessionName new session name
	 * @return true if in list
	 */
	private boolean isInCurrentSessionNames(final String newSessionName) {
		for (String sessionName : sessionListData.getSessionNames()) {
			if (sessionName.equals(newSessionName)) {
				return (true);
			}
		}
		return false;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void editSelectedDungeonUUID(final String selectedDungeonUUID) {
		this.selectedDungeonUUID = selectedDungeonUUID;
		selectedSessionUUID = null;
		editMode = true;
		setDungeonMaster(true);
		loadSelectedDungeon();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void joinSession(final String selectedDungeonUUID, final String sessionUUID) {
		this.selectedDungeonUUID = selectedDungeonUUID;
		selectedSessionUUID = sessionUUID;
		editMode = false;
		setDungeonMaster(false);
		loadSelectedDungeon();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void dmSession(final String selectedDungeonUUID, final String sessionUUID) {
		this.selectedDungeonUUID = selectedDungeonUUID;
		selectedSessionUUID = sessionUUID;
		editMode = false;
		setDungeonMaster(true);
		loadSelectedDungeon();
	}

	/**
	 * update fog of war.
	 */
	private void updateFogOfWar() {
		if (selectedDungeon != null) {
			Map<String, String> parameters = new HashMap<String, String>();
			parameters.put("sessionUUID", selectedSession.getSessionUUID());
			parameters.put("currentLevel", "" + currentLevelIndex);
			DungeonSessionLevel sessionLevel = getCurrentSessionLevelData();
			FogOfWarData fogOfWarData = (FogOfWarData) JavaScriptObject.createObject().cast();
			fogOfWarData.setFOW(sessionLevel.getFOW());
			String fowDataString = JsonUtils.stringify(fogOfWarData);
			IDataRequester dataRequester = ServiceManager.getDataRequester();
			dataRequester.requestData(fowDataString, "UPDATEFOW", parameters, new IUserCallback() {
				@Override
				public void onSuccess(final Object sender, final Object data) {
					ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.SessionDataSaved, null));
				}

				@Override
				public void onError(final Object sender, final IErrorInformation error) {
					lastError = error.getError();
				}
			});
			sessionLevel.setFOWVersion(sessionLevel.getFOWVersion() + 1);
			dataVersion.setItemVersion(VersionedItem.FOG_OF_WAR, dataVersion.getItemVersion(VersionedItem.FOG_OF_WAR) + 1);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData[] getMonstersForCurrentLevel() {
		if (selectedDungeon == null) {
			return null;
		}
		if (editMode) {
			return (dungeonLevelMonsters.getPogList());
		}
		return sessionLevelMonsters.getPogList();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData[] getRoomObjectsForCurrentLevel() {
		if (selectedDungeon == null) {
			return null;
		}
		if (editMode) {
			return (dungeonLevelRoomObjects.getPogList());
		}
		return sessionLevelRoomObjects.getPogList();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData[] getPlayersForCurrentSession() {
		if (editMode || selectedDungeon == null || selectedSession == null) {
			return null;
		}
		int currentLevel = getCurrentLevelIndex();
		ArrayList<PogData> playersOnLevel = new ArrayList<PogData>();
		for (PogData player : sessionLevelPlayers.getPogList()) {
			if (player.getDungeonLevel() == currentLevel) {
				playersOnLevel.add(player);
			}
		}
		return (PogData[]) playersOnLevel.toArray(new PogData[playersOnLevel.size()]);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public String[] getDungeonLevelNames() {
		if (selectedDungeon == null) {
			return (new String[0]);
		}
		DungeonLevel[] levels = selectedDungeon.getDungeonlevels();
		String[] levelNames = new String[levels.length];
		for (int i = 0; i < levels.length; ++i) {
			levelNames[i] = levels[i].getLevelName();
		}
		return (levelNames);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void doTimedTasks() {
		if (selectedSession != null) {
			loadSessionData(selectedSession.getVersion());
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void downloadDungeonFile(final String fileName) {
		String url = getUrlToDungeonData() + fileName;
		makeSureLoaderExists();
		downloadFileFromServer(fileName, url);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void downloadFile(final String url, final String fileName) {
		String resourceUrl = buildURL(url, fileName);
		makeSureLoaderExists();
		downloadFileFromServer(fileName, resourceUrl);
	}

	private String buildURL(final String url, final String fileName) {
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		String resourceUrl;
		if (url.endsWith("/")) {
			resourceUrl = dataRequester.getWebPath() + url + fileName;
		} else {
			resourceUrl = dataRequester.getWebPath() + url + "/" + fileName;
		}
		return resourceUrl;
	}

	/**
	 * Make sure download element exists.
	 */
	private native void makeSureLoaderExists() /*-{
		var aLink = document.getElementById('downloader');
		if (aLink == null) {
			aLink = document.createElement('a');
			aLink.setAttribute('id', 'downloader');
			document.body.appendChild(aLink);
		}
	}-*/;

	/**
	 * Download file using loader.
	 * 
	 * @param fileName to download
	 * @param urlData URL to resource
	 */
	private native void downloadFileFromServer(String fileName, String urlData) /*-{
		var aLink = document.getElementById('downloader');
		aLink.download = fileName;
		aLink.href = encodeURI(urlData);
		var event = new MouseEvent('click');
		aLink.dispatchEvent(event);
	}-*/;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isLegalDungeonName(final String nameToCheck) {
		if (nameToCheck == null || nameToCheck.isEmpty() || nameToCheck.length() < 4) {
			return (false);
		}
		return (true);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void addNewLevel(final DungeonLevel newLevel) {
		selectedDungeon.addDungeonlevel(newLevel);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void removeCurrentLevel() {
		selectedDungeon.remove(currentLevelIndex);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData findCharacterPog(final String uuid) {
		if (selectedSession == null) {
			return null;
		}
		return (sessionLevelPlayers.findPog(uuid));
	}

	/**
	 * Compute place pog should go.
	 * 
	 * @param pog to put
	 * @return Pog Place
	 */
	@Override
	public PogPlace computePlace(final PogData pog) {
		return (pog.getPogPlace());
	}

	/**
	 * Add or update Pog.
	 * 
	 * @param pog to add
	 */
	@Override
	public void addOrUpdatePog(final PogData pog) {
		addOrUpdatePog(pog, computePlace(pog));
	}

	/**
	 * Add or update Pog.
	 * 
	 * @param pog to add
	 * @param place where to add
	 */
	@Override
	public void addOrUpdatePog(final PogData pog, final PogPlace place) {
		PogCollection collection = getProperCollection(place, pog.getType());
		if (collection == null) {
			return;
		}
		collection.addOrUpdatePogCollection(pog);
		addOrUpdatePogToServer(pog, place);
		if (pog.isEqual(getSelectedPog())) {
			setSelectedPogInternal(pog);
		}
		updateDataVersion();
		ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.PogDataChanged, pog));
	}

	/**
	 * Save Pog to server.
	 * 
	 * @param pog to save
	 * @param place to save
	 */
	private void addOrUpdatePogToServer(final PogData pog, final PogPlace place) {
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", selectedDungeon.getUUID());
		if (selectedSession != null) {
			parameters.put("sessionUUID", selectedSession.getSessionUUID());
		} else {
			parameters.put("sessionUUID", "");
		}
		parameters.put("currentLevel", "" + currentLevelIndex);
		parameters.put("place", place.getName());
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		String pogDataString = JsonUtils.stringify(pog);
		dataRequester.requestData(pogDataString, "ADDORUPDATEPOG", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				if (editMode) {
					ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.SessionDataSaved, null));
				} else {
					ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.PogDataChanged, pog));
				}
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * Set hide FOW.
	 * 
	 * @param hideFOW true if changing.
	 */
	@Override
	public void setHideFOW(final boolean hideFOW) {
		if (hideFOW) {
			hideFOW();
		} else {
			showSavedFOW();
		}
		updateFogOfWar();
	}

	/**
	 * Saved FOW.
	 */
	private long[] savedFOW;

	private void hideFOW() {
		savedFOW = getCurrentSessionLevelData().getFOW();
		long[] fogOfWar = getCurrentSessionLevelData().createNewFOWData(getCurrentDungeonLevelData().getRows());
		getCurrentSessionLevelData().setFOW(fogOfWar);
	}

	/**
	 * Return original fow.
	 */
	private void showSavedFOW() {
		if (savedFOW == null) {
			return;
		}
		getCurrentSessionLevelData().setFOW(savedFOW);
		savedFOW = null;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isInFOWMap(final int column, final int row) {
		return (column >= 0 && row >= 0 && column < getCurrentDungeonLevelData().getColumns() && row < getCurrentDungeonLevelData().getRows());
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void deleteSelectedPog() {
		if (!isDungeonMaster) {
			return;
		}
		PogPlace place = computePlace(getSelectedPog());
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("dungeonUUID", selectedDungeon.getUUID());
		if (selectedSession != null) {
			parameters.put("sessionUUID", selectedSession.getSessionUUID());
		} else {
			parameters.put("sessionUUID", "");
		}
		parameters.put("currentLevel", "" + currentLevelIndex);
		parameters.put("place", place.getName());
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		String pogDataString = JsonUtils.stringify(getSelectedPog());
		dataRequester.requestData(pogDataString, "DELETEPOG", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				removeThisPog(getSelectedPog(), place);
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.SessionDataSaved, null));
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.PogDataChanged, null));
				setSelectedPog(null);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
			}
		});
	}

	/**
	 * remove this pog.
	 * 
	 * @param pog tp remove
	 * @param place where to remove it from
	 */
	private void removeThisPog(final PogData pog, final PogPlace place) {
		PogCollection collection = getProperCollection(place, pog.getType());
		if (collection == null) {
			return;
		}
		collection.remove(pog);
		updateDataVersion();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void getFileList(final String path, final IUserCallback callback) {
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("folder", path);
		dataRequester.requestData("", "FILELISTER", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				FileList files = JsonUtils.<FileList>safeEval((String) data);
				callback.onSuccess(path, files);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
				callback.onError(path, error);
			}
		});
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void deleteFile(final String url, final IUserCallback callback) {
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("path", url);
		dataRequester.requestData("", "DELETEFILE", parameters, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				callback.onSuccess(url, null);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
				lastError = error.getError();
				callback.onError(url, error);
			}
		});
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public boolean isValidPictureURL(final String url) {
		if (url == null) {
			return (false);
		}
		int i = url.lastIndexOf('.');
		String fileExtension = i > 0 ? url.substring(i + 1) : "";
		boolean valid = fileExtension.startsWith("jpeg") || fileExtension.startsWith("jpg") || fileExtension.startsWith("png") || fileExtension.startsWith("webp");
		return (valid);
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public boolean isDungeonGridVisible() {
		return (getSelectedDungeon().getShowGrid());
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void setIsDungeonGridVisible(final boolean isVisible) {
		getSelectedDungeon().setShowGrid(isVisible);
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public List<PogData> getSortedList(final PogPlace fromWhere, final String typeOfPogs) {
		PogCollection collection = getProperCollection(fromWhere, typeOfPogs);
		if (collection != null) {
			return (collection.getSortedListOfPogs());
		}
		return (null);
	}

	private PogCollection getProperCollection(final PogPlace fromWhere, final String typeOfPogs) {
		PogCollection collection = null;
		if (fromWhere == PogPlace.COMMON_RESOURCE) {
			if (typeOfPogs == Constants.POG_TYPE_MONSTER) {
				collection = getMonsterCollection();
			} else {
				collection = getRoomCollection();
			}
		} else if (fromWhere == PogPlace.SESSION_LEVEL) {
			if (typeOfPogs == Constants.POG_TYPE_MONSTER) {
				collection = sessionLevelMonsters;
			} else {
				collection = sessionLevelRoomObjects;
			}
		} else if (fromWhere == PogPlace.DUNGEON_LEVEL) {
			if (typeOfPogs == Constants.POG_TYPE_MONSTER) {
				collection = dungeonLevelMonsters;
			} else {
				collection = dungeonLevelRoomObjects;
			}
		} else if (fromWhere == PogPlace.SESSION_RESOURCE) {
			collection = sessionLevelPlayers;
		}
		return (collection);
	}

	/**
	 * Update data versions.
	 */
	private void updateDataVersion() {
		dataVersion.initialize();
		dataVersion.setItemVersion(VersionedItem.COMMON_RESOURCE_MONSTERS, getMonsterCollection().getPogListVserion());
		dataVersion.setItemVersion(VersionedItem.COMMON_RESOURCE_ROOMOBECTS, getRoomCollection().getPogListVserion());
		DungeonLevel dungeonLevel = getCurrentDungeonLevelData();
		if (dungeonLevel != null) {
			dataVersion.setItemVersion(VersionedItem.DUNGEON_LEVEL_MONSTERS, dungeonLevelMonsters.getPogListVserion());
			dataVersion.setItemVersion(VersionedItem.DUNGEON_LEVEL_ROOMOBJECTS, dungeonLevelRoomObjects.getPogListVserion());
		}
		DungeonSessionLevel sessionLevelData = getCurrentSessionLevelData();
		if (sessionLevelData != null) {
			dataVersion.setItemVersion(VersionedItem.SESSION_LEVEL_MONSTERS, sessionLevelMonsters.getPogListVserion());
			dataVersion.setItemVersion(VersionedItem.SESSION_LEVEL_ROOMOBJECTS, sessionLevelRoomObjects.getPogListVserion());
			dataVersion.setItemVersion(VersionedItem.SESSION_RESOURCE_PLAYERS, sessionLevelPlayers.getPogListVserion());
			dataVersion.setItemVersion(VersionedItem.FOG_OF_WAR, sessionLevelData.getFOWVersion());
		}
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public int getItemVersion(final VersionedItem itemToGet) {
		return dataVersion.getItemVersion(itemToGet);
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void updateDataVersion(final DataVersions needsUpdating) {
		dataVersion.updateFrom(needsUpdating);
	}
}
