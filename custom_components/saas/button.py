import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN, INTEGRATION_NAME, MODEL, CONF_NAME, CONF_NOTIFY_TARGET
import asyncio

# Set up logging
# _LOGGER = logging.getLogger(__name__)

class SAASSleepTrackingStart(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Sleep Tracking Start button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target  # Store notify_target as an instance variable
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_sleep_tracking_start_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Sleep Tracking Start"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.alarmclock.START_SLEEP_TRACK",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)
        
class SAASSleepTrackingStop(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Sleep Tracking Stop button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_sleep_tracking_stop_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Sleep Tracking Stop"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.alarmclock.STOP_SLEEP_TRACK",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)

class SAASSleepTrackingPause(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Sleep Tracking Pause button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_sleep_tracking_pause_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Sleep Tracking Pause"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.ACTION_PAUSE_TRACKING",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)

class SAASSleepTrackingResume(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Sleep Tracking Pause button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_sleep_tracking_resume_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Sleep Tracking Resume"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.ACTION_RESUME_TRACKING",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)

class SAASAlarmClockSnooze(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Alarm Clock Snooze button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_alarm_clock_snooze_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Alarm Clock Snooze"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.alarmclock.ALARM_SNOOZE",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)

class SAASAlarmClockDisable(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Alarm Clock Disable button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_alarm_clock_disable_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Alarm Clock Disable"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.alarmclock.ALARM_DISMISS_CAPTCHA",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)

class SAASSleepTrackingStartWithAlarm(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Sleep Tracking Start with Alarm button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_sleep_tracking_start_with_alarm_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Sleep Tracking Start with Alarm"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.alarmclock.START_SLEEP_TRACK_WITH_IDEAL_ALARM_ACTION",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)

class SAASLullabyStop(ButtonEntity):
    def __init__(self, hass, name, notify_target):
        """Initialize the button."""
        # _LOGGER.debug("Initializing SAAS Lullaby Stop button with name: %s", name)
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        self._state = "off"
        # _LOGGER.debug("Button initialized with state: %s", self._state)

    @property
    def unique_id(self):
        """Return a unique ID."""
        unique_id = f"saas_lullaby_stop_{self._name}"
        # _LOGGER.debug("Getting unique ID for the button: %s", unique_id)
        return unique_id

    @property
    def name(self):
        """Return the name of the button."""
        name = f"SAAS {self._name} Lullaby Stop"
        # _LOGGER.debug("Getting name of the button: %s", name)
        return name

    @property
    def is_on(self):
        """Return true if the button is on."""
        # _LOGGER.debug("Checking if the button is on. Current state: %s", self._state)
        return self._state == "on"

    @property
    def device_info(self):
        """Return information about the device."""
        device_info = {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
        # _LOGGER.debug("Getting device information: %s", device_info)
        return device_info

    def press(self):
        if not self._notify_target:
            self._hass.components.persistent_notification.async_create(
                "add a mobile device to use this function",
                title=self.name,
            )
            return
        """Press the button."""
        service_name = self._notify_target  # Remove the "notify." prefix
    
        service_data = {
            "message": "command_broadcast_intent",
            "data": {
                "intent_package_name": "com.urbandroid.sleep",
                "intent_action": "com.urbandroid.sleep.ACTION_LULLABY_STOP_PLAYBACK",
            },
        }
        # _LOGGER.debug("Pressing the button with service call:\n"
        #              "service: %s\n"
        #              "data:\n"
        #              "%s", service_name, service_data)
        self._hass.services.call(
            "notify",
            service_name,
            service_data,
            blocking=True,
        )
        self._state = "on"
        self.schedule_update_ha_state()
        # _LOGGER.debug("Button pressed. Current state: %s", self._state)


        
async def async_setup_entry(hass, config_entry, async_add_entities):
    notify_target = config_entry.data.get(CONF_NOTIFY_TARGET)
    if not notify_target:
        _LOGGER.warning("no notify_target configured; skipping button setup")
        return
    # _LOGGER.debug("Setting up SAAS Sleep Tracking buttons from a config entry with data: %s", config_entry.data)
    
    # Extract the necessary data from config_entry.data
    name = config_entry.data[CONF_NAME]
    notify_target = config_entry.data.get(CONF_NOTIFY_TARGET)
    
    # Create instances of SAASSleepTrackingStart, SAASSleepTrackingStop and SAASSleepTrackingPause
    entities = [
        SAASSleepTrackingStart(hass, name, notify_target),
        SAASSleepTrackingStop(hass, name, notify_target),
        SAASSleepTrackingPause(hass, name, notify_target),
        SAASSleepTrackingResume(hass, name, notify_target),
        SAASAlarmClockSnooze(hass, name, notify_target),
        SAASAlarmClockDisable(hass, name, notify_target),
        SAASSleepTrackingStartWithAlarm(hass, name, notify_target),
        SAASLullabyStop(hass, name, notify_target),
    ]

    # Call async_setup on each entity if it has that method
    for entity in entities:
        if hasattr(entity, "async_setup"):
            await entity.async_setup()

    # Add the entities
    async_add_entities(entities)
    # _LOGGER.debug("SAAS Sleep Tracking buttons set up successfully")