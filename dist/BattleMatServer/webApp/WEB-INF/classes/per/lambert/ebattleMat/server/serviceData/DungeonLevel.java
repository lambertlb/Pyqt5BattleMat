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
package per.lambert.ebattleMat.server.serviceData;

/**
 * Server side dungeon level information.
 * 
 * @author LLambert
 *
 */
public class DungeonLevel {
	/**
	 * URL to level picture.
	 */
	private String levelDrawing;
	/**
	 * Level name.
	 */
	private String levelName;
	/**
	 * size of grid cell.
	 */
	private double gridSize;
	/**
	 * X offset for top left of grid.
	 */
	private double gridOffsetX;
	/**
	 * Y offset for top left of grid.
	 */
	private double gridOffsetY;
	/**
	 * # of columns in level.
	 */
	private int columns;
	/**
	 * # of rows in level.
	 */
	private int rows;
	/**
	 * List of monsters on level.
	 */
	private PogList monsters = new PogList();
	/**
	 * List of room objects on level.
	 */
	private PogList roomObjects = new PogList();

	/**
	 * get URL to level picture.
	 * 
	 * @return URL to picture
	 */
	public String getLevelDrawing() {
		return levelDrawing;
	}

	/**
	 * Set URL to level picture.
	 * 
	 * @param levelDrawing URL to set
	 */
	public void setLevelDrawing(final String levelDrawing) {
		this.levelDrawing = levelDrawing;
	}

	/**
	 * get level name.
	 * 
	 * @return level name
	 */
	public String getLevelName() {
		return levelName;
	}

	/**
	 * Set level name.
	 * 
	 * @param levelName to set
	 */
	public void setLevelName(final String levelName) {
		this.levelName = levelName;
	}

	/**
	 * get size of grid cell.
	 * 
	 * @return size of grid cell
	 */
	public double getGridSize() {
		return gridSize;
	}

	/**
	 * set size of grid cell.
	 * 
	 * @param gridSize size of grid cell
	 */
	public void setGridSize(final double gridSize) {
		this.gridSize = gridSize;
	}

	/**
	 * get X offset for top left of grid.
	 * 
	 * @return X offset for top left of grid.
	 */
	public double getGridOffsetX() {
		return gridOffsetX;
	}

	/**
	 * set X offset for top left of grid.
	 * 
	 * @param gridOffsetX X offset for top left of grid.
	 */
	public void setGridOffsetX(final double gridOffsetX) {
		this.gridOffsetX = gridOffsetX;
	}

	/**
	 * get Y offset for top left of grid.
	 * 
	 * @return Y offset for top left of grid.
	 */
	public double getGridOffsetY() {
		return gridOffsetY;
	}

	/**
	 * set Y offset for top left of grid.
	 * 
	 * @param gridOffsetY Y offset for top left of grid.
	 */
	public void setGridOffsetY(final double gridOffsetY) {
		this.gridOffsetY = gridOffsetY;
	}

	/**
	 * get # of columns in level.
	 * 
	 * @return # of columns in level.
	 */
	public int getColumns() {
		return columns;
	}

	/**
	 * set # of columns in level.
	 * 
	 * @param columns # of columns in level.
	 */
	public void setColumns(final int columns) {
		this.columns = columns;
	}

	/**
	 * get # of rows in level.
	 * 
	 * @return # of rows in level.
	 */
	public int getRows() {
		return rows;
	}

	/**
	 * set # of rows in level.
	 * 
	 * @param rows # of rows in level.
	 */
	public void setRows(final int rows) {
		this.rows = rows;
	}

	/**
	 * get List of monsters on level.
	 * 
	 * @return List of monsters on level.
	 */
	public PogList getMonsters() {
		return monsters;
	}

	/**
	 * set List of monsters on level.
	 * 
	 * @param monsters List of monsters on level.
	 */
	public void setMonsters(final PogList monsters) {
		this.monsters = monsters;
	}

	/**
	 * get List of room objects on level.
	 * 
	 * @return List of room objects on level.
	 */
	public PogList getRoomObjects() {
		return roomObjects;
	}

	/**
	 * set List of room objects on level.
	 * 
	 * @param roomObjects List of room objects on level.
	 */
	public void setRoomObjects(final PogList roomObjects) {
		this.roomObjects = roomObjects;
	}
}
