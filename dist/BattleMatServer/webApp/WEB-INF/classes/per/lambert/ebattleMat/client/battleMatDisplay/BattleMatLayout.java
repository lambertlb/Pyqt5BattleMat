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

import com.google.gwt.dom.client.Style.Unit;
import com.google.gwt.event.logical.shared.ResizeEvent;
import com.google.gwt.event.logical.shared.ResizeHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.DockLayoutPanel;
import com.google.gwt.user.client.ui.LayoutPanel;
import com.google.gwt.user.client.ui.ResizeComposite;
import com.google.gwt.user.client.ui.SimpleLayoutPanel;
import com.google.gwt.user.client.ui.SplitLayoutPanel;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;

/**
 * Layout for battle mat.
 * 
 * @author LLambert
 *
 */
public class BattleMatLayout extends ResizeComposite {
	/**
	 * The LayoutPanel that is essentially this widget.
	 */
	private DockLayoutPanel dockPanel;
	/**
	 * panel for ribbon bar.
	 */
	private RibbonBarContainer ribbonBarPanel;
	/**
	 * Panel to hold battle mat canvas.
	 */
	private SimpleLayoutPanel battleMatCanvasPanel;
	/**
	 * Battle mat canvas.
	 */
	private BattleMatCanvas battleMatCanvas;
	/**
	 * main panel.
	 */
	private LayoutPanel mainPanel;
	/**
	 * East side of panel.
	 */
	private LayoutPanel east = new LayoutPanel();
	/**
	 * Asset management panel.
	 */
	private AssetManagementPanel assetManagementPanel = new AssetManagementPanel();
	/**
	 * Splitter panel.
	 */
	private SplitLayoutPanel splitPanel;
	/**
	 * Have panels been setup.
	 */
	private boolean panelsSetup;

	/**
	 * Sets up the widget. We create the GUI, set up event handling, and call initWidget on the holder panel.
	 */
	public BattleMatLayout() {
		createConent();
		initWidget(dockPanel);
		// ensure this widget takes up as much space as possible
		this.setSize("100%", "100%");
		setupEventHandler();
	}

	/**
	 * create content of panel.
	 */
	private void createConent() {
		dockPanel = new DockLayoutPanel(Unit.PX);
		ribbonBarPanel = new RibbonBarContainer();
		battleMatCanvasPanel = new SimpleLayoutPanel();
		mainPanel = new LayoutPanel();
		mainPanel.setSize("100%", "100%");
		battleMatCanvas = new BattleMatCanvas();
		battleMatCanvasPanel.clear();
		battleMatCanvasPanel.add(battleMatCanvas);
		east.setSize("100%", "100%");
		east.add(assetManagementPanel);
		splitPanel = new SplitLayoutPanel() {
			@Override
			public void onResize() {
				super.onResize();
				battleMatCanvas.onResize();
			};
		};
		mainPanel.add(splitPanel);
		dockPanel.clear();
		dockPanel.addNorth(ribbonBarPanel, Constants.RIBBON_BAR_SIZE);
		dockPanel.add(mainPanel);
		// MUST CALL THIS METHOD to set the constraints; if you don't not much
		// will be displayed!
		dockPanel.forceLayout();

		Window.addResizeHandler(new ResizeHandler() {
			public void onResize(final ResizeEvent event) {
				doWindowResize(event);
			}
		});
	}

	/**
	 * Setup event handlers.
	 */
	private void setupEventHandler() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.DungeonDataReadyToEdit) {
					dungeonDataChanged();
					return;
				} else if (event.getReasonForAction() == ReasonForAction.DungeonDataReadyToJoin) {
					dungeonDataChanged();
					return;
				} else if (event.getReasonForAction() == ReasonForAction.DungeonDataSaved) {
					dungeonDataChanged();
					return;
				}
			}
		});
	}

	/**
	 * delegate dungeon data changed.
	 */
	private void dungeonDataChanged() {
		if (!panelsSetup) {
			setupPanels();
		}
		boolean isDM = ServiceManager.getDungeonManager().isDungeonMaster();
		// hide the splitter
		east.setVisible(isDM);
		splitPanel.setWidgetSize(east, isDM ? Window.getClientWidth() / 5.0 : 0.0);
	}

	/**
	 * Setup panels for proper mode.
	 */
	private void setupPanels() {
		splitPanel.addEast(east, Window.getClientWidth() / 5);
		splitPanel.add(battleMatCanvasPanel);
		panelsSetup = true;
	}

	/**
	 * delegate window resized.
	 * 
	 * @param event event data
	 */
	private void doWindowResize(final ResizeEvent event) {
		battleMatCanvas.onResize();
	}
}
