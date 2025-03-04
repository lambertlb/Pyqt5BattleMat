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
package per.lambert.ebattleMat.server;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import per.lambert.ebattleMat.server.handlers.AddOrUpdatePogHandler;
import per.lambert.ebattleMat.server.handlers.CreateNewDungeonHandler;
import per.lambert.ebattleMat.server.handlers.CreateNewSessionHandler;
import per.lambert.ebattleMat.server.handlers.DeleteDungeonHandler;
import per.lambert.ebattleMat.server.handlers.DeleteFile;
import per.lambert.ebattleMat.server.handlers.DeletePogHandler;
import per.lambert.ebattleMat.server.handlers.DeleteSessionHandler;
import per.lambert.ebattleMat.server.handlers.DungeonListHandler;
import per.lambert.ebattleMat.server.handlers.FileLister;
import per.lambert.ebattleMat.server.handlers.FileUploadHandler;
import per.lambert.ebattleMat.server.handlers.LoadJsonDataHandler;
import per.lambert.ebattleMat.server.handlers.LoadSessionHandler;
import per.lambert.ebattleMat.server.handlers.LoginHandler;
import per.lambert.ebattleMat.server.handlers.SaveJsonDataHandler;
import per.lambert.ebattleMat.server.handlers.SessionListHandler;
import per.lambert.ebattleMat.server.handlers.UpdateFOWHander;

/**
 * Servlet exposed to outside.
 * @author LLambert
 *
 */
public class Dungeons extends HttpServlet {
	private static final long serialVersionUID = 1L;
	/**
	 * Collection of services exposed.
	 * 
	 * This is a map of service request id with instances of request handlers.
	 */
	private Map<String, IWebRequestHandler> webServices;
	/**
	 * Constructor for servlet.
	 */
	public Dungeons() {
		webServices = new HashMap<String, IWebRequestHandler>();
		webServices.put("LOGIN", new LoginHandler());
		webServices.put("LOADJSONFILE", new LoadJsonDataHandler());
		webServices.put("SAVEJSONFILE", new SaveJsonDataHandler());
		webServices.put("GETDUNGEONLIST", new DungeonListHandler());
		webServices.put("CREATENEWDUNGEON", new CreateNewDungeonHandler());
		webServices.put("DELETEDUNGEON", new DeleteDungeonHandler());
		webServices.put("GETSESSIONLIST", new SessionListHandler());
		webServices.put("CREATENEWSESSION", new CreateNewSessionHandler());
		webServices.put("DELETESESSION", new DeleteSessionHandler());
		webServices.put("LOADSESSION", new LoadSessionHandler());
		webServices.put("UPDATEFOW", new UpdateFOWHander());
		webServices.put("FILEUPLOAD", new FileUploadHandler());
		webServices.put("ADDORUPDATEPOG", new AddOrUpdatePogHandler());
		webServices.put("DELETEPOG", new DeletePogHandler());
		webServices.put("FILELISTER", new FileLister());
		webServices.put("DELETEFILE", new DeleteFile());
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void doPost(final HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
		// first, set the "content type" header of the response
		response.setContentType("application/xml");
		handlePostRequest(request, response, webServices, this);
	}
	/**
	 * Handle a service request.
	 * @param request to process
	 * @param response to return
	 * @param webServices handler to call
	 * @param servlet servlet data
	 * @throws ServletException if error
	 * @throws IOException if error
	 */
	public void handlePostRequest(final HttpServletRequest request, final HttpServletResponse response, final Map<String, IWebRequestHandler> webServices, final HttpServlet servlet) throws ServletException, IOException {
		String contentType = request.getContentType();
		StringBuffer jb = new StringBuffer();
		if (contentType.startsWith("text")) {
			String line = null;
			try {
				BufferedReader reader = request.getReader();
				while ((line = reader.readLine()) != null) {
					jb.append(line);
				}
			} catch (Exception e) {
				throw new ServletException();
			}
		}
		String command = request.getParameter("request");
		if (command == null) {
			throw new ServletException();
		}
		if (!command.equalsIgnoreCase("LOGIN")) {
			validateToken(request);
		}
		IWebRequestHandler handler = webServices.get(command);
		if (handler != null) {
			handler.handleRequest(request, response, servlet, jb.toString());
			return;
		}
	}

	/**
	 * Validate user token.
	 * 
	 * @param request with token
	 * @throws ServletException if error
	 */
	private void validateToken(final HttpServletRequest request) throws ServletException {
//		int token = Integer.parseUnsignedInt(request.getParameter("token"));
//		if (token == 0) {
//			throw new ServletException();
//		}
	}
}
