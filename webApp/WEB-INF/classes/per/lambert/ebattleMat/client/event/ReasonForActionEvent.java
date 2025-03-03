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
package per.lambert.ebattleMat.client.event;

import com.google.gwt.event.shared.GwtEvent;

import per.lambert.ebattleMat.client.interfaces.ReasonForAction;

/**
 * Event for handling reason for action.
 * 
 * @author LLambert
 *
 */
public class ReasonForActionEvent extends GwtEvent<ReasonForActionEventHandler> {
	/**
	 * Type of event.
	 */
	private static Type<ReasonForActionEventHandler> reasonForActionEventType = new Type<ReasonForActionEventHandler>();
	/**
	 * Reason for event.
	 */
	private ReasonForAction reason;
	/**
	 * Data for event.
	 */
	private Object data;

	/**
	 * Constructor.
	 * 
	 * @param reason for event
	 * @param data for event
	 */
	public ReasonForActionEvent(final ReasonForAction reason, final Object data) {
		this.reason = reason;
		this.data = data;
	}

	/**
	 * Get reason for action.
	 * 
	 * @return reason for action.
	 */
	public final ReasonForAction getReasonForAction() {
		return reason;
	}

	/**
	 * Get data for event.
	 * 
	 * @return data for event.
	 */
	public final Object getData() {
		return this.data;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public com.google.gwt.event.shared.GwtEvent.Type<ReasonForActionEventHandler> getAssociatedType() {
		return reasonForActionEventType;
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	protected void dispatch(final ReasonForActionEventHandler handler) {
		handler.onReasonForAction(this);
	}

	/**
	 * Get reason for event type.
	 * 
	 * @return type for reason of event
	 */
	public static Type<ReasonForActionEventHandler> getReasonForActionEventType() {
		return reasonForActionEventType;
	}
}
