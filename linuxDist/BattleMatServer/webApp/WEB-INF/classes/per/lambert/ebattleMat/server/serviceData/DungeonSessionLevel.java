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
 * Session Level.
 * 
 * @author LLambert
 *
 */
public class DungeonSessionLevel {
	/**
	 * Version of for of war.
	 */
	private int fogOfWarVersion;

	/**
	 * Get fog of war version.
	 * 
	 * @return fog of war version
	 */
	public int getFogOfWarVersion() {
		return fogOfWarVersion;
	}
	/**
	 * Bits for fog of war.
	 */
	private long[] fogOfWarData = new long[0];
	/**
	 * list of monsters.
	 */
	private PogList monsters = new PogList();
	/**
	 * list of room objects.
	 */
	private PogList roomObjects = new PogList();

	/**
	 * set Array for Fog of War.
	 * 
	 * @param newFogOfWar Array for Fog of War.
	 */
	public void setFogOfWar(final long[] newFogOfWar) {
		this.fogOfWarData = newFogOfWar;
		++fogOfWarVersion;
	}

	/**
	 * get list of monsters.
	 * 
	 * @return list of monsters.
	 */
	public PogList getMonsters() {
		return monsters;
	}

	/**
	 * set list of monsters.
	 * 
	 * @param monsters list of monsters.
	 */
	public void setMonsters(final PogList monsters) {
		this.monsters = monsters;
	}

	/**
	 * get list of room objects.
	 * 
	 * @return list of room objects.
	 */
	public PogList getRoomObjects() {
		return roomObjects;
	}

	/**
	 * set list of room objects.
	 * 
	 * @param roomObjects list of room objects.
	 */
	public void setRoomObjects(final PogList roomObjects) {
		this.roomObjects = roomObjects;
	}

	/**
	 * constructor for session level.
	 * 
	 * @param dungeonLevel dungeon level to copy
	 */
	public DungeonSessionLevel(final DungeonLevel dungeonLevel) {
		monsters = dungeonLevel.getMonsters().clone();
		roomObjects = dungeonLevel.getRoomObjects().clone();
		creatFogOfWar(dungeonLevel);
	}

	/**
	 * create fog of war data.
	 * @param dungeonLevel
	 */
	private void creatFogOfWar(final DungeonLevel dungeonLevel) {
		int intsNeeded = ((dungeonLevel.getColumns() * dungeonLevel.getRows()) / 32) + 1;
		fogOfWarData = new long[intsNeeded];
		for (int i = 0; i < fogOfWarData.length; ++i) {
			fogOfWarData[i] = 0xffffffff;
		}
	}
}
