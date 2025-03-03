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
 * Base class for managing flag bit.
 * 
 * This will simulate an enumeration but has the advantage of being sub-classed.
 * 
 * @author LLambert
 *
 */
public abstract class FlagBit {
	/**
	 * Value of item.
	 */
	private int value;

	/**
	 * Get value.
	 * 
	 * @return value
	 */
	public int getValue() {
		return value;
	}

	/**
	 * Name of item.
	 */
	private String name;

	/**
	 * Get name.
	 * 
	 * @return name
	 */
	public String getName() {
		return name;
	}

	/**
	 * Constructor.
	 * 
	 * @param flagName of value
	 * @param value of ordinal
	 */
	protected FlagBit(final String flagName, final int value) {
		this.value = value;
		name = flagName;
	}
}
