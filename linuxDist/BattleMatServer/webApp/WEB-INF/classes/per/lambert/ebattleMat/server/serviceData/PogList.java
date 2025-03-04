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
 * List of pogs.
 * 
 * @author LLambert
 *
 */
public class PogList {
	/**
	 * Version of this list.
	 */
	private int listVersion;
	/**
	 * List of pogs.
	 */
	private PogData[] pogList;
	
	/**
	 * Get version of list.
	 * @return version of list
	 */
	public int getListVersion() {
		return listVersion;
	}

	/**
	 * Get version of list.
	 * @param listVersion
	 */
	public void setListVersion(final int listVersion) {
		this.listVersion = listVersion;
	}

	/**
	 * Get list of pogs.
	 * 
	 * @return list of pogs.
	 */
	public PogData[] getPogList() {
		return pogList;
	}

	/**
	 * Constructor.
	 */
	public PogList() {
		this(0);
	}

	/**
	 * Constructor.
	 * 
	 * @param startingSize starting size.
	 */
	private PogList(final int startingSize) {
		pogList = new PogData[startingSize];
	}

	/**
	 * Update pog if it exists ot add it.
	 * 
	 * @param pog with data.
	 */
	public void addOrUpdate(final PogData pog) {
		for (PogData pogInList : pogList) {
			if (pogInList.equals(pog)) {
				pogInList.fullUpdate(pog);
				++listVersion;
				return;
			}
		}
		addPog(pog);
	}

	/**
	 * Add new pog to list.
	 * 
	 * @param pog to add
	 */
	private void addPog(final PogData pog) {
		PogData[] newList = new PogData[pogList.length + 1];
		for (int i = 0; i < pogList.length; ++i) {
			newList[i] = pogList[i];
		}
		newList[pogList.length] = pog;
		pogList = newList;
		++listVersion;
	}

	/**
	 * {@inheritDoc}
	 */
	public PogList clone() {
		PogList newList = new PogList(pogList.length);
		newList.setListVersion(listVersion);
		for (int i = 0; i < pogList.length; ++i) {
			newList.pogList[i] = pogList[i].clone();
		}
		return (newList);
	}

	/**
	 * delete this pog.
	 * 
	 * @param pogData to delete
	 */
	public void delete(final PogData pogData) {
		int index = find(pogData);
		if (index != -1) {
			PogData[] newList = new PogData[pogList.length - 1];
			for (int i = 0, j = 0; i < pogList.length; ++i) {
				if (i == index) {
					continue;
				}
				newList[j++] = pogList[i];
			}
			pogList = newList;
			++listVersion;
		}
	}

	/**
	 * Find pog.
	 * 
	 * @param pogData to find
	 * @return index of pog in arrary else -1.
	 */
	private int find(final PogData pogData) {
		for (int i = 0; i < pogList.length; ++i) {
			if (pogList[i].equals(pogData)) {
				return (i);
			}
		}
		return -1;
	}
}
