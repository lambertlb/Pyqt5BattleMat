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

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Enumeration of Dungeon master flags. This is a bit mask meaning every item is a power of two.
 * 
 * @author LLambert
 *
 */
public final class DungeonMasterFlag extends FlagBit {
	/**
	 * Next available value.
	 */
	private static int nextValue = 0;
	/**
	 * No flag.
	 */
	public static final DungeonMasterFlag NONE = new DungeonMasterFlag("None"); // 0
	/**
	 * This pog is invisible to players.
	 */
	public static final DungeonMasterFlag INVISIBLE_FROM_PLAYER = new DungeonMasterFlag("Invisible to Player"); // 1
	/**
	 * The background is transparent.
	 */
	public static final DungeonMasterFlag TRANSPARENT_BACKGROUND = new DungeonMasterFlag("Transparent Background"); // 2
	/**
	 * The pog is shifted a half cell to right.
	 */
	public static final DungeonMasterFlag SHIFT_RIGHT = new DungeonMasterFlag("Shifted to Right"); // 4
	/**
	 * The pog is shifted half a cell to the top.
	 */
	public static final DungeonMasterFlag SHIFT_TOP = new DungeonMasterFlag("Shifted to Top"); // 8
	/**
	 * Pog has dark background in edit mode.
	 */
	public static final DungeonMasterFlag DARK_BACKGROUND = new DungeonMasterFlag("Dark background in edit mode"); // 16

	/**
	 * Map of names vs flag bit.
	 */
	private static Map<String, FlagBit> nameMap;

	/**
	 * expose to sub-classes.
	 * 
	 * @return map of names
	 */
	protected static Map<String, FlagBit> getNameMap() {
		return nameMap;
	}

	/**
	 * Value vs flag bit.
	 */
	private static Map<Integer, FlagBit> valueMap;

	/**
	 * Constructor.
	 * 
	 * @param flagName flag name
	 */
	private DungeonMasterFlag(final String flagName) {
		super(flagName, nextValue);
		if (nextValue == 0) {
			nextValue = 1;
		} else {
			nextValue <<= 1;
		}
		if (nameMap == null) {
			nameMap = new LinkedHashMap<String, FlagBit>();
			valueMap = new LinkedHashMap<Integer, FlagBit>();
		}
		nameMap.put(flagName, (FlagBit) this);
		valueMap.put(getValue(), (FlagBit) this);
	}

	/**
	 * Get value for this name.
	 * 
	 * @param name to get
	 * @return flag bit
	 */
	public static FlagBit valueOf(final String name) {
		return (nameMap.get(name));
	}

	/**
	 * Get flag bit for this ordinal.
	 * 
	 * @param ordinal to get
	 * @return flag bit
	 */
	public static FlagBit valueOf(final int ordinal) {
		return (valueMap.get(ordinal));
	}

	/**
	 * Get collection of flags.
	 * 
	 * @return collection of flags.
	 */
	public static Collection<FlagBit> getValues() {
		ArrayList<FlagBit> list = new ArrayList<FlagBit>();
		for (FlagBit flagBit : getNameMap().values()) {
			list.add(flagBit);
		}
		return (list);
	}
}
