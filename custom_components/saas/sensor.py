import asyncio
import json
from datetime import timedelta
from collections import deque
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.components.mqtt import async_subscribe
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, CONF_NAME, CONF_TOPIC, CONF_AWAKE_STATES, CONF_SLEEP_STATES, CONF_AWAKE_DURATION, CONF_SLEEP_DURATION, INTEGRATION_NAME, MODEL


# Define the state mapping directly in the file
state_mapping = {
    'unknown': "Unknown",
    '{"event":"sleep_tracking_started"}': "Sleep Tracking Started",
    '{"event":"sleep_tracking_stopped"}': "Sleep Tracking Stopped",
    '{"event":"sleep_tracking_paused"}': "Sleep Tracking Paused",
    '{"event":"sleep_tracking_resumed"}': "Sleep Tracking Resumed",
    '{"event":"alarm_snooze_clicked"}': "Alarm Snoozed",
    '{"event":"alarm_snooze_canceled"}': "Snooze Canceled",
    '{"event":"time_to_bed_alarm_alert"}': "Time To Bed Alarm Alert",
    'alarm_alert_start': "Alarm Alert Started",
    'alarm_alert_dismiss': "Alarm Dismissed",
    '{"event":"alarm_skip_next"}': "Skip Next Alarm",
    '{"event":"show_skip_next_alarm"}': "Show Skip Next Alarm",
    '{"event":"rem"}': "REM",
    '{"event":"smart_period"}': "Smart Period",
    '{"event":"before_smart_period"}': "Before Smart Period",
    '{"event":"lullaby_start"}': "Lullaby Start",
    '{"event":"lullaby_stop"}': "Lullaby Stop",
    '{"event":"lullaby_volume_down"}': "Lullaby Volume Down",
    '{"event":"deep_sleep"}': "Deep Sleep",
    '{"event":"light_sleep"}': "Light Sleep",
    '{"event":"awake"}': "Awake",
    '{"event":"not_awake"}': "Not Awake",
    '{"event":"apnea_alarm"}': "Apnea Alarm",
    '{"event":"antisnoring"}': "Antisnoring",
    '{"event":"before_alarm"}': "Before Alarm",
    '{"event":"sound_event_snore"}': "Snore Detected",
    '{"event":"sound_event_talk"}': "Talk Detected",
    '{"event":"sound_event_cough"}': "Cough Detected",
    '{"event":"sound_event_baby"}': "Baby Cry Detected",
    '{"event":"sound_event_laugh"}': "Laugh Detected",
    '{"event":"alarm_rescheduled"}': "Alarm Rescheduled"
}

# Define the sound mapping directly in the file
sound_mapping = {
    '{"event":"sound_event_snore"}': "Snore Detected",
    '{"event":"sound_event_talk"}': "Talk Detected",
    '{"event":"sound_event_cough"}': "Cough Detected",
    '{"event":"sound_event_baby"}': "Baby Cry Detected",
    '{"event":"sound_event_laugh"}': "Laugh Detected",
}

disturbance_mapping = {
    '{"event":"apnea_alarm"}': "Apnea Alarm",
    '{"event":"antisnoring"}': "Antisnoring",
}

# Define the alarm event mapping directly in the file
alarm_event_mapping = {
    '{"event":"before_alarm"}': "Before Alarm",
    '{"event":"alarm_snooze_clicked"}': "Alarm Snoozed",
    '{"event":"alarm_snooze_canceled"}': "Snooze Canceled",
    '{"event":"time_to_bed_alarm_alert"}': "Time To Bed Alarm Alert",
    '{"event":"alarm_alert_start"}': "Alarm Alert Started",
    '{"event":"alarm_alert_dismiss"}': "Alarm Dismissed",
    '{"event":"alarm_skip_next"}': "Skip Next Alarm",
    '{"event":"show_skip_next_alarm"}': "Show Skip Next Alarm",
    '{"event":"rem"}': "REM",
    '{"event":"smart_period"}': "Smart Period",
    '{"event":"before_smart_period"}': "Before Smart Period",
}

# Define the sleep tracking event mapping directly in the file
sleep_tracking_mapping = {
    '{"event":"sleep_tracking_started"}': "Sleep Tracking Started",
    '{"event":"sleep_tracking_stopped"}': "Sleep Tracking Stopped",
    '{"event":"sleep_tracking_paused"}': "Sleep Tracking Paused",
    '{"event":"sleep_tracking_resumed"}': "Sleep Tracking Resumed",
}

# Define the wake status event mapping directly in the file
wake_status_mapping = {
    '{"event":"awake"}': "Awake",
    '{"event":"not_awake"}': "Not Awake",
}

class SAASSensor(Entity):
    async def async_setup(self):
        """Run when the entity is about to be added."""
        pass
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
            # Use the mapping to convert the MQTT payload to the corresponding state
            new_state = self._mapping.get(msg.payload)
            if new_state is not None:
                self._state = new_state
                self.async_schedule_update_ha_state()

        await async_subscribe(self._hass, self._hass.data[DOMAIN]["topic_template"], message_received)

class SAASSoundSensor(SAASSensor):
    """Representation of a SAAS - Sleep As Android Stats sound sensor."""

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sound_sensor_{self._name}"

    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Sound"

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Use the mapping to convert the MQTT payload to the corresponding state
            new_state = self._mapping.get(msg.payload, "None")
            self._state = new_state
            self.async_schedule_update_ha_state()

        await async_subscribe(self._hass, self._hass.data[DOMAIN]["topic_template"], message_received)

