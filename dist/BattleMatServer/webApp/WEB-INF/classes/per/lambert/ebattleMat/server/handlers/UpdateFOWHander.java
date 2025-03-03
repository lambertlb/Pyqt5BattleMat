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

/**
 * Handle update fog of war request.
 * 
 * @author LLambert
 *
 */
public class UpdateFOWHander implements IWebRequestHandler {
	/**
	 * Worker class for converting fog of war JSON data.
	 * 
	 * @author LLambert
	 *
	 */
	private final class FogOfWarData {
		/**
		 * Fog of war data.
		 */
		private long[] fogOfWar;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void handleRequest(final HttpServletRequest request, final HttpServletResponse resp, final HttpServlet servlet, final String jsonData) throws ServletException, IOException {
		String sessionUUID = request.getParameter("sessionUUID");
		int currentLevel = Integer.parseInt(request.getParameter("currentLevel"));
		Gson gson = new Gson();
		FogOfWarData fowData = gson.fromJson(jsonData, FogOfWarData.class);
		DungeonsManager.updateFOW(servlet, sessionUUID, currentLevel, fowData.fogOfWar);
		PrintWriter out = resp.getWriter();
		out.print("");
		out.flush();
	}

}
