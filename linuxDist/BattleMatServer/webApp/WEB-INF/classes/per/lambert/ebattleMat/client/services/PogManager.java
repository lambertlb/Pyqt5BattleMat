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

import com.google.gwt.core.client.JavaScriptObject;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.DungeonMasterFlag;
import per.lambert.ebattleMat.client.interfaces.IPogManager;
import per.lambert.ebattleMat.client.interfaces.PlayerFlag;
import per.lambert.ebattleMat.client.interfaces.PogPlace;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.serviceData.PogData;

/**
 * Pog manager.
 * 
 * @author LLambert
 *
 */
public abstract class PogManager implements IPogManager {
	/**
	 * Collection of monster templates.
	 */
	private PogCollection monsterCollection = new PogCollection(ReasonForAction.MonsterPogsLoaded, PogPlace.COMMON_RESOURCE);

	/**
	 * Get monster collection.
	 * @return monster collection
	 */
	protected PogCollection getMonsterCollection() {
		return monsterCollection;
	}

	/**
	 * Collection of room templates.
	 */
	private PogCollection roomCollection = new PogCollection(ReasonForAction.RoomObjectPogsLoaded, PogPlace.COMMON_RESOURCE);

	/**
	 * Get room collection.
	 * @return room collection
	 */
	protected PogCollection getRoomCollection() {
		return roomCollection;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData[] getRoomObjectTemplatePogs() {
		return roomCollection.getPogList();
	}

	/**
	 * Currently selected Pog.
	 */
	private PogData selectedPog;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData getSelectedPog() {
		return selectedPog;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setSelectedPog(final PogData selectedPog) {
		this.selectedPog = selectedPog;
		ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.PogWasSelected, null));
	}

	/**
	 * So sub-classes can set.
	 * 
	 * @param selectedPog selected pog.
	 */
	protected void setSelectedPogInternal(final PogData selectedPog) {
		this.selectedPog = selectedPog;
	}

	/**
	 * Pog being dragged.
	 */
	private PogData pogBeingDragged;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setPogBeingDragged(final PogData pogBeingDragged, final boolean fromRibbonBar) {
		this.pogBeingDragged = pogBeingDragged;
		this.fromRibbonBar = fromRibbonBar;
	}

	/**
	 * Pog was dragged from ribbon bar.
	 */
	private boolean fromRibbonBar;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isFromRibbonBar() {
		return fromRibbonBar;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData getPogBeingDragged() {
		return (pogBeingDragged);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public PogData createTemplatePog(final String type) {
		PogData pogData = (PogData) JavaScriptObject.createObject().cast();
		pogData.setUUID(Constants.generateUUID());
		pogData.setType(type);
		return (pogData);
	}

	/**
	 * Load in monster Pogs from resource file.
	 */
	public void loadMonsterPogs() {
		monsterCollection.loadFromServer(Constants.DUNGEON_MONSTER_LOCATION);
	}

	/**
	 * Load in room object Pogs from resource file.
	 */
	public void loadRoomObjectPogs() {
		roomCollection.loadFromServer(Constants.DUNGEON_ROOMOBJECT_LOCATION);
	}

	/**
	 * Get pog sizes.
	 * 
	 * @return pog sizes.
	 */
	@Override
	public String[] getPogSizes() {
		return (new String[] {"Normal", "Large", "Huge", "Gargantuan" });
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void updateNumberOfSelectedPog(final int newPogNumber) {
		if (selectedPog != null) {
			selectedPog.setPogNumber(newPogNumber);
			ServiceManager.getDungeonManager().addOrUpdatePog(selectedPog);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void toggleFlagOfSelectedPog(final PlayerFlag flag) {
		if (selectedPog != null) {
			if (selectedPog.isFlagSet(flag)) {
				selectedPog.clearFlags(flag);
			} else {
				selectedPog.setFlags(flag);
			}
			ServiceManager.getDungeonManager().addOrUpdatePog(selectedPog);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void toggleFlagOfSelectedPog(final DungeonMasterFlag flag) {
		if (!ServiceManager.getDungeonManager().isDungeonMaster()) {
			return;
		}
		if (selectedPog != null) {
			if (selectedPog.isFlagSet(flag)) {
				selectedPog.clearFlags(flag);
			} else {
				selectedPog.setFlags(flag);
			}
			ServiceManager.getDungeonManager().addOrUpdatePog(selectedPog);
		}
	}
}
