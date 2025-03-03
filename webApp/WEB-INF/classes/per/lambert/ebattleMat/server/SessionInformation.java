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
package per.lambert.ebattleMat.server;

import java.io.IOException;

import com.google.gson.Gson;

import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.server.serviceData.DungeonSessionData;
import per.lambert.ebattleMat.server.serviceData.DungeonSessionLevel;
import per.lambert.ebattleMat.server.serviceData.PogData;

/**
 * Worker class for managing dungeon session.
 * 
 * This is useful for caching session information.
 * 
 * @author LLambert
 *
 */
public class SessionInformation {
	/**
	 * Session is dirty.
	 */
	private boolean dirty;

	/**
	 * get is dirty.
	 * 
	 * @return true if dirty
	 */
	public boolean isDirty() {
		return dirty;
	}

	/**
	 * set is dirty.
	 * 
	 * @param dirty true if dirty
	 */
	public void setDirty(final boolean dirty) {
		this.dirty = dirty;
	}
	
	/**
	 * Directory of session.
	 */
	private String sessionDirectory;

	/**
	 * get session directory.
	 * 
	 * @return session directory.
	 */
	public String getSessionDirectory() {
		return sessionDirectory;
	}

	/**
	 * Set session directory.
	 * 
	 * @param sessionDirectory to set
	 */
	public void setSessionDirectory(final String sessionDirectory) {
		this.sessionDirectory = sessionDirectory;
	}

	/**
	 * Path to session.
	 */
	private String sessionPath;

	/**
	 * get session path.
	 * 
	 * @return session path
	 */
	public String getSessionPath() {
		return sessionPath;
	}

	/**
	 * set session path.
	 * 
	 * @param sessionPath to set
	 */
	public void setSessionPath(final String sessionPath) {
		this.sessionPath = sessionPath;
	}

	/**
	 * Data for session.
	 */
	private DungeonSessionData sessionData;

	/**
	 * Get session data.
	 * 
	 * @return session data
	 */
	public DungeonSessionData getSessionData() {
		return sessionData;
	}

	/**
	 * set session data.
	 * 
	 * @param sessionData to set
	 */
	public void setSessionData(final DungeonSessionData sessionData) {
		this.sessionData = sessionData;
	}

	/**
	 * get UUID of session.
	 * 
	 * @return uuid of session
	 */
	public String getUUID() {
		if (sessionData != null) {
			return (sessionData.getSessionUUID());
		}
		return (null);
	}

	/**
	 * Constructor.
	 */
	public SessionInformation() {
		this.sessionData = null;
		this.sessionPath = null;
		this.sessionDirectory = null;
	}

	/**
	 * Session information.
	 * 
	 * @param sessionData session data
	 * @param sessionPath session path
	 * @param sessionDirectory session directory
	 */
	public SessionInformation(final DungeonSessionData sessionData, final String sessionPath, final String sessionDirectory) {
		this();
		this.sessionData = sessionData;
		this.sessionPath = sessionPath;
		this.sessionDirectory = sessionDirectory;
	}

	/**
	 * get session level information.
	 * 
	 * @param currentLevel to get
	 * @return session level information or null
	 */
	private DungeonSessionLevel getSessionLevel(final int currentLevel) {
		if (currentLevel < 0 || currentLevel >= sessionData.getSessionLevels().length) {
			return (null);
		}
		return (sessionData.getSessionLevels()[currentLevel]);
	}

	/**
	 * Convert to JSON.
	 * 
	 * @return session data as JSON
	 */
	public String toJson() {
		if (sessionData != null) {
			Gson gson = new Gson();
			String sessionJson = gson.toJson(sessionData);
			return (sessionJson);
		}
		return ("");
	}

	/**
	 * Load in session data.
	 * 
	 * @param sessionPath path to data
	 * @param sessionDirectory directory for data
	 * @throws IOException if error
	 */
	public void load(final String sessionPath, final String sessionDirectory) throws IOException {
		this.sessionPath = sessionPath;
		this.sessionDirectory = sessionDirectory;
		String jsonData = DungeonsManager.readJsonFile(sessionPath);
		fromJson(jsonData);
	}

	/**
	 * convert from JSON data.
	 * 
	 * @param jsonData to convert
	 */
	public void fromJson(final String jsonData) {
		sessionData = null;
		if (jsonData != null && !jsonData.isEmpty()) {
			Gson gson = new Gson();
			sessionData = gson.fromJson(jsonData, DungeonSessionData.class);
		}
	}

	/**
	 * Save as JSON data.
	 * 
	 * @throws IOException if error
	 */
	public void save() throws IOException {
		Gson gson = new Gson();
		String sessionJson = gson.toJson(sessionData);
		DungeonsManager.saveJsonFile(sessionJson, sessionPath);
		dirty = false;
	}

	/**
	 * Add or update pog.
	 * @param pogData to add
	 * @param currentLevel where to add
	 */
	public void addOrUpdatePog(final PogData pogData, final int currentLevel) {
		DungeonSessionLevel sessionLevel = getSessionLevel(currentLevel);
		if (pogData.isType(Constants.POG_TYPE_MONSTER)) {
			sessionLevel.getMonsters().addOrUpdate(pogData);
		} else if (pogData.isType(Constants.POG_TYPE_ROOMOBJECT)) {
			sessionLevel.getRoomObjects().addOrUpdate(pogData);
		} else if (pogData.isType(Constants.POG_TYPE_PLAYER)) {
			sessionData.getPlayers().addOrUpdate(pogData);
		}
		sessionData.increamentVersion();
		dirty = true;
	}
	/**
	 * Save if dirty.
	 */
	public void saveIfDirty() {
		if (dirty) {
			try {
				save();
			} catch (IOException e) {
			}
			dirty = false;
		}
	}

	/**
	 * Update fog of war data in session level.
	 * 
	 * @param fowData to update
	 * @param currentLevel session level.
	 */
	public void updateFOW(final long[] fowData, final int currentLevel) {
		DungeonSessionLevel sessionLevel = getSessionLevel(currentLevel);
		if (sessionLevel == null) {
			return;
		}
		sessionLevel.setFogOfWar(fowData);
		sessionData.increamentVersion();
		dirty = true;
	}

	/**
	 * Delete pog from session.
	 * @param pogData pog
	 * @param level level
	 */
	public void delete(final PogData pogData, final int level) {
		DungeonSessionLevel sessionLevel = getSessionLevel(level);
		if (pogData.isType(Constants.POG_TYPE_MONSTER)) {
			sessionLevel.getMonsters().delete(pogData);
		} else if (pogData.isType(Constants.POG_TYPE_ROOMOBJECT)) {
			sessionLevel.getRoomObjects().delete(pogData);
		} else if (pogData.isType(Constants.POG_TYPE_PLAYER)) {
			sessionData.getPlayers().delete(pogData);
		}
		sessionData.increamentVersion();
		dirty = true;
	}
}
