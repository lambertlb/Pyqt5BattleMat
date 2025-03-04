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
package per.lambert.ebattleMat.client.controls.dungeonSelectDialog;

import java.util.Map;
import java.util.TreeMap;

import com.google.gwt.dom.client.Element;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.KeyUpEvent;
import com.google.gwt.event.dom.client.KeyUpHandler;
import com.google.gwt.event.logical.shared.ResizeEvent;
import com.google.gwt.event.logical.shared.ResizeHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.CheckBox;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.ListBox;
import com.google.gwt.user.client.ui.TextBox;

import per.lambert.ebattleMat.client.controls.OkCancelDialog;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.services.serviceData.SessionListData;

/**
 * Dungeon Selection control.
 * 
 * This has the job of allowing for selection of an existing dungeon or creating a new one. It also allows for creating a session for a particular dungeon.
 * 
 * @author LLambert
 *
 */
public class DungeonSelectDialog extends OkCancelDialog {
	/**
	 * Presenter for this view.
	 */
	private DungeonSelectPresenter dungeonSelectPresenter;
	/**
	 * List of available dungeons.
	 */
	private ListBox dungeonDropdownList;
	/**
	 * List of available sessions for the selected dungeon.
	 */
	private ListBox sessionDropdownList;
	/**
	 * Edit this dungeon template.
	 */
	private Button editDungeonButton;
	/**
	 * delete the selected dungeon.
	 */
	private Button deleteDungeonButton;
	/**
	 * delete the selected session.
	 */
	private Button deleteSessionButton;
	/**
	 * Create a new dungeon.
	 */
	private Button createDungeonButton;
	/**
	 * Create a new session.
	 */
	private Button createSessionButton;
	/**
	 * DM this session.
	 */
	private Button dmSessionButton;
	/**
	 * Join as player to this session.
	 */
	private Button joinASessionButton;
	/**
	 * Name of new dungeon.
	 */
	private TextBox newDungeonName;
	/**
	 * Name of new session.
	 */
	private TextBox newSessionName;
	/**
	 * Label for session name.
	 */
	private Label sessionLabel;
	/**
	 * Label for dungeon template.
	 */
	private Label templateLabel;
	/**
	 * Managing dungeon as DM.
	 */
	private CheckBox asDM;
	/**
	 * Grid for content.
	 */
	private Grid centerGrid;
	/**
	 * DM flag state changed.
	 */
	private boolean dmStateChanged;
	/**
	 * Grid has been populated.
	 */
	private boolean gridPopulated;

	/**
	 * Constructor for Dungeon Select control.
	 */
	public DungeonSelectDialog() {
		super("Dungeon Template Management", false, true, 400, 400);
		load();
	}

	/**
	 * Load in content.
	 */
	private void load() {
		getElement().getStyle().setZIndex(Constants.DIALOG_Z);
		dungeonSelectPresenter = new DungeonSelectPresenter();
		dungeonSelectPresenter.setView(this);
		createContent();
		setGlassEnabled(true);
		setText("Dungeon Select");
		setupEventHandlers();
		initialize();
	}

	/**
	 * Initialize view.
	 * 
	 * This is needed because the dialog can be reused many times.
	 */
	private void initialize() {
		resetNewDungeonName();
		setToDungeonMasterState();
		center();
	}

	/**
	 * Create content.
	 * 
	 * This should only ever happen once.
	 */
	private void createContent() {
		centerGrid = getCenterGrid();
		asDM = new CheckBox("I am DM");
		dungeonDropdownList = new ListBox();
		sessionDropdownList = new ListBox();
		editDungeonButton = new Button("Edit Dungeon");
		deleteDungeonButton = new Button("Delete Dungeon");
		deleteSessionButton = new Button("Delete Session");
		createDungeonButton = new Button("Create New Dungeon ->");
		createSessionButton = new Button("Create New Session ->");
		dmSessionButton = new Button("DM the Session");
		joinASessionButton = new Button("Join A Session");
		newDungeonName = new TextBox();
		newDungeonName.setText("Enter Dungeon Name");
		newSessionName = new TextBox();
		newSessionName.setText("Enter Session Name");
		sessionLabel = new Label("Session Management");
		templateLabel = new Label("Dungeon Template Management");
	}

