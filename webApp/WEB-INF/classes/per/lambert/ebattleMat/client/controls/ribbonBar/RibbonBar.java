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
package per.lambert.ebattleMat.client.controls.ribbonBar;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.CheckBox;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.Widget;

import per.lambert.ebattleMat.client.controls.NotesFloatingWindow;
import per.lambert.ebattleMat.client.controls.SelectedPogFloatingWindow;
import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.PogData;

/**
 * Ribbon bar on top of view.
 * 
 * This breaks down into columns and rows of bar items.
 * 
 * @author LLambert
 *
 */
public class RibbonBar extends Composite {

	/**
	 * UI Binder.
	 */
	private static RibbonBarUiBinder uiBinder = GWT.create(RibbonBarUiBinder.class);

	/**
	 * Interface for ui binder.
	 * 
	 * @author LLambert
	 *
	 */
	interface RibbonBarUiBinder extends UiBinder<Widget, RibbonBar> {
	}

	/**
	 * Panel for bar items.
	 */
	@SuppressWarnings("VisibilityModifier")
	@UiField
	HorizontalPanel panel;
	/**
	 * Grid to hold bar items.
	 */
	private Grid ribbonGrid;
	/**
	 * Control to show selected pog.
	 */
	private SelectedPog selectedPog;
	/**
	 * Fog of war toggle.
	 */
	private CheckBox fowToggle;
	/**
	 * List of levels to select.
	 */
	private ListBox levelSelect;
	/**
	 * List of character to select.
	 */
	private ListBox characterSelect;
	/**
	 * show selected pog.
	 */
	private CheckBox showSelectedPog;
	/**
	 * Selected pog floating window.
	 */
	private SelectedPogFloatingWindow pogWindow;
	/**
	 * show selected pog.
	 */
	private CheckBox showPogNotes;
	/**
	 * Selected pog notes floating window.
	 */
	private NotesFloatingWindow pogNotes;
	/**
	 * Link to help.
	 */
	private Anchor helpLink;
	/**
	 * Hide FOW.
	 */
	private CheckBox hideFOW;

