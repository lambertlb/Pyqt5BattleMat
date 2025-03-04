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
package per.lambert.ebattleMat.client.services;

import per.lambert.ebattleMat.client.interfaces.IDataRequester;
import per.lambert.ebattleMat.client.interfaces.IDungeonManager;
import per.lambert.ebattleMat.client.interfaces.IEventManager;

/**
 * Service manager.
 * 
 * Used to gain access to all available services. This is used so unit test can switch in mocks for testing.
 * 
 * @author LLambert
 *
 */
public final class ServiceManager {
	/**
	 * Event manager.
	 */
	private static IEventManager eventManager;

	/**
	 * get instance of event manager.
	 * 
	 * @return event manager
	 */
	public static IEventManager getEventManager() {
		if (eventManager == null) {
			eventManager = new EventManager();
		}
		return (eventManager);
	}

	/**
	 * set event manager for unit test.
	 * 
	 * @param eventManager for test
	 */
	public static void setEventManagerForUnitTest(final IEventManager eventManager) {
		ServiceManager.eventManager = eventManager;
	}

	/**
	 * dungeon manager.
	 */
	private static IDungeonManager dungeonManager;

	/**
	 * Get instance of dungeon manager.
	 * 
	 * @return dungeon manager.
	 */
	public static IDungeonManager getDungeonManager() {
		if (dungeonManager == null) {
			dungeonManager = new DungeonManager();
		}
		return (dungeonManager);
	}

	/**
	 * data requester.
	 */
	private static IDataRequester dataRequester;

	/**
	 * set requester or unit test.
	 * 
	 * @param dataRequester for test
	 */
	public static void setDataRequesterForUnitTest(final IDataRequester dataRequester) {
		ServiceManager.dataRequester = dataRequester;
	}

	/**
	 * get instance of data requester.
	 * 
	 * @return data requester.
	 */
	public static IDataRequester getDataRequester() {
		if (dataRequester == null) {
			dataRequester = new DataRequester();
		}
		return (dataRequester);
	}

	/**
	 * Constructor.
	 */
	private ServiceManager() {
	}
}
