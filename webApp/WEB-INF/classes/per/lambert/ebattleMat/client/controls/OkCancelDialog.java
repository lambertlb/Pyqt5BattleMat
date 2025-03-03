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

import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.FlowPanel;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Widget;

import per.lambert.ebattleMat.client.interfaces.Constants;

/**
 * Base dialog for dialogs needing OK and cancel buttons. It will contain a grid in the center where user can add content.
 * 
 * @author LLambert
 *
 */
public class OkCancelDialog extends ResizableDialog {
	/**
	 * Dock layout panel.
	 */
	private DockLayoutPanel dockLayoutPanel;
	/**
	 * Grid for sub-classes to use for content.
	 */
	private Grid centerGrid;
	/**
	 * OK button.
	 */
	private Button ok;
	/**
	 * Cancel button.
	 */
	private Button cancel;
	/**
	 * Panel to hold center content.
	 */
	private FlowPanel centerContent;
	/**
	 * Content on south side of dialog.
	 */
	private HorizontalPanel southContent;

	/**
	 * grid for user content.
	 * 
	 * @return grid for user content.
	 */
	protected Grid getCenterGrid() {
		return (centerGrid);
	}

	/**
	 * Constructor.
	 */
	public OkCancelDialog() {
		this("", false, false);
	}

	/**
	 * Constructor.
	 * 
	 * @param caption for dialog
	 * @param okVisible true if OK button is visible.
	 * @param cancelVisible true if Cancel button is visible
	 */
	public OkCancelDialog(final String caption, final boolean okVisible, final boolean cancelVisible) {
		this(caption, okVisible, cancelVisible, 400, 350);
	}

	/**
	 * Constructor.
	 * 
	 * @param caption for dialog
	 * @param okVisible true if OK button is visible.
	 * @param cancelVisible true if Cancel button is visible
	 * @param height of dialog
	 * @param width of dialog
	 */
	public OkCancelDialog(final String caption, final boolean okVisible, final boolean cancelVisible, final int height, final int width) {
		super();
		setText(caption);
		getElement().getStyle().setZIndex(Constants.DIALOG_Z);
		createContent(okVisible, cancelVisible);
		ok.setVisible(okVisible);
		cancel.setVisible(cancelVisible);
		dockLayoutPanel.setWidth("" + width + "px");
		dockLayoutPanel.setHeight("" + height + "px");
		this.setPopupPosition(100, 100);
	}

	/**
	 * Create content.
	 * 
	 * @param okVisible true if OK button is visible.
	 * @param cancelVisible true if Cancel button is visible
	 */
	private void createContent(final boolean okVisible, final boolean cancelVisible) {
		dockLayoutPanel = new DockLayoutPanel(Unit.PX);
		dockLayoutPanel.setStyleName("popupPanel");
		southContent = new HorizontalPanel();
		double southSize = (okVisible || cancelVisible) ? 30.0 : 0.0;
		dockLayoutPanel.addSouth(southContent, southSize);
		ok = new Button("Ok");
		ok.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				onOkClick(event);
			}
		});
		southContent.add(ok);
		cancel = new Button("Cancel");
		cancel.addClickHandler(new ClickHandler() {

			@Override
			public void onClick(final ClickEvent event) {
				onCancelClick(event);
			}
		});
		southContent.add(cancel);
		centerContent = new FlowPanel();
		centerContent.setHeight("100%");
		centerContent.setWidth("100%");
		centerGrid = new Grid();
		centerGrid.setWidth("100%");
		centerContent.add(centerGrid);
		dockLayoutPanel.add(centerContent);
		super.setWidget(dockLayoutPanel);
	}

	/**
	 * {@inheritDoc}
	 */
	public void setWidget(final Widget widgetToSet) {
		centerContent.clear();
		centerContent.add(widgetToSet);
	}

	/**
	 * Initialize content.
	 */
	private void initialize() {
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onWindowResized() {
		super.onWindowResized();
		int width = getDialogWidth();
		int height = getDialogHeight();
		dockLayoutPanel.setWidth("" + width + "px");
		dockLayoutPanel.setHeight("" + height + "px");
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void show() {
		super.show();
		adjustPosition();
		initialize();
	}

	/**
	 * Make sure dialog is still visible in case the browser was shrunk.
	 */
	private void adjustPosition() {
		int height = Window.getClientHeight();
		int width = Window.getClientWidth();
		String sLeft = getElement().getStyle().getLeft();
		String sTop = getElement().getStyle().getTop();
		if (sLeft != "" && sTop != "") {
			int top = Integer.parseInt(sTop.substring(0, sTop.length() - 2));
			int left = Integer.parseInt(sLeft.substring(0, sLeft.length() - 2));
			if (left > width || top > height) {
				setPopupPosition(100, 100);
			}
		}
	}

	/**
	 * enable or disable OK button.
	 * 
	 * @param enable true to enable.
	 */
	public void enableOk(final boolean enable) {
		enableWidget(ok, enable);
	}

	/**
	 * enable or disable Cancel button.
	 * 
	 * @param enable true to enable.
	 */
	public void enableCancel(final boolean enable) {
		enableWidget(cancel, enable);
	}

	/**
	 * OK button clicked.
	 * 
	 * @param event data
	 */
	protected void onOkClick(final ClickEvent event) {
	}

	/**
	 * Cancel button clicked.
	 * 
	 * @param event data
	 */
	protected void onCancelClick(final ClickEvent event) {
	}

	/**
	 * get top of ok button.
	 * 
	 * @return top of ok button
	 */
	protected int getOkTop() {
		return (ok.getAbsoluteTop());
	}

	/**
	 * get left of ok button.
	 * 
	 * @return left of ok button
	 */
	protected int getOkLeft() {
		return (ok.getAbsoluteLeft());
	}

	/**
	 * Add an ok click handler.
	 * 
	 * @param clickHandler to add
	 */
	public void addOkClickHandler(final ClickHandler clickHandler) {
		ok.addClickHandler(clickHandler);
	}

	/**
	 * Get widget used for resizing.
	 * 
	 * @return widget to used for resizing.
	 */
	public Widget getResizeWidget() {
		return (dockLayoutPanel);
	}
}