class SAASDisturbanceSensor(SAASSensor):
    """Representation of a SAAS - Sleep As Android Stats disturbance sensor."""

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_disturbance_sensor_{self._name}"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Disturbance"

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Use the mapping to convert the MQTT payload to the corresponding state
            new_state = self._mapping.get(msg.payload, "None")
            self._state = new_state
            self.async_schedule_update_ha_state()

        await async_subscribe(self._hass, self._hass.data[DOMAIN]["topic_template"], message_received)

class SAASAlarmEventSensor(SAASSensor):
    """Representation of a SAAS - Sleep As Android Stats alarm event sensor."""

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_alarm_event_sensor_{self._name}"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Alarm Event"

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Try to parse the payload as JSON
            try:
                payload = json.loads(msg.payload)
            except json.JSONDecodeError:
                # If it's not JSON, use the raw payload
                payload = msg.payload

            # Use the mapping to convert the MQTT payload to the corresponding state
            new_state = self._mapping.get(payload)
            if new_state is not None:
                self._state = new_state
                self.async_schedule_update_ha_state()

        await async_subscribe(self._hass, self._hass.data[DOMAIN]["topic_template"], message_received)

class SAASSleepTrackingSensor(SAASSensor):
    """Representation of a SAAS - Sleep As Android Stats sleep tracking sensor."""

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_sleep_tracking_sensor_{self._name}"
    
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Sleep Tracking"

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        async def message_received(msg):
            """Handle new MQTT messages."""
            # Use the mapping to convert the MQTT payload to the corresponding state
            new_state = self._mapping.get(msg.payload)
            if new_state is not None:
                self._state = new_state
                self.async_schedule_update_ha_state()

        await async_subscribe(self._hass, self._hass.data[DOMAIN]["topic_template"], message_received)

class SAASWakeStatusSensor(Entity):
    def __init__(self, hass, name, topic, awake_states, sleep_states, awake_duration, sleep_duration):
        self._state = None
        self._name = name
        self._topic = topic
        self._awake_states = awake_states
        self._sleep_states = sleep_states
        self._awake_duration = timedelta(minutes=awake_duration)
        self._sleep_duration = timedelta(minutes=sleep_duration)
        self._message_timestamps = deque()
        self._message_states = deque()

        async_track_time_interval(hass, self._async_update_state, timedelta(seconds=10))

    async def some_async_function(self):
        await async_subscribe(self.hass, self._topic, self._message_received)

        async_subscribe(hass, self._topic, self._message_received)


    
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
    def unique_id(self):
        """Return a unique ID."""
        return f"saas_wake_status_sensor_{self._name}"
            
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SAAS {self._name} Wake Status"
    
    @property
    def state(self):
        return self._state

    async def _message_received(self, msg):
        now = datetime.now()
        self._message_timestamps.append(now)
        self._message_states.append(msg)

        # Remove messages older than sleep_duration
        while self._message_timestamps and now - self._message_timestamps[0] > self._sleep_duration:
            self._message_timestamps.popleft()
            self._message_states.popleft()



    async def _async_update_state(self, now):
        # Check if the only messages in the last awake_duration are awake_states
        for timestamp, state in zip(self._message_timestamps, self._message_states):
            if now - timestamp <= self._awake_duration and state not in self._awake_states:
                break
        else:
            self._state = "Awake"
            return

        # Check if the only messages in the last sleep_duration are sleep_states
        for state in self._message_states:
            if state not in self._sleep_states:
                break
        else:
            self._state = "Asleep"
            return

        self._state = "Unknown"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the SAAS sensor platform."""
    name = hass.data[DOMAIN].get(CONF_NAME, "Default Name")
    topic = hass.data[DOMAIN].get(CONF_TOPIC)
    awake_states = hass.data[DOMAIN].get(CONF_AWAKE_STATES)
    sleep_states = hass.data[DOMAIN].get(CONF_SLEEP_STATES)
    awake_duration = hass.data[DOMAIN].get(CONF_AWAKE_DURATION)
    sleep_duration = hass.data[DOMAIN].get(CONF_SLEEP_DURATION)

    entities = [
        SAASSensor(hass, name, state_mapping),
        SAASSoundSensor(hass, name, sound_mapping),
        SAASDisturbanceSensor(hass, name, disturbance_mapping),
        SAASAlarmEventSensor(hass, name, alarm_event_mapping),
        SAASSleepTrackingSensor(hass, name, sleep_tracking_mapping),
        SAASWakeStatusSensor(hass, name, topic, awake_states, sleep_states, awake_duration, sleep_duration)
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

    entities = [
        SAASSensor(hass, name, state_mapping),
        SAASSoundSensor(hass, name, sound_mapping),
        SAASDisturbanceSensor(hass, name, disturbance_mapping),
        SAASAlarmEventSensor(hass, name, alarm_event_mapping),
        SAASSleepTrackingSensor(hass, name, sleep_tracking_mapping),
        SAASWakeStatusSensor(hass, name, topic, awake_states, sleep_states, awake_duration, sleep_duration)
    ]

    for entity in entities:
        if hasattr(entity, "async_setup"):
            await entity.async_setup()

    async_add_entities(entities)