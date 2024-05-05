from homeassistant.helpers.entity import Entity
from homeassistant.components.mqtt import async_subscribe
from .const import DOMAIN, CONF_NAME, INTEGRATION_NAME, MODEL

# Define the state mapping directly in the file
state_mapping = {
    "unknown": "Unknown",
    '{"event":"sleep_tracking_started"}': "Sleep Tracking Started",
    '{"event":"sleep_tracking_stopped"}': "Sleep Tracking Stopped",
    '{"event":"sleep_tracking_paused"}': "Sleep Tracking Paused",
    '{"event":"sleep_tracking_resumed"}': "Sleep Tracking Resumed",
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

class SAASSensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats sensor."""
    def __init__(self, hass, name, mapping):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._hass = hass
        self._mapping = mapping

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

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SAAS sensor platform."""
    name = hass.data[DOMAIN].get(CONF_NAME, "Default Name")
    add_entities([SAASSensor(hass, name, state_mapping), SAASSoundSensor(hass, name, sound_mapping)])