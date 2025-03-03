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

import java.io.IOException;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * interface that all web requests.
 * Must inherit from to add a new request.
 * 
 * @author LLambert
 * 
 */
public interface IWebRequestHandler {
	/**
	 * Handle request.
	 * @param request to handle
	 * @param response servlet response
	 * @param servlet servlet data
	 * @param jsonData JSON Data
	 * @throws ServletException Servlet Exception
	 * @throws IOException if there is an error
	 */
	void handleRequest(HttpServletRequest request, HttpServletResponse response, HttpServlet servlet, String jsonData)
			throws ServletException, IOException;
}
