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
 * Enumeration for player flags.
 * 
 * This is a bit mask so it can have up to 32 options.
 * 
 * @author LLambert
 *
 */
public final class PlayerFlag extends FlagBit {
	/**
	 * Next available value.
	 */
	private static int nextValue = 0;
	/**
	 * No option.
	 */
	public static final PlayerFlag NONE = new PlayerFlag("None"); // 0
	/**
	 * Pog is dead.
	 */
	public static final PlayerFlag DEAD = new PlayerFlag("Dead"); // 1
	/**
	 * Pog is invisible.
	 */
	public static final PlayerFlag INVISIBLE = new PlayerFlag("Invisible"); // 2
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
	private PlayerFlag(final String flagName) {
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
