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

import com.google.gwt.core.client.JavaScriptObject;
import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.dom.client.Style.VerticalAlign;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.KeyUpEvent;
import com.google.gwt.event.dom.client.KeyUpHandler;
import com.google.gwt.event.dom.client.LoadEvent;
import com.google.gwt.event.dom.client.LoadHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.CheckBox;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.DoubleBox;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Image;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.LayoutPanel;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.VerticalPanel;

import per.lambert.ebattleMat.client.controls.dungeonSelectDialog.DungeonSelectDialog;
import per.lambert.ebattleMat.client.controls.labeledTextBox.LabeledTextBox;
import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.DungeonLevel;

/**
 * Panel for managing a dungeon Level.
 * 
 * @author LLambert
 *
 */
public class DungeonLevelEditorPanel extends DockLayoutPanel {
	/**
	 * button bar at top.
	 */
	private HorizontalPanel buttonBar = new HorizontalPanel();
	/**
	 * Dungeon selection dialog button.
	 */
	private Button manageDungeonsButton;
	/**
	 * Manage dungeon dialog.
	 */
	private DungeonSelectDialog manageDungeons;
	/**
	 * Create new level button.
	 */
	private Button createNewLevelButton;
	/**
	 * Create remove level button.
	 */
	private Button removeLevelButton;
	/**
	 * Panel to hold center content.
	 */
	private LayoutPanel centerContent;
	/**
	 * Grid for sub-classes to use for content.
	 */
	private Grid centerGrid;
	/**
	 * Show grid on dungeon levels.
	 */
	private CheckBox showGrid;
	/**
	 * grid size in pixels.
	 */
	private DoubleBox gridSize;
	/**
	 * Button to copy grid size.
	 */
	private Button gridSizeCopy;
	/**
	 * X Offset of grid from top Left.
	 */
	private LabeledTextBox gridOffsetX;
	/**
	 * Y Offset of grid from top Left.
	 */
	private LabeledTextBox gridOffsetY;
	/**
	 * Label for new level.
	 */
	private Label levelNameLabel;
	/**
	 * Name of new level.
	 */
	private TextBox levelName;
	/**
	 * Use to copy currently selected picture URL.
	 */
	private Button copyResourceURL;
	/**
	 * URL of level picture.
	 */
	private TextBox pictureURL;
	/**
	 * Save level information.
	 */
	private Button save;
	/**
	 * cancel Edits.
	 */
	private Button cancel;
	/**
	 * Current level we are working on.
	 */
	private DungeonLevel currentLevel;
	/**
	 * Form has changed.
	 */
	private boolean isDirty;
	/**
	 * New level needs to be created.
	 */
	private boolean newLevel;
	/**
	 * Image of level.
	 */
	private Image image = new Image();
	/**
	 * parent panel width.
	 */
	private int parentWidth;
	/**
	 * parent panel height.
	 */
	private int parentHeight;
	/**
	 * Image width.
	 */
	private int imageWidth;
	/**
	 * image height.
	 */
	private int imageHeight;
	/**
	 * Image loaded.
	 */
	private boolean imageLoaded;

	/**
	 * Constructor.
	 */
	public DungeonLevelEditorPanel() {
		super(Unit.PX);
		createContent();
		setupEventHandling();
	}

