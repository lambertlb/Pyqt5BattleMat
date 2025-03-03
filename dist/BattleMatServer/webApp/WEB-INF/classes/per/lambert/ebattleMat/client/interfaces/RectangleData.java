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
package per.lambert.ebattleMat.client.interfaces;

/**
 * Manage coordinates for selection rectangle.
 * 
 * @author LLambert
 *
 */
public class RectangleData {
	/**
	 * Top of rectangle.
	 */
	private int top;

	/**
	 * Get top of rectangle.
	 * 
	 * @return top of rectangle
	 */
	public int getTop() {
		return top;
	}

	/**
	 * Set top of rectangle.
	 * 
	 * @param top
	 */
	public void setTop(final int top) {
		this.top = top;
	}

	/**
	 * Left of rectangle.
	 */
	private int left;

	/**
	 * Get left of rectangle.
	 * 
	 * @return left of rectangle
	 */
	public int getLeft() {
		return left;
	}

	/**
	 * Set left of rectangle.
	 * 
	 * @param left
	 */
	public void setLeft(final int left) {
		this.left = left;
	}

	/**
	 * Bottom of rectangle.
	 */
	private int bottom;

	/**
	 * Get bottom of rectangle.
	 * 
	 * @return bottom of rectangle
	 */
	public int getBottom() {
		return bottom;
	}

	/**
	 * Set bottom of rectangle.
	 * 
	 * @param bottom
	 */
	public void setBottom(final int bottom) {
		this.bottom = bottom;
	}

	/**
	 * Right of rectangle.
	 */
	private int right;

	/**
	 * Get right of rectangle.
	 * 
	 * @return right of rectangle
	 */
	public int getRight() {
		return right;
	}

	/**
	 * Set right of rectangle.
	 * 
	 * @param right
	 */
	public void setRight(final int right) {
		this.right = right;
	}

	/**
	 * Width of square.
	 * 
	 * @return width
	 */
	public int getWidth() {
		return (right - left);
	}

	/**
	 * get height of square.
	 * 
	 * @return height
	 */
	public int getHeight() {
		return (bottom - top);
	}
}
