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

import java.util.UUID;

/**
 * Pog data server side.
 * 
 * @author LLambert
 *
 */
public class PogData {
	/**
	 * Name of pog.
	 */
	private String pogName;
	/**
	 * URL of pog image.
	 */
	private String pogImageUrl;
	/**
	 * Type of Pog.
	 */
	private String pogType;
	/**
	 * Size of pog in grid squares.
	 */
	private int pogSize;
	/**
	 * Column pog is in grid.
	 */
	private int pogColumn;
	/**
	 * Row pog is in grid.
	 */
	private int pogRow;
	/**
	 * UUID of pog instance.
	 */
	private String uuid;
	/**
	 * Level of dungeon pog is on.
	 */
	private int dungeonLevel;
	/**
	 * Flag bits for dungeon master.
	 */
	private int dungeonMasterFlags;
	/**
	 * Flag bits for player.
	 */
	private int playerFlags;
	/**
	 * Pog notes.
	 */
	private String notes;
	/**
	 * DM Pog notes.
	 */
	private String dmNotes;

	/**
	 * Pog Number.
	 */
	private int pogNumber;

	/**
	 * Constructor.
	 */
	public PogData() {
	}

	/**
	 * Constructor.
	 * 
	 * @param pogData to clone
	 */
	public PogData(final PogData pogData) {
		fullUpdate(pogData);
		uuid = pogData.uuid;
	}

	/**
	 * Update everything but UUIDs.
	 * 
	 * @param pogData with data
	 */
	public void fullUpdate(final PogData pogData) {
		updatePog(pogData);
		playerFlags = pogData.playerFlags;
		dungeonMasterFlags = pogData.dungeonMasterFlags;
		pogName = pogData.pogName;
		pogImageUrl = pogData.pogImageUrl;
		pogType = pogData.pogType;
		pogSize = pogData.pogSize;
		pogNumber = pogData.pogNumber;
	}

	/**
	 * Update pog with new data.
	 * 
	 * @param withUpdates with updates
	 */
	private void updatePog(final PogData withUpdates) {
		this.pogColumn = withUpdates.pogColumn;
		this.pogRow = withUpdates.pogRow;
		dungeonLevel = withUpdates.dungeonLevel;
		notes = withUpdates.notes;
		dmNotes = withUpdates.dmNotes;
	}

	/**
	 * {@inheritDoc}
	 */
	public PogData clone() {
		PogData clone = new PogData(this);
		UUID uuid = UUID.randomUUID();
		clone.uuid = uuid.toString();
		return (clone);
	}

	/**
	 * Is pog this type?
	 * 
	 * @param typeToCheck type to check
	 * @return true if is
	 */
	public boolean isType(final String typeToCheck) {
		return (pogType.equals(typeToCheck));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean equals(final Object toCompare) {
		if (toCompare instanceof PogData) {
			return (equals((PogData) toCompare));
		}
		return (false);
	}

	/**
	 * Are these the same?
	 * 
	 * @param toCompare to compare
	 * @return true if same uuid
	 */
	public boolean equals(final PogData toCompare) {
		if (toCompare == null) {
			return (false);
		}
		return (uuid.equals(toCompare.uuid));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int hashCode() {
		return uuid.hashCode();
	}
}
