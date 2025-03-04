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
package per.lambert.ebattleMat.server.handlers;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

import per.lambert.ebattleMat.server.DungeonsManager;
import per.lambert.ebattleMat.server.IWebRequestHandler;

import java.util.Map;

/**
 * Handler for session list request.
 * @author LLambert
 *
 */
public class SessionListHandler implements IWebRequestHandler {
	/**
	 * response data for session list.
	 * @author LLambert
	 *
	 */
	private final class SessionListResponseData {
		/**
		 * dungeon UUID.
		 */
		@SuppressWarnings("unused")
		private String dungeonUUID;
		/**
		 * Session names.
		 */
		private String[] sessionNames;
		/**
		 * UUID for session names.
		 */
		private String[] sessionUUIDs;
		/**
		 * Constructor.
		 * @param sessionListData collection of session information
		 * @param dungeonUUID for session
		 */
		private SessionListResponseData(final Map<String,String> sessionListData, final String dungeonUUID) {
			this.dungeonUUID = dungeonUUID;
			sessionNames = new String[sessionListData.size()];
			sessionUUIDs = new String[sessionListData.size()];
			int i = 0;
			for (Map.Entry<String, String> entry : sessionListData.entrySet()) {
				sessionNames[i] = entry.getKey();
				sessionUUIDs[i] =  entry.getValue();
				++i;
			}
		}
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public void handleRequest(final HttpServletRequest request, final HttpServletResponse resp, final HttpServlet servlet, final String jsonData) throws ServletException, IOException {
		String dungeonUUID = request.getParameter("dungeonUUID");
		SessionListResponseData sessionListResponseData = new SessionListResponseData(DungeonsManager.getSessionListData(servlet, dungeonUUID), dungeonUUID);
		Gson gson = new Gson();
		String responseDataString = gson.toJson(sessionListResponseData);

		PrintWriter out = resp.getWriter();
		out.print(responseDataString);
		out.flush();
	}

}