	/**
	 * Create content.
	 */
	private void createContent() {
		manageDungeonsButton = new Button("Manage Dungeons");
		manageDungeonsButton.addStyleName("ribbonBarLabel");
		manageDungeonsButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				if (manageDungeons == null) {
					manageDungeons = new DungeonSelectDialog();
				}
				manageDungeons.enableCancel(true);
				manageDungeons.show();
			}
		});
		buttonBar.add(manageDungeonsButton);

		createNewLevelButton = new Button("New Level");
		createNewLevelButton.addStyleName("ribbonBarLabel");
		createNewLevelButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				handleCreateNewLevel();
			}
		});
		buttonBar.add(createNewLevelButton);

		removeLevelButton = new Button("DELETE Level");
		removeLevelButton.addStyleName("ribbonBarLabel");
		removeLevelButton.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				handleRemoveLevel();
			}
		});
		buttonBar.add(removeLevelButton);

		addNorth(buttonBar, 30);
		createLevelEditor();
		add(centerContent);
		this.forceLayout();
	}

	/**
	 * Create level editor.
	 */
	private void createLevelEditor() {
		centerContent = new LayoutPanel();
		centerContent.setHeight("100%");
		centerContent.setWidth("100%");
		centerGrid = new Grid();
		centerGrid.setWidth("100%");
		centerGrid.resize(8, 2);
		centerGrid.getColumnFormatter().setWidth(0, "100px");
		VerticalPanel vpanel = new VerticalPanel();
		vpanel.add(centerGrid);
		vpanel.add(image);
		centerContent.add(vpanel);
		createShowGrid();
		createGridSizeEntry();
		createGridOffsetX();
		createGridOffsetY();
		createLevelName();
		createLevelPictureURL();
		createSaveAndCancelButtons();
	}

	/**
	 * Create show grid content.
	 */
	private void createShowGrid() {
		showGrid = new CheckBox("Show Grid ");
		showGrid.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		showGrid.setStyleName("ribbonBarLabel");
		showGrid.getElement().getStyle().setVerticalAlign(VerticalAlign.MIDDLE);
		centerGrid.setWidget(1, 0, showGrid);
	}

	/**
	 * Create grid size content.
	 */
	private void createGridSizeEntry() {
		gridSize = new DoubleBox();
		gridSize.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		gridSize.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		gridSize.setStyleName("ribbonBarLabel");

		gridSizeCopy = new Button("Grid Size");
		gridSizeCopy.setTitle("Use CTL click on map to draw rectange. A size will be computed. Click Button to copy to grid size");
		gridSizeCopy.setStyleName("ribbonBarLabel");
		gridSizeCopy.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				copyGridSize();
			}
		});
		centerGrid.setWidget(2, 0, gridSizeCopy);
		centerGrid.setWidget(2, 1, gridSize);
	}

	/**
	 * Copy grid size into editor.
	 * 
	 * Size can be calculated by ctl click on map and drawing a rectangle the size of a grid square.
	 */
	private void copyGridSize() {
		gridSize.setValue(ServiceManager.getDungeonManager().getComputedGridWidth());
		isDirty = true;
		validateContent();
	}

	/**
	 * Create X grid offset content.
	 */
	private void createGridOffsetX() {
		gridOffsetX = new LabeledTextBox("Offset X", 0.0);
		gridOffsetX.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		gridOffsetX.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		gridOffsetX.setStyleName("ribbonBarLabel");
		gridOffsetX.setEntryWidth("30px");
		centerGrid.setWidget(3, 0, gridOffsetX);
	}

	/**
	 * Create Y grid offset content.
	 */
	private void createGridOffsetY() {
		gridOffsetY = new LabeledTextBox("Offset Y", 0.0);
		gridOffsetY.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		gridOffsetY.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				isDirty = true;
				validateContent();
			}
		});
		gridOffsetY.setStyleName("ribbonBarLabel");
		gridOffsetY.setEntryWidth("30px");
		centerGrid.setWidget(3, 1, gridOffsetY);
	}

	/**
	 * Create level name content.
	 */
	private void createLevelName() {
		levelNameLabel = new Label("Level Name");
		levelNameLabel.setStyleName("ribbonBarLabel");
		levelName = new TextBox();
		levelName.setWidth("100%");
		levelName.addValueChangeHandler(new ValueChangeHandler<String>() {
			@Override
			public void onValueChange(final ValueChangeEvent<String> event) {
				isDirty = true;
				validateContent();
			}
		});
		levelName.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				isDirty = true;
				validateContent();
			}
		});

		levelName.setStyleName("ribbonBarLabel");
		centerGrid.setWidget(0, 0, levelNameLabel);
		centerGrid.setWidget(0, 1, levelName);
	}

	/**
	 * Create picture url content.
	 */
	private void createLevelPictureURL() {
		copyResourceURL = new Button("Use Select picture resource");
		copyResourceURL.setStyleName("ribbonBarLabel");
		copyResourceURL.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				copyResourceURL();
				urlChanged();
			}
		});
		pictureURL = new TextBox();
		pictureURL.addChangeHandler(new ChangeHandler() {
			@Override
			public void onChange(final ChangeEvent event) {
				urlChanged();
			}
		});
		pictureURL.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				urlChanged();
			}
		});
		pictureURL.setWidth("100%");
		centerGrid.setWidget(4, 0, copyResourceURL);
		centerGrid.setWidget(4, 1, pictureURL);
	}

	/**
	 * Handle url changed.
	 */
	private void urlChanged() {
		isDirty = true;
		validateContent();
		pictureURL.setTitle(pictureURL.getText());
	}

	/**
	 * Create save and cancel buttons.
	 */
	private void createSaveAndCancelButtons() {
		save = new Button("Save");
		save.setStyleName("ribbonBarLabel");
		save.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				saveFormData();
			}
		});
		cancel = new Button("Cancel");
		cancel.setStyleName("ribbonBarLabel");
		cancel.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				cancelFormData();
			}
		});
		centerGrid.setWidget(6, 0, save);
		centerGrid.setWidget(6, 1, cancel);
	}

	/**
	 * Initialize view.
	 * 
	 * Must be run before reusing the view.
	 */
	private void initialize() {
		newLevel = false;
		gridSize.setValue(30.0);
		gridOffsetX.setValue(0.0);
		gridOffsetY.setValue(0.0);
		levelName.setValue("New Level");
		pictureURL.setValue("");
		validateContent();
	}

	/**
	 * save button was clicked so save changes.
	 */
	private void saveFormData() {
		DungeonLevel levelData = ServiceManager.getDungeonManager().getCurrentDungeonLevelData();
		if (levelData == null) {
			return;
		}
		int nextAvailableLevelIndex = ServiceManager.getDungeonManager().getNextAvailableLevelNumber();
		ServiceManager.getDungeonManager().setIsDungeonGridVisible(showGrid.getValue());
		currentLevel.setGridSize(gridSize.getValue());
		currentLevel.setGridOffsetX(gridOffsetX.getDoubleValue());
		currentLevel.setGridOffsetY(gridOffsetY.getDoubleValue());
		currentLevel.setLevelName(levelName.getValue());
		currentLevel.setLevelDrawing(pictureURL.getText());
		if (newLevel) {
			ServiceManager.getDungeonManager().addNewLevel(currentLevel);
		}
		ServiceManager.getDungeonManager().saveDungeonData();
		if (newLevel) {
			ServiceManager.getDungeonManager().setCurrentLevel(nextAvailableLevelIndex);
		}
		newLevel = false;
		isDirty = false;
		validateContent();
	}

	/**
	 * Changes were canceled.
	 */
	private void cancelFormData() {
		gatherData();
	}

	/**
	 * copy selected picture url.
	 */
	private void copyResourceURL() {
		String url = ServiceManager.getDungeonManager().getAssetURL();
		if (ServiceManager.getDungeonManager().isValidPictureURL(url)) {
			pictureURL.setText(url);
		}
	}

	/**
	 * setup event handling.
	 */
	private void setupEventHandling() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.DungeonDataLoaded) {
					gatherData();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonSelectedLevelChanged) {
					gatherData();
					return;
				}
			}
		});
		image.addLoadHandler(new LoadHandler() {
			public void onLoad(final LoadEvent event) {
				imageLoaded();
			}
		});
	}

	/**
	 * Gather data.
	 */
	private void gatherData() {
		currentLevel = ServiceManager.getDungeonManager().getCurrentDungeonLevelData();
		if (currentLevel == null) {
			return;
		}
		addLevelDataToForm();
		validateContent();
		ResizableDialog.enableWidget(save, false);
		ResizableDialog.enableWidget(cancel, false);
		isDirty = false;
	}

	/**
	 * Add level to form.
	 */
	private void addLevelDataToForm() {
		showGrid.setValue(ServiceManager.getDungeonManager().isDungeonGridVisible());
		gridSize.setValue(currentLevel.getGridSize());
		gridOffsetX.setValue(currentLevel.getGridOffsetX());
		gridOffsetY.setValue(currentLevel.getGridOffsetY());
		levelName.setValue(currentLevel.getLevelName());
		pictureURL.setText(currentLevel.getLevelDrawing());
		pictureURL.setTitle(currentLevel.getLevelDrawing());
	}

	/**
	 * Validate content.
	 */
	private void validateContent() {
		boolean isOK = true;
		double numberCheck = 0;
		if (!ServiceManager.getDungeonManager().isLegalDungeonName(levelName.getValue())) {
			isOK = false;
			levelNameLabel.addStyleName("badLabel");
		} else {
			levelNameLabel.removeStyleName("badLabel");
		}
		if (!ServiceManager.getDungeonManager().isValidPictureURL(pictureURL.getText())) {
			isOK = false;
			pictureURL.addStyleName("badLabel");
		} else {
			pictureURL.removeStyleName("badLabel");
			drawPicture();
		}
		try {
			numberCheck = gridSize.getValue();
			if (numberCheck < 4) {
				isOK = false;
				gridSize.addStyleName("badLabel");
			} else {
				gridSize.removeStyleName("badLabel");
			}
		} catch (Exception ex) {
			isOK = false;
			gridSize.addStyleName("badLabel");
		}
		try {
			numberCheck = gridOffsetX.getDoubleValue();
			gridOffsetX.removeStyleName("badLabel");
		} catch (Exception ex) {
			isOK = false;
			gridOffsetX.addStyleName("badLabel");
		}
		try {
			numberCheck = gridOffsetY.getDoubleValue();
			gridOffsetY.removeStyleName("badLabel");
		} catch (Exception ex) {
			isOK = false;
			gridOffsetY.addStyleName("badLabel");
		}
		ResizableDialog.enableWidget(save, isOK && isDirty);
		ResizableDialog.enableWidget(cancel, isDirty);
	}

	private void drawPicture() {
		imageLoaded = false;
		String url = pictureURL.getText();
		image.setUrl(ServiceManager.getDungeonManager().getUrlToDungeonResource(url));
	}

	/**
	 * create a new level in this dungeon.
	 */
	private void handleCreateNewLevel() {
		initialize();
		currentLevel = (DungeonLevel) JavaScriptObject.createObject().cast();
		addLevelDataToForm();
		newLevel = true;
		validateContent();
	}

	/**
	 * handle removing current level.
	 */
	private void handleRemoveLevel() {
		ServiceManager.getDungeonManager().removeCurrentLevel();
		ServiceManager.getDungeonManager().saveDungeonData();
		ServiceManager.getDungeonManager().setCurrentLevel(0);
	}

	/**
	 * 
	 * {@inheritDoc}
	 */
	@Override
	public void onResize() {
		super.onResize();
		if (imageLoaded) {
			imageLoaded();
		}
	}

	private void imageLoaded() {
		imageLoaded = true;
		parentWidth = getOffsetWidth();
		parentHeight = getOffsetHeight();
		imageWidth = image.getWidth();
		imageHeight = image.getHeight();
		double totalZoom;
		if (isScaleByWidth()) {
			totalZoom = (double) parentWidth / (double) imageWidth;
		} else {
			totalZoom = (double) parentHeight / (double) imageHeight;
		}
		if (!Double.isNaN(totalZoom) && totalZoom != 0.0) {
			image.setPixelSize((int) (imageWidth * totalZoom), (int) (imageHeight * totalZoom));
		}
	}

	/**
	 * Should we scale by width.
	 * 
	 * @return true if we should scale by width
	 */
	private boolean isScaleByWidth() {
		double scaleWidth = (double) parentWidth / (double) imageWidth;
		double scaleHeight = (double) parentHeight / (double) imageHeight;
		return scaleWidth < scaleHeight;
	}
}
