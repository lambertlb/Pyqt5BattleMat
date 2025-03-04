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
 * Enumeration of reasons for events.
 * 
 * @author LLambert
 *
 */
public enum ReasonForAction {
	/**
	 * Login happened.
	 */
	Login,
	/**
	 * Dungeon has been selected and being loaded.
	 */
	DungeonSelected,
	/**
	 * Dungeon data has been loaded.
	 */
	DungeonDataLoaded,
	/**
	 * Dungeon data has been saved.
	 */
	DungeonDataSaved,
	/**
	 * Dungeon has been loaded and is ready to be edited.
	 */
	DungeonDataReadyToEdit,
	/**
	 * Dungeon session has been loaded for the first time and is ready to be joined.
	 */
	DungeonDataReadyToJoin,
	/**
	 * A new dungeon was created on server.
	 */
	DungeonDataCreated,
	/**
	 * Dungeon was deleted on server.
	 */
	DungeonDataDeleted,
	/**
	 * Dungeon level selection has changed.
	 */
	DungeonSelectedLevelChanged,
	/**
	 * Monster template pog list has changed.
	 */
	MonsterPogsLoaded,
	/**
	 * Room Object template pog list has changed.
	 */
	RoomObjectPogsLoaded,
	/**
	 * Selected Pog has changed.
	 */
	PogWasSelected,
	/**
	 * Toggle Fog of War has changed.
	 */
	ToggleFowSelected,
	/**
	 * Bubble to lower widgets that a mouse down occurred.
	 */
	MouseDownEventBubble,
	/**
	 * Bubble to lower widgets that a mouse up occurred.
	 */
	MouseUpEventBubble,
	/**
	 * Bubble to lower widgets that a mouse move occurred.
	 */
	MouseMoveEventBubble,
	/**
	 * Received a new list of sessions.
	 */
	SessionListChanged,
	/**
	 * Session data has been saved to server.
	 */
	SessionDataSaved,
	/**
	 * New session data has arrived from server.
	 */
	SessionDataChanged,
	/**
	 * Dungeon master state changed.
	 */
	DMStateChange,
	/**
	 * Pog data changed.
	 */
	PogDataChanged,
	/**
	 * Last reason used for array sizing.
	 */
	LastReason
}
