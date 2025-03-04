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
package per.lambert.ebattleMat.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.ui.RootLayoutPanel;

import per.lambert.ebattleMat.client.battleMatDisplay.BattleMatLayout;
import per.lambert.ebattleMat.client.controls.dungeonSelectDialog.DungeonSelectDialog;
import per.lambert.ebattleMat.client.controls.loginControl.LoginControl;
import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;

/**
 * Entry point class define on <code>onModuleLoad()</code>.
 */
public class ElectronicBattleMat implements EntryPoint {
	/**
	 * Root layout panel.
	 */
	private RootLayoutPanel rootLayoutPanel;
	/**
	 * layout panel for battle mat.
	 */
	private BattleMatLayout layout;
	/**
	 * dungeon select control.
	 */
	private DungeonSelectDialog dungeonSelectControl;
	/**
	 * timer to run tasks periodically.
	 */
	private Timer taskTimer;

	/**
	 * This is the entry point method.
	 */
	public void onModuleLoad() {
		rootLayoutPanel = RootLayoutPanel.get();
		setupEventHandler();
		layout = new BattleMatLayout();
		rootLayoutPanel.add(layout);
		LoginControl lc = new LoginControl();
		lc.getElement().getStyle().setZIndex(400);
		lc.show();

		taskTimer = new Timer() {
			@Override
			public void run() {
				ServiceManager.getDungeonManager().doTimedTasks();
			}
		};
		taskTimer.scheduleRepeating(1000);
	}

	/**
	 * Setup event handlers.
	 */
	private void setupEventHandler() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.Login) {
					showDungeonManagerDialog();
					return;
				}
			}
		});
	}

	/**
	 * Show dungeon manager dialog.
	 */
	private void showDungeonManagerDialog() {
		if (dungeonSelectControl == null) {
			dungeonSelectControl = new DungeonSelectDialog();
			dungeonSelectControl.enableCancel(false);
		}
		dungeonSelectControl.show();
	}
}
