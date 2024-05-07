from .const import DOMAIN, CONF_NAME, CONF_TOPIC, CONF_QOS, STATE_MAPPING, CONF_AWAKE_DURATION, CONF_SLEEP_DURATION, CONF_AWAKE_STATES, CONF_SLEEP_STATES, DEFAULT_AWAKE_DURATION, DEFAULT_SLEEP_DURATION, DEFAULT_AWAKE_STATES, DEFAULT_SLEEP_STATES
from homeassistant import config_entries
from homeassistant.core import callback
from voluptuous import Schema, Required, In
from homeassistant.helpers import config_validation as cv

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""    
        errors = {}
    
        if user_input is not None:
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
                    Required(CONF_AWAKE_STATES, default=DEFAULT_AWAKE_STATES): cv.multi_select(STATE_MAPPING),
                    Required(CONF_SLEEP_STATES, default=DEFAULT_SLEEP_STATES): cv.multi_select(STATE_MAPPING),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title=user_input.get(CONF_NAME, ""), data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=Schema(
                {
                    Required(CONF_NAME, default=self.config_entry.options.get(CONF_NAME)): str,
                    Required(CONF_TOPIC, default=self.config_entry.options.get(CONF_TOPIC)): str,
                    Required(CONF_QOS, default=self.config_entry.options.get(CONF_QOS, 0)): In([0, 1, 2]),
                    Required(CONF_AWAKE_DURATION, default=self.config_entry.options.get(CONF_AWAKE_DURATION, DEFAULT_AWAKE_DURATION)): int,
                    Required(CONF_SLEEP_DURATION, default=self.config_entry.options.get(CONF_SLEEP_DURATION, DEFAULT_SLEEP_DURATION)): int,
                    Required(CONF_AWAKE_STATES, default=self.config_entry.options.get(CONF_AWAKE_STATES, DEFAULT_AWAKE_STATES)): cv.multi_select(STATE_MAPPING),
                    Required(CONF_SLEEP_STATES, default=self.config_entry.options.get(CONF_SLEEP_STATES, DEFAULT_SLEEP_STATES)): cv.multi_select(STATE_MAPPING),
                }
            ),
        )