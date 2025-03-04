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
package per.lambert.ebattleMat.client.battleMatDisplay;

import java.util.ArrayList;

import com.google.gwt.canvas.client.Canvas;
import com.google.gwt.canvas.dom.client.Context2d;
import com.google.gwt.canvas.dom.client.CssColor;
import com.google.gwt.dom.client.Element;
import com.google.gwt.dom.client.ImageElement;
import com.google.gwt.dom.client.Style.BorderStyle;
import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.event.dom.client.ContextMenuEvent;
import com.google.gwt.event.dom.client.ContextMenuHandler;
import com.google.gwt.event.dom.client.DoubleClickEvent;
import com.google.gwt.event.dom.client.DoubleClickHandler;
import com.google.gwt.event.dom.client.DragLeaveEvent;
import com.google.gwt.event.dom.client.DragLeaveHandler;
import com.google.gwt.event.dom.client.DragOverEvent;
import com.google.gwt.event.dom.client.DragOverHandler;
import com.google.gwt.event.dom.client.DropEvent;
import com.google.gwt.event.dom.client.DropHandler;
import com.google.gwt.event.dom.client.LoadEvent;
import com.google.gwt.event.dom.client.LoadHandler;
import com.google.gwt.event.dom.client.MouseDownEvent;
import com.google.gwt.event.dom.client.MouseDownHandler;
import com.google.gwt.event.dom.client.MouseMoveEvent;
import com.google.gwt.event.dom.client.MouseMoveHandler;
import com.google.gwt.event.dom.client.MouseUpEvent;
import com.google.gwt.event.dom.client.MouseUpHandler;
import com.google.gwt.event.dom.client.MouseWheelEvent;
import com.google.gwt.event.dom.client.MouseWheelHandler;
import com.google.gwt.user.client.DOM;
import com.google.gwt.user.client.ui.AbsolutePanel;
import com.google.gwt.user.client.ui.Image;
import com.google.gwt.user.client.ui.LayoutPanel;
import com.google.gwt.user.client.ui.RootLayoutPanel;
import com.google.gwt.user.client.ui.RootPanel;

import per.lambert.ebattleMat.client.controls.PogPopupMenu;
import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.DungeonMasterFlag;
import per.lambert.ebattleMat.client.interfaces.IDungeonManager;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.PogPlace;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.interfaces.RectangleData;
import per.lambert.ebattleMat.client.interfaces.VersionedItem;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.DataVersions;
import per.lambert.ebattleMat.client.services.serviceData.DungeonLevel;
import per.lambert.ebattleMat.client.services.serviceData.PogData;
import per.lambert.ebattleMat.client.touchHelper.DoubleTapEvent;
import per.lambert.ebattleMat.client.touchHelper.DoubleTapHandler;
import per.lambert.ebattleMat.client.touchHelper.PanEndEvent;
import per.lambert.ebattleMat.client.touchHelper.PanEndHandler;
import per.lambert.ebattleMat.client.touchHelper.PanEvent;
import per.lambert.ebattleMat.client.touchHelper.PanHandler;
import per.lambert.ebattleMat.client.touchHelper.PanStartEvent;
import per.lambert.ebattleMat.client.touchHelper.PanStartHandler;
import per.lambert.ebattleMat.client.touchHelper.TouchHelper;
import per.lambert.ebattleMat.client.touchHelper.TouchInformation;
import per.lambert.ebattleMat.client.touchHelper.ZoomEndEvent;
import per.lambert.ebattleMat.client.touchHelper.ZoomEndHandler;
import per.lambert.ebattleMat.client.touchHelper.ZoomEvent;
import per.lambert.ebattleMat.client.touchHelper.ZoomHandler;
import per.lambert.ebattleMat.client.touchHelper.ZoomStartEvent;
import per.lambert.ebattleMat.client.touchHelper.ZoomStartHandler;

/**
 * @author LLambert
 * 
 *         Class to manage a scaled image with overlays.
 * 
 *         This support panning and zooming all images.
 */
public class BattleMatCanvas extends AbsolutePanel implements MouseWheelHandler, MouseDownHandler, MouseMoveHandler, MouseUpHandler {
	/**
	 * Offset for clearing rectangle.
	 */
	private static final int CLEAR_OFFEST = -10;
	/**
	 * Default zoom constant.
	 */
	private static final double DEFAULT_ZOOM = 1.1;
	/**
	 * Maximum zoom factor.
	 */
	private static final double MAX_ZOOM = .2;
	/**
	 * Show grid.
	 */
	private boolean showGrid = false;
	/**
	 * Adjusted grid spacing so the grid lines matches exactly to one that might already be in a picture.
	 */
	private double gridSpacing = 50;
	/**
	 * Main canvas that is drawn.
	 */
	private Canvas canvas = Canvas.createIfSupported();
	/**
	 * background canvas for temporary drawing and then scaled and drawn on the main canvas.
	 */
	private Canvas backCanvas = Canvas.createIfSupported();
	/**
	 * Fog of war canvas.
	 */
	private Canvas fowCanvas = Canvas.createIfSupported();
	/**
	 * Fog of war canvas.
	 */
	private Canvas fowBackCanvas = Canvas.createIfSupported();
	/**
	 * line style grey.
	 */
	private final CssColor gridColor = CssColor.make("grey");
	/**
	 * Fog of war color.
	 */
	private final String fogOfWarColor = "black";
	/**
	 * Width of actual image.
	 */
	private int imageWidth = 0;
	/**
	 * Height of actual image.
	 */
	private int imageHeight = 0;
	/**
	 * Width of parent window.
	 */
	private int parentWidth = 0;
	/**
	 * Height of parent window.
	 */
	private int parentHeight = 0;
	/**
	 * image element for drawing.
	 */
	private ImageElement imageElement;
	/**
	 * current zoom factor for image.
	 */
	private double totalZoom = 1;
	/**
	 * Offset of image in the horizontal direction. Used for panning the image.
	 */
	private double offsetX = 0;
	/**
	 * Offset of image in the vertical direction. Used for panning the image.
	 */
	private double offsetY = 0;
	/**
	 * grid origin offset X. Used to align the overlay grid with a grid that maybe in picture.
	 */
	private double gridOffsetX = 0;
	/**
	 * grid origin offset Y. Used to align the overlay grid with a grid that maybe in picture.
	 */
	private double gridOffsetY = 0;
	/**
	 * Used by pan images.
	 */
	private boolean mouseDown = false;
	/**
	 * X position of mouse down.
	 */
	private double mouseDownXPos = 0;
	/**
	 * Y position of mouse down.
	 */
	private double mouseDownYPos = 0;
	/**
	 * Number of horizontal lines needed in the grid.
	 */
	private int horizontalLines = 0;
	/**
	 * Number of vertical lines needed in the grid.
	 */
	private int verticalLines = 0;
	/**
	 * column current drag operation is in.
	 */
	private int dragColumn = -1;
	/**
	 * row current drag operation is in.
	 */
	private int dragRow = -1;
	/**
	 * Image for main canvas.
	 */
	private Image image = new Image();
	/**
	 * panel to managing the greyed out area when pog is being dragged.
	 */
	private LayoutPanel greyOutPanel;
	/**
	 * Hidden panel to handle loading the image.
	 */
	private LayoutPanel hidePanel;
	/**
	 * List of pog canvases currently on level.
	 */
	private ArrayList<PogCanvas> monsterPogs = new ArrayList<PogCanvas>();
	/**
	 * List of pog canvases currently on level.
	 */
	private ArrayList<PogCanvas> roomObjectPogs = new ArrayList<PogCanvas>();
	/**
	 * List of pog canvases currently on level.
	 */
	private ArrayList<PogCanvas> playerPogs = new ArrayList<PogCanvas>();
	/**
	 * Toggle fog of war.
	 */
	private boolean toggleFOW;
	/**
	 * true if clearing fog or war.
	 */
	private boolean clearFOW;
	/**
	 * Selected column.
	 */
	private int selectedColumn;
	/**
	 * Selected row.
	 */
	private int selectedRow;
	/**
	 * Currently selected pog canvas.
	 */
	private PogCanvas selectedPogCanvas;
	/**
	 * Width of pog border.
	 */
	private double pogBorderWidth = 100;
	/**
	 * Helper for mobile touches.
	 */
	private TouchHelper touchHelper;
	/**
	 * Distance between fingers.
	 */
	private double distanceBetweenFingers;
	/**
	 * popup menu.
	 */
	private PogPopupMenu popup;
	/**
	 * are we selecting cells.
	 */
	private boolean doingSelection;
	/**
	 * Selection coordinates.
	 */
	private RectangleData selectionCoodinates = new RectangleData();
	/**
	 * Are we currently panning.
	 */
	private boolean isPanning;
	/**
	 * History of data versions.
	 */
	private DataVersions dataVersionsHistory = new DataVersions();
	/**
	 * Current dungeon UUID.
	 */
	private String currentDungeonID;
	/**
	 * Current session UUID.
	 */
	private String currentSessionID;
	/**
	 * Current dungeon or session level.
	 */
	private int currentLevel;
	/**
	 * Has image been loaded.
	 */
	private boolean imageLoaded;
	/**
	 * Currently loaded dungeon picture.
	 */
	private String dungeonPicture;

