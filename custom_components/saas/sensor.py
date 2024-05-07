import asyncio
import json
from datetime import timedelta, datetime
from collections import deque
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.mqtt import async_subscribe
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_NAME, CONF_TOPIC, CONF_AWAKE_STATES, CONF_SLEEP_STATES, CONF_AWAKE_DURATION, CONF_SLEEP_DURATION, INTEGRATION_NAME, MODEL, STATE_MAPPING, SOUND_MAPPING, DISTURBANCE_MAPPING, ALARM_EVENT_MAPPING, SLEEP_TRACKING_MAPPING
import logging

_LOGGER = logging.getLogger(__name__)

class SAASSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor."""

    def __init__(self, hass, name, mapping):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping

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
        await async_subscribe(self._hass, self._hass.data[DOMAIN][CONF_TOPIC], message_received)

class SAASAlarmEventSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Alarm Events."""

    def __init__(self, hass, name, mapping):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping
        self._value1 = None
        self._time = None

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
        await async_subscribe(self._hass, self._hass.data[DOMAIN][CONF_TOPIC], message_received)

    
class SAASSoundSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Sound Events."""
    def __init__(self, hass, name, mapping):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping

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
        await async_subscribe(self._hass, self._hass.data[DOMAIN][CONF_TOPIC], message_received)

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
    def __init__(self, hass, name, mapping):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping

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
        await async_subscribe(self._hass, self._hass.data[DOMAIN][CONF_TOPIC], message_received)

class SAASDisturbanceSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Disturbance Events."""
    def __init__(self, hass, name, mapping):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping

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
        await async_subscribe(self._hass, self._hass.data[DOMAIN][CONF_TOPIC], message_received)

class SAASWakeStatusSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor for Wake Status."""


    def __init__(self, hass, name, awake_states, sleep_states, awake_duration, sleep_duration):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._awake_states = awake_states
        self._sleep_states = sleep_states
        self._awake_duration = timedelta(seconds=awake_duration)
        self._sleep_duration = timedelta(seconds=sleep_duration)
        self._last_message_time = datetime.now()
        _LOGGER.info(f"Subscribing to topic: {self._hass.data[DOMAIN][CONF_TOPIC]}")

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_wake_status_sensor_{self._name}"

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

    async def message_received(self, msg):
        """Handle new MQTT messages."""
        # Parse the incoming message
        msg_json = json.loads(msg.payload)

        _LOGGER.info(f"Received MQTT message: {msg_json}")

        # Extract the EVENT field
        event = msg_json.get('event')

        if event is None:
            _LOGGER.warning(f"No 'event' key in the MQTT message: {msg_json}")
            return

        # Update the last message time
        self._last_message_time = datetime.now()

        # Check if the event matches the awake or asleep states
        if event in self._awake_states:
            self._state = 'Awake'
        elif event in self._sleep_states:
            self._state = 'Asleep'

        self.async_schedule_update_ha_state()

        _LOGGER.info(f"Message received. Event: {event}, State: {self._state}")

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Subscribe to the topic from the user input
        await async_subscribe(self._hass, self._hass.data[DOMAIN][CONF_TOPIC], self.message_received)

        # Connect to the time changed event
        async_dispatcher_connect(self._hass, 'time_changed', self._time_changed)

        # Schedule time interval updates
        async_track_time_interval(self._hass, self._time_changed, timedelta(seconds=10))

    async def _time_changed(self, event_time):
        """Handle the time changed event."""
        if self._state == 'Awake' and datetime.utcnow() - self._last_message_time > self._awake_duration:
            self._state = 'Asleep'
        elif self._state == 'Asleep' and datetime.utcnow() - self._last_message_time > self._sleep_duration:
            self._state = 'Awake'
        self.async_schedule_update_ha_state()

        _LOGGER.info(f"Time changed. State: {self._state}")


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the SAAS sensor platform."""
    name = hass.data[DOMAIN].get(CONF_NAME, "Default Name")
    topic = hass.data[DOMAIN].get(CONF_TOPIC)
    awake_states = hass.data[DOMAIN].get(CONF_AWAKE_STATES)
    sleep_states = hass.data[DOMAIN].get(CONF_SLEEP_STATES)
    awake_duration = hass.data[DOMAIN].get(CONF_AWAKE_DURATION)
    sleep_duration = hass.data[DOMAIN].get(CONF_SLEEP_DURATION)

    entities = [
        SAASSensor(hass, name, STATE_MAPPING),
        SAASAlarmEventSensor(hass, name, ALARM_EVENT_MAPPING),
        SAASSoundSensor(hass, name, SOUND_MAPPING),
        SAASSleepTrackingSensor(hass, name, SLEEP_TRACKING_MAPPING), 
        SAASDisturbanceSensor(hass, name, DISTURBANCE_MAPPING),
        SAASWakeStatusSensor(hass, name, awake_states, sleep_states, awake_duration, sleep_duration)
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
    hass.data[DOMAIN] = entry.data

    entities = [
        SAASSensor(hass, name, STATE_MAPPING),
        SAASAlarmEventSensor(hass, name, ALARM_EVENT_MAPPING),
        SAASSoundSensor(hass, name, SOUND_MAPPING),
        SAASSleepTrackingSensor(hass, name, SLEEP_TRACKING_MAPPING), 
        SAASDisturbanceSensor(hass, name, DISTURBANCE_MAPPING),
        SAASWakeStatusSensor(hass, name, awake_states, sleep_states, awake_duration, sleep_duration) 
    ]


    for entity in entities:
        if hasattr(entity, "async_setup"):
            await entity.async_setup()

    async_add_entities(entities)