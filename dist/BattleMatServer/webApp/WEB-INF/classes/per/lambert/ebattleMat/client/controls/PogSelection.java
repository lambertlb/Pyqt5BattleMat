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

import java.util.List;

import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.event.logical.shared.OpenEvent;
import com.google.gwt.event.logical.shared.OpenHandler;
import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.ScrollPanel;
import com.google.gwt.user.client.ui.Tree;
import com.google.gwt.user.client.ui.TreeItem;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.PogPlace;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.PogData;

/**
 * Control for handling pog selection.
 * 
 * @author LLambert
 *
 */
public class PogSelection extends DockLayoutPanel {

	/**
	 * Tree of pogs.
	 */
	private Tree pogTree = new Tree();
	/**
	 * Player tree.
	 */
	private TreeItem playerTree = new TreeItem();
	/**
	 * Common Pogs.
	 */
	private TreeItem commonPogTree = new TreeItem();
	/**
	 * Common Monsters.
	 */
	private TreeItem commonMonsterTree = new TreeItem();
	/**
	 * Common Room Objects.
	 */
	private TreeItem commonObjectsTree = new TreeItem();
	/**
	 * Dungeon Level Pogs.
	 */
	private TreeItem dungeonLevelTree = new TreeItem();
	/**
	 * Dungeon Level Monsters.
	 */
	private TreeItem dungeonLevelMonsterTree = new TreeItem();
	/**
	 * Dungeon Level Room Objects.
	 */
	private TreeItem dungeonLevelObjectsTree = new TreeItem();
	/**
	 * Session Level Pogs.
	 */
	private TreeItem sessionLevelTree = new TreeItem();
	/**
	 * Session Level Monsters.
	 */
	private TreeItem sessionLevelMonsterTree = new TreeItem();
	/**
	 * Session Level Room Objects.
	 */
	private TreeItem sessionLevelObjectsTree = new TreeItem();
	/**
	 * Array of exp-andable tree items.
	 */
	private TreeItem[] expandableItems = {playerTree, commonMonsterTree, commonObjectsTree, dungeonLevelMonsterTree, dungeonLevelObjectsTree, sessionLevelMonsterTree, sessionLevelObjectsTree };
	/**
	 * Array of pog places vs expandables.
	 */
	private PogPlace[] pogPlaces = {PogPlace.SESSION_RESOURCE, PogPlace.COMMON_RESOURCE, PogPlace.COMMON_RESOURCE, PogPlace.DUNGEON_LEVEL, PogPlace.DUNGEON_LEVEL, PogPlace.SESSION_LEVEL, PogPlace.SESSION_LEVEL };
	/**
	 * Array of pog types matching expandables.
	 */
	private String[] pogTypes = {Constants.POG_TYPE_PLAYER, Constants.POG_TYPE_MONSTER, Constants.POG_TYPE_ROOMOBJECT, Constants.POG_TYPE_MONSTER, Constants.POG_TYPE_ROOMOBJECT, Constants.POG_TYPE_MONSTER, Constants.POG_TYPE_ROOMOBJECT };

	/**
	 * Constructor.
	 */
	public PogSelection() {
		super(Unit.PX);
		setSize("100%", "100%");
		createContent();
		setupEventHandling();
	}

