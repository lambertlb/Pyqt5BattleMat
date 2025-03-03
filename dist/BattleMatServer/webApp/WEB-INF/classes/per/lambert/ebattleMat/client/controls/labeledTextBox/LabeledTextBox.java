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
package per.lambert.ebattleMat.client.controls.labeledTextBox;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.event.dom.client.KeyUpHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.DoubleBox;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.TextBox;
import com.google.gwt.user.client.ui.Widget;

/**
 * Text Box with a preceding label.
 * 
 * @author LLambert
 *
 */
public class LabeledTextBox extends Composite {

	/**
	 * UI Binder.
	 */
	private static LabeledTextBoxUiBinder uiBinder = GWT.create(LabeledTextBoxUiBinder.class);

	/**
	 * Interface to binder.
	 * 
	 * @author LLambert
	 *
	 */
	interface LabeledTextBoxUiBinder extends UiBinder<Widget, LabeledTextBox> {
	}

	/**
	 * Textbox contains a double.
	 */
	private boolean asDouble;

	/**
	 * Constructor for text box.
	 * 
	 * @param labelText label text
	 * @param editText edit text
	 */
//	public LabeledTextBox(final String labelText, final String editText) {
//		initWidget(uiBinder.createAndBindUi(this));
//		asDouble = false;
//		setLabelText(labelText);
//	}

	/**
	 * Constructor for text box.
	 * 
	 * @param labelText label text
	 * @param value edit text
	 */
	public LabeledTextBox(final String labelText, final Double value) {
		initWidget(uiBinder.createAndBindUi(this));
		asDouble = true;
		setLabelText(labelText);
	}

	/**
	 * Label for text box.
	 */
	@SuppressWarnings("VisibilityModifier")
	@UiField
	Label textBoxLabel;
	/**
	 * Text box.
	 */
	@SuppressWarnings("VisibilityModifier")
	@UiField
	TextBox textBox;
	/**
	 * text box for double value.
	 */
	@SuppressWarnings("VisibilityModifier")
	@UiField
	DoubleBox doubleBox;

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected final void onLoad() {
		super.onLoad();
		if (asDouble) {
			textBox.setVisible(false);
			doubleBox.setVisible(true);
		} else {
			textBox.setVisible(true);
			doubleBox.setVisible(false);
		}
	}

	/**
	 * Set label text.
	 * 
	 * @param labelText to set
	 */
	public final void setLabelText(final String labelText) {
		textBoxLabel.setText(labelText);
	}

	/**
	 * Set text box value.
	 * 
	 * @param value to set
	 */
	public final void setValue(final String value) {
		textBox.setValue(value);
	}

	/**
	 * Set double box value.
	 * 
	 * @param value to set
	 */
	public final void setValue(final Double value) {
		doubleBox.setValue(value);
	}

	/**
	 * Get text box value.
	 * 
	 * @return value
	 */
	public final String getTextValue() {
		return (textBox.getValue());
	}

	/**
	 * Get double box value.
	 * 
	 * @return value
	 */
	public final Double getDoubleValue() {
		return (doubleBox.getValue());
	}

	/**
	 * Add value changed handler.
	 * 
	 * @param changeHandler to add
	 */
	public final void addChangeHandler(final ChangeHandler changeHandler) {
		if (asDouble) {
			doubleBox.addChangeHandler(changeHandler);
		} else {
			textBox.addChangeHandler(changeHandler);
		}
	}

	/**
	 * Add key up handler.
	 * 
	 * @param keyUpHandler to add.
	 */
	public final void addKeyUpHandler(final KeyUpHandler keyUpHandler) {
		if (asDouble) {
			doubleBox.addKeyUpHandler(keyUpHandler);
		} else {
			textBox.addKeyUpHandler(keyUpHandler);
		}
	}

	public final void setEntryWidth(final String width) {
		if (asDouble) {
			doubleBox.setWidth(width);
		} else {
			textBox.setWidth(width);
		}
	}
}
