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
package per.lambert.ebattleMat.client.battleMatDisplay;

import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.TabLayoutPanel;

import per.lambert.ebattleMat.client.controls.ArtAssetsPanel;
import per.lambert.ebattleMat.client.controls.DungeonLevelEditorPanel;
import per.lambert.ebattleMat.client.controls.PogEditor;

/**
 * Panel used for managing assets in battle map.
 * @author llambert
 *
 */
public class AssetManagementPanel extends DockLayoutPanel {

	/**
	 * Tab panel.
	 */
	private TabLayoutPanel tabPanel = new TabLayoutPanel(1.5, Unit.EM);
	/**
	 * Panel for handling art assests.
	 */
	private ArtAssetsPanel artAssetsPanel = new ArtAssetsPanel();
	/**
	 * Panel for editing dungeon.
	 */
	private DungeonLevelEditorPanel dungeonPanel = new DungeonLevelEditorPanel();
	/**
	 * Panel for editing pogs.
	 */
	private PogEditor pogEditor = new PogEditor();
	/**
	 * Constructor.
	 */
	public AssetManagementPanel() {
		super(Unit.PX);
		setSize("100%", "100%");
		tabPanel.setWidth("100%");
		tabPanel.setHeight("100%");
		tabPanel.add(artAssetsPanel, "Art Assets");
		tabPanel.add(dungeonPanel, "Dungeon Editor");
		tabPanel.add(pogEditor, "Pog Editor");
		add(tabPanel);
		this.forceLayout();
	}
}
