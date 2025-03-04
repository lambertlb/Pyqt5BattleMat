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
 * Dungeon data server side.
 * 
 * @author LLambert
 *
 */
public class DungeonData {
	/**
	 * UUID for dungeon.
	 */
	private String uuid;
	/**
	 * Name of dungeon.
	 */
	private String dungeonName;
	/**
	 * dungeon level information.
	 */
	private DungeonLevel[] dungeonLevels;
	/**
	 * Show grid on levels.
	 */
	private boolean showGrid;

	/**
	 * get uuid for dungeon.
	 * 
	 * @return uuid for dungeon
	 */
	public String getUuid() {
		return uuid;
	}

	/**
	 * set uuid for dungeon.
	 * 
	 * @param uuid for dungeon
	 */
	public void setUuid(final String uuid) {
		this.uuid = uuid;
	}

	/**
	 * Get dungeon name.
	 * 
	 * @return dungeon name
	 */
	public String getDungeonName() {
		return dungeonName;
	}

	/**
	 * Set dungeon name.
	 * 
	 * @param dungeonName dungeon name.
	 * 
	 */
	public void setDungeonName(final String dungeonName) {
		this.dungeonName = dungeonName;
	}

	/**
	 * get dungeon levels.
	 * 
	 * @return dungeon levels
	 */
	public DungeonLevel[] getDungeonLevels() {
		return dungeonLevels;
	}

	/**
	 * set dungeon levels.
	 * 
	 * @param dungeonLevels dungeon Levels
	 */
	public void setDungeonLevels(final DungeonLevel[] dungeonLevels) {
		this.dungeonLevels = dungeonLevels;
	}

	/**
	 * get show grid.
	 * 
	 * @return true if shown
	 */
	public boolean isShowGrid() {
		return showGrid;
	}

	/**
	 * Set show grid.
	 * 
	 * @param showGrid true if shown
	 */
	public void setShowGrid(final boolean showGrid) {
		this.showGrid = showGrid;
	}
}
