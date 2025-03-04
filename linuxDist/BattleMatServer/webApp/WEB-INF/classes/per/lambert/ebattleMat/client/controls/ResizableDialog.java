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
package per.lambert.ebattleMat.client.controls;

import com.google.gwt.dom.client.Element;
import com.google.gwt.dom.client.NativeEvent;
import com.google.gwt.dom.client.Style.Cursor;
import com.google.gwt.dom.client.Style.Position;
import com.google.gwt.event.dom.client.DomEvent;
import com.google.gwt.event.dom.client.MouseDownEvent;
import com.google.gwt.event.dom.client.MouseMoveEvent;
import com.google.gwt.event.dom.client.MouseUpEvent;
import com.google.gwt.user.client.DOM;
import com.google.gwt.user.client.Event;
import com.google.gwt.user.client.Event.NativePreviewEvent;
import com.google.gwt.user.client.ui.DialogBox;
import com.google.gwt.user.client.ui.FlowPanel;
import com.google.gwt.user.client.ui.Widget;

import per.lambert.ebattleMat.client.touchHelper.PanEndEvent;
import per.lambert.ebattleMat.client.touchHelper.PanEndHandler;
import per.lambert.ebattleMat.client.touchHelper.PanEvent;
import per.lambert.ebattleMat.client.touchHelper.PanHandler;
import per.lambert.ebattleMat.client.touchHelper.PanStartEvent;
import per.lambert.ebattleMat.client.touchHelper.PanStartHandler;
import per.lambert.ebattleMat.client.touchHelper.TouchHelper;

/**
 * DialogBox has a grid that contains the the grow handles following is the coordinates for the the various handles.
 * 0,2 Top Right 0,1 Top Center 0,0 Top Left 1,0 Middle Left 1,2 Middle Right 2,2 Bottom Right 2,1 Bottom Center 2,0 Bottom Left
 * 
 * @author LLambert
 *
 */
public class ResizableDialog extends DialogBox {

	/**
	 * Position of resize.
	 * 
	 * @author LLambert
	 *
	 */
	private enum ResizePosition {
		/**
		 * Top of window.
		 */
		TOP,
		/**
		 * Top right corner of window.
		 */
		TOPRIGHT,
		/**
		 * Top left corner of window.
		 */
		TOPLEFT,
		/**
		 * Right side of window.
		 */
		RIGHT,
		/**
		 * Left side of window.
		 */
		LEFT,
		/**
		 * Bottom of window.
		 */
		BOTTOM,
		/**
		 * Bottom right corner of window.
		 */
		BOTTOMRIGHT,
		/**
		 * Bottom left of window.
		 */
		BOTTOMLEFT,
		/**
		 * Undefined position.
		 */
		UNDEFINED
	}

	/**
	 * Margin around edge of window.
	 */
	private static final int MARGIN = 5;
	/**
	 * Minimum width of window.
	 */
	private static final int MIN_WIDTH = 100;
	/**
	 * Minimum height of window.
	 */
	private static final int MIN_HEIGHT = 100;
	/**
	 * Starting X of drag.
	 */
	private int startingX;
	/**
	 * Starting Y of drag.
	 */
	private int startingY;
	/**
	 * Position of last click.
	 */
	private ResizePosition resizePosition = ResizePosition.UNDEFINED;
	/**
	 * Delta X from starting position.
	 */
	private int deltaXFromStarting;
	/**
	 * Delta Y from starting position.
	 */
	private int deltaYFromStarting;
	/**
	 * Height of client window.
	 */
	private int clientHeight;
	/**
	 * Width of client window.
	 */
	private int clientWidth;
	/**
	 * Content holder.
	 */
	private FlowPanel content;
	/**
	 * Helper for mobile touches.
	 */
	private TouchHelper touchHelper;
	/**
	 * Starting X for Pan operation.
	 */
	private int startingPanX;
	/**
	 * Starting Y for Pan operation.
	 */
	private int startingPanY;
	/**
	 * We are doing a window move operation.
	 */
	private boolean windowMove;
	/**
	 * Doing window resize operation.
	 */
	private boolean windowResize;