	/**
	 * Setup event handling.
	 */
	private void setupEventHandling() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.DungeonDataLoaded) {
					dungeonDataLoaded();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.SessionDataChanged) {
					sessionDataChanged();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.SessionDataSaved) {
					sessionDataChanged();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.PogDataChanged) {
					pogDataChanged();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataReadyToJoin) {
					sessionDataChanged();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.PogWasSelected) {
					selectPog();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonSelectedLevelChanged) {
					newLevelSelected();
					return;
				}
			}
		});
		pogTree.addSelectionHandler(new SelectionHandler<TreeItem>() {
			@Override
			public void onSelection(final SelectionEvent<TreeItem> event) {
				selectionChanged(event.getSelectedItem());
			}
		});
		pogTree.addOpenHandler(new OpenHandler<TreeItem>() {
			@Override
			public void onOpen(final OpenEvent<TreeItem> event) {
				treeItemOpened(event.getTarget());
			}
		});
	}

	/**
	 * Create form content.
	 */
	private void createContent() {
		DockLayoutPanel northPanel = new DockLayoutPanel(Unit.PX);
		northPanel.setSize("100%", "100%");
		addBranches();
		ScrollPanel scrollPanel = new ScrollPanel(pogTree);
		scrollPanel.setWidth("95%"); // needed this to get full scroll bar to show
		add(scrollPanel);
	}

	/**
	 * Add branches to tree.
	 */
	private void addBranches() {
		setupTreeItem(playerTree, "Players");
		pogTree.addItem(playerTree);
		commonPogTree.setText("Common Resource Pogs");
		pogTree.addItem(commonPogTree);
		setupTreeItem(commonMonsterTree, "Monsters");
		commonPogTree.addItem(commonMonsterTree);
		setupTreeItem(commonObjectsTree, "Room Objects");
		commonPogTree.addItem(commonObjectsTree);
		dungeonLevelTree.setText("Dungeon Level Pogs");
		pogTree.addItem(dungeonLevelTree);
		setupTreeItem(dungeonLevelMonsterTree, "Monsters");
		dungeonLevelTree.addItem(dungeonLevelMonsterTree);
		setupTreeItem(dungeonLevelObjectsTree, "Room Objects");
		dungeonLevelTree.addItem(dungeonLevelObjectsTree);
		sessionLevelTree.setText("Session Level Pogs");
		pogTree.addItem(sessionLevelTree);
		setupTreeItem(sessionLevelMonsterTree, "Monsters");
		sessionLevelTree.addItem(sessionLevelMonsterTree);
		setupTreeItem(sessionLevelObjectsTree, "Room Objects");
		sessionLevelTree.addItem(sessionLevelObjectsTree);
	}

	/**
	 * set up with dummy node.
	 * 
	 * @param treeItem
	 * @param text
	 */
	private void setupTreeItem(final TreeItem treeItem, final String text) {
		treeItem.setText(text);
		treeItem.addItem(new TreeItem());
	}

	/**
	 * Dungeon data just loaded.
	 */
	private void dungeonDataLoaded() {
		boolean inEditMode = ServiceManager.getDungeonManager().isEditMode();
		fillCommonResourceTrees();
		fillDungeonLevelTrees();
		if (!inEditMode) {
			fillPlayerTree();
			fillSessionLevelTree();
		}
		playerTree.setVisible(!inEditMode);
		sessionLevelTree.setVisible(!inEditMode);
	}

	/**
	 * new level of dungeon selected.
	 */
	private void newLevelSelected() {
		fillDungeonLevelTrees();
		if (!ServiceManager.getDungeonManager().isEditMode()) {
			fillSessionLevelTree();
		}
	}

	/**
	 * Session data changed.
	 */
	private void sessionDataChanged() {
		fillSessionLevelTree();
		fillPlayerTree();
	}

	/**
	 * Pog data has changed.
	 */
	private void pogDataChanged() {
		dungeonDataLoaded();
	}

	/**
	 * Fill trees for common resources.
	 */
	private void fillCommonResourceTrees() {
		if (commonMonsterTree.getState()) {
			buildSortedTree(commonMonsterTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.COMMON_RESOURCE, Constants.POG_TYPE_MONSTER));
		}
		if (commonObjectsTree.getState()) {
			buildSortedTree(commonObjectsTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.COMMON_RESOURCE, Constants.POG_TYPE_ROOMOBJECT));
		}
	}

	/**
	 * Fill trees with level based pogs.
	 */
	private void fillDungeonLevelTrees() {
		if (dungeonLevelMonsterTree.getState()) {
			buildSortedTree(dungeonLevelMonsterTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.DUNGEON_LEVEL, Constants.POG_TYPE_MONSTER));
		}
		if (dungeonLevelObjectsTree.getState()) {
			buildSortedTree(dungeonLevelObjectsTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.DUNGEON_LEVEL, Constants.POG_TYPE_ROOMOBJECT));
		}
	}

	/**
	 * Fill tree with player pogs.
	 */
	private void fillPlayerTree() {
		if (playerTree.getState()) {
			buildSortedTree(playerTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.SESSION_RESOURCE, Constants.POG_TYPE_PLAYER));
		}
	}

	/**
	 * Fill tree with session level pogs.
	 */
	private void fillSessionLevelTree() {
		if (sessionLevelMonsterTree.getState()) {
			buildSortedTree(sessionLevelMonsterTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.SESSION_LEVEL, Constants.POG_TYPE_MONSTER));
		}
		if (sessionLevelObjectsTree.getState()) {
			buildSortedTree(sessionLevelObjectsTree, ServiceManager.getDungeonManager().getSortedList(PogPlace.SESSION_LEVEL, Constants.POG_TYPE_ROOMOBJECT));
		}
	}

	/**
	 * Add new tree item.
	 * 
	 * @param treeItem
	 * @param pog
	 */
	private void addTreeItem(final TreeItem treeItem, final PogData pog) {
		TreeItem newItem = new TreeItem();
		newItem.getElement().setClassName("my-TreeItem");
		newItem.setText(pog.getName());
		newItem.setUserObject(pog);
		treeItem.addItem(newItem);
		PogData selectedPog = ServiceManager.getDungeonManager().getSelectedPog();
		if (pog.isEqual(selectedPog)) {
			pogTree.setSelectedItem(newItem);
		}
		
	}

	/**
	 * sort and add these to tree.
	 * 
	 * @param treeItem
	 * @param pogs
	 */
	private void buildSortedTree(final TreeItem treeItem, final List<PogData> pogs) {
		if (pogs == null) {
			return;
		}
		treeItem.removeItems();
		for (PogData key : pogs) {
			addTreeItem(treeItem, key);
		}
	}

	/**
	 * handle tree item selected.
	 * 
	 * @param selectedItem
	 */
	private void selectionChanged(final TreeItem selectedItem) {
		PogData data = (PogData) selectedItem.getUserObject();
		if (data != null) {
			ServiceManager.getDungeonManager().setSelectedPog(data);
		}
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void onResize() {
		super.onResize();
	}

	/**
	 * tree item was opened.
	 * 
	 * @param target
	 */
	private void treeItemOpened(final TreeItem target) {
		if (target == null) {
			return;
		}
		int index = 0;
		for (TreeItem treeItem : expandableItems) {
			if (treeItem == target) {
				buildSortedTree(treeItem, ServiceManager.getDungeonManager().getSortedList(pogPlaces[index], pogTypes[index]));
				break;
			}
			++index;
		}
	}

	/**
	 * We just forced selection so don't want to loop.
	 */
	private boolean justDidSelection;

	/**
	 * Pog was selected.
	 */
	private void selectPog() {
		if (justDidSelection) {
			justDidSelection = false;
			return;
		}
		PogData selectedPog = ServiceManager.getDungeonManager().getSelectedPog();
		if (selectedPog == null) {
			return;
		}
		int index = 0;
		for (PogPlace place : pogPlaces) {
			if (place == selectedPog.getPogPlace()) {
				TreeItem parent = expandableItems[index];
				if (parent.isVisible() && parent.getState()) {
					for (int childIndex = 0; childIndex < parent.getChildCount(); ++childIndex) {
						TreeItem child = parent.getChild(childIndex);
						if (selectedPog.isEqual((PogData) child.getUserObject())) {
							justDidSelection = true;
							pogTree.setSelectedItem(child);
							return;
						}
					}
				}
			}
			++index;
		}
	}

}
