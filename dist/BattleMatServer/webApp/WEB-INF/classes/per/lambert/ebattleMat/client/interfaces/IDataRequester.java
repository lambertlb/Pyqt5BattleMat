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
package per.lambert.ebattleMat.client.interfaces;

import java.util.Map;

/**
 * interface for handling a web request.
 * 
 * @author LLambert
 *
 */
public interface IDataRequester {
	/**
	 * handle web request.
	 * 
	 * @param requestData request data
	 * @param requestType request type
	 * @param parameters for request
	 * @param callback user callback.
	 */
	void requestData(String requestData, String requestType, Map<String, String> parameters, IUserCallback callback);

	/**
	 * Get path to service.
	 * 
	 * @return path to service
	 */
	String getWebPath();

	/**
	 * Build the URL for this request type. This will add the following additional parameters.
	 * 
	 * @param requestType request type to server
	 * @param parameters parameters for the request
	 * @return URL for server
	 */
	String buildUrl(String requestType, Map<String, String> parameters);
}