	/**
	 * Constructor.
	 */
	public ResizableDialog() {
		content = new FlowPanel();
		content.setSize("100%", "100%");
		content.getElement().getStyle().setPosition(Position.RELATIVE);
		super.setWidget(content);
		touchHelper = new TouchHelper(this);
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
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void setWidget(final Widget widget) {
		content.clear();
		content.add(widget);
	}

	/**
	 * Get minimum width.
	 * 
	 * @return minimum width.
	 */
	public int getMinWidth() {
		return (MIN_WIDTH);
	}

	/**
	 * Get minimum height.
	 * 
	 * @return minimum height.
	 */
	public int getMinHeight() {
		return (MIN_HEIGHT);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void beginDragging(final MouseDownEvent event) {
		resizePosition = computeResizePosition(event.getClientX(), event.getClientY());
		if (resizePosition != ResizePosition.BOTTOMRIGHT) {
			super.beginDragging(event);
			return;
		}
		DOM.setCapture(getElement());
		startingX = event.getClientX();
		startingY = event.getClientY();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void continueDragging(final MouseMoveEvent event) {
		if (resizePosition != ResizePosition.BOTTOMRIGHT) {
			super.continueDragging(event);
			return;
		}
		int deltaX = event.getClientX() - startingX;
		int deltaY = event.getClientY() - startingY;
		startingX = event.getClientX();
		startingY = event.getClientY();
		resizeWindow(deltaX, deltaY);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void endDragging(final MouseUpEvent event) {
		if (resizePosition != ResizePosition.BOTTOMRIGHT) {
			super.endDragging(event);
			return;
		}
		DOM.releaseCapture(getElement());
		resizePosition = ResizePosition.UNDEFINED;
		onWindowResized();
	}

	/**
	 * On window resized.
	 * 
	 * for Sub-classes to know when window size changed.
	 */
	protected void onWindowResized() {
	}

	/**
	 * Set new size of window.
	 * 
	 * @param deltaX delta X
	 * @param deltaY delta Y
	 */
	private void resizeWindow(final int deltaX, final int deltaY) {
		int width = content.getOffsetWidth() + deltaX;
		width = width < getMinWidth() ? getMinWidth() : width;
		content.setWidth(width + "px");
		int height = content.getOffsetHeight() + deltaY;
		height = height < getMinHeight() ? getMinHeight() : height;
		content.setHeight(height + "px");
		onWindowResized();
	}

	/**
	 * compute Resize Position.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return position of window being resized.
	 */
	private ResizePosition computeResizePosition(final int clientX, final int clientY) {
		computeNewWindowSize();
		if (isBottomRight(clientX, clientY)) {
			return ResizePosition.BOTTOMRIGHT;
		}
		if (isTop(clientX, clientY)) {
			return ResizePosition.TOP;
		}
		return ResizePosition.UNDEFINED;
	}

	/**
	 * Get new size of window.
	 */
	private void computeNewWindowSize() {
		Element growElement = this.getCellElement(2, 2).getParentElement();
		clientWidth = growElement.getClientWidth();
		clientHeight = growElement.getClientHeight();
		// make these bigger for touch
		if (clientWidth < 25) {
			clientWidth = 25;
		}
		if (clientHeight < 25) {
			clientHeight = 25;
		}
	}

	/**
	 * Compute delta from starting positions.
	 * 
	 * @param clientX X position in client.
	 * @param clientY Y position in client.
	 * @param row to examine.
	 * @param column column to examine.
	 */
	private void computeDeltas(final int clientX, final int clientY, final int row, final int column) {
		Element growElement = this.getCellElement(row, column).getParentElement();
		deltaXFromStarting = clientX - growElement.getAbsoluteLeft() + growElement.getScrollLeft() + growElement.getOwnerDocument().getScrollLeft();
		deltaYFromStarting = clientY - growElement.getAbsoluteTop() + growElement.getScrollTop() + growElement.getOwnerDocument().getScrollTop();
	}

	/**
	 * Was change to top of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if top was changed.
	 */
	private boolean isTop(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 0, 1);
		return (deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight);
	}

	/**
	 * Was change to top left of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if top left was changed.
	 */
	@SuppressWarnings("unused")
	private boolean isTopLeft(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 0, 0);
		return ((deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth && deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight + MARGIN)
				|| (deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight && deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth + MARGIN));
	}

	/**
	 * Was change to top right of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if top right was changed.
	 */
	@SuppressWarnings("unused")
	private boolean isTopRight(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 0, 2);
		return ((deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth && deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight + MARGIN)
				|| (deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight && deltaXFromStarting >= -MARGIN && deltaXFromStarting < clientWidth));
	}

	/**
	 * Was change to bottom left of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if bottom left was changed.
	 */
	@SuppressWarnings("unused")
	private boolean isBottomLeft(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 2, 0);
		return ((deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth && deltaYFromStarting >= -MARGIN && deltaYFromStarting < clientHeight)
				|| (deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight && deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth + MARGIN));
	}

