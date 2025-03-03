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

import java.util.HashMap;
import java.util.Map;

import com.google.gwt.dom.client.Element;
import com.google.gwt.dom.client.InputElement;
import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.FileUpload;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitEvent;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.ScrollPanel;
import com.google.gwt.user.client.ui.Tree;
import com.google.gwt.user.client.ui.TreeItem;
import com.google.gwt.user.client.ui.VerticalPanel;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.IDataRequester;
import per.lambert.ebattleMat.client.interfaces.IErrorInformation;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.IUserCallback;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.FileList;

/**
 * Panel for handle all art assest in dungeon.
 * 
 * @author llambert
 *
 */
public class ArtAssetsPanel extends DockLayoutPanel {
	/**
	 * button bar at top.
	 */
	private HorizontalPanel buttonBar = new HorizontalPanel();
	/**
	 * Add image to dungeon.
	 */
	private Button uploadAsset = new Button("Upload Asset");
	/**
	 * Art assets.
	 */
	private Button downloadAssetsButton = new Button("Download Asset");
	/**
	 * Art assets.
	 */
	private Button deleteAssetsButton = new Button("Delete Asset");
	/**
	 * Form panel for uploading files.
	 */
	private FormPanel formPanel = new FormPanel();
	/**
	 * Up load widget.
	 */
	private FileUpload fileUpload = new FileUpload();
	/**
	 * Tree of files.
	 */
	private Tree fileTree = new Tree();
	/**
	 * Dungeon asset tree.
	 */
	private TreeItem dungeonAssets = new TreeItem();
	/**
	 * Monster asset tree.
	 */
	private TreeItem monsterAssets = new TreeItem();
	/**
	 * Room asset tree.
	 */
	private TreeItem roomAssets = new TreeItem();
	/**
	 * Label for url.
	 */
	private Label urlLabel = new Label();

	/**
	 * Constructor.
	 */
	public ArtAssetsPanel() {
		super(Unit.PX);
		setSize("100%", "100%");
		createContent();
		setupEventHandling();
	}

