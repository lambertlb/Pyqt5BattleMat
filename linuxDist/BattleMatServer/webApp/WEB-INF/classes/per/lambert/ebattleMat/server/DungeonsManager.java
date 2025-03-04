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
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.HashMap;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;
import java.util.UUID;
import java.util.concurrent.locks.ReentrantLock;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;

import org.apache.commons.io.FileUtils;

import com.google.gson.Gson;

import per.lambert.ebattleMat.client.interfaces.Constants;
import per.lambert.ebattleMat.client.interfaces.PogPlace;
import per.lambert.ebattleMat.server.serviceData.DungeonData;
import per.lambert.ebattleMat.server.serviceData.DungeonLevel;
import per.lambert.ebattleMat.server.serviceData.DungeonSessionData;
import per.lambert.ebattleMat.server.serviceData.DungeonSessionLevel;
import per.lambert.ebattleMat.server.serviceData.PogData;
import per.lambert.ebattleMat.server.serviceData.PogList;

/**
 * Manager for dungeon information.
 * 
 * This is a static class that serves as a central handlers for all service requests.
 * 
 * It does a lock on the data so requests are serialized. This means that if two people make changes to the same dungeon data then last one wins. This will also cache session data to minimize the amount of data being accessed on disk.
 * 
 * @author LLambert
 *
 */
public final class DungeonsManager {
	/**
	 * lock used to manage concurrency.
	 */
	private static ReentrantLock lock = new ReentrantLock();
	/**
	 * Map of dungeon UUIDs to dungeon directory path.
	 */
	private static Map<String, String> uuidTemplatePathMap = new HashMap<String, String>();

	/**
	 * get Map of dungeon UUIDs to dungeon directory path.
	 * 
	 * @return Map of dungeon UUIDs to dungeon directory path
	 */
	public static Map<String, String> getUuidTemplatePathMap() {
		return uuidTemplatePathMap;
	}

	/**
	 * cache of sessions.
	 */
	private static Map<String, SessionInformation> sessionCache = new HashMap<String, SessionInformation>();
	/**
	 * Timer for periodic tasks.
	 */
	private static Timer timer;
	/**
	 * map of dungeon names to UUIDs.
	 */
	private static Map<String, String> dungeonNameToUUIDMap = new HashMap<String, String>();

	/**
	 * get map of dungeon names to UUIDs.
	 * 
	 * @return map of dungeon names to UUIDs.
	 */
	public static Map<String, String> getDungeonNameToUUIDMap() {
		return dungeonNameToUUIDMap;
	}

	/**
	 * used to initialize static data. This forces the initialization code to run when this class is loaded the first time.
	 */
	@SuppressWarnings("unused")
	private static boolean initialized = initializeDungeonManager();

	/**
	 * Hide constructor because this is a singleton.
	 */
	private DungeonsManager() {
	}

	/**
	 * initialize dungeon data.
	 * 
	 * @return boolean to make sure this is called at class load.
	 */
	private static boolean initializeDungeonManager() {
		TimerTask repeatedTask = new TimerTask() {
			public void run() {
				DungeonsManager.periodicTimer();
			}
		};
		timer = new Timer("Timer");

		long delay = 5000L;
		long period = 5000L;
		timer.scheduleAtFixedRate(repeatedTask, delay, period);
		return true;
	}

