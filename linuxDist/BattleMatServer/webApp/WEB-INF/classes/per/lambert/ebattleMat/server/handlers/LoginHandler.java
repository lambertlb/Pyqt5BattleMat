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

import per.lambert.ebattleMat.server.IWebRequestHandler;
import per.lambert.ebattleMat.server.serviceData.ServiceResponseData;

/**
 * Login handler.
 * 
 * @author LLambert
 *
 */
public class LoginHandler implements IWebRequestHandler {
	/**
	 * Response data for login.
	 * @author LLambert
	 *
	 */
	private final class LoginResponseData extends ServiceResponseData {
		/**
		 * Token for user.
		 */
		@SuppressWarnings("unused")
		private int token;

		/**
		 * Set token.
		 * @param token to set
		 */
		public void setToken(final int token) {
			this.token = token;
		}
	}

	/**
	 * {@inheritDoc}
	 * 
	 */
	@Override
	public final void handleRequest(final HttpServletRequest request, final HttpServletResponse resp,
			final HttpServlet servlet, final String jsonData) throws ServletException, IOException {
		LoginResponseData responseData = new LoginResponseData();
		String username = request.getParameter("username");
		String password = request.getParameter("password");
		if (username == null || username == "" || password == null || password == "") {
			responseData.setError(1);
		} else {
			responseData.setToken(username.hashCode());
		}
		Gson gson = new Gson();
		String responseDataString = gson.toJson(responseData);

		PrintWriter out = resp.getWriter();
		out.print(responseDataString);
		out.flush();

	}

}
