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

import com.google.gwt.user.client.ui.Grid;

import per.lambert.ebattleMat.client.controls.ribbonBar.SelectedPog;
import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.PogData;

/**
 * Show selected pog in a floating window.
 * 
 * @author LLambert
 *
 */
public class SelectedPogFloatingWindow extends OkCancelDialog {
	/**
	 * Grid for content.
	 */
	private Grid centerGrid;
	/**
	 * Canvas for pog display.
	 */
	private SelectedPog selectedPog;

	/**
	 * Constructor.
	 */
	public SelectedPogFloatingWindow() {
		super("Selected Pog", false, false, 70, 70);
		getElement().getStyle().setZIndex(Constants.DIALOG_Z - 1);
		load();
		setModal(false);
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.PogWasSelected) {
					pogSelected();
					return;
				}
			}
		});
	}

	/**
	 * load in view.
	 */
	private void load() {
		createContent();
		setupEventHandlers();
		initialize();
	}

	/**
	 * Create content for the view.
	 */
	private void createContent() {
		centerGrid = getCenterGrid();
		centerGrid.clear();
		centerGrid.resize(1, 1);
		centerGrid.getColumnFormatter().setWidth(0, "100%");
		selectedPog = new SelectedPog(getResizeWidget());
		centerGrid.setWidget(0, 0, selectedPog);
	}

	/**
	 * Setup event handlers.
	 */
	private void setupEventHandlers() {
	}

	/**
	 * Initialize view.
	 * 
	 * Must be run before reusing the view.
	 */
	private void initialize() {
	}

	/**
	 * Pog was selected so set name in title.
	 */
	private void pogSelected() {
		PogData selectedPog = ServiceManager.getDungeonManager().getSelectedPog();
		if (selectedPog != null) {
			setText(selectedPog.getName());
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onWindowResized() {
		super.onWindowResized();
		selectedPog.reDraw();
	}

	/**
	 * Show window. {@inheritDoc}
	 */
	@Override
	public void show() {
		getElement().getStyle().setZIndex(Constants.DIALOG_Z - 1);
		super.show();
		selectedPog.pogSelected();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getMinWidth() {
		return 70;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getMinHeight() {
		return 70;
	}
}
