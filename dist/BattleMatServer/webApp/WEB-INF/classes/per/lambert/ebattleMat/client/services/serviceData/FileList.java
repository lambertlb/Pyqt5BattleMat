/*
 * Copyright (C) 2023 Leon Lambert.
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
 * Java script class with response data from file lister.
 * 
 * @author llambert
 *
 */
public class FileList extends JavaScriptObject {
	/**
	 * Constructor.
	 */
	protected FileList() {
	}
	/**
	 * Get path of files.
	 * 
	 * @return path of files
	 */
	public final native String getFilePath() /*-{
		if (this.filePath === undefined) {
			this.filePath = "";
		}
		return (this.filePath);
	}-*/;
	/**
	 * get File names.
	 * 
	 * @return file names
	 */
	public final native String[] getFileNames() /*-{
		if (this.fileNames === undefined) {
			this.fileNames = [];
		}
		return (this.fileNames);
	}-*/;

}
