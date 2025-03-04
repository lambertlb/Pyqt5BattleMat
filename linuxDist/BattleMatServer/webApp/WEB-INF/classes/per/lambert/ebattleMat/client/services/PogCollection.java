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
package per.lambert.ebattleMat.client.services;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.google.gwt.core.client.JsonUtils;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.interfaces.IDataRequester;
import per.lambert.ebattleMat.client.interfaces.IErrorInformation;
import per.lambert.ebattleMat.client.interfaces.IUserCallback;
import per.lambert.ebattleMat.client.interfaces.PogPlace;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.serviceData.PogData;
import per.lambert.ebattleMat.client.services.serviceData.PogList;

/**
 * Pog collection.
 * 
 * This will hold information about a pog list.
 * 
 * @author llambert
 *
 */
public class PogCollection {
	/**
	 * Compare allowing duplicates.
	 * 
	 * @author LLambert
	 *
	 */
	private final class PogComparator implements Comparator<PogData> {
		@Override
		public int compare(final PogData a, final PogData b) {
			int cp = a.getName().compareToIgnoreCase(b.getName());
			return cp == 0 ? 1 : cp;
		}
	}

	/**
	 * load event.
	 */
	private ReasonForAction loadEvent;
	/**
	 * Place where pog resides.
	 */
	private PogPlace pogPlace;
	/**
	 * Map of pog data vs name.
	 */
	private Map<String, PogData> pogMap = new HashMap<String, PogData>();
	/**
	 * List of pog templates.
	 */
	private PogList pogList;

	/**
	 * get array of pog templates.
	 * 
	 * @return array of pog templates
	 */
	public PogData[] getPogList() {
		return pogList.getPogList();
	}

	/**
	 * Constructor.
	 * 
	 * @param eventToFireWhenLoaded event to fire when loaded
	 * @param pogPlace place where pog resides.
	 */
	public PogCollection(final ReasonForAction eventToFireWhenLoaded, final PogPlace pogPlace) {
		loadEvent = eventToFireWhenLoaded;
		this.pogPlace = pogPlace;
	}

	/**
	 * Find this pog based on UUID.
	 * 
	 * @param pogUUID to find
	 * @return pog data if found
	 */
	public PogData findPog(final String pogUUID) {
		return (pogMap.get(pogUUID));
	}

	/**
	 * Clear out collections.
	 */
	private void clear() {
		pogMap.clear();
	}

	/**
	 * Load in Pogs from resource file.
	 * 
	 * @param typeToLoad type to load
	 */
	public void loadFromServer(final String typeToLoad) {
		clear();
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("fileName", typeToLoad + "pogs.json");
		dataRequester.requestData("", "LOADJSONFILE", parameters, new IUserCallback() {

			@Override
			public void onSuccess(final Object sender, final Object data) {
				loadPogTemplates(data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}
		});
	}

	/**
	 * Got data from server fill in collections.
	 * 
	 * @param data received
	 */
	private void loadPogTemplates(final Object data) {
		setPogList(JsonUtils.<PogList>safeEval((String) data));
	}

	/**
	 * Set pog list.
	 * 
	 * @param pogList to use
	 */
	public void setPogList(final PogList pogList) {
		this.pogList = pogList;
		rebuildCollections();
	}

	/**
	 * Rebuild all collections.
	 */
	private void rebuildCollections() {
		clear();
		for (PogData pogTemplate : pogList.getPogList()) {
			pogTemplate.setPogPlace(pogPlace); // add pog place to pog on client side
			addToCollections(pogTemplate);
		}
		if (loadEvent != ReasonForAction.LastReason) {
			ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(loadEvent, null));
		}
	}

	/**
	 * Add information to various collections.
	 * 
	 * @param pogToAdd with data to add
	 */
	private void addToCollections(final PogData pogToAdd) {
		pogMap.put(pogToAdd.getUUID(), pogToAdd);
	}

	/**
	 * add or update this pog.
	 * 
	 * @param pog to add or update
	 */
	public void addOrUpdatePogCollection(final PogData pog) {
		PogData existing = findPog(pog.getUUID());
		if (existing == null) {
			addPog(pog);
		} else {
			pogList.update(pog, existing);
		}
	}

	/**
	 * Add this pog.
	 * @param pog
	 */
	private void addPog(final PogData pog) {
		pog.setPogPlace(pogPlace);
		pogList.addPog(pog);
		addToCollections(pog);
	}

	/**
	 * Remove this pog.
	 * 
	 * @param pog
	 */
	public void remove(final PogData pog) {
		if (findPog(pog.getUUID()) == null) {
			return;
		}
		pogList.remove(pog);
		pogMap.remove(pog.getUUID());
	}

	/**
	 * get a sorted list of pogs.
	 * 
	 * @return sorted list
	 */
	public List<PogData> getSortedListOfPogs() {
		if (pogList == null || pogList.getPogList() == null) {
			return (null);
		}
		List<PogData> keys = new ArrayList<>();
		for (PogData pog : pogList.getPogList()) {
			keys.add(pog);
		}
		Collections.sort(keys, new PogComparator());
		return (keys);
	}

	/**
	 * Get version of pog list.
	 * 
	 * @return versionof list
	 */
	public int getPogListVserion() {
		if (pogList == null) {
			return (-1);
		}
		return (pogList.getListVersion());
	}
	
	/**
	 * Update Pogs with data in list.
	 * @param updateList
	 */
	public void	updateCollection(final PogList updateList) {
		if (pogList == null) {
			setPogList(updateList);
			return;
		}
		ArrayList<PogData> toRemove = new ArrayList<PogData>(Arrays.asList(pogList.getPogList()));
		ArrayList<PogData> toAdd = new ArrayList<PogData>();
		for (PogData pd : updateList.getPogList()) {
			pd.setPogPlace(pogPlace);
			PogData found = pogMap.get(pd.getUUID());
			if (found != null) {
				found.fullUpdate(pd);
				toRemove.remove(found);
				continue;
			}
			toAdd.add(pd);
		}
		for (PogData pg : toRemove) {
			remove(pg);
		}
		for (PogData pg : toAdd) {
			addPog(pg);
		}
	}
}
