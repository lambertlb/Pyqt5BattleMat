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
package per.lambert.ebattleMat.client.services.serviceData;

import com.google.gwt.core.client.JavaScriptObject;

/**
 * Fog of war data.
 * @author LLambert
 *
 */
public class FogOfWarData extends JavaScriptObject {
	/**
	 * Constructor for fog of war data.
	 */
	protected FogOfWarData() {
	}

	/**
	 * get fog of war.
	 * @return data for fog of war.
	 */
	public final native int[] getFOW() /*-{
		if (this.fogOfWar === undefined) {
			return (null);
		}
		return (this.fogOfWar);
	}-*/;

	/**
	 * Set fog of war data.
	 * @param fogOfWar data.
	 */
	public final native void setFOW(long[] fogOfWar) /*-{
		this.fogOfWar = fogOfWar;
	}-*/;
}