	/**
	 * setup event handling.
	 */
	private void setupEventHandling() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.DungeonDataLoaded) {
					loadFiles();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.SessionDataSaved) {
					loadFiles();
					return;
				}
			}
		});
		fileTree.addSelectionHandler(new SelectionHandler<TreeItem>() {
			@Override
			public void onSelection(final SelectionEvent<TreeItem> event) {
				handleItemSelected(event.getSelectedItem());
			}

		});
	}

	/**
	 * create content.
	 */
	private void createContent() {
		downloadAssetsButton.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				downloadAsset();
			}
		});
		downloadAssetsButton.setEnabled(false);
		buttonBar.add(downloadAssetsButton);
		deleteAssetsButton.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				deletAsset();
			}
		});
		deleteAssetsButton.setEnabled(false);
		buttonBar.add(deleteAssetsButton);

		uploadAsset.setEnabled(false);
		buttonBar.add(uploadAsset);
		setupForFileUpload();
		buttonBar.add(formPanel);
		DockLayoutPanel northPanel = new DockLayoutPanel(Unit.PX);
		northPanel.setSize("100%", "100%");
		northPanel.addNorth(buttonBar, 30);
		northPanel.add(urlLabel);
		addNorth(northPanel, 60);
		fileTree.clear();
		dungeonAssets.setText("Dungeon Assets");
		monsterAssets.setText("Global Monster Assets");
		roomAssets.setText("Global Room Assets");
		fileTree.addItem(dungeonAssets);
		fileTree.addItem(monsterAssets);
		fileTree.addItem(roomAssets);
		ScrollPanel scrollPanel = new ScrollPanel(fileTree);
		scrollPanel.setWidth("95%");
		add(scrollPanel);
		setStyles();
	}

	/**
	 * Set styles.
	 */
	private void setStyles() {
		urlLabel.setStyleName("ribbonBarLabel");
		uploadAsset.setStyleName("ribbonBarLabel");
		downloadAssetsButton.setStyleName("ribbonBarLabel");
		deleteAssetsButton.setStyleName("ribbonBarLabel");
		fileUpload.setStyleName("ribbonBarLabel");
	}

	/**
	 * Setup for file uploading.
	 */
	private void setupForFileUpload() {
		VerticalPanel panel = new VerticalPanel();
		formPanel.setWidget(panel);
		fileUpload.setName("uploadElement");
		panel.add(fileUpload);
		fileUpload.setEnabled(false);
		uploadAsset.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				uploadFile();
				uploadAsset.setEnabled(false);
				fileUpload.setEnabled(false);
			}
		});
		formPanel.addSubmitHandler(new FormPanel.SubmitHandler() {
			public void onSubmit(final SubmitEvent event) {
				if (fileUpload.getFilename().length() == 0) {
					event.cancel();
				}
			}
		});
		formPanel.addSubmitCompleteHandler(new FormPanel.SubmitCompleteHandler() {
			public void onSubmitComplete(final SubmitCompleteEvent event) {
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataLoaded, null));
				setInputValue("");
			}
		});
		fileUpload.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				if (fileTree.getSelectedItem() != null) {
					uploadAsset.setEnabled(true);
				}
			}
		});
	}

	/**
	 * Load in files.
	 */
	private void loadFiles() {
		disableButtons();
		ServiceManager.getDungeonManager().getFileList(ServiceManager.getDungeonManager().getDirectoryForCurrentDungeon(), new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				buildTreeOfAssets((FileList) data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}
		});
		ServiceManager.getDungeonManager().getFileList("/" + Constants.DUNGEON_DATA_LOCATION + Constants.DUNGEON_MONSTER_LOCATION, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				buildTreeOfAssets((FileList) data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}
		});
		ServiceManager.getDungeonManager().getFileList("/" + Constants.DUNGEON_DATA_LOCATION + Constants.DUNGEON_ROOMOBJECT_LOCATION, new IUserCallback() {
			@Override
			public void onSuccess(final Object sender, final Object data) {
				buildTreeOfAssets((FileList) data);
			}

			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}
		});
	}

	/**
	 * Build tree of assets.
	 * 
	 * @param data file list
	 */
	private void buildTreeOfAssets(final FileList data) {
		TreeItem itemToPopulate;
		if (data.getFilePath().contains("dungeons")) {
			itemToPopulate = dungeonAssets;
		} else if (data.getFilePath().contains("monsters")) {
			itemToPopulate = monsterAssets;
		} else {
			itemToPopulate = roomAssets;
		}
		itemToPopulate.removeItems();
		itemToPopulate.setUserObject(data.getFilePath());
		for (String filename : data.getFileNames()) {
			TreeItem asset = new TreeItem();
			asset.setText(filename);
			asset.setUserObject(filename);
			itemToPopulate.addItem(asset);
		}
	}

	/**
	 * Tree item selected.
	 * 
	 * @param selectedItem selected item
	 */
	private void handleItemSelected(final TreeItem selectedItem) {
		disableButtons();
		String data = (String) selectedItem.getUserObject();
		if (data == null) {
			return;
		}
		if (data.startsWith("/")) {
			fileUpload.setEnabled(true);
			return;
		}
		if (data.endsWith(".json")) {
			downloadAssetsButton.setEnabled(true);
			fileUpload.setEnabled(true);
			return;
		}
		deleteAssetsButton.setEnabled(true);
		downloadAssetsButton.setEnabled(true);
		fileUpload.setEnabled(true);
		String txt = buildUrlToFilename(data);
		urlLabel.setText(txt);
		ServiceManager.getDungeonManager().setAssetURL(txt);
	}

	/**
	 * enable or disable appropriate buttons.
	 */
	private void disableButtons() {
		deleteAssetsButton.setEnabled(false);
		downloadAssetsButton.setEnabled(false);
		fileUpload.setEnabled(false);
	}

	/**
	 * Up load file.
	 * 
	 * Much of this belongs in model but forced to be here because need form to do the work.
	 * 
	 */
	private void uploadFile() {
		String serverPath = getUrlToFileOnserver();
		if (serverPath == null) {
			return;
		}
		Map<String, String> parameters = new HashMap<String, String>();
		parameters.put("filePath", serverPath);
		IDataRequester dataRequester = ServiceManager.getDataRequester();
		String url = dataRequester.buildUrl("FILEUPLOAD", parameters);
		formPanel.setAction(url);
		formPanel.setEncoding(FormPanel.ENCODING_MULTIPART);
		formPanel.setMethod(FormPanel.METHOD_POST);
		formPanel.submit();
	}

	/**
	 * get url to file.
	 * 
	 * @return url or null
	 */
	private String getUrlToFileOnserver() {
		String filename = fileUpload.getFilename();
		if (filename == null || filename.isEmpty()) {
			return (null);
		}
		return buildUrlToFilename(filename);
	}

	/**
	 * Build url for filename.
	 * 
	 * This assumes parent node has path to file
	 * 
	 * @param filename
	 * @return url or null
	 */
	private String buildUrlToFilename(final String filename) {
		TreeItem selected = fileTree.getSelectedItem();
		if (selected == null) {
			return (null);
		}
		if (!((String) selected.getUserObject()).contains("/")) {
			selected = selected.getParentItem();
		}
		int i = filename.lastIndexOf("/");
		if (i == -1) {
			i = filename.lastIndexOf("\\");
		}
		String rtnName = filename;
		if (i != -1 && (i + 1) < filename.length()) {
			rtnName = filename.substring(i + 1);
		}
		String base = (String) selected.getUserObject();
		if (!base.endsWith("/") && !base.endsWith("\\")) {
			base = base + "/";
		}
		String url = base + rtnName;
		return (url);
	}

	/**
	 * Set value of input control.
	 * 
	 * @param value to set
	 */
	public void setInputValue(final String value) {
		Element ele = fileUpload.getElement();
		InputElement inp = InputElement.as(ele);
		inp.setValue(value);
	}

	/**
	 * down load a file.
	 */
	private void downloadAsset() {
		String filename = (String) fileTree.getSelectedItem().getUserObject();
		String folder = (String) fileTree.getSelectedItem().getParentItem().getUserObject();
		ServiceManager.getDungeonManager().downloadFile(folder, filename);
	}

	/**
	 * down load a file.
	 */
	private void deletAsset() {
		TreeItem selected = fileTree.getSelectedItem();
		String url = buildUrlToFilename((String) selected.getUserObject());
		ServiceManager.getDungeonManager().deleteFile(url, new IUserCallback() {
			@Override
			public void onError(final Object sender, final IErrorInformation error) {
			}

			@Override
			public void onSuccess(final Object sender, final Object data) {
				ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.DungeonDataLoaded, null));
			}
		});
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void onResize() {
		super.onResize();
	}
}
