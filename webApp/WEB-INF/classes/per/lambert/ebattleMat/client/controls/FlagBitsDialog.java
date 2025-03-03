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

import java.util.Collection;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.user.client.ui.CheckBox;
import com.google.gwt.user.client.ui.Grid;

import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.FlagBit;

/**
 * Dialog to manage integer of bits controlled by the flags.
 * 
 * @author LLambert
 *
 */
public class FlagBitsDialog extends OkCancelDialog {
	/**
	 * Collection of flags.
	 */
	private Collection<FlagBit> flagBits;
	/**
	 * Bits that reflect the flags.
	 */
	private int bits;

	/**
	 * Get bits.
	 * 
	 * @return current bits
	 */
	public int getBits() {
		return bits;
	}

	/**
	 * Set bits.
	 * 
	 * @param bits starting bits
	 */
	public void setBits(final int bits) {
		this.bits = bits;
	}

	/**
	 * Amount of flags per column.
	 */
	private int amountOfFlagsPerColumn;
	/**
	 * Grid for content.
	 */
	private Grid centerGrid;

	/**
	 * Constructor for flag bit dialog.
	 * 
	 * @param flagName name of dialog
	 * @param flagBits collection of flags
	 */
	public FlagBitsDialog(final String flagName, final Collection<FlagBit> flagBits) {
		super(flagName, true, true, 400, 400);
		this.flagBits = flagBits;
		amountOfFlagsPerColumn = (flagBits.size()) / 2;
		getElement().getStyle().setZIndex(Constants.DIALOG_Z + 1);
		load();
	}

	/**
	 * Load in dialog.
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
		centerGrid.resize(amountOfFlagsPerColumn, 3);
		int row = 0;
		int column = 0;
		for (FlagBit flag : flagBits) {
			if (flag.getValue() == 0) {
				continue;
			}
			CheckBox checkBox = new CheckBox(flag.getName());
			checkBox.setStyleName("ribbonBarLabel");
			centerGrid.setWidget(row, column, checkBox);
			if (++row >= amountOfFlagsPerColumn) {
				row = 0;
				++column;
			}
		}
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
	 * {@inheritDoc}
	 */
	@Override
	public void show() {
		super.show();
		initialize();
		setUIFromBits();
		center();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onOkClick(final ClickEvent event) {
		fillBitsFromUI();
		close();
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void onCancelClick(final ClickEvent event) {
		close();
	}

	/**
	 * close dialog.
	 */
	public void close() {
		hide();
	}

	/**
	 * Get bits that reflect boxes that are checked.
	 */
	private void fillBitsFromUI() {
		bits = 0;
		int row = 0;
		int column = 0;
		for (FlagBit flag : flagBits) {
			if (flag.getValue() == 0) {
				continue;
			}
			CheckBox checkBox = (CheckBox) centerGrid.getWidget(row, column);
			if (checkBox.getValue()) {
				bits |= flag.getValue();
			}
			if (++row >= amountOfFlagsPerColumn) {
				row = 0;
				++column;
			}
		}
	}

	/**
	 * Set check boxes to match bits.
	 */
	private void setUIFromBits() {
		int row = 0;
		int column = 0;
		for (FlagBit flag : flagBits) {
			if (flag.getValue() == 0) {
				continue;
			}
			CheckBox checkBox = (CheckBox) centerGrid.getWidget(row, column);
			if ((bits & flag.getValue()) != 0) {
				checkBox.setValue(true);
			} else {
				checkBox.setValue(false);
			}
			if (++row >= amountOfFlagsPerColumn) {
				row = 0;
				++column;
			}
		}
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
