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
package per.lambert.ebattleMat.client.controls.dungeonSelectDialog;

import java.util.Map;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.event.ReasonForActionEventHandler;
import per.lambert.ebattleMat.client.interfaces.IEventManager;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;
import per.lambert.ebattleMat.client.services.serviceData.SessionListData;

/**
 * Presenter for Dungeon master control view.
 * 
 * @author LLambert
 *
 */
public class DungeonSelectPresenter {
	/**
	 * View to manage.
	 */
	private DungeonSelectDialog view;
	/**
	 * acting as DM.
	 */
	private boolean isDungeonMaster;
	/**
	 * New dungeon name.
	 */
	private String newDungeonName;
	/**
	 * UUID for selected dungeon.
	 */
	private String selectedDungeonUUID;
	/**
	 * New session name.
	 */
	private String newSessionName;
	/**
	 * UUID for new session.
	 */
	private String newSessionUUID;

	/**
	 * Acting as DM?
	 * 
	 * @return true if DM flag set.
	 */
	public boolean isDungeonMaster() {
		return isDungeonMaster;
	}

	/**
	 * Set acting as DM flag.
	 * 
	 * @param isDungeonMaster true if DM
	 */
	public void setDungeonMaster(final boolean isDungeonMaster) {
		this.isDungeonMaster = isDungeonMaster;
		templateSelected = false;
		okToCreateDungeon = false;
		refreshView();
	}

	/**
	 * Has dungeon template been set?
	 */
	private boolean templateSelected;

	/**
	 * get Has dungeon template been set.
	 * 
	 * @return true if set.
	 */
	public boolean isTemplateSelected() {
		return templateSelected;
	}

	/**
	 * Is it ok to create a new dungeon?
	 */
	private boolean okToCreateDungeon;

	/**
	 * get Is it ok to create a new dungeon.
	 * 
	 * @return Is it ok to create a new dungeon
	 */
	public boolean isOkToCreateDungeon() {
		return okToCreateDungeon;
	}

	/**
	 * is it ok to delete dungeon?
	 */
	private boolean okToDelete;

	/**
	 * get is it ok to delete dungeon?
	 * 
	 * @return is it ok to delete dungeon?
	 */
	public boolean isOkToDelete() {
		return okToDelete;
	}

	/**
	 * get is ok to show sesion data?
	 * 
	 * @return is ok to show sesion data
	 */
	public boolean isOkToShowSessions() {
		return isValidDungeonForSessions && ServiceManager.getDungeonManager().getSessionListData() != null;
	}

	/**
	 * is this dungeon valid to manage a session.
	 */
	private boolean isValidDungeonForSessions;

	/**
	 * get is this dungeon valid to manage a session.
	 * 
	 * @return is this dungeon valid to manage a session
	 */
	public boolean isValidDungeonForSessions() {
		return isValidDungeonForSessions;
	}

	/**
	 * is ok to create a session?
	 */
	private boolean okToCreateSession;

	/**
	 * get is ok to create a session?
	 * 
	 * @return is ok to create a session?
	 */
	public boolean isOkToCreateSession() {
		return okToCreateSession;
	}

	/**
	 * has session been selected.
	 */
	private boolean sessionSelected;

	/**
	 * get has session been selected.
	 * 
	 * @return has session been selected.
	 */
	public boolean isSessionSelected() {
		return sessionSelected;
	}

	/**
	 * is ok to delete session.
	 */
	private boolean okToDeleteSession;

	/**
	 * get is ok to delete session.
	 * 
	 * @return is ok to delete session.
	 */
	public boolean isOkToDeleteSession() {
		return okToDeleteSession;
	}

	/**
	 * is ok to DM a session.
	 */
	private boolean okToDMSession;

	/**
	 * get is ok to DM a session.
	 * 
	 * @return is ok to DM a session.
	 */
	public boolean isOkToDMSession() {
		return okToDMSession;
	}

	/**
	 * is ok to join a session.
	 */
	private boolean okToJoinSession;

	/**
	 * get is ok to join a session.
	 * 
	 * @return is ok to join a session.
	 */
	public boolean isOkToJoinSession() {
		return okToJoinSession;
	}

	/**
	 * Constructor for presenter.
	 */
	public DungeonSelectPresenter() {
		IEventManager eventManager = ServiceManager.getEventManager();
		eventManager.addHandler(ReasonForActionEvent.getReasonForActionEventType(), new ReasonForActionEventHandler() {
			public void onReasonForAction(final ReasonForActionEvent event) {
				if (event.getReasonForAction() == ReasonForAction.DungeonDataDeleted) {
					refreshView();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataLoaded) {
					refreshView();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.DungeonDataCreated) {
					refreshView();
					return;
				}
				if (event.getReasonForAction() == ReasonForAction.SessionListChanged) {
					refreshSessionData();
					return;
				}
			}
		});
	}

	/**
	 * Refresh the view.
	 */
	public void refreshView() {
		resetDungeonLogic();
		view.loadDungeonList();
		view.setToDungeonMasterState();
		refreshSession();
	}

	/**
	 * Reset logic for dungeon.
	 */
	private void resetDungeonLogic() {
		okToCreateDungeon = false;
		okToDelete = false;
		templateSelected = false;
		newDungeonName = "";
		selectedDungeonUUID = "";
	}