	/**
	 * Was change to bottom right of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if bottom right was changed.
	 */
	private boolean isBottomRight(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 2, 2);
		return ((deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth && deltaYFromStarting >= -MARGIN && deltaYFromStarting < clientHeight)
				|| (deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight && deltaXFromStarting >= -MARGIN && deltaXFromStarting < clientWidth));
	}

	/**
	 * Was change to bottom of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if bottom was changed.
	 */
	@SuppressWarnings("unused")
	private boolean isBottom(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 2, 1);
		return (deltaYFromStarting >= 0 && deltaYFromStarting < clientHeight);
	}

	/**
	 * Was change to left of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if left was changed.
	 */
	@SuppressWarnings("unused")
	private boolean isLeft(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 1, 0);
		return (deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth);
	}

	/**
	 * Was change to right of window.
	 * 
	 * @param clientX x coordinate.
	 * @param clientY y coordinate.
	 * @return true if right was changed.
	 */
	@SuppressWarnings("unused")
	private boolean isRight(final int clientX, final int clientY) {
		computeDeltas(clientX, clientY, 1, 2);
		return (deltaXFromStarting >= 0 && deltaXFromStarting < clientWidth);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void onBrowserEvent(final Event event) {
		switch (event.getTypeInt()) {
		case Event.ONMOUSEDOWN:
		case Event.ONMOUSEUP:
		case Event.ONMOUSEMOVE:
		case Event.ONMOUSEOVER:
		case Event.ONMOUSEOUT:
			ResizePosition possible = computeResizePosition(event.getClientX(), event.getClientY());
			if (resizePosition != ResizePosition.UNDEFINED || possible != ResizePosition.UNDEFINED) {
				switch (DOM.eventGetType(event)) {
				case Event.ONMOUSEOVER:
				case Event.ONMOUSEOUT:
					Element related = event.getRelatedEventTarget().cast();
					if (related != null && getElement().isOrHasChild(related)) {
						return;
					}
					break;
				default:
				}
				DomEvent.fireNativeEvent(event, this, this.getElement());
				getElement().getStyle().setCursor(possible != ResizePosition.UNDEFINED ? Cursor.POINTER : Cursor.AUTO);
				return;
			}
			getElement().getStyle().setCursor(possible != ResizePosition.UNDEFINED ? Cursor.POINTER : Cursor.AUTO);
		default:
			break;
		}
		super.onBrowserEvent(event);
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onPreviewNativeEvent(final NativePreviewEvent event) {
		NativeEvent nativeEvent = event.getNativeEvent();
		if (!event.isCanceled() && (event.getTypeInt() == Event.ONMOUSEDOWN) && computeResizePosition(nativeEvent.getClientX(), nativeEvent.getClientY()) != ResizePosition.UNDEFINED) {
			nativeEvent.preventDefault();
		}
		super.onPreviewNativeEvent(event);
	}

	/**
	 * Do Pan Start.
	 * @param event pan event data
	 */
	private void doPanStart(final PanStartEvent event) {
		startingPanX = event.getTouchInformation().getClientX();
		startingPanY = event.getTouchInformation().getClientY();
		ResizePosition where = computeResizePosition(startingPanX, startingPanY);
		if (where == ResizePosition.TOP) {
			windowMove = true;
		} else if (where == ResizePosition.BOTTOMRIGHT) {
			windowResize = true;
		}
	}

	/**
	 * Done panning.
	 * @param event pan event data
	 */
	private void doPanEnd(final PanEndEvent event) {
		windowMove = false;
		windowResize = false;
	}

	/**
	 * Do Pan operation.
	 * @param event pan event data
	 */
	private void doPan(final PanEvent event) {
		int xPos = event.getTouchInformation().getClientX();
		int yPos = event.getTouchInformation().getClientY();
		int deltaX = xPos - startingPanX;
		int deltaY = yPos - startingPanY;
		if (windowMove) {
			moveWindow(deltaX, deltaY);
		} else if (windowResize) {
			resizeWindow(deltaX, deltaY);
		}
		startingPanX = xPos;
		startingPanY = yPos;
	}

	/**
	 * Move window.
	 * @param deltaX delta X of move.
	 * @param deltaY delta Y of move.
	 */
	private void moveWindow(final int deltaX, final int deltaY) {
		int top = this.getAbsoluteTop();
		int left = this.getAbsoluteLeft();
		setPopupPosition(left + deltaX, top + deltaY);
	}

	/**
	 * Get width of dialog.
	 * 
	 * @return width of dialog
	 */
	protected int getDialogWidth() {
		return (content.getOffsetWidth());
	}

	/**
	 * Get height of dialog.
	 * 
	 * @return height of dialog
	 */
	protected int getDialogHeight() {
		return (content.getOffsetHeight());
	}

	/**
	 * Enable or disable a widget.
	 * 
	 * @param widget to enable or disable
	 * @param enable true to enable
	 */
	public static void enableWidget(final Widget widget, final boolean enable) {
		if (enable) {
			widget.getElement().removeAttribute("disabled");
		} else {
			widget.getElement().setAttribute("disabled", "disabled");
		}
	}
}