	/**
	 * Periodic tasks.
	 */
	private static void periodicTimer() {
		lock.lock();
		try {
			checkIfTimeToSaveSessionData();
			checkIfNeedToPurgeCachedData();
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Check if session data needs to be saved because it is dirty.
	 */
	private static void checkIfTimeToSaveSessionData() {
		for (SessionInformation sessionInformation : sessionCache.values()) {
			sessionInformation.saveIfDirty();
		}
	}

	/**
	 * Purge out old data that is not being used anymore.
	 * 
	 * There might be sessions that are over so no reason to hold onto data.
	 */
	private static void checkIfNeedToPurgeCachedData() {
	}

	/**
	 * Save dungeon data.
	 * 
	 * @param request to send
	 * @param servlet servlet data
	 * @param dataToWrite data to write
	 * @throws IOException thrown if error
	 */
	public static void saveDungeonData(final HttpServletRequest request, final HttpServlet servlet, final String dataToWrite) throws IOException {
		String dungeonUUID = request.getParameter("dungeonUUID");
		if (dungeonUUID == null || dungeonUUID.isEmpty()) {
			return;
		}
		lock.lock();
		try {
			saveDungeonData(servlet, dataToWrite, dungeonUUID);
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Save dungeon data.
	 * 
	 * @param servlet servlet data
	 * @param dataToWrite data to write
	 * @param dungeonUUID dungeon UUID
	 * @throws IOException thrown if error
	 */
	private static void saveDungeonData(final HttpServlet servlet, final String dataToWrite, final String dungeonUUID) throws IOException {
		String filePath = uuidTemplatePathMap.get(dungeonUUID) + "/dungeonData.json";
		saveJsonFile(dataToWrite, servlet.getServletContext().getRealPath(filePath));
	}

	/**
	 * rebuild dungeon list.
	 * 
	 * @param servlet servlet data
	 */
	private static void rebuildDungeonList(final HttpServlet servlet) {
		uuidTemplatePathMap.clear();
		dungeonNameToUUIDMap.clear();
		getDungeonListData(servlet);
	}

	/**
	 * Get list of dungeons.
	 * 
	 * @param servlet servlet data
	 */
	public static void getDungeonListData(final HttpServlet servlet) {
		lock.lock();
		if (uuidTemplatePathMap.size() != 0) {
			lock.unlock();
			return;
		}
		try {
			String directoryPath = servlet.getServletContext().getRealPath(Constants.SERVER_DUNGEONS_LOCATION);
			File directory = new File(directoryPath);
			for (File possibleDungeon : directory.listFiles()) {
				if (possibleDungeon.isDirectory()) {
					getDungeonName(servlet, possibleDungeon);
				}
			}
		} catch (MalformedURLException e) {
		} catch (IOException e) {
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Get name of dungeon from dungeon data.
	 * 
	 * @param servlet servlet data
	 * @param possibleDungeon possible dungeon
	 * @throws IOException thrown if error
	 */
	private static void getDungeonName(final HttpServlet servlet, final File possibleDungeon) throws IOException {
		String directoryName = possibleDungeon.getName();
		DungeonData dungeonData = getDungeonData(servlet, directoryName);
		String dungeonName = dungeonData.getDungeonName();
		String uuid = dungeonData.getUuid();
		addToDungeonCache(directoryName, dungeonName, uuid);
	}

	/**
	 * Add dungeon to cache.
	 * 
	 * @param directoryName directory name
	 * @param dungeonName dungeon name
	 * @param uuid UUID of dungeon
	 */
	private static void addToDungeonCache(final String directoryName, final String dungeonName, final String uuid) {
		lock.lock();
		try {
			uuidTemplatePathMap.put(uuid, Constants.SERVER_DUNGEONS_LOCATION + directoryName);
			dungeonNameToUUIDMap.put(uuid, dungeonName);
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Get dungeon data.
	 * 
	 * @param servlet servlet data
	 * @param directoryName directory name
	 * @return dungeon data
	 * @throws IOException thrown if error
	 */
	private static DungeonData getDungeonData(final HttpServlet servlet, final String directoryName) throws IOException {
		String directoryPath = Constants.SERVER_DUNGEONS_LOCATION + directoryName;
		return getDungeonDataFromPath(servlet, directoryPath);
	}

	/**
	 * Get dungeon data from UUID.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID dungeon UUID
	 * @return dungeon data
	 * @throws IOException thrown if error
	 */
	private static DungeonData getDungeonDataFromUUID(final HttpServlet servlet, final String dungeonUUID) throws IOException {
		String directoryPath = uuidTemplatePathMap.get(dungeonUUID);
		return getDungeonDataFromPath(servlet, directoryPath);
	}

	/**
	 * Get dungeon data from path.
	 * 
	 * @param servlet servlet data
	 * @param directoryPath directory path
	 * @return dungeon data
	 * @throws IOException thrown if error
	 */
	private static DungeonData getDungeonDataFromPath(final HttpServlet servlet, final String directoryPath) throws IOException {
		String filePath = servlet.getServletContext().getRealPath(directoryPath + "/dungeonData.json");
		String jsonData = readJsonFile(filePath);
		Gson gson = new Gson();
		DungeonData dungeonData = gson.fromJson(jsonData, DungeonData.class);
		return (dungeonData);
	}

	/**
	 * Copy a template dungeon to make a new one.
	 * 
	 * @param servlet servlet data
	 * @param templateDungeonUUID template dungeon UUID
	 * @param newDungeonName name of new dungeon
	 * @throws IOException thrown if error
	 */
	public static void copyDungeon(final HttpServlet servlet, final String templateDungeonUUID, final String newDungeonName) throws IOException {
		lock.lock();
		try {
			String dstDirectory = newDungeonName.replaceAll("[^a-zA-Z0-9]", "_"); // get rid of garbage characters in name
			File srcDir = new File(servlet.getServletContext().getRealPath(uuidTemplatePathMap.get(templateDungeonUUID)));
			File destDir = new File(servlet.getServletContext().getRealPath(Constants.SERVER_DUNGEONS_LOCATION + dstDirectory));
			FileUtils.copyDirectory(srcDir, destDir);
			deleteAnyOldSessions(destDir);
			DungeonData dungeonData = getDungeonData(servlet, dstDirectory);
			dungeonData.setDungeonName(newDungeonName);
			UUID uuid = UUID.randomUUID();
			String uuidString = uuid.toString();
			dungeonData.setUuid(uuidString);
			addToDungeonCache(dstDirectory, newDungeonName, uuidString);
			Gson gson = new Gson();
			String jsonData = gson.toJson(dungeonData);
			saveDungeonData(servlet, jsonData, uuidString);
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Delete this dungeon.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon to delete
	 * @throws IOException thrown if error
	 */
	public static void deleteDungeon(final HttpServlet servlet, final String dungeonUUID) throws IOException {
		lock.lock();
		try {
			File srcDir = new File(servlet.getServletContext().getRealPath(uuidTemplatePathMap.get(dungeonUUID)));
			FileUtils.deleteDirectory(srcDir);
			rebuildDungeonList(servlet);
		} finally {
			lock.unlock();
		}
	}

	/**
	 * get dungeon data as a string.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon to read
	 * @return dungeon data as string
	 * @throws IOException thrown if error
	 */
	public static String getDungeonDataAsString(final HttpServlet servlet, final String dungeonUUID) throws IOException {
		lock.lock();
		try {
			if (!uuidTemplatePathMap.containsKey(dungeonUUID)) {
				return (null);
			}
			String filePath = servlet.getServletContext().getRealPath(uuidTemplatePathMap.get(dungeonUUID) + "/dungeonData.json");
			return (readJsonFile(filePath));
		} finally {
			lock.unlock();
		}
	}

	/**
	 * get a map of session data for this dungeon.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon with sessions
	 * @return map of session names vs UUIDs
	 */
	public static Map<String, String> getSessionListData(final HttpServlet servlet, final String dungeonUUID) {
		Map<String, String> sessionListData = new HashMap<String, String>();
		lock.lock();
		try {
			String sessionsPath = uuidTemplatePathMap.get(dungeonUUID) + Constants.SESSIONS_FOLDER;
			String directoryPath = servlet.getServletContext().getRealPath(sessionsPath);
			makeSureDirectoryExists(directoryPath);
			File directory = new File(directoryPath);
			for (File possibleSession : directory.listFiles()) {
				if (possibleSession.isDirectory()) {
					putSessionNameInCache(servlet, sessionsPath, possibleSession, sessionListData);
				}
			}
		} catch (MalformedURLException e) {
		} catch (IOException e) {
		} finally {
			lock.unlock();
		}
		return sessionListData;
	}

	/**
	 * Put session name into cache.
	 * 
	 * @param servlet servlet data
	 * @param sessionsPath session path
	 * @param possibleSession possible session
	 * @param sessionListData Map of session data
	 * @throws IOException thrown if error
	 */
	private static void putSessionNameInCache(final HttpServlet servlet, final String sessionsPath, final File possibleSession, final Map<String, String> sessionListData) throws IOException {
		SessionInformation sessionInformation = loadSessionInformation(possibleSession);
		DungeonSessionData sessionData = sessionInformation.getSessionData();
		sessionListData.put(sessionData.getSessionName(), sessionData.getSessionUUID());
	}

	/**
	 * Create a session for this dungeon.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon that needs the session
	 * @param newSessionName name of new session
	 * @throws IOException thrown if error
	 */
	public static void createSession(final HttpServlet servlet, final String dungeonUUID, final String newSessionName) throws IOException {
		lock.lock();
		try {
			String templateDirectory = servlet.getServletContext().getRealPath(uuidTemplatePathMap.get(dungeonUUID));
			String sessionDirectory = templateDirectory + Constants.SESSIONS_FOLDER + newSessionName.replaceAll("[^a-zA-Z0-9]", "_");
			makeSureDirectoryExists(sessionDirectory);
			DungeonData dungeonData = getDungeonDataFromUUID(servlet, dungeonUUID);
			DungeonSessionData sessionData = createSessionData(servlet, sessionDirectory, dungeonUUID, newSessionName, dungeonData);
			String filePath = sessionDirectory + "/" + "sessionData.json";
			SessionInformation sessionInformation = new SessionInformation(sessionData, filePath, sessionDirectory);
			sessionInformation.save();
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Create session data.
	 * 
	 * @param servlet servlet data
	 * @param sessionDirectory session directory
	 * @param dungeonUUID UUID of dungeon
	 * @param newSessionName new session name
	 * @param dungeonData dungeon data
	 * @return new session data
	 */
	private static DungeonSessionData createSessionData(final HttpServlet servlet, final String sessionDirectory, final String dungeonUUID, final String newSessionName, final DungeonData dungeonData) {
		UUID uuid = UUID.randomUUID();
		String uuidString = uuid.toString();
		DungeonSessionData newSessionData = new DungeonSessionData(newSessionName, dungeonUUID, uuidString);
		newSessionData.setSessionLevels(new DungeonSessionLevel[dungeonData.getDungeonLevels().length]);
		for (int i = 0; i < dungeonData.getDungeonLevels().length; ++i) {
			newSessionData.getSessionLevels()[i] = getSessionLevel(i, dungeonData, newSessionData);
		}
		return (newSessionData);
	}

	/**
	 * get new session data for this dungeon level.
	 * 
	 * @param level in dungeon
	 * @param dungeonData dungeon data
	 * @param newSessionData new session level
	 * @return session level
	 */
	private static DungeonSessionLevel getSessionLevel(final int level, final DungeonData dungeonData, final DungeonSessionData newSessionData) {
		DungeonSessionLevel sessionLevel = new DungeonSessionLevel(dungeonData.getDungeonLevels()[level]);
		return (sessionLevel);
	}

	/**
	 * Delete a session.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon with sessions
	 * @param sessionUUID UUID of session to delete
	 * @throws IOException thrown if error
	 */
	public static void deleteSession(final HttpServlet servlet, final String dungeonUUID, final String sessionUUID) throws IOException {
		lock.lock();
		try {
			SessionInformation sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
			if (sessionInformation != null) {
				removeSessionFromCache(sessionUUID);
				File possibleSession = new File(sessionInformation.getSessionDirectory());
				FileUtils.deleteDirectory(possibleSession);
			}
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Get session information.
	 * 
	 * Get from cache if there else load from disk.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon with sessions
	 * @param sessionUUID UUID of session to get
	 * @return session information
	 * @throws IOException thrown if error
	 */
	private static SessionInformation getSessionInformation(final HttpServlet servlet, final String dungeonUUID, final String sessionUUID) throws IOException {
		lock.lock();
		try {
			SessionInformation sessionInformation = getSessionFromCache(sessionUUID);
			if (sessionInformation != null) {
				return (sessionInformation);
			}
			String sessionsPath = uuidTemplatePathMap.get(dungeonUUID) + Constants.SESSIONS_FOLDER;
			String directoryPath = servlet.getServletContext().getRealPath(sessionsPath);
			File sessionsDirectory = new File(directoryPath);
			for (File possibleSession : sessionsDirectory.listFiles()) {
				if (possibleSession.isDirectory()) {
					SessionInformation possibleSessionInformation = loadSessionInformation(possibleSession);
					if (sessionUUID.equals(possibleSessionInformation.getUUID())) {
						addSessionToCache(possibleSessionInformation);
						return (possibleSessionInformation);
					}
				}
			}
		} finally {
			lock.unlock();
		}
		return null;
	}

	/**
	 * Load in session information from file.
	 * 
	 * @param possibleSession possible session
	 * @return session information
	 * @throws IOException thrown if error
	 */
	private static SessionInformation loadSessionInformation(final File possibleSession) throws IOException {
		SessionInformation possibleSessionInformation = new SessionInformation();
		possibleSessionInformation.load(possibleSession.getPath() + "/sessionData.json", possibleSession.getPath());
		return possibleSessionInformation;
	}

	/**
	 * Get session information from cache.
	 * 
	 * @param sessionUUID UUID of session
	 * @return session information or null
	 */
	private static SessionInformation getSessionFromCache(final String sessionUUID) {
		lock.lock();
		try {
			return (sessionCache.get(sessionUUID));
		} finally {
			lock.unlock();
		}
	}

	/**
	 * remove session from cache.
	 * 
	 * @param sessionUUID UUID of session
	 */
	private static void removeSessionFromCache(final String sessionUUID) {
		lock.lock();
		try {
			if (sessionCache.containsKey(sessionUUID)) {
				sessionCache.remove(sessionUUID);
			}
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Add session to cache.
	 * 
	 * @param sessionInformation to add
	 */
	private static void addSessionToCache(final SessionInformation sessionInformation) {
		lock.lock();
		try {
			if (sessionCache.containsKey(sessionInformation.getUUID())) {
				sessionCache.remove(sessionInformation.getUUID());
			}
			sessionCache.put(sessionInformation.getUUID(), sessionInformation);
		} finally {
			lock.unlock();
		}
	}

	/**
	 * get session data as string.
	 * 
	 * This will check version. if the version number hasn't changed it will just return empty string.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon with sessions.
	 * @param sessionUUID UUID of session
	 * @param version of session
	 * @return session data as string or empty string if version hasn't changed.
	 * @throws IOException thrown if error
	 */
	public static String getSessionDataAsString(final HttpServlet servlet, final String dungeonUUID, final String sessionUUID, final int version) throws IOException {
		lock.lock();
		try {
			SessionInformation sessionInformation;
			if (version != -1) {
				sessionInformation = getSessionFromCache(sessionUUID);
			} else {
				sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
			}
			if (sessionInformation != null && sessionInformation.getSessionData().getVersion() != version) {
				return (sessionInformation.toJson());
			}
			return ("");
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Save session data.
	 * 
	 * @param request data
	 * @param servlet servlet data
	 * @param jsonData of session
	 * @param sessionUUID UUID of session
	 * @throws IOException thrown if error
	 */
	public static void saveSessionData(final HttpServletRequest request, final HttpServlet servlet, final String jsonData, final String sessionUUID) throws IOException {
		String dungeonUUID = request.getParameter("dungeonUUID");
		if (dungeonUUID == null || dungeonUUID.isEmpty()) {
			return;
		}
		lock.lock();
		try {
			SessionInformation sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
			if (sessionInformation != null) {
				sessionInformation.fromJson(jsonData);
				sessionInformation.save();
			}
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Update fog of war.
	 * 
	 * @param servlet servlet data
	 * @param sessionUUID UUID of session
	 * @param currentLevel level in dungeon
	 * @param fogOfWar array of fog of war bits
	 */
	public static void updateFOW(final HttpServlet servlet, final String sessionUUID, final int currentLevel, final long[] fogOfWar) {
		lock.lock();
		try {
			SessionInformation sessionInformation = getSessionFromCache(sessionUUID);
			if (sessionInformation != null) {
				sessionInformation.updateFOW(fogOfWar, currentLevel);
			}
		} finally {
			lock.unlock();
		}
	}

	/**
	 * get this json file as a string.
	 * 
	 * @param servlet servlet data
	 * @param fileName to read
	 * @return string with data
	 * @throws IOException thrown if error
	 */
	public static String getFileAsString(final HttpServlet servlet, final String fileName) throws IOException {
		lock.lock();
		try {
			String filePath = servlet.getServletContext().getRealPath(Constants.SERVER_DUNGEON_DATA_LOCATION + fileName);
			return (readJsonFile(filePath));
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Save JSON data to file.
	 * 
	 * @param dataToWrite data to write
	 * @param filePath to file
	 * @throws IOException thrown if error
	 */
	public static void saveJsonFile(final String dataToWrite, final String filePath) throws IOException {
		BufferedWriter output = null;
		try {
			lock.lock();
			File file = new File(filePath);
			file.delete();
			output = new BufferedWriter(new FileWriter(file));
			output.write(dataToWrite);
		} catch (IOException e) {
			if (output != null) {
				output.close();
				output = null;
			}
		} finally {
			if (output != null) {
				output.close();
				output = null;
			}
			lock.unlock();
		}
	}

	/**
	 * read file with JSON data.
	 * 
	 * @param filePath to file
	 * @return string with file data
	 */
	public static String readJsonFile(final String filePath) {
		StringBuilder builder = new StringBuilder();
		BufferedReader input = null;
		try {
			lock.lock();
			File file = new File(filePath);
			input = new BufferedReader(new FileReader(file));
			String line;
			while ((line = input.readLine()) != null) {
				builder.append(line);
			}
		} catch (IOException e) {
		} finally {
			if (input != null) {
				try {
					input.close();
				} catch (IOException e) {
				}
			}
			lock.unlock();
		}
		return builder.toString();
	}

	/**
	 * Delete all old sessions that might exist.
	 * 
	 * @param destinationDirectory to delete
	 * @throws IOException thrown if error
	 */
	private static void deleteAnyOldSessions(final File destinationDirectory) throws IOException {
		String sessionsPath = destinationDirectory.getPath() + "/" + Constants.SESSIONS_FOLDER;
		File sessions = new File(sessionsPath);
		lock.lock();
		try {
			FileUtils.deleteDirectory(sessions);
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Make sure path exists.
	 * 
	 * @param directoryPath to check
	 */
	private static void makeSureDirectoryExists(final String directoryPath) {
		File path = new File(directoryPath);
		if (!path.exists()) {
			path.mkdir();
		}
	}

	/**
	 * Save Pog data.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon
	 * @param sessionUUID UUID of session
	 * @param level level in dungeon
	 * @param place place where to add
	 * @param pogJsonData JSON data of Pog
	 * @throws IOException thrown if error
	 */
	public static void savePog(final HttpServlet servlet, final String dungeonUUID, final String sessionUUID, final int level, final PogPlace place, final String pogJsonData) throws IOException {
		lock.lock();
		try {
			Gson gson = new Gson();
			PogData pogData = gson.fromJson(pogJsonData, PogData.class);
			if (place == PogPlace.COMMON_RESOURCE) {
				addOrUpdatePogToCommonResource(servlet, pogData);
			} else if (place == PogPlace.DUNGEON_LEVEL) {
				addOrUpdatePogToDungeonInstance(servlet, pogData, dungeonUUID, level);
			} else if (place == PogPlace.SESSION_RESOURCE) {
				addOrUpdatePogToSessionResource(servlet, pogData, dungeonUUID, sessionUUID, level);
			} else if (place == PogPlace.SESSION_LEVEL) {
				addOrUpdatePogToSessionInstance(servlet, pogData, dungeonUUID, sessionUUID, level);
			}
		} finally {
			lock.unlock();
		}
	}

	/**
	 * Add or update pog to proper resource.
	 * 
	 * @param servlet servlet data
	 * @param pogData to add
	 * @throws IOException if error
	 */
	private static void addOrUpdatePogToCommonResource(final HttpServlet servlet, final PogData pogData) throws IOException {
		if (pogData.isType(Constants.POG_TYPE_MONSTER)) {
			addOrUpdatePogToCommonResource(servlet, pogData, Constants.MONSTER_FOLDER);
		} else if (pogData.isType(Constants.POG_TYPE_ROOMOBJECT)) {
			addOrUpdatePogToCommonResource(servlet, pogData, Constants.ROOM_OBJECT_FOLDER);
		}
	}

	/**
	 * Add or Update pog to resource folder.
	 * 
	 * @param servlet with data
	 * @param pogData to update
	 * @param folder resource folder
	 * @throws IOException if error
	 */
	private static void addOrUpdatePogToCommonResource(final HttpServlet servlet, final PogData pogData, final String folder) throws IOException {
		String resourcePath = Constants.SERVER_RESOURCE_LOCATION + folder + "pogs.json";
		String filePath = servlet.getServletContext().getRealPath(resourcePath);
		String fileData = readJsonFile(filePath);
		Gson gson = new Gson();
		PogList pogList = gson.fromJson(fileData, PogList.class);
		pogList.addOrUpdate(pogData);
		String updatedData = gson.toJson(pogList);
		saveJsonFile(updatedData, filePath);
	}

	/**
	 * Add or update pog instance to a dungeon level within the template.
	 * 
	 * @param pogData pog data
	 * @param dungeonUUID UUID of dungeon.
	 * @param level dungeon level
	 * @param servlet data
	 * @throws IOException if error
	 */
	private static void addOrUpdatePogToDungeonInstance(final HttpServlet servlet, final PogData pogData, final String dungeonUUID, final int level) throws IOException {
		DungeonData dungeonData = getDungeonDataFromUUID(servlet, dungeonUUID);
		DungeonLevel dungeonLevel = dungeonData.getDungeonLevels()[level];
		if (pogData.isType(Constants.POG_TYPE_MONSTER)) {
			dungeonLevel.getMonsters().addOrUpdate(pogData);
		} else if (pogData.isType(Constants.POG_TYPE_ROOMOBJECT)) {
			dungeonLevel.getRoomObjects().addOrUpdate(pogData);
		}
		Gson gson = new Gson();
		String jsonData = gson.toJson(dungeonData);
		saveDungeonData(servlet, jsonData, dungeonUUID);
	}

	/**
	 * Add or update pog instance to a session level.
	 * 
	 * @param servlet data
	 * @param pogData pog data
	 * @param dungeonUUID UUID of dungeon.
	 * @param sessionUUID UUID of session
	 * @param level dungeon level
	 * @throws IOException if error
	 */
	private static void addOrUpdatePogToSessionInstance(final HttpServlet servlet, final PogData pogData, final String dungeonUUID, final String sessionUUID, final int level) throws IOException {
		SessionInformation sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
		sessionInformation.addOrUpdatePog(pogData, level);
	}

	/**
	 * Add or update pog instance to a session resource level.
	 * 
	 * This should only be player information.
	 * 
	 * @param servlet data
	 * @param pogData pog data
	 * @param dungeonUUID UUID of dungeon.
	 * @param sessionUUID UUID of session
	 * @param level dungeon level
	 * @throws IOException if error
	 */
	private static void addOrUpdatePogToSessionResource(final HttpServlet servlet, final PogData pogData, final String dungeonUUID, final String sessionUUID, final int level) throws IOException {
		SessionInformation sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
		if (pogData.isType(Constants.POG_TYPE_PLAYER)) {
			sessionInformation.addOrUpdatePog(pogData, level);
		}
	}

	/**
	 * Save Pog data.
	 * 
	 * @param servlet servlet data
	 * @param dungeonUUID UUID of dungeon
	 * @param sessionUUID UUID of session
	 * @param level level in dungeon
	 * @param place place where to add
	 * @param pogJsonData JSON data of Pog
	 * @throws IOException thrown if error
	 */
	public static void deletePog(final HttpServlet servlet, final String dungeonUUID, final String sessionUUID, final int level, final PogPlace place, final String pogJsonData) throws IOException {
		lock.lock();
		try {
			Gson gson = new Gson();
			PogData pogData = gson.fromJson(pogJsonData, PogData.class);
			if (place == PogPlace.COMMON_RESOURCE) {
				deletePogInCommonResource(servlet, pogData);
			} else if (place == PogPlace.DUNGEON_LEVEL) {
				deletePogInDungeonInstance(servlet, pogData, dungeonUUID, level);
			} else if (place == PogPlace.SESSION_RESOURCE) {
				deletePogInSessionResource(servlet, pogData, dungeonUUID, sessionUUID, level);
			} else if (place == PogPlace.SESSION_LEVEL) {
				deletePogInSessionInstance(servlet, pogData, dungeonUUID, sessionUUID, level);
			}
		} finally {
			lock.unlock();
		}
	}

	private static void deletePogInCommonResource(final HttpServlet servlet, final PogData pogData) throws IOException {
		if (pogData.isType(Constants.POG_TYPE_MONSTER)) {
			deletePogInCommonResource(servlet, pogData, Constants.MONSTER_FOLDER);
		} else if (pogData.isType(Constants.POG_TYPE_ROOMOBJECT)) {
			deletePogInCommonResource(servlet, pogData, Constants.ROOM_OBJECT_FOLDER);
		}
	}

	private static void deletePogInCommonResource(final HttpServlet servlet, final PogData pogData, final String folder) throws IOException {
		String resourcePath = Constants.SERVER_RESOURCE_LOCATION + folder + "pogs.json";
		String filePath = servlet.getServletContext().getRealPath(resourcePath);
		String fileData = readJsonFile(filePath);
		Gson gson = new Gson();
		PogList pogList = gson.fromJson(fileData, PogList.class);
		pogList.delete(pogData);
		String updatedData = gson.toJson(pogList);
		saveJsonFile(updatedData, filePath);
	}

	private static void deletePogInDungeonInstance(final HttpServlet servlet, final PogData pogData, final String dungeonUUID, final int level) throws IOException {
		DungeonData dungeonData = getDungeonDataFromUUID(servlet, dungeonUUID);
		DungeonLevel dungeonLevel = dungeonData.getDungeonLevels()[level];
		if (pogData.isType(Constants.POG_TYPE_MONSTER)) {
			dungeonLevel.getMonsters().delete(pogData);
		} else if (pogData.isType(Constants.POG_TYPE_ROOMOBJECT)) {
			dungeonLevel.getRoomObjects().delete(pogData);
		}
		Gson gson = new Gson();
		String jsonData = gson.toJson(dungeonData);
		saveDungeonData(servlet, jsonData, dungeonUUID);
	}

	private static void deletePogInSessionResource(final HttpServlet servlet, final PogData pogData, final String dungeonUUID, final String sessionUUID, final int level) throws IOException {
		SessionInformation sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
		if (pogData.isType(Constants.POG_TYPE_PLAYER)) {
			sessionInformation.delete(pogData, level);
		}
	}

	private static void deletePogInSessionInstance(final HttpServlet servlet, final PogData pogData, final String dungeonUUID, final String sessionUUID, final int level) throws IOException {
		SessionInformation sessionInformation = getSessionInformation(servlet, dungeonUUID, sessionUUID);
		sessionInformation.delete(pogData, level);
	}

	/**
	 * Delete this file.
	 * 
	 * @param request request
	 * @param filePath to delete
	 * @throws IOException thrown if error
	 */
	public static void deleteFile(final HttpServletRequest request, final String filePath) throws IOException {
		lock.lock();
		try {
			String path = request.getSession().getServletContext().getRealPath(filePath);
			File file = new File(path);
			file.delete();
		} finally {
			lock.unlock();
		}
	}
}
