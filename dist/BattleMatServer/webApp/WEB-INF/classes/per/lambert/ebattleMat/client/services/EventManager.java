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

import com.google.gwt.event.shared.EventHandler;
import com.google.gwt.event.shared.GwtEvent;
import com.google.gwt.event.shared.GwtEvent.Type;
import com.google.gwt.event.shared.HandlerManager;
import com.google.gwt.event.shared.HandlerRegistration;

import per.lambert.ebattleMat.client.interfaces.IEventManager;

/**
 * Event buss wrapper.
 * @author LLambert
 *
 */
public class EventManager implements IEventManager {

	/**
	 * GWT event bus.
	 */
	private final HandlerManager eventBus;

	/**
	 * constructor for event manager.
	 */
	public EventManager() {
		this.eventBus = new HandlerManager(new Object());
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public <H extends EventHandler> HandlerRegistration addHandler(final Type<H> eventType, final H handler) {
		return (eventBus.addHandler(eventType, handler));
	}

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void fireEvent(final GwtEvent<?> event) {
		eventBus.fireEvent(event);
	}

}
