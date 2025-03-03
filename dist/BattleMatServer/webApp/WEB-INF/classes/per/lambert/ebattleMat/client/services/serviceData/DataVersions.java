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
package per.lambert.ebattleMat.client.services.serviceData;

import per.lambert.ebattleMat.client.interfaces.VersionedItem;

/**
 * Class for keeping track of data versions.
 * 
 * @author LLambert
 *
 */
public class DataVersions {
	/**
	 * Array of data versions.
	 */
	private int[] dataVersion;

	/**
	 * Constructor.
	 */
	public DataVersions() {
		dataVersion = new int[VersionedItem.LAST_VERSIONED_ITEM.ordinal()];
		initialize();
	}

	/**
	 * Initialize versions.
	 */
	public void initialize() {
		for (int i = 0; i < VersionedItem.LAST_VERSIONED_ITEM.ordinal(); ++i) {
			dataVersion[i] = -1;
		}
	}

	/**
	 * get version of this item.
	 * 
	 * @param item
	 * @return version of item.
	 */
	public int getItemVersion(final VersionedItem item) {
		return (dataVersion[item.ordinal()]);
	}
	
	/**
	 * Set version of item.
	 * @param item
	 * @param version
	 */
	public void setItemVersion(final VersionedItem item, final int version) {
		dataVersion[item.ordinal()] = version;
	}
	
	/**
	 * Update to the data in this master copy.
	 * @param needsUpdating
	 */
	public void updateFrom(final DataVersions needsUpdating) {
		for (int i = 0; i < dataVersion.length; ++i) {
			needsUpdating.dataVersion[i] = dataVersion[i];
		}
	}
}
