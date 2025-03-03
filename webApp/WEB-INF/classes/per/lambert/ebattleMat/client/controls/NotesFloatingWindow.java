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
import com.google.gwt.event.dom.client.KeyUpEvent;
import com.google.gwt.event.dom.client.KeyUpHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.FocusPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.ScrollPanel;
import com.google.gwt.user.client.ui.TabLayoutPanel;

import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.services.ServiceManager;

/**
 * Floating window display notes on a pog.
 * 
 * @author LLambert
 *
 */
public class NotesFloatingWindow extends OkCancelDialog {
	/**
	 * Panel to capture key events.
	 */
	private FocusPanel editPanel;
	/**
	 * Panel to capture key events.
	 */
	private FocusPanel dmEditPanel;
	/**
	 * Panel for scroll area.
	 */
	private ScrollPanel scrollPanel;
	/**
	 * Panel for scroll area.
	 */
	private ScrollPanel dmScrollPanel;
	/**
	 * Layout panel.
	 */
	private DockLayoutPanel dockLayoutPanel;
	/**
	 * Panel for buttons.
	 */
	private HorizontalPanel buttonPanel;
	/**
	 * Save changes button.
	 */
	private Button save;
	/**
	 * Cancel button.
	 */
	private Button cancel;
	/**
	 * size of font.
	 */
	private NumberSpinner fontSize;
	/**
	 * Tab panel.
	 */
	private TabLayoutPanel tabPanel;
	/**
	 * Notes from host.
	 */
	private String notes;
	/**
	 * DM notes from host.
	 */
	private String dmNotes;
	/**
	 * Constructor.
	 */
	public NotesFloatingWindow() {
		super("Pog Notes", false, false, 200, 200);
		getElement().getStyle().setZIndex(Constants.DIALOG_Z - 1);
		load();
		setModal(false);
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
		editPanel = new FocusPanel();
		editPanel.setSize("100%", "100%");
		editPanel.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				handleTextChanged(event);
			}
		});
		scrollPanel = new ScrollPanel(editPanel);
		scrollPanel.setSize("100%", "100%");

		dmEditPanel = new FocusPanel();
		dmEditPanel.setSize("100%", "100%");
		dmEditPanel.addKeyUpHandler(new KeyUpHandler() {
			@Override
			public void onKeyUp(final KeyUpEvent event) {
				handleTextChanged(event);
			}
		});
		dmScrollPanel = new ScrollPanel(dmEditPanel);
		dmScrollPanel.setSize("100%", "100%");

		dockLayoutPanel = new DockLayoutPanel(Unit.PX);
		dockLayoutPanel.setStyleName("popupPanel");
		dockLayoutPanel.setSize("100%", "100%");
		addButtonSupport();

		tabPanel = new TabLayoutPanel(2.5, Unit.EM);
		tabPanel.setSize("100%", "100%");

		setWidget(dockLayoutPanel);
	}

	/**
	 * Add button support.
	 */
	private void addButtonSupport() {
		buttonPanel = new HorizontalPanel();
		save = new Button("Save");
		save.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				saveNotes();
			}
		});
		buttonPanel.add(save);
		cancel = new Button("Cancel");
		cancel.addClickHandler(new ClickHandler() {
			@Override
			public void onClick(final ClickEvent event) {
				onCancel();
			}
		});
		buttonPanel.add(cancel);
		// add ability to adjust font size.
		fontSize = new NumberSpinner(14, 14, 20);
		fontSize.setValue(14);
		buttonPanel.add(fontSize);
		editPanel.getElement().getStyle().setFontSize(fontSize.getValue(), Unit.PX);
		dmEditPanel.getElement().getStyle().setFontSize(fontSize.getValue(), Unit.PX);
		fontSize.addChangeHandler(new ValueChangeHandler<Integer>() {
			@Override
			public void onValueChange(final ValueChangeEvent<Integer> event) {
				if (event.getValue() >= 14 && event.getValue() <= 20) {
					editPanel.getElement().getStyle().setFontSize(fontSize.getValue(), Unit.PX);
					dmEditPanel.getElement().getStyle().setFontSize(fontSize.getValue(), Unit.PX);
				}
			}
		});
	}

	/**
	 * cancel pressed.
	 */
	private void onCancel() {
		setupDisplayWithData();
	}

	/**
	 * Add an save click handler.
	 * 
	 * @param clickHandler to add
	 */
	public void addSaveClickHandler(final ClickHandler clickHandler) {
		save.addClickHandler(clickHandler);
	}

	/**
	 * Add an cancel click handler.
	 * 
	 * @param clickHandler to add
	 */
	public void addCancelClickHandler(final ClickHandler clickHandler) {
		cancel.addClickHandler(clickHandler);
	}

	/**
	 * Save changed notes.
	 */
	private void saveNotes() {
		notes = editPanel.getElement().getInnerText();
		dmNotes = dmEditPanel.getElement().getInnerText();
		enableWidget(save, false);
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
		getElement().getStyle().setZIndex(Constants.DIALOG_Z - 1);
		tabPanel.clear();
		tabPanel.add(scrollPanel, "Notes");
		if (ServiceManager.getDungeonManager().isDungeonMaster()) {
			tabPanel.add(dmScrollPanel, "DM Notes");
		}
		dockLayoutPanel.clear();
		dockLayoutPanel.addSouth(buttonPanel, 30);
		dockLayoutPanel.add(tabPanel);
		if (!ServiceManager.getDungeonManager().isDungeonMaster()) {
			enableWidget(save, false);
		}
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onWindowResized() {
		super.onWindowResized();
	}

	/**
	 * Get the text from the selected pog.
	 */
	private void setupDisplayWithData() {
		String textToSet = "";
		String dmTextToSet = "";
		scrollPanel.scrollToTop();
		scrollPanel.scrollToLeft();
		dmScrollPanel.scrollToTop();
		dmScrollPanel.scrollToLeft();
		if (notes != null) {
			textToSet = notes;
		}
		if (dmNotes != null) {
			dmTextToSet = dmNotes;
		}
		editPanel.getElement().setInnerText(textToSet);
		dmEditPanel.getElement().setInnerText(dmTextToSet);
		makeContentEditable(ServiceManager.getDungeonManager().isDungeonMaster());
		enableWidget(save, false);
	}
	/**
	 * get Notes text.
	 * 
	 * @return notes text
	 */
	public String getNotesText() {
		return (notes);
	}

	/**
	 * Set text for notes.
	 * 
	 * @param notesText
	 */
	public void setNotesText(final String notesText) {
		notes = notesText;
		setupDisplayWithData();
	}

	/**
	 * get Notes text.
	 * 
	 * @return notes text
	 */
	public String getDMNotesText() {
		return (dmNotes);
	}

	/**
	 * Set text for notes.
	 * 
	 * @param notesText
	 */
	public void setDMNotesText(final String notesText) {
		dmNotes = notesText;
		setupDisplayWithData();
	}

	/**
	 * Make html content editable.
	 * 
	 * @param editable true if editable
	 */
	private void makeContentEditable(final boolean editable) {
		if (editable) {
			editPanel.getElement().setAttribute("contenteditable", "true");
			dmEditPanel.getElement().setAttribute("contenteditable", "true");
		} else {
			editPanel.getElement().setAttribute("contenteditable", "false");
			dmEditPanel.getElement().setAttribute("contenteditable", "false");
		}
	}

	/**
	 * Handle text changed event.
	 * 
	 * @param event with the information
	 */
	private void handleTextChanged(final KeyUpEvent event) {
		if (save != null) {
			enableWidget(save, true);
		}
	}

	/**
	 * Show window. {@inheritDoc}
	 */
	@Override
	public void show() {
		initialize();
		super.show();
		setupDisplayWithData();
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
		return 200;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public int getMinHeight() {
		return 200;
	}

}
