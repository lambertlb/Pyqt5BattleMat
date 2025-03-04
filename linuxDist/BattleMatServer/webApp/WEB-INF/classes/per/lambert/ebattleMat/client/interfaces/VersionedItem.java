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

/**
 * Enumeration of items that can be versioned.
 * 
 * @author LLambert
 *
 */
public enum VersionedItem {
	/**
	 * Monsters in common resources.
	 */
	COMMON_RESOURCE_MONSTERS,
	/**
	 * Room objects in common resources.
	 */
	COMMON_RESOURCE_ROOMOBECTS,
	/**
	 * Monsters in dungeon level.
	 */
	DUNGEON_LEVEL_MONSTERS,
	/**
	 * Room objects in dungeon level.
	 */
	DUNGEON_LEVEL_ROOMOBJECTS,
	/**
	 * Monsters in session level.
	 */
	SESSION_LEVEL_MONSTERS,
	/**
	 * Room objects in session level.
	 */
	SESSION_LEVEL_ROOMOBJECTS,
	/**
	 * Player list.
	 */
	SESSION_RESOURCE_PLAYERS,
	/**
	 * Fog of war data.
	 */
	FOG_OF_WAR,
	/**
	 * Last value used for array sizing.
	 */
	LAST_VERSIONED_ITEM
}
