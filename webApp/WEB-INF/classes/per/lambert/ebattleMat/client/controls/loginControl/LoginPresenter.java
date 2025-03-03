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
package per.lambert.ebattleMat.client.controls.loginControl;

import per.lambert.ebattleMat.client.event.ReasonForActionEvent;
import per.lambert.ebattleMat.client.interfaces.DungeonServerError;
import per.lambert.ebattleMat.client.interfaces.IDungeonManager;
import per.lambert.ebattleMat.client.interfaces.IErrorInformation;
import per.lambert.ebattleMat.client.interfaces.IUserCallback;
import per.lambert.ebattleMat.client.interfaces.ReasonForAction;
import per.lambert.ebattleMat.client.services.ServiceManager;

/**
 * Login control presenter.
 * 
 * @author LLambert
 *
 */
public class LoginPresenter {

	/**
	 * View to manage.
	 */
	private LoginControl view;

	/**
	 * Message about login.
	 */
	private String message = "";

	/**
	 * Get message.
	 * 
	 * @return message
	 */
	public String getMessage() {
		return message;
	}

	/**
	 * set message.
	 * 
	 * @param message to set
	 */
	public void setMessage(final String message) {
		this.message = message;
	}

	/**
	 * User name.
	 */
	private String username;

	/**
	 * get user name.
	 * 
	 * @return user name
	 */
	public String getUsername() {
		return username;
	}

	/**
	 * Set user name.
	 * 
	 * @param username to set
	 */
	public void setUsername(final String username) {
		this.username = username;
	}

	/**
	 * password.
	 */
	private String password;

	/**
	 * get password.
	 * 
	 * @return password
	 */
	public String getPassword() {
		return password;
	}

	/**
	 * Set password.
	 * 
	 * @param password to set
	 */
	public void setPassword(final String password) {
		this.password = password;
	}

	/**
	 * Is enabled.
	 */
	private boolean isEnabled;

	/**
	 * get is enabled.
	 * 
	 * @return is enabled
	 */
	public boolean getIsEnabled() {
		return isEnabled;
	}

	/**
	 * Set is enabled.
	 * 
	 * @param isEnabled if set
	 */
	public void setIsEnabled(final boolean isEnabled) {
		this.isEnabled = isEnabled;
	}

	/**
	 * Set view.
	 * 
	 * @param view to set
	 */
	public void setView(final LoginControl view) {
		this.view = view;
	}

	/**
	 * Ok button pressed.
	 */
	public void ok() {
		setIsEnabled(false);
		view.update();
		final IDungeonManager dungeonManagement = ServiceManager.getDungeonManager();

		dungeonManagement.login(username, password, new IUserCallback() {
			public void onError(final Object sender, final IErrorInformation error) {
				loginComplete("Login Fail");
			}

			public void onSuccess(final Object sender, final Object data) {
				if (dungeonManagement.getLastError() == DungeonServerError.Succsess) {
					view.close();
					ServiceManager.getEventManager().fireEvent(new ReasonForActionEvent(ReasonForAction.Login, null));
				} else {
					loginComplete("Login Fail");
				}
			}
		});
	}

	/**
	 * Login complete.
	 * 
	 * @param message to display on view
	 */
	void loginComplete(final String message) {
		setMessage(message);
		setIsEnabled(true);
		view.update();
	}
}
