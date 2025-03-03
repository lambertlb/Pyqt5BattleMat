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
 * Message from server with a list of dungeons.
 * @author LLambert
 *
 */
public class DungeonListData extends JavaScriptObject {
	/**
	 * constructor for list of dungeons.
	 */
	protected DungeonListData() {
	}
	/**
	 * get array of dungeon names.
	 * @return array of dungeon names
	 */
	public final native String[] getDungeonNames() /*-{
		return this.dungeonNames;
	}-*/;
	/**
	 * get array of UUIDs associated with the dungeon names.
	 * @return array of UUIDs associated with the dungeon names.
	 */
	public final native String[] getDungeonUUIDS() /*-{
		return this.dungeonUUIDS;
	}-*/;
	/**
	 * get array of directory names associated with the dungeon names.
	 * @return array of directory names associated with the dungeon names.
	 */
	public final native String[] getDungeonDirectories() /*-{
		return this.dungeonDirectories;
	}-*/;
}
