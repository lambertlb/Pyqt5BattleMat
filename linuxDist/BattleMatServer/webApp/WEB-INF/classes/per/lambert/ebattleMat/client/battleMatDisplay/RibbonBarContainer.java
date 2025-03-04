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

import com.google.gwt.core.client.GWT;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

/**
 * Container for ribbon bar.
 * @author LLambert
 *
 */
public class RibbonBarContainer extends Composite {

	/**
	 * UI binder.
	 */
	private static RibbonBarContainerUiBinder uiBinder = GWT.create(RibbonBarContainerUiBinder.class);

	/**
	 * Interface for UI binder.
	 * @author LLambert
	 *
	 */
	interface RibbonBarContainerUiBinder extends UiBinder<Widget, RibbonBarContainer> {
	}

	/**
	 * Constructor.
	 */
	public RibbonBarContainer() {
		initWidget(uiBinder.createAndBindUi(this));
	}
}