	/**
	 * Widget for managing all battle mat activities.
	 */
	public BattleMatCanvas() {
		showGrid = false;
		createContainers();
		createContextMenu();
		setupEventHandling();
	}

	/**
	 * Create main containers of view.
	 */
	private void createContainers() {
		hidePanel = new LayoutPanel();
		hidePanel.add(image);
		hidePanel.setVisible(false);
		greyOutPanel = new LayoutPanel();
		greyOutPanel.getElement().getStyle().setZIndex(Constants.GREYOUT_Z);
		fowCanvas.getElement().getStyle().setZIndex(Constants.FOW_Z);
		fowCanvas.setStyleName("noEvents");
		fowBackCanvas.setStyleName("noEvents");
		touchHelper = new TouchHelper(canvas);
	}

	/**
	 * Create pop up menu for when the DM right clicks on battle mat.
	 */
	private void createContextMenu() {
		popup = new PogPopupMenu();
		popup.getElement().getStyle().setZIndex(Constants.POPUPMENU_Z);
	}

	/**
	 * Setup event handlers.
	 */
	private void setupEventHandling() {
		setupDragAndDropEventHandlers();
		canvas.addMouseWheelHandler(this);
		canvas.addMouseMoveHandler(this);
		canvas.addMouseDownHandler(this);
		canvas.addMouseUpHandler(this);
		setupEventManagerHandling();
		addTouchHandlerEvents();
		handleContextMenuEvents();

		// handle when main image is loaded
		image.addLoadHandler(new LoadHandler() {
			public void onLoad(final LoadEvent event) {
				setImage();
				checkForDataChanges();
			}
		});
	}

	/**
	 * Setup drag and drop.
	 */
	private void setupDragAndDropEventHandlers() {
		this.addDomHandler(new DragOverHandler() {
			@Override
			public void onDragOver(final DragOverEvent event) {
				highlightGridSquare(event.getNativeEvent().getClientX(), event.getNativeEvent().getClientY());
			}
		}, DragOverEvent.getType());
		this.addDomHandler(new DropHandler() {
			@Override
			public void onDrop(final DropEvent event) {
				event.preventDefault();
				dropPog(event);
				ServiceManager.getDungeonManager().setPogBeingDragged(null, false);
			}
		}, DropEvent.getType());
		this.addDomHandler(new DragLeaveHandler() {
			@Override
			public void onDragLeave(final DragLeaveEvent event) {
			}
		}, DragLeaveEvent.getType());
	}

	/**
	 * Handle context menu events. We want to disable native context menu since we do our own.
	 */
	private void handleContextMenuEvents() {
		RootLayoutPanel.get().addDomHandler(new ContextMenuHandler() {
			@Override
			public void onContextMenu(final ContextMenuEvent event) {
				event.preventDefault();
				event.stopPropagation();
			}
		}, ContextMenuEvent.getType());
		RootPanel.get().addDomHandler(new ContextMenuHandler() {
			@Override
			public void onContextMenu(final ContextMenuEvent event) {
				event.preventDefault();
				event.stopPropagation();
			}
		}, ContextMenuEvent.getType());
	}

