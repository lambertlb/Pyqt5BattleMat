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
package per.lambert.ebattleMat.server.serviceData;

/**
 * Session Data for a dungeon.
 * 
 * @author LLambert
 *
 */
public class DungeonSessionData {
	/**
	 * session version.
	 */
	private int version;
	/**
	 * Session name.
	 */
	private String sessionName;
	/**
	 * dungeon UUID.
	 */
	private String dungeonUUID;
	/**
	 * session UUID.
	 */
	private String sessionUUID;
	/**
	 * players in this session.
	 */
	private PogList players = new PogList();
	/**
	 * Level for this session.
	 */
	private DungeonSessionLevel[] sessionLevels;

	/**
	 * get session version.
	 * 
	 * @return session version
	 */
	public int getVersion() {
		return version;
	}

	/**
	 * increment session version.
	 */
	public void increamentVersion() {
		if (++version == Integer.MAX_VALUE) {
			version = 1;
		}
	}

	/**
	 * get Session name.
	 * 
	 * @return Session name.
	 */
	public String getSessionName() {
		return sessionName;
	}

	/**
	 * set Session name.
	 * 
	 * @param sessionName Session name.
	 */
	public void setSessionName(final String sessionName) {
		this.sessionName = sessionName;
	}

	/**
	 * get dungeon UUID.
	 * 
	 * @return dungeon UUID.
	 */
	public String getDungeonUUID() {
		return dungeonUUID;
	}

	/**
	 * set dungeon UUID.
	 * 
	 * @param dungeonUUID dungeon UUID.
	 */
	public void setDungeonUUID(final String dungeonUUID) {
		this.dungeonUUID = dungeonUUID;
	}

	/**
	 * get session UUID.
	 * 
	 * @return session UUID.
	 */
	public String getSessionUUID() {
		return sessionUUID;
	}

	/**
	 * set session UUID.
	 * 
	 * @param sessionUUID session UUID.
	 */
	public void setSessionUUID(final String sessionUUID) {
		this.sessionUUID = sessionUUID;
	}

	/**
	 * get players in this session.
	 * 
	 * @return players in this session.
	 */
	public PogList getPlayers() {
		return players;
	}

	/**
	 * set players in this session.
	 * 
	 * @param players players in this session.
	 */
	public void setPlayers(final PogList players) {
		this.players = players;
	}

	/**
	 * get Level for this session.
	 * 
	 * @return Level for this session.
	 */
	public DungeonSessionLevel[] getSessionLevels() {
		return sessionLevels;
	}

	/**
	 * set Level for this session.
	 * 
	 * @param sessionLevels Level for this session.
	 */
	public void setSessionLevels(final DungeonSessionLevel[] sessionLevels) {
		this.sessionLevels = sessionLevels;
	}

	/**
	 * Constructor for session data.
	 * 
	 * @param newSessionName new session name
	 * @param dungeonUUID dungeon UUID
	 * @param sessionUUID session UUID
	 */
	public DungeonSessionData(final String newSessionName, final String dungeonUUID, final String sessionUUID) {
		version = 1;
		sessionName = newSessionName;
		this.dungeonUUID = dungeonUUID;
		this.sessionUUID = sessionUUID;
	}
}
