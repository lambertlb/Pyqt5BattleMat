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
package per.lambert.ebattleMat.client.services;

import java.util.Iterator;
import java.util.Map;

import com.google.gwt.http.client.Request;
import com.google.gwt.http.client.RequestBuilder;
import com.google.gwt.http.client.RequestCallback;
import com.google.gwt.http.client.RequestException;
import com.google.gwt.http.client.Response;
import com.google.gwt.http.client.UrlBuilder;
import com.google.gwt.user.client.Window.Location;

import per.lambert.ebattleMat.client.interfaces.DungeonServerError;
import per.lambert.ebattleMat.client.interfaces.IDataRequester;
import per.lambert.ebattleMat.client.interfaces.IErrorInformation;
import per.lambert.ebattleMat.client.interfaces.IUserCallback;

/**
 * Low level class to manage messages between client and server.
 * 
 * @author LLambert
 *
 */
public class DataRequester implements IDataRequester {
	/**
	 * Path to web service.
	 */
	private String webPath;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void requestData(final String requestData, final String requestType, final Map<String, String> parameters, final IUserCallback callback) {
		String url = buildUrl(requestType, parameters);
		RequestBuilder builder = new RequestBuilder(RequestBuilder.POST, url);
		try {
			builder.sendRequest(requestData, new RequestCallback() {
				// (i) callback handler when there is an error
				public void onError(final Request request, final Throwable exception) {
					handleCallbackError(DungeonServerError.Undefined1, null, callback);
				}

				@Override
				public void onResponseReceived(final Request request, final Response response) {
					if (Response.SC_OK == response.getStatusCode()) {
						callback.onSuccess(this, response.getText());
					} else {
						handleCallbackError(DungeonServerError.Undefined1, null, callback);
					}
				}
			});
		} catch (RequestException e) {
			handleCallbackError(DungeonServerError.Undefined1, e, callback);
		}
	}

	/**
	 * Build the URL for this request type.
	 * 
	 * This will add the following additional parameters. Token is authorization token for this login request is the request to the server
	 * 
	 * @param requestType request type to server
	 * @param parameters parameters for the request
	 * @return URL for server
	 */
	@Override
	public String buildUrl(final String requestType, final Map<String, String> parameters) {
		parameters.put("token", "" + ServiceManager.getDungeonManager().getToken());
		parameters.put("request", "" + requestType);
		String url = constructURL(parameters, "electronicbattlemat/dungeons");
		return url;
	}

	/**
	 * Construct url to service.
	 * 
	 * @param parameters parameters to use
	 * @param additional addition to url
	 * @return URL
	 */
	private String constructURL(final Map<String, String> parameters, final String additional) {
		final UrlBuilder urlBuilder = new UrlBuilder();
		urlBuilder.setProtocol(Location.getProtocol());
		urlBuilder.setHost(Location.getHost());
		String port = Location.getPort();
		if (port != null && !port.isEmpty()) {
			urlBuilder.setPort(Integer.parseInt(port));
		}
		urlBuilder.setPath(constructPath() + additional);
		if (parameters != null) {
			addParametersToURL(parameters, urlBuilder);
		}
		String url = urlBuilder.buildString();
		return url;
	}

	/**
	 * Get proper web path.
	 * 
	 * @return proper web path
	 */
	private String constructPath() {
		String path = Location.getPath();
		if (path.toLowerCase().endsWith(".html")) {
			int index = path.lastIndexOf("/");
			path = path.substring(0, index + 1);
		}
		return path;
	}

	/**
	 * Get path to service.
	 * 
	 * @return path to service
	 */
	@Override
	public String getWebPath() {
		if (webPath == null) {
			webPath = constructURL(null, "");
		}
		return (webPath);
	}

	/**
	 * Handle callback with error.
	 * 
	 * @param dungeonError error from server
	 * @param exception if one was thrown
	 * @param userCallback user callback
	 */
	private void handleCallbackError(final DungeonServerError dungeonError, final Throwable exception, final IUserCallback userCallback) {
		userCallback.onError(this, new IErrorInformation() {
			@Override
			public Throwable getException() {
				return exception;
			}

			@Override
			public DungeonServerError getError() {
				return dungeonError;
			}

			@Override
			public String getErrorMessage() {
				if (exception != null) {
					return (exception.getMessage());
				}
				return "";
			}
		});
	}

	/**
	 * Add parameters to URL.
	 * 
	 * @param parameters parameters for url
	 * @param urlBuilder url builder
	 */
	private static void addParametersToURL(final Map<String, String> parameters, final UrlBuilder urlBuilder) {
		if (parameters != null) {
			Iterator<Map.Entry<String, String>> contactIterator = parameters.entrySet().iterator();
			while (contactIterator.hasNext()) {
				Map.Entry<String, String> anEntry = contactIterator.next();
				String parameter = anEntry.getKey();
				String value = anEntry.getValue();
				urlBuilder.setParameter(parameter, value);
			}
		}
	}

}
