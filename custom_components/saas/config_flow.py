import logging
import voluptuous as vol
from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_TOPIC,
    CONF_QOS,
    AVAILABLE_STATES,
    CONF_AWAKE_DURATION,
    CONF_SLEEP_DURATION,
    CONF_AWAKE_STATES,
    CONF_SLEEP_STATES,
    DEFAULT_AWAKE_DURATION,
    DEFAULT_SLEEP_DURATION,
    DEFAULT_AWAKE_STATES,
    DEFAULT_SLEEP_STATES,
    CONF_NOTIFY_TARGET,
)
from homeassistant import config_entries
from homeassistant.core import callback
from voluptuous import Schema, Required, In, Optional
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SAAS."""
    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        # Build notify targets list
        notify_services = self.hass.services.async_services().get("notify", {})
        notify_targets = {
            key.replace("mobile_app_", "").title(): key
            for key in notify_services.keys()
            if key.startswith("mobile_app_")
        }

        if user_input is not None:
            # Map back the chosen label to service name
            if user_input.get(CONF_NOTIFY_TARGET):
                user_input[CONF_NOTIFY_TARGET] = notify_targets.get(user_input[CONF_NOTIFY_TARGET])
            if not user_input.get(CONF_NAME):
                errors[CONF_NAME] = "required"
            if not errors:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=Schema(
                {
                    Required(CONF_NAME): str,
                    Required(CONF_TOPIC): str,
                    Required(CONF_QOS, default=0): In([0, 1, 2]),
                    Required(CONF_AWAKE_DURATION, default=DEFAULT_AWAKE_DURATION): int,
                    Required(CONF_SLEEP_DURATION, default=DEFAULT_SLEEP_DURATION): int,
                    Required(CONF_AWAKE_STATES, default=DEFAULT_AWAKE_STATES): cv.multi_select(AVAILABLE_STATES),
                    Required(CONF_SLEEP_STATES, default=DEFAULT_SLEEP_STATES): cv.multi_select(AVAILABLE_STATES),
                    Optional(CONF_NOTIFY_TARGET): vol.In(list(notify_targets.keys())),
                }
            ),
            errors=errors,
        )

    async def async_migrate_entry(self, hass, entry):
        """Migrate old config entries to the new schema."""
        _LOGGER.debug("Migrating config entry %s from version %s", entry.entry_id, entry.version)
        data = {**entry.data}
        options = {**entry.options}

        # If you renamed keys in entry.data/options, do it here when entry.version == 1
        # e.g.:
        # if entry.version == 1:
        #     data["topic_template"] = data.pop("topic")
        #     entry.version = 2

        # For no data changes, just bump the version:
        entry.version = self.VERSION
        hass.config_entries.async_update_entry(entry, data=data, options=options)
        _LOGGER.info("Migrated config entry %s to version %s", entry.entry_id, entry.version)
        return True

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        """Get the options flow handler."""
        return OptionsFlowHandler(entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle SAAS options."""

    def __init__(self, entry):
        """Initialize options flow."""
        super().__init__()
        self._config_entry = entry  # use private attribute

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        # Load current options or fall back to data
        current = self._config_entry.options.copy()
        for key in [
            CONF_NAME,
            CONF_TOPIC,
            CONF_QOS,
            CONF_AWAKE_DURATION,
            CONF_SLEEP_DURATION,
            CONF_AWAKE_STATES,
            CONF_SLEEP_STATES,
            CONF_NOTIFY_TARGET,
        ]:
            if key not in current and key in self._config_entry.data:
                current[key] = self._config_entry.data[key]

        # Build notify targets list
        notify_services = self.hass.services.async_services().get("notify", {})
        notify_targets = {
            key.replace("mobile_app_", "").title(): key
            for key in notify_services.keys()
            if key.startswith("mobile_app_")
        }

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    Required(CONF_NAME, default=current.get(CONF_NAME, "")): str,
                    Required(CONF_TOPIC, default=current.get(CONF_TOPIC, "")): str,
                    Required(CONF_QOS, default=current.get(CONF_QOS, 0)): In([0, 1, 2]),
                    Required(CONF_AWAKE_DURATION, default=current.get(CONF_AWAKE_DURATION, DEFAULT_AWAKE_DURATION)): int,
                    Required(CONF_SLEEP_DURATION, default=current.get(CONF_SLEEP_DURATION, DEFAULT_SLEEP_DURATION)): int,
                    Required(CONF_AWAKE_STATES, default=current.get(CONF_AWAKE_STATES, DEFAULT_AWAKE_STATES)): cv.multi_select(AVAILABLE_STATES),
                    Required(CONF_SLEEP_STATES, default=current.get(CONF_SLEEP_STATES, DEFAULT_SLEEP_STATES)): cv.multi_select(AVAILABLE_STATES),
                    Optional(CONF_NOTIFY_TARGET, default=current.get(CONF_NOTIFY_TARGET, "")): vol.In(list(notify_targets.keys())),
                }
            ),
            errors={},
        )
