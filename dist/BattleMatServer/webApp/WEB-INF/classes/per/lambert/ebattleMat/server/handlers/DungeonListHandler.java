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
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

import per.lambert.ebattleMat.server.DungeonsManager;
import per.lambert.ebattleMat.server.IWebRequestHandler;

/**
 * Handler for getting a dungeon list.
 * @author LLambert
 *
 */
public class DungeonListHandler implements IWebRequestHandler {
	/**
	 * Response for getting a dungeon list.
	 * @author LLambert
	 *
	 */
	private final class DungeonListResponseData {
		/**
		 * array of dungeon names.
		 */
		private String[] dungeonNames;
		/**
		 * array of uuids.
		 */
		private String[] dungeonUUIDS;
		/**
		 * array of directories the dungeons are in.
		 */
		private String[] dungeonDirectories;
		/**
		 * Handle the request.
		 * @param dungeonListData map of dungeons and UUIDS
		 * @param dungeonDirectoryData map of dungeon and directory names
		 */
		private DungeonListResponseData(final Map<String,String> dungeonListData, final Map<String,String> dungeonDirectoryData) {
			dungeonNames = new String[dungeonListData.size()];
			dungeonUUIDS = new String[dungeonListData.size()];
			dungeonDirectories = new String[dungeonListData.size()];
			int i = 0;
			for (Map.Entry<String, String> entry : dungeonListData.entrySet()) {
				dungeonNames[i] = entry.getValue();
				dungeonUUIDS[i] =  entry.getKey();
				++i;
			}
			i = 0;
			for (Map.Entry<String, String> entry : dungeonDirectoryData.entrySet()) {
				dungeonDirectories[i] = entry.getValue();
				++i;
			}
		}
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public void handleRequest(final HttpServletRequest request, final HttpServletResponse resp, final HttpServlet servlet, final String jsonData) throws ServletException, IOException {
		DungeonsManager.getDungeonListData(servlet);
		DungeonListResponseData dungeonListResponseData = new DungeonListResponseData(DungeonsManager.getDungeonNameToUUIDMap(), DungeonsManager.getUuidTemplatePathMap());
		Gson gson = new Gson();
		String responseDataString = gson.toJson(dungeonListResponseData);
		PrintWriter out = resp.getWriter();
		out.print(responseDataString);
		out.flush();
	}

}