	/**
	 * Setup event handlers.
	 */
	private void setupEventHandlers() {
		asDM.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.setDungeonMaster(asDM.getValue());
			}
		});
		editDungeonButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.editDungeon();
			}
		});
		deleteDungeonButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.deleteTemplate();
			}
		});
		deleteSessionButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.deleteSession();
			}
		});
		createDungeonButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.createDungeon();
			}
		});
		createSessionButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.createSession();
			}
		});
		joinASessionButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.joinSession();
			}
		});
		dmSessionButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				dungeonSelectPresenter.dmSession();
			}
		});
		dungeonDropdownList.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				dungeonSelectPresenter.selectNewDungeonName(dungeonDropdownList.getSelectedItemText(), dungeonDropdownList.getSelectedValue());
			}
		});
		newDungeonName.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				dungeonSelectPresenter.newDungeonNameText(newDungeonName.getValue());
			}
		});
		newDungeonName.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				dungeonSelectPresenter.newDungeonNameText(newDungeonName.getValue());
			}
		});
		newDungeonName.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				newDungeonName.selectAll();
			}
		});
		sessionDropdownList.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				dungeonSelectPresenter.selectSessionName(sessionDropdownList.getSelectedItemText(), sessionDropdownList.getSelectedValue());
			}
		});
		newSessionName.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				newSessionName.selectAll();
			}
		});
		newSessionName.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				dungeonSelectPresenter.newSessionNameText(newSessionName.getValue());
			}
		});
		Window.addResizeHandler(new ResizeHandler() {
			@Override
			public void onResize(final ResizeEvent event) {
				if (isShowing()) {
					center();
				}
			}
		});
	}

	/**
	 * populate grid.
	 */
	private void populateGrid() {
		if (gridPopulated && dmStateChanged == dungeonSelectPresenter.isDungeonMaster()) {
			return;
		}
		gridPopulated = true;
		dmStateChanged = dungeonSelectPresenter.isDungeonMaster();
		centerGrid.clear();
		centerGrid.resize(12, 2);
		if (dungeonSelectPresenter.isDungeonMaster()) {
			populateDMView();
		} else {
			populatePlayerView();
		}
		Element element = centerGrid.getCellFormatter().getElement(1, 0);
		element.setAttribute("colspan", "3");
		sessionLabel.addStyleName("sessionLabel");
		templateLabel.addStyleName("sessionLabel");
	}

	/**
	 * Populate common content for player and DM.
	 */
	private void populateCommon() {
		centerGrid.setWidget(0, 0, asDM);
		centerGrid.setWidget(1, 0, templateLabel);
		centerGrid.setWidget(2, 0, dungeonDropdownList);
	}

	/**
	 * Populate grid for a player.
	 */
	private void populatePlayerView() {
		populateCommon();
		centerGrid.setWidget(3, 0, sessionDropdownList);
		centerGrid.setWidget(4, 0, joinASessionButton);
	}

	/**
	 * Populate grid for a dungeon master.
	 */
	private void populateDMView() {
		populateCommon();
		centerGrid.setWidget(3, 0, createDungeonButton);
		centerGrid.setWidget(3, 1, newDungeonName);
		centerGrid.setWidget(4, 0, editDungeonButton);
		centerGrid.setWidget(5, 0, deleteDungeonButton);
		centerGrid.setWidget(6, 0, sessionLabel);
		centerGrid.setWidget(7, 0, sessionDropdownList);
		centerGrid.setWidget(8, 0, dmSessionButton);
		centerGrid.setWidget(9, 0, deleteSessionButton);
		centerGrid.setWidget(10, 0, createSessionButton);
		centerGrid.setWidget(10, 1, newSessionName);

		Element element2 = centerGrid.getCellFormatter().getElement(6, 0);
		element2.setAttribute("colspan", "3");
	}

	/**
	 * Close this dialog.
	 */
	public void close() {
		dungeonSelectPresenter.close();
		hide();
	}

	/**
	 * setup based on dungeon master state.
	 */
	public void setToDungeonMasterState() {
		populateGrid();
		if (dungeonSelectPresenter.isDungeonMaster()) {
			setupDisplayForDungeonMaster();
		} else {
			setupDisplayForPlayer();
		}
	}

	/**
	 * setup for dungeon master.
	 */
	private void setupDisplayForDungeonMaster() {
		enableWidget(createDungeonButton, dungeonSelectPresenter.isOkToCreateDungeon());
		enableWidget(editDungeonButton, dungeonSelectPresenter.isTemplateSelected());
		enableWidget(deleteDungeonButton, dungeonSelectPresenter.isOkToDelete());
		enableWidget(newDungeonName, true);
//		if (!dungeonSelectPresenter.isTemplateSelected()) {
//			newDungeonName.setText("Enter Dungeon Name");
//		}
		setupSessionDisplayForDungeonMaster();
	}

	/**
	 * reset new dungeon name.
	 */
	public void resetNewDungeonName() {
		newDungeonName.setText("Enter Dungeon Name");
	}
	/**
	 * load in list of dungeons.
	 */
	public void loadDungeonList() {
		dungeonDropdownList.clear();
		dungeonDropdownList.addItem("Select a Dungeon for Operations");
		Map<String, String> dungeonNameToUUIDMap = dungeonSelectPresenter.getDungeonToUUIDMap();
		TreeMap<String, String> sorted = new TreeMap<>(dungeonNameToUUIDMap);
		for (Map.Entry<String, String> entry : sorted.entrySet()) {
			dungeonDropdownList.addItem(entry.getKey(), entry.getValue());
		}
		dungeonDropdownList.setVisibleItemCount(1);
	}

	/**
	 * setup display for a player.
	 */
	private void setupDisplayForPlayer() {
		enableWidget(sessionDropdownList, dungeonSelectPresenter.isOkToShowSessions());
		enableWidget(joinASessionButton, dungeonSelectPresenter.isOkToJoinSession());
	}

	/**
	 * {@inheritDoc}
	 */
	public void show() {
		super.show();
		dungeonSelectPresenter.refreshView();
		getElement().getStyle().setZIndex(Constants.DIALOG_Z + 2);
		initialize();
	}

	/**
	 * Setup session section as dungeon master.
	 */
	private void setupSessionDisplayForDungeonMaster() {
		enableWidget(sessionDropdownList, dungeonSelectPresenter.isOkToShowSessions());
		enableWidget(createSessionButton, dungeonSelectPresenter.isOkToCreateSession());
		enableWidget(deleteSessionButton, dungeonSelectPresenter.isOkToDeleteSession());
		enableWidget(dmSessionButton, dungeonSelectPresenter.isOkToDMSession());
		enableWidget(newSessionName, dungeonSelectPresenter.isOkToDelete());
		if (!dungeonSelectPresenter.isOkToDelete()) {
			resetNewSessionText();
		}
	}

	/**
	 * Reset the text for a nw session.
	 */
	public void resetNewSessionText() {
		newSessionName.setText("Enter Session Name");
	}

	/**
	 * Load list with sessions for this dungeon.
	 */
	public void loadSessionList() {
		setupSessionDisplayForDungeonMaster();
		sessionDropdownList.clear();
		sessionDropdownList.addItem(dungeonSelectPresenter.isDungeonMaster() ? "Select a Session to DM" : "Select a Session to Join");
		sessionDropdownList.setVisibleItemCount(1);
		if (!dungeonSelectPresenter.isOkToShowSessions()) {
			return;
		}
		SessionListData getSessionListData = dungeonSelectPresenter.getSessionListData();
		if (getSessionListData != null) {
			for (int i = 0; i < getSessionListData.getSessionNames().length; ++i) {
				sessionDropdownList.addItem(getSessionListData.getSessionNames()[i], getSessionListData.getSessionUUIDs()[i]);
			}
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onCancelClick(final ClickEvent event) {
		hide();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getMinWidth() {
		return 400;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getMinHeight() {
		return 400;
	}
}
