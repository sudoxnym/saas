import asyncio, json, logging, time, inspect, pytz
from datetime import timedelta, datetime, timezone
from collections import deque
from homeassistant.helpers.event import async_track_time_interval, async_call_later
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.mqtt import async_subscribe
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt as dt_util
from homeassistant.components import mqtt
from .const import DOMAIN, CONF_NAME, CONF_TOPIC, CONF_AWAKE_STATES, CONF_SLEEP_STATES, CONF_AWAKE_DURATION, CONF_SLEEP_DURATION, INTEGRATION_NAME, MODEL, STATE_MAPPING, SOUND_MAPPING, DISTURBANCE_MAPPING, ALARM_EVENT_MAPPING, SLEEP_TRACKING_MAPPING, LULLABY_MAPPING, REVERSE_STATE_MAPPING, SLEEP_STAGE_MAPPING


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

import inspect
from datetime import datetime

class SAASSensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor."""

    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sensor_{self._name}"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} State"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
    
    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event)
            if new_state is not None:
                self._state = new_state
                self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASAlarmEventSensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Alarm Events."""

    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self._value1 = None
        self._value2 = None
        self._time = None
        self.entry_id = entry_id 
        self._reset_timer = None
        self._last_event = None

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_alarm_event_sensor_{self._name}"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Alarm Event"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
    
    @property
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        return {
            "Last Event": self._last_event,
            "Message": self._value2 if self._value2 else "No message received",
            "Timestamp": self._value1 if self._value1 else "No timestamp received",
            "Time": self._time.strftime('%H:%M') if self._time else "No time received",
            "Date": self._time.strftime('%m/%d/%Y') if self._time else "No date received",
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def reset_state(_):
            """Reset the state to None after a delay."""
            self._state = 'None'
            self.async_write_ha_state()

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Cancel the previous state reset timer
            if self._reset_timer:
                self._reset_timer.cancel()
            
            # Schedule a state reset after 15 seconds
            self._reset_timer = async_call_later(self._hass, 15, reset_state)

            # Parse the incoming message
            msg_json = json.loads(msg.payload)
        
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")
        
            # Extract the 'value1' and 'value2' fields
            value1 = msg_json.get('value1')
        
            # Parse 'value1' as a datetime
            if value1:
                timestamp = int(value1) / 1000.0
                self._time = datetime.fromtimestamp(timestamp)
                self._value1 = value1
                _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Parsed 'value1' as datetime: {self._time} for sensor {self.name}")
        
            # Extract the 'value2' field
            value2 = msg_json.get('value2')
        
            # Store 'value2' as the message if it exists
            self._value2 = value2 if value2 else "None"
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Stored 'value2' as message: {self._value2} for sensor {self.name}")
        
            # Extract the EVENT field
            event = msg_json.get('event')
        
            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return
        
            _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Extracted Event {event} from message for sensor {self.name}")
        
            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event)
            if new_state is not None:
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Mapped {event} to {new_state} for sensor {self.name}")
                self._state = new_state
                self._last_event = new_state  # Update the last event
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
                self.async_write_ha_state()
    
        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASSoundSensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Sound Events."""
    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sound_sensor_{self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Sound"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            if new_state is not None:
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Mapped {event} to {new_state} for sensor {self.name}")
                self._state = new_state
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
                self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASSoundSensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Sound Events."""
    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sound_sensor_{self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Sound"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            if new_state is not None:
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Mapped {event} to {new_state} for sensor {self.name}")
                self._state = new_state
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
                self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASSleepTrackingSensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Sleep Tracking."""
    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sleep_tracking_sensor_{self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Sleep Tracking"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)
        
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")
        
            # Extract the EVENT field
            event = msg_json.get('event')
        
            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return
        
            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event)  # Removed default to "None"
            if new_state is not None:  # Only update state if a mapping is found
                self._state = new_state
                _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
                self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASDisturbanceSensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Disturbance Events."""
    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_disturbance_sensor_{self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Disturbance"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            self._state = new_state
            _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASLullabySensor(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Lullaby."""
    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_lullaby_sensor_{self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Lullaby"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            self._state = new_state
            _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASSleepStage(RestoreEntity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Sleep Stage."""
    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self.entry_id = entry_id 

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sleep_stage_sensor_{self._name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Sleep Stage"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Received MQTT message: {msg_json} for sensor {self.name}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): No 'event' key in the MQTT message: {msg_json} for sensor {self.name}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            self._state = new_state
            _LOGGER.debug(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Set state to {new_state} for sensor {self.name}")
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self._hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

class SAASWakeStatusSensor(RestoreEntity):
    def __init__(self, hass, name, awake_states, sleep_states, awake_duration, sleep_duration, mqtt_topic, entry_id):
        self._state = None
        self._name = name
        self.awake_bucket = []
        self.sleep_bucket = []
        self.awake_duration = timedelta(seconds=awake_duration)
        self.sleep_duration = timedelta(seconds=sleep_duration)
        self.awake_states = awake_states
        self.sleep_states = sleep_states
        self.hass = hass
        self.mqtt_topic = mqtt_topic
        self.entry_id = entry_id

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_wake_status_{self._name}"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Wake Status"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }

    def process_message(self, message):
        try:
            now = dt_util.utcnow()  # Define 'now' before using it for logging
    
            # Extract the 'event' from the incoming message
            event = message.get('event')
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Extracted Event {event} from message.")
    
            # Map the event to a known state, or "Unknown" if the event is not recognized
            mapped_value = STATE_MAPPING.get(event, "Unknown")
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Mapped {event} to {mapped_value}.")
    
            # If the event could not be mapped to a known state, set the sensor state to "Unknown"
            if mapped_value == "Unknown":
                self._state = "Unknown"
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Event {event} could not be mapped to a known state. Setting sensor state to 'Unknown'.")
    
            # If the mapped value is in the awake states, add it to the awake bucket and clear the sleep bucket
            if mapped_value in self.awake_states:
                self.awake_bucket.append((mapped_value, now))
                self.sleep_bucket = []
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Mapped value {mapped_value} is in awake states. Adding to awake bucket and clearing sleep bucket.")
    
            # If the mapped value is in the sleep states, add it to the sleep bucket and clear the awake bucket
            elif mapped_value in self.sleep_states:
                self.sleep_bucket.append((mapped_value, now))
                self.awake_bucket = []
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Mapped value {mapped_value} is in sleep states. Adding to sleep bucket and clearing awake bucket.")
    
        except Exception as e:
            _LOGGER.error(f"Error processing message: {e}")
    
    async def async_update(self, _=None):
        """Update the state."""
        now = dt_util.utcnow()
    
        # If any message in the awake bucket has reached the awake duration, set the state to "Awake"
        if self.awake_bucket and any(now - timestamp >= self.awake_duration for _, timestamp in self.awake_bucket):
            if self._state != "Awake":
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): State changed to 'Awake'")
            self._state = "Awake"
        
        # If any message in the sleep bucket has reached the sleep duration, set the state to "Asleep"
        elif self.sleep_bucket and any(now - timestamp >= self.sleep_duration for _, timestamp in self.sleep_bucket):
            if self._state != "Asleep":
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): State changed to 'Asleep'")
            self._state = "Asleep"
            
        # Remove messages from the awake bucket that are older than the awake duration and log if a message is removed
        self.awake_bucket = [(val, timestamp) for val, timestamp in self.awake_bucket if now - timestamp < self.awake_duration]
        for val, timestamp in self.awake_bucket:
            if now - timestamp >= self.awake_duration:
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Removed message from awake bucket.")
        
        # Remove messages from the sleep bucket that are older than the sleep duration and log if a message is removed
        self.sleep_bucket = [(val, timestamp) for val, timestamp in self.sleep_bucket if now - timestamp < self.sleep_duration]
        for val, timestamp in self.sleep_bucket:
            if now - timestamp >= self.sleep_duration:
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Removed message from sleep bucket.")
                
        # Log the contents of the awake bucket if it is not empty
        if self.awake_bucket:
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Awake bucket: {self.awake_bucket}")
    
        # Log the contents of the sleep bucket if it is not empty
        if self.sleep_bucket:
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Sleep bucket: {self.sleep_bucket}")

    async def interval_callback(self, _):
        """Wrapper function for async_track_time_interval."""
        # Call the async_update method to update the state
        await self.async_update()
    
    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()
    
        # Load the previous state from the state machine
        state = await self.async_get_last_state()
        if state:
            self._state = state.state
            _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Loaded state: {self._state} for sensor {self.name}")
    
        # Schedule the interval callback to run every second
        async_track_time_interval(
            self.hass, 
            self.interval_callback, 
            timedelta(seconds=1)
        )
    
        # Subscribe to the MQTT topic to receive messages
        await mqtt.async_subscribe(
            self.hass,
            self.mqtt_topic, 
            lambda message: self.process_message(json.loads(message.payload))
        )

    async def async_will_remove_from_hass(self):
        """Run when entity will be removed from hass."""
        # Save the current state to the state machine
        self.hass.states.async_set(self.entity_id, self._state)
        _LOGGER.info(f"{datetime.now().strftime('%H:%M:%S:%f')} (Line {inspect.currentframe().f_lineno}): Saved state: {self._state} for sensor {self.name}")

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the SAAS sensor platform from a config entry."""
    name = entry.data.get(CONF_NAME, "Default Name")
    topic = entry.data.get(CONF_TOPIC)
    awake_states = entry.data.get(CONF_AWAKE_STATES)
    sleep_states = entry.data.get(CONF_SLEEP_STATES)
    awake_duration = entry.data.get(CONF_AWAKE_DURATION)
    sleep_duration = entry.data.get(CONF_SLEEP_DURATION)
    entry_id = entry.entry_id
    hass.data[DOMAIN][entry.entry_id] = entry.data

    entities = [
        SAASSensor(hass, name, STATE_MAPPING, entry_id),
        SAASAlarmEventSensor(hass, name, ALARM_EVENT_MAPPING, entry_id),
        SAASSoundSensor(hass, name, SOUND_MAPPING, entry_id),
        SAASSleepTrackingSensor(hass, name, SLEEP_TRACKING_MAPPING, entry_id), 
        SAASDisturbanceSensor(hass, name, DISTURBANCE_MAPPING, entry_id),
        SAASLullabySensor(hass, name, LULLABY_MAPPING, entry_id),
        SAASSleepStage(hass, name, SLEEP_STAGE_MAPPING, entry_id),
        SAASWakeStatusSensor(hass, name, awake_states, sleep_states, awake_duration, sleep_duration, topic, entry_id)
    ]

    for entity in entities:
        if hasattr(entity, "async_setup"):
            await entity.async_setup()

    async_add_entities(entities)