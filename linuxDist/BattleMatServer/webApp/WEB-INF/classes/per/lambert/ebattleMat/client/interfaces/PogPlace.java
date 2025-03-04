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
 * Enumeration of where Pogs can reside on server.
 * 
 * @author LLambert
 *
 */
public final class PogPlace extends FlagBit {
	/**
	 * Next available value.
	 */
	private static int nextValue = 0;
	/**
	 * Resides in dungeon instance area.
	 */
	public static final PogPlace DUNGEON_LEVEL = new PogPlace("Dungeon Level");
	/**
	 * Resides in Session level instance area.
	 */
	public static final PogPlace SESSION_LEVEL = new PogPlace("Session Level");
	/**
	 * Resides in Session common resource area.
	 */
	public static final PogPlace SESSION_RESOURCE = new PogPlace("Player Location");
	/**
	 * Resides in Common resource area available to all dungeons.
	 */
	public static final PogPlace COMMON_RESOURCE = new PogPlace("Common Resource");


	/**
	 * Map of names vs flag bit.
	 */
	private static Map<String, FlagBit> nameMap;

	/**
	 * expose to sub-classes.
	 * 
	 * @return map of names
	 */
	private static Map<String, FlagBit> getNameMap() {
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
	private PogPlace(final String flagName) {
		super(flagName, nextValue);
		++nextValue;
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
	public static PogPlace valueOf(final String name) {
		return ((PogPlace)nameMap.get(name));
	}

	/**
	 * Get flag bit for this ordinal.
	 * 
	 * @param ordinal to get
	 * @return flag bit
	 */
	public static PogPlace valueOf(final int ordinal) {
		return ((PogPlace)valueMap.get(ordinal));
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