	/**
	 * Constructor.
	 */
	public RibbonBar() {
		initWidget(uiBinder.createAndBindUi(this));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onLoad() {
		super.onLoad();
		createControls();
		setupEventHandler();
		setupView();
	}

	/**
	 * Create controls.
	 */
	private void createControls() {
		createCommonControls();
		createDMControls();
	}

	/**
	 * Create common controls.
	 */
	private void createCommonControls() {
		ribbonGrid = new Grid();
		ribbonGrid.resize(2, 10);
		ribbonGrid.setCellPadding(0);
		ribbonGrid.setCellSpacing(0);
		ribbonGrid.addStyleName("ribbonBarLabel");
		selectedPog = new SelectedPog(panel);
		createLevelSelection();
		createCharacterSelection();
		createShowPogsDialog();
		createShowPogNotesDialog();
		pogSelection();
	}

	/**
	 * Create DM controls.
	 */
	private void createDMControls() {
		fowToggle = new CheckBox("Toggle FOW");
		fowToggle.addStyleName("ribbonBarLabel");
		fowToggle.getElement().getStyle().setBackgroundColor("white");
		fowToggle.setTitle("Toggle Fog of War");
		fowToggle.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				ServiceManager.getDungeonManager().setFowToggle(fowToggle.getValue());
			}
		});
		helpLink = new Anchor("Help", "/help.html", "_blank");
		hideFOW = new CheckBox("Hide FOW");
		hideFOW.addStyleName("ribbonBarLabel");
		hideFOW.getElement().getStyle().setBackgroundColor("white");
		hideFOW.setTitle("Hide Fog of War");
		hideFOW.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				ServiceManager.getDungeonManager().setHideFOW(hideFOW.getValue());
			}
		});
	}

	/**
	 * create show pog notes controls.
	 */
	private void createShowPogNotesDialog() {
		showPogNotes = new CheckBox("Show Pog Notes");
		showPogNotes.setStyleName("ribbonBarLabel");
		showPogNotes.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				if (showPogNotes.getValue()) {
					pogNotes.show();
				} else {
					pogNotes.hide();
				}
			}
		});
		pogNotes = new NotesFloatingWindow();
		pogWindow.setModal(false);
		pogNotes.addSaveClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				pogNotesSaved();
			}
		});
	}

	private void pogNotesSaved() {
		PogData pogData = ServiceManager.getDungeonManager().getSelectedPog();
		pogData.setNotes(pogNotes.getNotesText());
		pogData.setDmNotes(pogNotes.getDMNotesText());
		ServiceManager.getDungeonManager().addOrUpdatePog(pogData);
	}

	/**
	 * Create show selected pog controls.
	 */
	private void createShowPogsDialog() {
		showSelectedPog = new CheckBox("Show Selected Pog");
		showSelectedPog.setStyleName("ribbonBarLabel");
		showSelectedPog.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				if (showSelectedPog.getValue()) {
					pogWindow.show();
				} else {
					pogWindow.hide();
				}
			}
		});
		pogWindow = new SelectedPogFloatingWindow();
		pogWindow.setModal(false);
	}

	/**
	 * create character selection controls.
	 */
	private void createCharacterSelection() {
		characterSelect = new ListBox();
		characterSelect.setVisibleItemCount(1);
		characterSelect.addStyleName("ribbonBarLabel");
		characterSelect.addChangeHandler(new ChangeHandler() {

			@Override
			public void onChange(final ChangeEvent event) {
				characterWasSelected();
			}
		});
	}

	/**
	 * Create level selection controls.
	 */
	private void createLevelSelection() {
		levelSelect = new ListBox();
		levelSelect.setVisibleItemCount(1);
		levelSelect.addStyleName("ribbonBarLabel");
		levelSelect.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				ServiceManager.getDungeonManager().setCurrentLevel(levelSelect.getSelectedIndex());
			}
		});
	}

	/**
	 * Setup event handlers.
	 */
	private void setupEventHandler() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.DMStateChange) {
					setupView();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataLoaded) {
					dungeonDataLoaded();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataSaved) {
					dungeonDataLoaded();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.SessionDataChanged) {
					characterPogsLoaded();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataReadyToJoin) {
					characterPogsLoaded();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.PogWasSelected) {
					pogSelection();
					return;
				}
			}
		});
	}

	/**
	 * New pog was selected so adjust controls.
	 */
	private void pogSelection() {
		PogData selectedPog = ServiceManager.getDungeonManager().getSelectedPog();
		if (selectedPog != null) {
			pogNotes.setNotesText(selectedPog.getNotes());
			pogNotes.setDMNotesText(selectedPog.getDmNotes());
		}
	}

	/**
	 * Setup view.
	 */
	private void setupView() {
		setupViewCommon();
		if (ServiceManager.getDungeonManager().isDungeonMaster()) {
			setupForDungeonMaster();
		} else {
			setupForPlayer();
		}
	}

	/**
	 * Setup common portion of view.
	 * 
	 * These are items the same between player and DM.
	 */
	private void setupViewCommon() {
		panel.clear();
		ribbonGrid.clear();
		panel.getElement().getStyle().setBackgroundColor("grey");
		panel.add(selectedPog);
		panel.add(ribbonGrid);
	}

	/**
	 * Setup for player.
	 */
	private void setupForPlayer() {
		ribbonGrid.setWidget(0, 0, levelSelect);
		ribbonGrid.setWidget(1, 0, characterSelect);
		ribbonGrid.setWidget(0, 2, showSelectedPog);
		ribbonGrid.setWidget(1, 2, showPogNotes);
	}

	/**
	 * Setup for dungeon master.
	 */
	private void setupForDungeonMaster() {
		setupForCommonDMControls();
		if (ServiceManager.getDungeonManager().isEditMode()) {
			ribbonGrid.setWidget(0, 5, helpLink);
		} else {
			ribbonGrid.setWidget(1, 0, characterSelect);
			ribbonGrid.setWidget(1, 4, fowToggle);
			ribbonGrid.setWidget(0, 7, helpLink);
			ribbonGrid.setWidget(0, 4, hideFOW);
		}
	}

	/**
	 * Setup controls for all DM modes.
	 */
	private void setupForCommonDMControls() {
		ribbonGrid.setWidget(0, 0, levelSelect);
		ribbonGrid.setWidget(0, 3, showSelectedPog);
		ribbonGrid.setWidget(1, 3, showPogNotes);
	}

	/**
	 * Dungeon data loaded.
	 */
	private void dungeonDataLoaded() {
		levelSelect.clear();
		String[] levelNames = ServiceManager.getDungeonManager().getDungeonLevelNames();
		for (String levelName : levelNames) {
			levelSelect.addItem(levelName);
		}
		levelSelect.setSelectedIndex(ServiceManager.getDungeonManager().getCurrentLevelIndex());
	}

	/**
	 * Character pogs loaded.
	 */
	private void characterPogsLoaded() {
		characterSelect.clear();
		characterSelect.addItem("Select Character Pog", "");
		PogData[] players = ServiceManager.getDungeonManager().getPlayersForCurrentSession();
		if (players == null) {
			return;
		}
		for (PogData pogData : players) {
			characterSelect.addItem(pogData.getName(), pogData.getUUID());
		}
	}

	/**
	 * Character was selected.
	 */
	private void characterWasSelected() {
		String uuid = characterSelect.getSelectedValue();
		if (uuid == null || uuid.isEmpty()) {
			return;
		}
		PogData characterPog = ServiceManager.getDungeonManager().findCharacterPog(uuid);
		if (characterPog != null) {
			ServiceManager.getDungeonManager().setSelectedPog(characterPog);
		}
	}
}
