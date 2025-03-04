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

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.fileupload.FileItemIterator;
import org.apache.commons.fileupload.FileItemStream;
import org.apache.commons.fileupload.servlet.ServletFileUpload;

import per.lambert.ebattleMat.server.IWebRequestHandler;

/**
 * File upload handler.
 * 
 * @author LLambert
 *
 */
public class FileUploadHandler implements IWebRequestHandler {
	/**
	 * {@inheritDoc}
	 */
	@Override
	public void handleRequest(final HttpServletRequest request, final HttpServletResponse response, final HttpServlet servlet, final String jsonData) throws ServletException, IOException {
		ServletFileUpload upload = new ServletFileUpload();
		response.setContentType("text/plain");
		String filePath = request.getParameter("filePath");
		FileOutputStream fileOutSt = null;
		try {
			FileItemIterator iter = upload.getItemIterator(request);
			while (iter.hasNext()) {
				FileItemStream item = iter.next();
				InputStream stream = item.openStream();

				String name = servlet.getServletContext().getRealPath(filePath);
				File file = new File(name);
				file.delete();
				fileOutSt = new FileOutputStream(name);
				int len;
				byte[] buffer = new byte[8192];
				while ((len = stream.read(buffer, 0, buffer.length)) != -1) {
					fileOutSt.write(buffer, 0, len);
				}
				fileOutSt.close();
				fileOutSt = null;
		}
		} catch (Exception e) {
			throw new RuntimeException(e);
		} finally {
			if (fileOutSt != null) {
				fileOutSt.close();
			}
		}

	}

}
