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

/**
 * Client side definition for a dungeon level.
 * 
 * THis needs to match per.lambert.ebattleMat.server.serviceData.DungeonLevel
 * 
 * @author LLambert
 *
 */
public class DungeonLevel extends DungeonSessionLevel {
	/**
	 * Constructor for Dungeon Level.
	 */
	protected DungeonLevel() {
	}

	/**
	 * get drawing for level.
	 * 
	 * @return drawing for level.
	 */
	public final native String getLevelDrawing() /*-{
		return this.levelDrawing;
	}-*/;

	/**
	 * Set drawing for level.
	 * 
	 * @param levelDrawing for level
	 */
	public final native void setLevelDrawing(String levelDrawing) /*-{
		this.levelDrawing = levelDrawing;
	}-*/;

	/**
	 * get level name.
	 * 
	 * @return level name
	 */
	public final native String getLevelName() /*-{
		return this.levelName;
	}-*/;

	/**
	 * set level name.
	 * 
	 * @param levelName to set
	 */
	public final native void setLevelName(String levelName) /*-{
		this.levelName = levelName;
	}-*/;

	/**
	 * get size of grid cell.
	 * 
	 * @return size of grid cell
	 */
	public final native double getGridSize() /*-{
		if (this.gridSize === undefined) {
			return (30);
		}
		return this.gridSize;
	}-*/;

	/**
	 * set size of grid cell.
	 * 
	 * @param gridSize to set
	 */
	public final native void setGridSize(double gridSize) /*-{
		this.gridSize = gridSize;
	}-*/;

	/**
	 * get x offset from top left for grid.
	 * 
	 * @return x offset
	 */
	public final native double getGridOffsetX() /*-{
		if (this.gridOffsetX === undefined) {
			return (0);
		}
		return this.gridOffsetX;
	}-*/;

	/**
	 * set x offset from top left for grid.
	 * 
	 * @param offset to set
	 */
	public final native void setGridOffsetX(double offset) /*-{
		this.gridOffsetX = offset;
	}-*/;

	/**
	 * get y offset from top left for grid.
	 * 
	 * @return y offset
	 */
	public final native double getGridOffsetY() /*-{
		if (this.gridOffsetY === undefined) {
			return (0);
		}
		return this.gridOffsetY;
	}-*/;

	/**
	 * set y offset from top left for grid.
	 * 
	 * @param offset to set
	 */
	public final native void setGridOffsetY(double offset) /*-{
		this.gridOffsetY = offset;
	}-*/;

	/**
	 * Number of columns in this level.
	 * @return number of columns
	 */
	public final native int getColumns() /*-{
		if (this.columns === undefined) {
			return (0);
		}
		return this.columns;
	}-*/;

	/**
	 * Set number of columns in this level.
	 * @param columns to set
	 */
	public final native void setColumns(int columns) /*-{
		this.columns = columns;
	}-*/;

	/**
	 * Number of rows in this level.
	 * @return number of rows
	 */
	public final native int getRows() /*-{
		if (this.rows === undefined) {
			return (0);
		}
		return this.rows;
	}-*/;

	/**
	 * Set number of rows in this level.
	 * @param rows to set
	 */
	public final native void setRows(int rows) /*-{
		this.rows = rows;
	}-*/;
}