	/**
	 * Handle event manager events.
	 */
	private void setupEventManagerHandling() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.MouseDownEventBubble) {
					onMouseDown((MouseDownEvent) event.getData());
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.MouseUpEventBubble) {
					onMouseUp((MouseUpEvent) event.getData());
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.MouseMoveEventBubble) {
					onMouseMove((MouseMoveEvent) event.getData());
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.PogWasSelected) {
					newSelectedPog();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.PogDataChanged) {
					checkForDataChanges();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataReadyToEdit) {
					checkForDataChanges();
					return;
				} else if (event.getReasonForAction() == ReasonForAction.DungeonDataReadyToJoin) {
					checkForDataChanges();
					return;
				} else if (event.getReasonForAction() == ReasonForAction.SessionDataChanged) {
					checkForDataChanges();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonSelectedLevelChanged) {
					checkForDataChanges();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataSaved) {
					checkForDataChanges();
					return;
				}
			}
		});
	}

	/**
	 * Add touch handlers.
	 */
	private void addTouchHandlerEvents() {
		touchHelper.addDoubleTapHandler(new DoubleTapHandler() {
			@Override
			public void onDoubleTap(final DoubleTapEvent event) {
				doDoubleTap(event);
			}
		});
		touchHelper.addPanStartHandler(new PanStartHandler() {
			@Override
			public void onPanStart(final PanStartEvent event) {
				doPanStart(event);
			}
		});
		touchHelper.addPanEndHandler(new PanEndHandler() {
			@Override
			public void onPanEnd(final PanEndEvent event) {
				doPanEnd(event);
			}
		});
		touchHelper.addPanHandler(new PanHandler() {
			@Override
			public void onPan(final PanEvent event) {
				doPan(event);
			}
		});
		touchHelper.addZoomHandler(new ZoomHandler() {
			@Override
			public void onZoom(final ZoomEvent event) {
				doZoom(event);
			}
		});
		touchHelper.addZoomStartHandler(new ZoomStartHandler() {
			@Override
			public void onZoomStart(final ZoomStartEvent event) {
				doZoomStart(event);
			}
		});
		touchHelper.addZoomEndHandler(new ZoomEndHandler() {
			@Override
			public void onZoomEnd(final ZoomEndEvent event) {
				doZoomEnd(event);
			}
		});
		canvas.addDoubleClickHandler(new DoubleClickHandler() {
			@Override
			public void onDoubleClick(final DoubleClickEvent event) {
				restoreOriginalView();
			}
		});
	}

	/**
	 * Set the image for this control.
	 */
	private void setImage() {
		totalZoom = 1;
		offsetX = 0;
		offsetY = 0;
		this.imageElement = (ImageElement) image.getElement().cast();
		parentWidthChanged(getParent().getOffsetWidth(), getParent().getOffsetHeight());
		imageLoaded = true;
	}

	/**
	 * Parent window size has changed.
	 * 
	 * @param widthOfParent new width of window.
	 * @param heightOfParent new height of window.
	 */
	private void parentWidthChanged(final int widthOfParent, final int heightOfParent) {
		parentWidth = widthOfParent;
		parentHeight = heightOfParent;
		imageWidth = image.getWidth();
		imageHeight = image.getHeight();
		sizeACanvas(canvas, parentWidth, parentHeight);
		sizeACanvas(backCanvas, parentWidth, parentHeight);
		sizeACanvas(fowCanvas, parentWidth, parentHeight);
		sizeACanvas(fowBackCanvas, imageWidth, imageHeight);
		calculateStartingZoom();
		backCanvas.getContext2d().setTransform(totalZoom, 0, 0, totalZoom, 0, 0);
		drawEverything();
	}

	/**
	 * Adjust canvas size to parent size.
	 * 
	 * @param canvas to adjust
	 * @param width
	 * @param height
	 */
	private void sizeACanvas(final Canvas canvas, final int width, final int height) {
		canvas.setWidth(width + "px");
		canvas.setCoordinateSpaceWidth(width);
		canvas.setHeight(height + "px");
		canvas.setCoordinateSpaceHeight(height);
	}

	/**
	 * Calculate the starting zoom factor.
	 */
	private void calculateStartingZoom() {
		totalZoom = 1;
	}

	/**
	 * Zoom in or out of image depending on direction of mouse wheel.
	 * 
	 * @param event with mouse wheel information
	 */
	public final void onMouseWheel(final MouseWheelEvent event) {
		int move = event.getDeltaY();
		double xPos = (event.getRelativeX(canvas.getElement()));
		double yPos = (event.getRelativeY(canvas.getElement()));

		double deltaZoom = DEFAULT_ZOOM;
		if (move >= 0) {
			deltaZoom = 1 / DEFAULT_ZOOM;
		}
		zoomCanvas(xPos, yPos, deltaZoom);
	}

	/**
	 * Zoom canvas base on delta positions.
	 * 
	 * @param xPos current X
	 * @param yPos current Y
	 * @param deltaZoom delta zoom factor
	 */
	private void zoomCanvas(final double xPos, final double yPos, final double deltaZoom) {
		double newX = (xPos - offsetX) / totalZoom;
		double newY = (yPos - offsetY) / totalZoom;
		double xPosition = (-newX * deltaZoom) + newX;
		double yPosition = (-newY * deltaZoom) + newY;

		double newZoom = deltaZoom * totalZoom;
		if (newZoom < MAX_ZOOM) {
			newZoom = MAX_ZOOM;
		} else {
			offsetX += (xPosition * totalZoom);
			offsetY += (yPosition * totalZoom);
		}
		totalZoom = newZoom;
		drawEverything();
	}

	/**
	 * Handle mouse down. This has several options on what to do. If control key is down then we are selecting an area of FOW. If shift key is down we are selecting specific cells of FOW.
	 * 
	 * @param event with mouse information
	 */
	public final void onMouseDown(final MouseDownEvent event) {
		if (DOM.getCaptureElement() == null) {
			mouseDownXPos = event.getRelativeX(image.getElement());
			mouseDownYPos = event.getRelativeY(image.getElement());
			if (event.getNativeEvent().getCtrlKey()) {
				handleSelectionStart(event);
			} else {
				if (event.isShiftKeyDown()) {
					toggleFOW = true;
				} else {
					toggleFOW = ServiceManager.getDungeonManager().getFowToggle();
				}
				checkForFOWHandling(event.getNativeEvent().getClientX(), event.getNativeEvent().getClientY());
			}
			DOM.setCapture(canvas.getElement());
			this.mouseDown = true;
		}
	}

	/**
	 * Handle start of selection.
	 * 
	 * @param event
	 */
	private void handleSelectionStart(final MouseDownEvent event) {
		doingSelection = true;
		computeSelectedColumnAndRow(event.getNativeEvent().getClientX(), event.getNativeEvent().getClientY());
		selectionCoodinates.setLeft((int) mouseDownXPos - getAbsoluteLeft());
		selectionCoodinates.setTop((int) mouseDownYPos - getAbsoluteTop());
		selectionCoodinates.setRight((int) mouseDownXPos - getAbsoluteLeft());
		selectionCoodinates.setBottom((int) mouseDownYPos - getAbsoluteTop());
	}

	/**
	 * Is this position visible to player.
	 * 
	 * @param clientX position
	 * @param clientY position
	 * @return true if in window and not covered by FOW
	 */
	private boolean isSelectedVisible(final int clientX, final int clientY) {
		if (clientX < 0 || clientY < 0) {
			return (false);
		}
		return (ServiceManager.getDungeonManager().isInFOWMap(selectedColumn, selectedRow));
	}

	/**
	 * Check if we need to handle fog of war.
	 * 
	 * @param clientX X Coordinate of operation.
	 * @param clientY Y Coordinate of operation.
	 */
	private void checkForFOWHandling(final int clientX, final int clientY) {
		computeSelectedColumnAndRow(clientX, clientY);
		if (!isSelectedVisible(clientX, clientY)) {
			return;
		}
		if (toggleFOW && ServiceManager.getDungeonManager().isDungeonMaster()) {
			clearFOW = ServiceManager.getDungeonManager().isFowSet(selectedColumn, selectedRow);
			handleProperFOWAtSelectedPosition();
		}
	}

	/**
	 * Handle mouse movement. It needs to handle if we are doing a selection of FOW cells. It needs to handle if we are toggling FOW. It also need to handle panning the image if the previous conditions are not met.
	 * 
	 * @param event with mouse information.
	 */
	public final void onMouseMove(final MouseMoveEvent event) {
		if (!mouseDown) {
			return;
		}
		if (doingSelection) {
			drawSelectionRectange(event);
		} else {
			if (!toggleFOW) {
				handleMouseMoveWhilePanning(event);
			} else if (ServiceManager.getDungeonManager().isDungeonMaster()) {
				handleFowMouseMove(event.getNativeEvent().getClientX(), event.getNativeEvent().getClientY());
			}
		}
	}

	/**
	 * draw selection rectangle.
	 * 
	 * @param event
	 */
	private void drawSelectionRectange(final MouseMoveEvent event) {
		eraseSelectionRectangle();
		Context2d context = canvas.getContext2d();
		selectionCoodinates.setRight((int) (event.getRelativeX(image.getElement()) - getAbsoluteLeft()));
		selectionCoodinates.setBottom((int) (event.getRelativeY(image.getElement()) - getAbsoluteTop()));
		context.beginPath();
		context.setStrokeStyle("red");
		context.rect(selectionCoodinates.getLeft(), selectionCoodinates.getTop(), selectionCoodinates.getWidth(), selectionCoodinates.getHeight());
		context.stroke();
	}

	/**
	 * Clear selection rectangle.
	 */
	private void eraseSelectionRectangle() {
		Context2d context = canvas.getContext2d();
		context.beginPath();
		context.clearRect(selectionCoodinates.getLeft(), selectionCoodinates.getTop(), selectionCoodinates.getWidth(), selectionCoodinates.getHeight());
		context.stroke();
		drawEverything();
	}

	/**
	 * Handle mouse move dealing with fog of war.
	 * 
	 * @param clientX X Coordinate of operation.
	 * @param clientY Y Coordinate of operation.
	 */
	private void handleFowMouseMove(final int clientX, final int clientY) {
		computeSelectedColumnAndRow(clientX, clientY);
		if (isSelectedVisible(clientX, clientY)) {
			handleProperFOWAtSelectedPosition();
		}
	}

	/**
	 * Handle fog of war selected position.
	 */
	private void handleProperFOWAtSelectedPosition() {
		boolean currentFOW = ServiceManager.getDungeonManager().isFowSet(selectedColumn, selectedRow);
		// only adjust if different
		if (currentFOW != !clearFOW) {
			ServiceManager.getDungeonManager().setFow(selectedColumn, selectedRow, !currentFOW);
			drawFOW(!currentFOW, gridSpacing, selectedColumn, selectedRow);
			if (!doingSelection) {
				bitBlitFOW();
			}
		}
	}

	/**
	 * Handle mouse move while panning.
	 * 
	 * @param event event data
	 */
	private void handleMouseMoveWhilePanning(final MouseMoveEvent event) {
		double xPos = event.getRelativeX(image.getElement());
		double yPos = event.getRelativeY(image.getElement());
		handleCanvasMoveWhilePanning(xPos, yPos);
	}

	/**
	 * Handle moving canvas while panning.
	 * 
	 * @param xPos center X of pan
	 * @param yPos center Y of pan
	 */
	private void handleCanvasMoveWhilePanning(final double xPos, final double yPos) {
		isPanning = true;
		offsetX += (xPos - mouseDownXPos);
		offsetY += (yPos - mouseDownYPos);
		adjustPogs(!isPanning);
		drawEverything();
		mouseDownXPos = xPos;
		mouseDownYPos = yPos;
	}

	/**
	 * Handle mouse up event. Handle doing cell selection if required. Else finish pan operation.
	 * 
	 * @param event with mouse information
	 */
	public final void onMouseUp(final MouseUpEvent event) {
		if (doingSelection) {
			eraseSelectionRectangle();
			selectionCoodinates.setRight((int) (event.getRelativeX(image.getElement()) - getAbsoluteLeft()));
			selectionCoodinates.setBottom((int) (event.getRelativeY(image.getElement()) - getAbsoluteTop()));
			if (ServiceManager.getDungeonManager().isDungeonMaster()) {
				if (!ServiceManager.getDungeonManager().isEditMode()) {
					handleFOWSelection(event);
				} else {
					handleGridSizeComputation(event);
				}
			}
			doingSelection = false;
			drawEverything();
		}
		panOperationComplete();
		DOM.releaseCapture(canvas.getElement());
	}

	/**
	 * Mouse up so close selection. This means clearing or setting FOW on all cells within selection.
	 * 
	 * @param event mouse position
	 */
	private void handleFOWSelection(final MouseUpEvent event) {
		computeColumnAndRow(selectionCoodinates.getLeft(), selectionCoodinates.getTop());
		int startingColumn = selectedColumn;
		int startingRow = selectedRow;
		computeColumnAndRow(selectionCoodinates.getRight(), selectionCoodinates.getBottom());
		int endingColumn = selectedColumn;
		int endingRow = selectedRow;
		int top = startingRow;
		int left = startingColumn;
		int bottom = endingRow;
		int right = endingColumn;
		// Make sure we are always working from top left to bottom right
		if (endingRow < startingRow) {
			top = endingRow;
			bottom = startingRow;
		}
		if (endingColumn < startingColumn) {
			left = endingColumn;
			right = startingColumn;
		}
		// use top left cell as reference. Toggle what it is currently set to
		clearFOW = ServiceManager.getDungeonManager().isFowSet(left, top);
		toggleFOW = true;
		for (int x = left; x <= right; x += 1) {
			for (int y = top; y <= bottom; y += 1) {
				selectedColumn = x;
				selectedRow = y;
				if (isSelectedVisible(x, y)) {
					handleProperFOWAtSelectedPosition();
				}
			}
		}
	}

	/**
	 * compute size of grid.
	 * 
	 * @param event mouse position
	 */
	private void handleGridSizeComputation(final MouseUpEvent event) {
		double gridWidth = Math.abs(selectionCoodinates.getRight() - selectionCoodinates.getLeft()) / totalZoom;
		ServiceManager.getDungeonManager().setComputedGridWidth(gridWidth);
	}

	/**
	 * pan completion.
	 */
	private void panOperationComplete() {
		if (toggleFOW) {
			ServiceManager.getDungeonManager().saveFow();
			dataVersionsHistory.setItemVersion(VersionedItem.FOG_OF_WAR, dataVersionsHistory.getItemVersion(VersionedItem.FOG_OF_WAR) + 1);
		}
		mouseDown = false;
		toggleFOW = false;
		if (isPanning) {
			isPanning = false;
			drawEverything();
		}
		removeHighlightGridSquare();
	}

	/**
	 * Main method for drawing image.
	 */
	private void drawEverything() {
		calculateDimensions();
		backCanvas.getContext2d().clearRect(CLEAR_OFFEST, CLEAR_OFFEST, imageWidth + gridSpacing + 50, imageHeight + gridSpacing + 50);
		backCanvas.getContext2d().setTransform(totalZoom, 0, 0, totalZoom, offsetX, offsetY);
		backCanvas.getContext2d().drawImage(imageElement, 0, 0);
		canvas.getContext2d().clearRect(CLEAR_OFFEST, CLEAR_OFFEST, parentWidth + gridSpacing, parentHeight + gridSpacing);
		canvas.getContext2d().drawImage(backCanvas.getCanvasElement(), 0, 0);
		bitBlitFOW();
		if (!isPanning) {
			drawGridLines();
			adjustPogs(!isPanning);
		}
	}

	/**
	 * Draw fog of war.
	 */
	private void bitBlitFOW() {
		fowCanvas.getElement().getStyle().setOpacity(0);
		fowCanvas.getContext2d().setTransform(1, 0, 0, 1, 0, 0);
		fowCanvas.getContext2d().clearRect(CLEAR_OFFEST, CLEAR_OFFEST, parentWidth + gridSpacing, parentHeight + gridSpacing);
		if (ServiceManager.getDungeonManager().isDungeonMaster()) {
			fowCanvas.getElement().getStyle().setOpacity(Constants.FOW_OPACITY_FOR_DM);
		} else {
			fowCanvas.getElement().getStyle().setOpacity(Constants.FOW_OPACITY_FOR_PLAYER);
		}
		fowCanvas.getContext2d().setTransform(totalZoom, 0, 0, totalZoom, gridOffsetX, gridOffsetY);
		fowCanvas.getContext2d().drawImage(fowBackCanvas.getCanvasElement(), offsetX / totalZoom, offsetY / totalZoom);
	}

	/**
	 * Calculate numbers dependent on parent to image size and grid spacing.
	 */
	private void calculateDimensions() {
		getGridData();
		verticalLines = (int) (imageWidth / gridSpacing) + 1;
		horizontalLines = (int) (imageHeight / gridSpacing) + 1;
		ServiceManager.getDungeonManager().setSessionLevelSize(verticalLines, horizontalLines);
	}

	/**
	 * Get grid data from dungeon manager.
	 */
	private void getGridData() {
		gridOffsetX = ServiceManager.getDungeonManager().getCurrentDungeonLevelData().getGridOffsetX() * totalZoom;
		gridOffsetY = ServiceManager.getDungeonManager().getCurrentDungeonLevelData().getGridOffsetY() * totalZoom;
		gridSpacing = ServiceManager.getDungeonManager().getCurrentDungeonLevelData().getGridSize();
		showGrid = ServiceManager.getDungeonManager().isDungeonGridVisible();
	}

	/**
	 * Draw the grid line on main canvas. This will be done based on scale and offset of the background image. This way the lines themselves do not get scaled and look weird.
	 */
	private void drawGridLines() {
		if (showGrid) {
			drawVerticalGridLines();
			drawHorizontalGridLines();
			outlinePicture();
		}
	}

	/**
	 * Convert column index to pixel position.
	 * 
	 * @param column to convert
	 * @return pixel position
	 */
	private double columnToPixel(final int column) {
		return ((adjustedGridSize() * column) + offsetX + gridOffsetX);
	}

	/**
	 * Convert row index to pixel position.
	 * 
	 * @param row to convert
	 * @return pixel position
	 */
	private double rowToPixel(final int row) {
		return ((adjustedGridSize() * row) + offsetY + gridOffsetY);
	}

	/**
	 * Draw vertical grid lines.
	 */
	private void drawVerticalGridLines() {
		canvas.getContext2d().beginPath();
		canvas.getContext2d().setStrokeStyle(gridColor);
		for (int i = 0; i < verticalLines; ++i) {
			double x = columnToPixel(i);
			double y = rowToPixel(horizontalLines);
			canvas.getContext2d().moveTo(x, gridOffsetY + offsetY);
			canvas.getContext2d().lineTo(x, y);
		}
		canvas.getContext2d().stroke();
	}

	/**
	 * Draw horizontal grid lines.
	 */
	private void drawHorizontalGridLines() {
		canvas.getContext2d().beginPath();
		canvas.getContext2d().setStrokeStyle(gridColor);
		for (int i = 0; i < horizontalLines; ++i) {
			double y = rowToPixel(i);
			double x = columnToPixel(verticalLines);
			canvas.getContext2d().moveTo(gridOffsetX + offsetX, y);
			canvas.getContext2d().lineTo(x, y);
		}
		canvas.getContext2d().stroke();
	}

	/**
	 * Outline the image.
	 */
	private void outlinePicture() {
		canvas.getContext2d().beginPath();
		canvas.getContext2d().setStrokeStyle(gridColor);
		double width = (adjustedGridSize() * (verticalLines));
		double height = (adjustedGridSize() * (horizontalLines));
		canvas.getContext2d().rect(offsetX + gridOffsetX, offsetY + gridOffsetY, width, height);
		canvas.getContext2d().stroke();
	}

	/**
	 * Adjust pog positions.
	 * 
	 * Pog data has the column and row and the widget needs to be moved to the proper pixel.
	 * 
	 * @param setVisible true if visible.
	 */
	private void adjustPogs(final boolean setVisible) {
		computPogBorderWidth();
		adjustPogsInList(setVisible, monsterPogs);
		adjustPogsInList(setVisible, roomObjectPogs);
		adjustPogsInList(setVisible, playerPogs);
	}

	private void adjustPogsInList(final boolean setVisible, final ArrayList<PogCanvas> pogList) {
		for (PogCanvas pog : pogList) {
			pog.setVisible(setVisible);
			if (!setVisible) {
				continue;
			}
			int x = (int) (columnToPixel(pog.getPogColumn()));
			int y = (int) (rowToPixel(pog.getPogRow()));
			if (pog.getPogData().isFlagSet(DungeonMasterFlag.SHIFT_RIGHT)) {
				x += (adjustedGridSize() / 2);
			}
			if (pog.getPogData().isFlagSet(DungeonMasterFlag.SHIFT_TOP)) {
				y -= (adjustedGridSize() / 2);
			}
			setWidgetPosition(pog, x, y);
			pog.setPogSizing(adjustedGridSize(), pogBorderWidth, totalZoom);
			if (!ServiceManager.getDungeonManager().isDungeonMaster() && pog.isInVisibleToPlayer()) {
				pog.getElement().getStyle().setBorderWidth(0, Unit.PX);
			} else {
				pog.getElement().getStyle().setBorderWidth(pogBorderWidth, Unit.PX);
			}
		}
	}

	/**
	 * Compute width of border.
	 */
	private void computPogBorderWidth() {
		pogBorderWidth = totalZoom * getStartingBorderWidth();
		if (pogBorderWidth < 5.0) {
			pogBorderWidth = 5.0;
		}
		if (pogBorderWidth * 2 > adjustedGridSize()) {
			pogBorderWidth = 0;
		}
	}

	/**
	 * Starting border width.
	 * 
	 * @return starting border width
	 */
	private double getStartingBorderWidth() {
		return (gridSpacing / 10);
	}

	/**
	 * Draw fog of war for this cell.
	 * 
	 * If the fog of war bit is not set then make the cell transparent.
	 * 
	 * @param isSet true if need to be draw.
	 * @param size width and height of cell
	 * @param column of cell
	 * @param row of cell
	 */
	private void drawFOW(final boolean isSet, final double size, final int column, final int row) {
		int x = (int) ((column * gridSpacing));
		int y = (int) ((row * gridSpacing));
		double newSize = size + 1;
		if (isSet) {
			fowBackCanvas.getContext2d().setFillStyle(fogOfWarColor);
			fowBackCanvas.getContext2d().fillRect(x - 1, y - 1, newSize, newSize);
		} else {
			fowBackCanvas.getContext2d().clearRect(x - 1, y - 1, newSize, newSize);
		}
	}

	/**
	 * Drop a pog into a cell.
	 * 
	 * @param event event data
	 */
	private void dropPog(final DropEvent event) {
		PogData pogBeingDragged = ServiceManager.getDungeonManager().getPogBeingDragged();
		if (pogBeingDragged == null) {
			return;
		}
		removeHighlightGridSquare();
		// only DM an drop pog into FOW
		if (!ServiceManager.getDungeonManager().isDungeonMaster()) {
			if (ServiceManager.getDungeonManager().isFowSet(dragColumn, dragRow)) {
				return;
			}
		}
		if (dragColumn < 0 || dragRow < 0) { // no dragging off screen.
			return;
		}
		updateOrCreatePogCanvasForThisCell();
		drawEverything();
	}

	/**
	 * Update the pog canvas for this cell. Create one if none exists.
	 */
	private void updateOrCreatePogCanvasForThisCell() {
		PogData pogBeingDragged = ServiceManager.getDungeonManager().getPogBeingDragged();
		PogCanvas existingPog = findPogCanvas(pogBeingDragged);
		if (existingPog == null && !ServiceManager.getDungeonManager().isFromRibbonBar()) {
			return; // this can happen if not finished with previous server request.
		}
		// only clone if dropped from ribbon bar
		if (existingPog == null || (!existingPog.getPogData().isThisAPlayer()) && ServiceManager.getDungeonManager().isFromRibbonBar()) {
			existingPog = addClonePogToCanvas(ServiceManager.getDungeonManager().getPogBeingDragged());
		} else {
			remove(existingPog); // ensure it is on top by removing then adding back.
		}
		add(existingPog);
		existingPog.setPogPosition(dragColumn, dragRow);
		existingPog.getPogData().setDungeonLevel(ServiceManager.getDungeonManager().getCurrentLevelIndex());
		ServiceManager.getDungeonManager().addOrUpdatePog(existingPog.getPogData());
		ServiceManager.getDungeonManager().setSelectedPog(existingPog.getPogData());
	}

	/**
	 * Find This pog canvas.
	 * 
	 * @param pogToFind
	 * @return found pog canvas
	 */
	private PogCanvas findPogCanvas(final PogData pogToFind) {
		for (PogCanvas pog : playerPogs) {
			if (pog.getPogData().isEqual(pogToFind)) {
				return (pog);
			}
		}
		for (PogCanvas pog : monsterPogs) {
			if (pog.getPogData().isEqual(pogToFind)) {
				return (pog);
			}
		}
		for (PogCanvas pog : roomObjectPogs) {
			if (pog.getPogData().isEqual(pogToFind)) {
				return (pog);
			}
		}
		return (null);
	}

	/**
	 * get proper Z for pog based on type.
	 * 
	 * @param pogData pog data
	 * @return Proper Z
	 */
	private int getPogZ(final PogData pogData) {
		if (pogData.isThisAMonster()) {
			return (Constants.MONSTERS_Z);
		}
		if (pogData.isThisAPlayer()) {
			return (Constants.PLAYERS_Z);
		}
		return (Constants.ROOMOBJECTS_Z);
	}

	/**
	 * Add a pog to the canvas. If the pog is not a player then clone the data. This is because there can only be one player instance but there can be many of the other types.
	 * 
	 * @param pogData pog data
	 * @return pog canvas
	 */
	private PogCanvas addClonePogToCanvas(final PogData pogData) {
		getGridData();
		PogData clonePog;
		if (pogData.isThisAPlayer()) {
			clonePog = pogData;
		} else {
			clonePog = pogData.clone();
			if (ServiceManager.getDungeonManager().isEditMode()) {
				clonePog.setPogPlace(PogPlace.DUNGEON_LEVEL);
			} else {
				clonePog.setPogPlace(PogPlace.SESSION_LEVEL);
			}
		}
		return (addPogToCanvas(clonePog));
	}

	/**
	 * Add this pog to canvas with the specified Z order.
	 * 
	 * @param clonePog pog data
	 * @return pog canvas
	 */
	private PogCanvas addPogToCanvas(final PogData clonePog) {
		PogCanvas scalablePog = new PogCanvas(clonePog, popup);
		addPogToProperList(scalablePog);
		scalablePog.getElement().getStyle().setZIndex(getPogZ(clonePog));
		computPogBorderWidth();
		add(scalablePog, (int) columnToPixel(scalablePog.getPogColumn()) + (int) pogBorderWidth, (int) rowToPixel(scalablePog.getPogRow() + (int) pogBorderWidth));
		scalablePog.getElement().getStyle().setBorderStyle(BorderStyle.SOLID);
		scalablePog.getElement().getStyle().setBorderColor("grey");
		return (scalablePog);
	}

	/**
	 * Add pog to proper list.
	 * 
	 * @param scalablePog
	 */
	private void addPogToProperList(final PogCanvas scalablePog) {
		if (scalablePog.getPogData().getType() == Constants.POG_TYPE_MONSTER) {
			monsterPogs.add(scalablePog);
		} else if (scalablePog.getPogData().getType() == Constants.POG_TYPE_ROOMOBJECT) {
			roomObjectPogs.add(scalablePog);
		} else if (scalablePog.getPogData().getType() == Constants.POG_TYPE_PLAYER) {
			playerPogs.add(scalablePog);
		}

	}

	/**
	 * Get adjusted grid size. This is compensated for zoom factor
	 * 
	 * @return adjusted grid size
	 */
	private double adjustedGridSize() {
		return (gridSpacing * totalZoom);
	}

	/**
	 * Remove highlighting from grid cell.
	 */
	private void removeHighlightGridSquare() {
		greyOutPanel.getElement().getStyle().setBackgroundColor("grey");
		greyOutPanel.setVisible(false);
	}

	/**
	 * Highlight the cell at X and Y.
	 * 
	 * @param clientX Top left X
	 * @param clientY Top Left Y
	 */
	private void highlightGridSquare(final int clientX, final int clientY) {
		PogData pogBeingDragged = ServiceManager.getDungeonManager().getPogBeingDragged();
		if (pogBeingDragged == null) {
			return;
		}
		computeSelectedColumnAndRow(clientX, clientY);
		int pogWidth = pogBeingDragged.getSize() - 1;
		if (selectedColumn < 0 || selectedColumn + pogWidth >= verticalLines || selectedRow < 0 || selectedRow + pogWidth >= horizontalLines) {
			dragColumn = -1;
			dragRow = -1;
			removeHighlightGridSquare();
			return;
		}
		if (dragColumn == selectedColumn && dragRow == selectedRow) {
			return;
		}
		dragColumn = selectedColumn;
		dragRow = selectedRow;
		handleDragBox();
	}

	/**
	 * Compute Column and row from the X and Y positions.
	 * 
	 * @param clientX X position
	 * @param clientY Y position
	 */
	private void computeSelectedColumnAndRow(final int clientX, final int clientY) {
		double xCoord = clientX - getAbsoluteLeft();
		double yCoord = clientY - getAbsoluteTop();
		selectedColumn = ((int) (((xCoord - offsetX - gridOffsetX)) / adjustedGridSize()));
		selectedRow = ((int) (((yCoord - offsetY - gridOffsetY)) / adjustedGridSize()));
	}

	/**
	 * Compute Column and row from the X and Y positions.
	 * 
	 * @param clientX X position
	 * @param clientY Y position
	 */
	private void computeColumnAndRow(final int clientX, final int clientY) {
		selectedColumn = ((int) (((clientX - offsetX - gridOffsetX)) / adjustedGridSize()));
		selectedRow = ((int) (((clientY - offsetY - gridOffsetY)) / adjustedGridSize()));
	}

	/**
	 * Handle the box that indicates which cell a pog is being dragged into.
	 */
	private void handleDragBox() {
		if (dragColumn < 0 || dragRow < 0) {
			removeHighlightGridSquare();
			return;
		}
		double size = adjustedGridSize() * ServiceManager.getDungeonManager().getPogBeingDragged().getSize();
		greyOutPanel.getElement().getStyle().setZIndex(Constants.GREYOUT_Z);
		greyOutPanel.getElement().getStyle().setBackgroundColor(computeDragColor());
		greyOutPanel.setWidth("" + size + "px");
		greyOutPanel.setHeight("" + size + "px");
		super.setWidgetPosition(greyOutPanel, (int) columnToPixel(dragColumn), (int) rowToPixel(dragRow));
		greyOutPanel.setVisible(true);
	}

	/**
	 * Get color for drag indicator. Players are only allowed to drag over non-fog of war areas.
	 * 
	 * @return color string
	 */
	private String computeDragColor() {
		if (!ServiceManager.getDungeonManager().isDungeonMaster()) {
			if (ServiceManager.getDungeonManager().isFowSet(dragColumn, dragRow)) {
				return ("red");
			}
		}
		return ("grey");
	}

	/**
	 * Handle newly selected pog.
	 */
	private void newSelectedPog() {
		deSelectPog();
		PogData pog = ServiceManager.getDungeonManager().getSelectedPog();
		if (pog == null) {
			return;
		}
		PogCanvas found = findPogCanvas(pog);
		if (found != null) {
			selectedPogCanvas = found;
			selectedPogCanvas.getElement().getStyle().setBorderColor("black");
		}
	}

	/**
	 * de-select current pog.
	 */
	private void deSelectPog() {
		if (selectedPogCanvas != null) {
			selectedPogCanvas.getElement().getStyle().setBorderColor("grey");
			selectedPogCanvas = null;
		}
	}

	/**
	 * Handle double tap.
	 * 
	 * @param event with data.
	 */
	private void doDoubleTap(final DoubleTapEvent event) {
		// restoreOriginalView();
	}

	/**
	 * Restore view to original.
	 */
	private void restoreOriginalView() {
		offsetX = 0;
		offsetY = 0;
		calculateStartingZoom();
		drawEverything();
	}

	/**
	 * Get X coordinate relative between touch and target element.
	 * 
	 * @param touchInformation touch information
	 * @param target widget
	 * @return X coordinate relative between mouse click and target element.
	 */
	private int getRelativeX(final TouchInformation touchInformation, final Element target) {
		return touchInformation.getClientX() - target.getAbsoluteLeft() + target.getScrollLeft() + target.getOwnerDocument().getScrollLeft();
	}

	/**
	 * Get Y coordinate relative between touch and target element.
	 * 
	 * @param touchInformation touch information
	 * @param target widget
	 * @return Y coordinate relative between mouse click and target element.
	 */
	private int getRelativeY(final TouchInformation touchInformation, final Element target) {
		return touchInformation.getClientY() - target.getAbsoluteTop() + target.getScrollTop() + target.getOwnerDocument().getScrollTop();
	}

	/**
	 * Handle Pan start.
	 * 
	 * @param event with data
	 */
	private void doPanStart(final PanStartEvent event) {
		mouseDownXPos = getRelativeX(event.getTouchInformation(), canvas.getElement());
		mouseDownYPos = getRelativeY(event.getTouchInformation(), canvas.getElement());
		toggleFOW = ServiceManager.getDungeonManager().getFowToggle();
		checkForFOWHandling(event.getTouchInformation().getClientX(), event.getTouchInformation().getClientY());
		this.mouseDown = !toggleFOW;
	}

	/**
	 * Handle Pan end.
	 * 
	 * @param event with data
	 */
	private void doPanEnd(final PanEndEvent event) {
		this.mouseDown = false;
		panOperationComplete();
	}

	/**
	 * Handle Pan.
	 * 
	 * @param event with data
	 */
	private void doPan(final PanEvent event) {
		if (mouseDown) {
			double xPos = event.getTouchInformation().getPageX();
			double yPos = event.getTouchInformation().getPageY();
			handleCanvasMoveWhilePanning(xPos, yPos);
		} else if (toggleFOW && ServiceManager.getDungeonManager().isDungeonMaster()) {
			handleFowMouseMove(event.getTouchInformation().getClientX(), event.getTouchInformation().getClientY());
		}
	}

	/**
	 * Handle zoom start event.
	 * 
	 * @param event with data
	 */
	private void doZoomStart(final ZoomStartEvent event) {
		distanceBetweenFingers = event.getZoomInformation().getStartingDistance();
	}

	/**
	 * Handle zoom end event.
	 * 
	 * @param event with data
	 */
	private void doZoomEnd(final ZoomEndEvent event) {
	}

	/**
	 * Handle zoom event.
	 * 
	 * @param event with data
	 */
	private void doZoom(final ZoomEvent event) {
		double currentDistance = event.getZoomInformation().getCurrentDistance();
		double xPos = event.getZoomInformation().currentCenterX();
		double yPos = event.getZoomInformation().currentCenterY();
		zoomCanvas(xPos, yPos, currentDistance / distanceBetweenFingers);
		distanceBetweenFingers = currentDistance;
	}

	/**
	 * Parent window resized.
	 */
	public void onResize() {
		IDungeonManager dungeonManager = ServiceManager.getDungeonManager();
		if (dungeonManager.getCurrentDungeonLevelData() == null) {
			return;
		}
		setImage();
		dataVersionsHistory.initialize();
		dungeonDataUpdated();
	}

	/**
	 * See if any changes in data.
	 */
	private void checkForDataChanges() {
		IDungeonManager dungeonManager = ServiceManager.getDungeonManager();
		if (dungeonManager.getCurrentDungeonLevelData() == null) {
			return;
		}
		boolean initView = false;
		if (dungeonManager.getCurrentDungeonUUID() != currentDungeonID) {
			initView = true;
		} else if (dungeonManager.getCurrentSessionUUID() != currentSessionID) {
			initView = true;
		} else if (dungeonManager.getCurrentLevelIndex() != currentLevel) {
			initView = true;
		} else if (dungeonManager.getCurrentDungeonLevelData().getLevelDrawing() != dungeonPicture) {
			initView = true;
		}
		if (initView) {
			intializeView();
		} else {
			dungeonDataUpdated();
		}
		currentDungeonID = dungeonManager.getCurrentDungeonUUID();
		currentSessionID = dungeonManager.getCurrentSessionUUID();
		currentLevel = dungeonManager.getCurrentLevelIndex();
	}

	/**
	 * Initialize view.
	 */
	private void intializeView() {
		dataVersionsHistory.initialize();
		monsterPogs.clear();
		roomObjectPogs.clear();
		playerPogs.clear();
		super.clear();
		super.add(canvas, 0, 0);
		super.add(fowCanvas, 0, 0);
		super.add(hidePanel, -1, -1);
		super.add(greyOutPanel, 100, 100);
		DungeonLevel dungeonLevel = ServiceManager.getDungeonManager().getCurrentDungeonLevelData();
		if (dungeonLevel == null) {
			return;
		}
		dungeonPicture = dungeonLevel.getLevelDrawing();
		String imageUrl = ServiceManager.getDungeonManager().getUrlToDungeonResource(dungeonPicture);
		image.setUrl(imageUrl);
		imageLoaded = false;
	}

	/**
	 * Dungeon data changed.
	 */
	public void dungeonDataUpdated() {
		if (!imageLoaded) {
			return;
		}
		deSelectPog();
		updateNeededData();
		newSelectedPog();
	}

	/**
	 * Add all pogs from dungeon to canvas.
	 */
	private void updateNeededData() {
		getGridData();
		updatePogs(VersionedItem.SESSION_RESOURCE_PLAYERS, ServiceManager.getDungeonManager().getPlayersForCurrentSession(), playerPogs);
		if (ServiceManager.getDungeonManager().isEditMode()) {
			updatePogs(VersionedItem.DUNGEON_LEVEL_MONSTERS, ServiceManager.getDungeonManager().getMonstersForCurrentLevel(), monsterPogs);
			updatePogs(VersionedItem.DUNGEON_LEVEL_ROOMOBJECTS, ServiceManager.getDungeonManager().getRoomObjectsForCurrentLevel(), roomObjectPogs);
			
		} else {
			updatePogs(VersionedItem.SESSION_LEVEL_MONSTERS, ServiceManager.getDungeonManager().getMonstersForCurrentLevel(), monsterPogs);
			updatePogs(VersionedItem.SESSION_LEVEL_ROOMOBJECTS, ServiceManager.getDungeonManager().getRoomObjectsForCurrentLevel(), roomObjectPogs);
		}
		updateFogOfWar();
		drawEverything();
		ServiceManager.getDungeonManager().updateDataVersion(dataVersionsHistory);
	}

	/**
	 * Remove of add pogs to canvas based on pog lists.
	 * 
	 * @param versionedItem
	 * @param pogs
	 * @param pogList
	 */
	private void updatePogs(final VersionedItem versionedItem, final PogData[] pogs, final ArrayList<PogCanvas> pogList) {
		if (pogs == null || ServiceManager.getDungeonManager().getItemVersion(versionedItem) == dataVersionsHistory.getItemVersion(versionedItem)) {
			return;
		}
		@SuppressWarnings("unchecked")
		ArrayList<PogCanvas> existingPogs = (ArrayList<PogCanvas>) pogList.clone();
		ArrayList<PogData> pogsToBeAdded = new ArrayList<PogData>();

		getPogsTHatNeedToBeAddedOrRemoved(pogs, existingPogs, pogsToBeAdded);
		for (PogCanvas pog : existingPogs) {
			pogList.remove(pog);
			remove(pog);
		}
		for (PogData pog : pogsToBeAdded) {
			addPogToCanvas(pog);
		}
	}

	/**
	 * Find all the pogs that need to be added or removed from canvas.
	 * 
	 * @param sourcePogs
	 * @param existingPogs
	 * @param pogsToBeAdded
	 */
	private void getPogsTHatNeedToBeAddedOrRemoved(final PogData[] sourcePogs, final ArrayList<PogCanvas> existingPogs, final ArrayList<PogData> pogsToBeAdded) {
		for (PogData pog : sourcePogs) {
			boolean found = false;
			for (int index = 0; index < existingPogs.size(); ++index) {
				PogCanvas pg = existingPogs.get(index);
				if (pog.isEqual(pg.getPogData())) {
					existingPogs.remove(pg);
					pg.updatePogData(pog);
					found = true;
					break;
				}
			}
			if (!found) {
				pogsToBeAdded.add(pog);
			}
		}
	}

	/**
	 * Draw fog of war.
	 * 
	 * If this is DM let them see through it.
	 */
	private void updateFogOfWar() {
		if (ServiceManager.getDungeonManager().isEditMode() || ServiceManager.getDungeonManager().getItemVersion(VersionedItem.FOG_OF_WAR) == dataVersionsHistory.getItemVersion(VersionedItem.FOG_OF_WAR)) {
			return;
		}
		IDungeonManager dungeonManager = ServiceManager.getDungeonManager();
		double size = gridSpacing;
		for (int i = 0; i < verticalLines; ++i) {
			for (int j = 0; j < horizontalLines; ++j) {
				drawFOW(dungeonManager.isFowSet(i, j), size, i, j);
			}
		}
	}
}
