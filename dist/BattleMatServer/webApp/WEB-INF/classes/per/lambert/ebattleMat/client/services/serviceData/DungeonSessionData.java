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
package per.lambert.ebattleMat.client.services.serviceData;

import com.google.gwt.core.client.JavaScriptObject;

/**
 * Client side session data.
 * 
 * This needs to match per.lambert.ebattleMat.server.serviceData.DungeonSessionData
 * 
 * @author LLambert
 *
 */
public class DungeonSessionData extends JavaScriptObject {

	/**
	 * Constructor for session data.
	 */
	protected DungeonSessionData() {
	}

	/**
	 * get session version.
	 * 
	 * @return session version
	 */
	public final native int getVersion() /*-{
		if (this.version === undefined) {
			this.version = 0;
		}
		return (this.version);
	}-*/;

	/**
	 * Get session name.
	 * 
	 * @return session name
	 */
	public final native String getSessionName() /*-{
		if (this.sessionName === undefined) {
			this.sessionName = "";
		}
		return (this.sessionName);
	}-*/;

	/**
	 * Set session name.
	 * 
	 * @param sessionName session name.
	 */
	public final native void setSessionName(String sessionName) /*-{
		this.sessionName = sessionName;
	}-*/;

	/**
	 * get dungeon UUID.
	 * 
	 * @return dungeon UUID.
	 */
	public final native String getDungeonUUID() /*-{
		if (this.dungeonUUID === undefined) {
			this.dungeonUUID = "";
		}
		return (this.dungeonUUID);
	}-*/;

	/**
	 * set dungeon UUID.
	 * 
	 * @param dungeonUUID dungeon UUID.
	 */
	public final native void setDungeonUUID(String dungeonUUID) /*-{
		this.dungeonUUID = dungeonUUID;
	}-*/;

	/**
	 * set session UUID.
	 * 
	 * @return session UUID.
	 */
	public final native String getSessionUUID() /*-{
		if (this.sessionUUID === undefined) {
			this.sessionUUID = "";
		}
		return (this.sessionUUID);
	}-*/;

	/**
	 * Get list of players.
	 * 
	 * @return list of players.
	 */
	public final native PogList getPlayers() /*-{
		if (this.players === undefined) {
			this.players = {
				"pogList" : []
			};
		}
		return (this.players);
	}-*/;

	/**
	 * get levels for session.
	 * 
	 * @return levels for session
	 */
	public final native DungeonSessionLevel[] getSessionLevels() /*-{
		if (this.sessionLevels === undefined) {
			this.sessionLevels = [];
		}
		return this.sessionLevels;
	}-*/;
}
