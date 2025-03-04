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
 * Session list.
 * 
 * @author LLambert
 *
 */
public class SessionListData extends JavaScriptObject {
	/**
	 * Constructor.
	 */
	protected SessionListData() {
	}

	/**
	 * get UUID of dungeon.
	 * 
	 * @return UUID of dungeon
	 */
	public final native String getDungeonUUID() /*-{
		if (this.dungeonUUID === undefined) {
			this.dungeonUUID = "";
		}
		return (this.dungeonUUID);
	}-*/;

	/**
	 * Set UUID of dungeon.
	 * 
	 * @param dungeonUUID to set
	 */
	public final native void setDungeonUUID(String dungeonUUID) /*-{
		this.dungeonUUID = dungeonUUID;
	}-*/;

	/**
	 * get Session names.
	 * 
	 * @return Session names.
	 */
	public final native String[] getSessionNames() /*-{
		return this.sessionNames;
	}-*/;

	/**
	 * Get UUIDs for session names.
	 * @return UUIDs for session names
	 */
	public final native String[] getSessionUUIDs() /*-{
		return this.sessionUUIDs;
	}-*/;
}
