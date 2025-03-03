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
package per.lambert.ebattleMat.client.services.serviceData;

import com.google.gwt.core.client.JavaScriptObject;

/**
 * Login response from server.
 * 
 * @author LLambert
 *
 */
public class LoginResponseData extends JavaScriptObject {
	/**
	 * COnstructor.
	 */
	protected LoginResponseData() {
	}

	/**
	 * get error from login.
	 * 
	 * @return non-zero if error
	 */
	public final native int getError() /*-{
		return this.error;
	}-*/; // (3)

	/**
	 * set error code.
	 * 
	 * @param error code
	 */
	public final native void setError(int error) /*-{
		this.error = error;
	}-*/; // (3)

	/**
	 * get user token.
	 * 
	 * This needs to be used in all future requests.
	 * 
	 * @return user token.
	 */
	public final native int getToken() /*-{
		return this.token;
	}-*/; // (3)

	/**
	 * set token code.
	 * 
	 * @param token code
	 */
	public final native void setToken(int token) /*-{
		this.token = token;
	}-*/; // (3)
}
