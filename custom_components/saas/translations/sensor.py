import asyncio
import json
from datetime import timedelta, datetime
from collections import deque
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.mqtt import async_subscribe
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt as dt_util
from homeassistant.components import mqtt
from .const import DOMAIN, CONF_NAME, CONF_TOPIC, CONF_AWAKE_STATES, CONF_SLEEP_STATES, CONF_AWAKE_DURATION, CONF_SLEEP_DURATION, INTEGRATION_NAME, MODEL, STATE_MAPPING, SOUND_MAPPING, DISTURBANCE_MAPPING, ALARM_EVENT_MAPPING, SLEEP_TRACKING_MAPPING, LULLABY_MAPPING, REVERSE_STATE_MAPPING
import logging
import time

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class SAASSensor(Entity):
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

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event)
            if new_state is not None:
                self._state = new_state
                self.async_schedule_update_ha_state()
            #else:
                #_LOGGER.warning(f"No mapping found for event '{event}'")

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

class SAASAlarmEventSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Alarm Events."""

    def __init__(self, hass, name, mapping, entry_id):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self._value1 = None
        self._time = None
        self.entry_id = entry_id 

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
    
    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                _LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event)
            if new_state is not None:
                self._state = new_state
                self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    
class SAASSoundSensor(Entity):
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

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                #_LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            self._state = new_state
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

    async def message_received(msg):
        """Handle new MQTT messages."""
        # Parse the incoming message
        msg_json = json.loads(msg.payload)

        _LOGGER.info(f"Received MQTT message: {msg_json}")

        # Extract the EVENT field
        event = msg_json.get('event')

        if event is None:
            _LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
            return

        # Use the mapping to convert the event to the corresponding state
        new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
        if new_state is not None:
            self._state = new_state
            self.async_schedule_update_ha_state()
        #else:
            #_LOGGER.warning(f"No mapping found for event '{event}'")


class SAASSleepTrackingSensor(Entity):
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

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                #_LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            self._state = new_state
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

class SAASDisturbanceSensor(Entity):
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

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                #_LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = DISTURBANCE_MAPPING.get(event, "None")
            self._state = new_state
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)

class SAASLullabySensor(Entity):
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

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Parse the incoming message
            msg_json = json.loads(msg.payload)

            _LOGGER.info(f"Received MQTT message: {msg_json}")

            # Extract the EVENT field
            event = msg_json.get('event')

            if event is None:
                #_LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
                return

            # Use the mapping to convert the event to the corresponding state
            new_state = self._mapping.get(event, "None")  # Default to "None" if no mapping found
            self._state = new_state
            self.async_schedule_update_ha_state()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][self.entry_id][CONF_TOPIC], message_received)
class SAASWakeStatusSensor(Entity):
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
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Extracted Event {event} from message.")
    
            # Map the event to a known state, or "Unknown" if the event is not recognized
            mapped_value = STATE_MAPPING.get(event, "Unknown")
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Mapped {event} to {mapped_value}.")
    
            # If the event could not be mapped to a known state, set the sensor state to "Unknown"
            if mapped_value == "Unknown":
                self._state = "Unknown"
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Event {event} could not be mapped to a known state. Setting sensor state to 'Unknown'.")
    
            # If the mapped value is in the awake states, add it to the awake bucket and clear the sleep bucket
            if mapped_value in self.awake_states:
                self.awake_bucket.append((mapped_value, now))
                self.sleep_bucket = []
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Mapped value {mapped_value} is in awake states. Adding to awake bucket and clearing sleep bucket.")
    
            # If the mapped value is in the sleep states, add it to the sleep bucket and clear the awake bucket
            elif mapped_value in self.sleep_states:
                self.sleep_bucket.append((mapped_value, now))
                self.awake_bucket = []
                _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Mapped value {mapped_value} is in sleep states. Adding to sleep bucket and clearing awake bucket.")
    
            # Remove messages from the awake bucket that are older than the awake duration
            self.awake_bucket = [(val, timestamp) for val, timestamp in self.awake_bucket if now - timestamp < self.awake_duration]
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Removing messages from awake bucket that are older than the awake duration.")
    
            # Remove messages from the sleep bucket that are older than the sleep duration
            self.sleep_bucket = [(val, timestamp) for val, timestamp in self.sleep_bucket if now - timestamp < self.sleep_duration]
            _LOGGER.debug(f"{dt_util.as_local(now).strftime('%H:%M:%S:%f')}: Removing messages from sleep bucket that are older than the sleep duration.")
        except Exception as e:
            _LOGGER.error(f"Error processing message: {e}")

    async def async_update(self):
        """Update the state."""
        now = dt_util.utcnow()
    
        # Remove messages from the awake bucket that are older than the awake duration
        self.awake_bucket = [(val, timestamp) for val, timestamp in self.awake_bucket if now - timestamp < self.awake_duration]
    
        # Remove messages from the sleep bucket that are older than the sleep duration
        self.sleep_bucket = [(val, timestamp) for val, timestamp in self.sleep_bucket if now - timestamp < self.sleep_duration]
    
        # If all messages in the awake bucket are within the awake duration, set the state to "Awake"
        if self.awake_bucket and all(now - timestamp <= self.awake_duration for _, timestamp in self.awake_bucket):
            self._state = "Awake"
    
        # If all messages in the sleep bucket are within the sleep duration, set the state to "Asleep"
        elif self.sleep_bucket and all(now - timestamp <= self.sleep_duration for _, timestamp in self.sleep_bucket):
            self._state = "Asleep"
    
    async def interval_callback(self, _):
        """Wrapper function for async_track_time_interval."""
        # Call the async_update method to update the state
        await self.async_update()
    
    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()
    
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
async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the SAAS sensor platform from a config entry."""
    name = hass.data[DOMAIN][entry.entry_id].get(CONF_NAME, "Default Name")
    topic = hass.data[DOMAIN][entry.entry_id].get(CONF_TOPIC)
    awake_states = hass.data[DOMAIN][entry.entry_id].get(CONF_AWAKE_STATES)
    sleep_states = hass.data[DOMAIN][entry.entry_id].get(CONF_SLEEP_STATES)
    awake_duration = hass.data[DOMAIN][entry.entry_id].get(CONF_AWAKE_DURATION)
    sleep_duration = hass.data[DOMAIN][entry.entry_id].get(CONF_SLEEP_DURATION)

    entities = [
        SAASSensor(hass, name, STATE_MAPPING, entry_id),
        SAASAlarmEventSensor(hass, name, ALARM_EVENT_MAPPING, entry_id),
        SAASSoundSensor(hass, name, SOUND_MAPPING, entry_id),
        SAASSleepTrackingSensor(hass, name, SLEEP_TRACKING_MAPPING, entry_id), 
        SAASDisturbanceSensor(hass, name, DISTURBANCE_MAPPING, entry_id),
        SAASLullabySensor(hass, name, LULLABY_MAPPING, entry_id),
        SAASWakeStatusSensor(hass, name, awake_states, sleep_states, awake_duration, sleep_duration, topic, entry_id)
    ]

    for entity in entities:
        if hasattr(entity, "async_setup"):
            await entity.async_setup()

    async_add_entities(entities)

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
        SAASWakeStatusSensor(hass, name, awake_states, sleep_states, awake_duration, sleep_duration, topic, entry_id)
    ]

    for entity in entities:
        if hasattr(entity, "async_setup"):
            await entity.async_setup()

    async_add_entities(entities)