	/**
	 * refresh session information.
	 */
	private void refreshSession() {
		resetSessionLogic();
		refreshSessionData();
	}

	/**
	 * reset session logic.
	 */
	private void resetSessionLogic() {
		isValidDungeonForSessions = false;
		okToCreateSession = false;
		sessionSelected = false;
		okToDeleteSession = false;
		okToDMSession = false;
		okToJoinSession = false;
	}

	/**
	 * refresh session data.
	 */
	protected void refreshSessionData() {
		view.loadSessionList();
	}

	/**
	 * Set view for presenter.
	 * 
	 * @param dungeonSelectControl view for presenter.
	 */
	public void setView(final DungeonSelectDialog dungeonSelectControl) {
		view = dungeonSelectControl;
	}

	/**
	 * Get map of dungeons to UUIDs.
	 * 
	 * @return map of dungeons to UUIDs.
	 */
	public Map<String, String> getDungeonToUUIDMap() {
		return ServiceManager.getDungeonManager().getDungeonToUUIDMap();
	}

	/**
	 * Get a list of session data.
	 * 
	 * @return list of session data.
	 */
	public SessionListData getSessionListData() {
		return ServiceManager.getDungeonManager().getSessionListData();
	}

	/**
	 * Select a new dungeon.
	 * 
	 * @param dungeonName name of dungeon
	 * @param dungeonUUID UUID of dungeon.
	 */
	public void selectNewDungeonName(final String dungeonName, final String dungeonUUID) {
		resetSessionLogic();
		resetDungeonLogic();
		templateSelected = !dungeonName.startsWith("Select ");
		selectedDungeonUUID = dungeonUUID;
		if (templateSelected) {
			okToDelete = ServiceManager.getDungeonManager().okToDeleteThisTemplate(dungeonUUID);
			isValdidDungeonTemplateForSessions(dungeonName);
		}
		if (isValidDungeonForSessions) {
			ServiceManager.getDungeonManager().getSessionList(dungeonUUID);
		}
		view.setToDungeonMasterState();
	}

	/**
	 * Select this session.
	 * 
	 * @param sessionName session name to select.
	 * @param sessionUUID UUID of session to select.
	 */
	public void selectSessionName(final String sessionName, final String sessionUUID) {
		newSessionName = sessionName;
		newSessionUUID = sessionUUID;
		okToDeleteSession = !newSessionName.startsWith("Select ");
		okToDMSession = okToDeleteSession;
		okToJoinSession = okToDeleteSession;
		view.setToDungeonMasterState();
	}

	/**
	 * Is this dungeon template ok to have sessions?
	 * 
	 * @param dungeonName dungeon name to check.
	 */
	private void isValdidDungeonTemplateForSessions(final String dungeonName) {
		isValidDungeonForSessions = !dungeonName.startsWith("Select ") && !dungeonName.startsWith("Template ");
	}

	/**
	 * Edit the selected dungeon.
	 */
	public void editDungeon() {
		ServiceManager.getDungeonManager().editSelectedDungeonUUID(selectedDungeonUUID);
		view.close();
	}

	/**
	 * Check new dungeon name text.
	 * 
	 * @param newDungeonName new dungeon name
	 */
	public void newDungeonNameText(final String newDungeonName) {
		okToCreateDungeon = !newDungeonName.startsWith("Enter ") && newDungeonName.length() > 4;
		this.newDungeonName = newDungeonName;
		view.setToDungeonMasterState();
	}

	/**
	 * Check new session name text.
	 * 
	 * @param newSessionName new session name.
	 */
	public void newSessionNameText(final String newSessionName) {
		okToCreateSession = ServiceManager.getDungeonManager().isNameValidForNewSession(newSessionName);
		this.newSessionName = newSessionName;
		view.setToDungeonMasterState();
	}

	/**
	 * Create a new dungeon.
	 */
	public void createDungeon() {
		ServiceManager.getDungeonManager().createNewDungeon(newDungeonName);
		view.resetNewDungeonName();
	}

	/**
	 * Create a new session.
	 */
	public void createSession() {
		ServiceManager.getDungeonManager().createNewSession(selectedDungeonUUID, newSessionName);
		okToCreateSession = false;
		view.resetNewSessionText();
	}

	/**
	 * Delete a dungeon template.
	 */
	public void deleteTemplate() {
		ServiceManager.getDungeonManager().deleteTemplate(selectedDungeonUUID);
	}

	/**
	 * Join a session.
	 */
	public void joinSession() {
		ServiceManager.getDungeonManager().joinSession(selectedDungeonUUID, newSessionUUID);
		view.close();
	}

	/**
	 * DM a session.
	 */
	public void dmSession() {
		ServiceManager.getDungeonManager().dmSession(selectedDungeonUUID, newSessionUUID);
		view.close();
	}

	/**
	 * Delete a session.
	 */
	public void deleteSession() {
		ServiceManager.getDungeonManager().deleteSession(selectedDungeonUUID, newSessionUUID);
		okToDeleteSession = false;
	}

	/**
	 * View is closing.
	 */
	public void close() {
	}
}
