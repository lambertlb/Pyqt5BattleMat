/*
 * Copyright (C) 2023 Leon Lambert.
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
package per.lambert.ebattleMat.client.controls;

import com.google.gwt.dom.client.Style.FontWeight;
import com.google.gwt.user.client.Command;
import com.google.gwt.user.client.ui.MenuBar;
import com.google.gwt.user.client.ui.MenuItem;
import com.google.gwt.user.client.ui.PopupPanel;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.DungeonMasterFlag;
import per.lambert.ebattleMat.client.interfaces.PlayerFlag;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.PogData;

/**
 * This suports popup menu for pog options.
 * 
 * @author llambert
 *
 */
public class PogPopupMenu extends PopupPanel {
	/**
	 * data for pog.
	 */
	private PogData pog;
	/**
	 * Dead toggle.
	 */
	private MenuItem deadToggle;
	/**
	 * player invisible toggle.
	 */
	private MenuItem pogInvisibleToggle;
	/**
	 * Invisible from player toggle.
	 */
	private MenuItem pogInvisibleFromPlayerToggle;
	/**
	 * transparent toggle.
	 */
	private MenuItem transparentToggle;
	/**
	 * shift right toggle.
	 */
	private MenuItem shiftRightToggle;
	/**
	 * shift top toggle.
	 */
	private MenuItem shiftTopToggle;
	/**
	 * dark background toggle.
	 */
	private MenuItem darkBackgroundToggle;

	/**
	 * Custom popup menu for pogs.
	 */
	public PogPopupMenu() {
		super(true);
		createContent();
	}

	/**
	 * Create content.
	 */
	private void createContent() {
		MenuBar menu = new MenuBar(true);
		addPlayerMenuItems(menu);
		addDMMenuItems(menu);
		addPogNumberMenu(menu);
		addUtilityMenuItems(menu);
		add(menu);
	}

	/**
	 * Add utility items to menu bar.
	 * 
	 * @param menu where to add
	 */
	private void addUtilityMenuItems(final MenuBar menu) {
		MenuBar utilityMenu = new MenuBar(true);
		utilityMenu.getElement().getStyle().setZIndex(Constants.POPUPMENU_Z);
		utilityMenu.addItem("Delete Selected Pog", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().deleteSelectedPog();
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.SessionDataSaved, null));
				hide();
			}
		});
		menu.addItem("Utilities", utilityMenu);
	}

	/**
	 * Add pog numbers to menu bar.
	 * 
	 * @param menu where to add
	 */
	private void addPogNumberMenu(final MenuBar menu) {
		MenuBar pogNumberMenu = new MenuBar(true);
		for (int i = 0; i <= Constants.MAX_POGNUMBER; ++i) {
			createPogNumberMenuItem(pogNumberMenu, i);
		}
		menu.addItem("Pog Number", pogNumberMenu);
	}

	/**
	 * Add dungeon manager menu items.
	 * 
	 * @param menu where to add
	 */
	private void addDMMenuItems(final MenuBar menu) {
		MenuBar dmMenu = new MenuBar(true);
		pogInvisibleFromPlayerToggle = dmMenu.addItem("Invisible Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(DungeonMasterFlag.INVISIBLE_FROM_PLAYER);
				hide();
			}
		});
		transparentToggle = dmMenu.addItem("Transparent Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(DungeonMasterFlag.TRANSPARENT_BACKGROUND);
				hide();
			}
		});
		shiftRightToggle = dmMenu.addItem("Shift Right Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(DungeonMasterFlag.SHIFT_RIGHT);
				hide();
			}
		});
		shiftTopToggle = dmMenu.addItem("Shift Top Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(DungeonMasterFlag.SHIFT_TOP);
				hide();
			}
		});
		darkBackgroundToggle = dmMenu.addItem("Dark Background Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(DungeonMasterFlag.DARK_BACKGROUND);
				hide();
			}
		});
		menu.addItem("DM FLags", dmMenu);
	}

	/**
	 * Create and add player items to menu.
	 * 
	 * @param menu place to add
	 */
	private void addPlayerMenuItems(final MenuBar menu) {
		MenuBar playerMenu = new MenuBar(true);
		playerMenu.getElement().getStyle().setZIndex(Constants.POPUPMENU_Z);
		deadToggle = playerMenu.addItem("Dead Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(PlayerFlag.DEAD);
				hide();
			}
		});
		pogInvisibleToggle = playerMenu.addItem("Invisible Toggle", new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().toggleFlagOfSelectedPog(PlayerFlag.INVISIBLE);
				hide();
			}
		});
		menu.addItem("Player FLags", playerMenu);
	}

	/**
	 * Add number to pog number menu.
	 * 
	 * @param pogNumberMenu to add to
	 * @param i number to add
	 */
	private void createPogNumberMenuItem(final MenuBar pogNumberMenu, final int i) {
		pogNumberMenu.addItem("" + i, new Command() {
			@Override
			public void execute() {
				ServiceManager.getDungeonManager().updateNumberOfSelectedPog(i);
				hide();
			}
		});
	}

	/**
	 * Use this pog data.
	 * 
	 * @param pog to use
	 */
	public void setPogData(final PogData pog) {
		this.pog = pog;
		if (pog == null) {
			return;
		}
		setupMenuItems();
	}

	/**
	 * Use pog data to setup pog items.
	 */
	private void setupMenuItems() {
		setupPlayerToggles();
		setupDMToggles();
	}

	/**
	 * adjust menu item depending is set or not. Since menu items do not support check marks we will use bold to show it as being set.
	 * 
	 * @param item to change
	 * @param isSet true if set
	 */
	private void showIfItemIsSet(final MenuItem item, final boolean isSet) {
		if (isSet) {
			item.getElement().getStyle().setFontWeight(FontWeight.BOLD);
		} else {
			item.getElement().getStyle().setFontWeight(FontWeight.NORMAL);
		}
	}

	/**
	 * Setup player toggles.
	 */
	private void setupPlayerToggles() {
		showIfItemIsSet(deadToggle, pog.isFlagSet(PlayerFlag.DEAD));
		showIfItemIsSet(pogInvisibleToggle, pog.isFlagSet(PlayerFlag.INVISIBLE));
	}

	/**
	 * Setup DM toggles.
	 */
	private void setupDMToggles() {
		showIfItemIsSet(pogInvisibleFromPlayerToggle, pog.isFlagSet(DungeonMasterFlag.INVISIBLE_FROM_PLAYER));
		showIfItemIsSet(transparentToggle, pog.isFlagSet(DungeonMasterFlag.TRANSPARENT_BACKGROUND));
		showIfItemIsSet(shiftRightToggle, pog.isFlagSet(DungeonMasterFlag.SHIFT_RIGHT));
		showIfItemIsSet(shiftTopToggle, pog.isFlagSet(DungeonMasterFlag.SHIFT_TOP));
		showIfItemIsSet(darkBackgroundToggle, pog.isFlagSet(DungeonMasterFlag.DARK_BACKGROUND));
	}
}
