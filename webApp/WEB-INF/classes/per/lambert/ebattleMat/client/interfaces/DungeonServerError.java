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
 * Defines values for all errors that can occur in the application.
 *
 */
public enum DungeonServerError {
	/**
	 * Generic Error.
	 */
	GenericError(-1),
	/**
	 * Success so no error.
	 */
	Succsess(0),
	/**
	 * Undefined error.
	 */
	Undefined1(1);
	/**
	 * value of enumeration.
	 */
	private int value;

	/**
	 * Constructor for dungeon errors.
	 * 
	 * @param value of enumeration
	 */
	DungeonServerError(final int value) {
		this.value = value;
	}

	/**
	 * Get value of enumeration.
	 * 
	 * @return value of enumeration.
	 */
	public int getErrorValue() {
		return value;
	}

	/**
	 * Get enumeration value for this integer.
	 * 
	 * @param value to lookup
	 * @return error for integer
	 */
	public static DungeonServerError fromInt(final int value) {
		for (DungeonServerError error : DungeonServerError.values()) {
			if (error.getErrorValue() == value) {
				return error;
			}
		}
		return DungeonServerError.GenericError;
	}
}
