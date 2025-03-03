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
 * Java script class to manage Dungeon data from server.
 * 
 * This need to match per.lambert.ebattleMat.server.serviceData.DungeonData
 * 
 * @author LLambert
 *
 */
public class DungeonData extends JavaScriptObject {

	/**
	 * Constructor for dungeon data.
	 */
	protected DungeonData() {
	}

	/**
	 * Get UUID for this dungeon.
	 * 
	 * @return uuid for dungeon
	 */
	public final native String getUUID() /*-{
		if (this.uuid === undefined) {
			this.uuid = "";
		}
		return (this.uuid);
	}-*/;

	/**
	 * Set UUID for this dungeon.
	 * 
	 * @param uuid for dungeon
	 */
	public final native void setUUID(String uuid) /*-{
		this.uuid = uuid;
	}-*/;

	/**
	 * Get name of dungeon.
	 * 
	 * @return name of dungeon
	 */
	public final native String getDungeonName() /*-{
		if (this.dungeonName === undefined) {
			this.dungeonName = "";
		}
		return (this.dungeonName);
	}-*/;

	/**
	 * Set dungeon name.
	 * 
	 * @param dungeonName to set
	 */
	public final native void setDungeonName(String dungeonName) /*-{
		this.dungeonName = dungeonName;
	}-*/;

	/**
	 * get information about dungeon levels.
	 * 
	 * @return dungeon levels
	 */
	public final native DungeonLevel[] getDungeonlevels() /*-{
		if (this.dungeonLevels === undefined) {
			dungeonLevels = null;
		}
		return this.dungeonLevels;
	}-*/;

	/**
	 * Add a new dungeon level.
	 * 
	 * @param newLevel new level to add
	 */
	public final native void addDungeonlevel(DungeonLevel newLevel) /*-{
		this.dungeonLevels.push(newLevel);
	}-*/;

	/**
	 * Show grid on dungeon levels.
	 * 
	 * @param showGrid true to show
	 */
	public final native void setShowGrid(boolean showGrid) /*-{
		if (this.showGrid === undefined) {
			this.showGrid = false;
		}
		this.showGrid = showGrid;
	}-*/;

	/**
	 * Get show grid flag.
	 * 
	 * @return true if grid is to be shown
	 */
	public final native boolean getShowGrid() /*-{
		if (this.showGrid === undefined) {
			this.showGrid = false;
		}
		return (this.showGrid);
	}-*/;
	/**
	 * remove dungeon level.
	 * 
	 * @param levelIndex to remove
	 */
	public final void remove(final int levelIndex) {
		DungeonLevel[] list = getDungeonlevels();
		if (list == null || levelIndex < 0 || levelIndex >= list.length || list.length == 1) {
			return;
		}
		initList();
		int index = 0;
		for (DungeonLevel dungeonLevel : list) {
			if (levelIndex != index) {
				addDungeonlevel(dungeonLevel);
			}
			++index;
		}
	}

	/**
	 * create new list.
	 */
	private native void initList() /*-{
		this.dungeonLevels = [];
	}-*/;
}
