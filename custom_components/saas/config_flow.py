import logging
import traceback
import voluptuous as vol
from .const import DOMAIN, CONF_NAME, CONF_TOPIC, CONF_QOS, AVAILABLE_STATES, CONF_AWAKE_DURATION, CONF_SLEEP_DURATION, CONF_AWAKE_STATES, CONF_SLEEP_STATES, DEFAULT_AWAKE_DURATION, DEFAULT_SLEEP_DURATION, DEFAULT_AWAKE_STATES, DEFAULT_SLEEP_STATES, CONF_NOTIFY_TARGET
from homeassistant import config_entries
from homeassistant.core import callback
from voluptuous import Schema, Required, In, Optional
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send

_logger = logging.getLogger(__name__)

class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""    
        errors = {}
    
        # Get the list of notify targets
        notify_services = self.hass.services.async_services().get('notify', {})
        notify_targets = {target.replace('mobile_app_', '').title(): target for target in notify_services.keys() if target.startswith('mobile_app_')}
    
        if user_input is not None:
            # Map the selected option back to the actual notify target name
            user_input[CONF_NOTIFY_TARGET] = notify_targets[user_input[CONF_NOTIFY_TARGET]]
    
            # Validate the user input here
            # If the input is valid, create an entry
            # If the input is not valid, add an error message to the 'errors' dictionary
            # For example:
            if not user_input[CONF_NAME]:
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
        _logger.debug("Entering async_step_init with user_input: %s", user_input)
    
        errors = {}  # Define errors here
    
        try:
            # Fetch the initial configuration data
            current_data = self.hass.data[DOMAIN].get(self.config_entry.entry_id, self.config_entry.options)
            _logger.debug("Current data fetched: %s", current_data)
    
            # Get the list of notify targets
            notify_services = self.hass.services.async_services().get('notify', {})
            notify_targets = {target.replace('mobile_app_', '').title(): target for target in notify_services.keys() if target.startswith('mobile_app_')}
    
            if user_input is not None:
                # Validate the user input here
                # If the input is valid, create an entry
                # If the input is not valid, add an error message to the 'errors' dictionary
                # For example:
                if not user_input[CONF_NAME]:
                    errors[CONF_NAME] = "required"
                if errors:
                    return self.async_show_form(step_id="init", data_schema=self.get_data_schema(current_data), errors=errors)  # Pass errors to async_show_form
    
                # Map the selected option back to the actual notify target name
                user_input[CONF_NOTIFY_TARGET] = notify_targets[user_input[CONF_NOTIFY_TARGET]]
    
                # Merge current_data with user_input
                updated_data = {**current_data, **user_input}
                _logger.debug("User input is not None, updated data: %s", updated_data)
    
                _logger.debug("Updating entry with updated data: %s", updated_data)
    
                if updated_data is not None:
                    self.hass.data[DOMAIN][self.config_entry.entry_id] = updated_data  # Save updated data
    
                    # Update the entry data
                    self.hass.config_entries.async_update_entry(self.config_entry, data=updated_data)  
    
                    # Send a signal to reload the integration
                    async_dispatcher_send(self.hass, f"{DOMAIN}_reload_{self.config_entry.entry_id}")
    
                    return self.async_create_entry(title="", data=updated_data)
    
            _logger.debug("User input is None, showing form with current_data: %s", current_data)
            return self.async_show_form(step_id="init", data_schema=self.get_data_schema(current_data), errors=errors)  # Pass errors to async_show_form
    
        except Exception as e:
            _logger.error("Error in async_step_init: %s", str(e))
            return self.async_abort(reason=str(e))

    def get_data_schema(self, current_data):
        # Get the list of notify targets
        notify_services = self.hass.services.async_services().get('notify', {})
        notify_targets = {target.replace('mobile_app_', '').title(): target for target in notify_services.keys() if target.startswith('mobile_app_')}
    
        # Extract the part after 'mobile_app_' and capitalize
        notify_target = current_data.get(CONF_NOTIFY_TARGET, "")
        notify_target = notify_target.replace('mobile_app_', '').title() if notify_target.startswith('mobile_app_') else notify_target
    
        return Schema(
            {
                Required(CONF_NAME, default=current_data.get(CONF_NAME, "")): str,
                Required(CONF_TOPIC, default=current_data.get(CONF_TOPIC, "")): str,
                Required(CONF_QOS, default=current_data.get(CONF_QOS, 0)): In([0, 1, 2]),
                Required(CONF_AWAKE_DURATION, default=current_data.get(CONF_AWAKE_DURATION, DEFAULT_AWAKE_DURATION)): int,
                Required(CONF_SLEEP_DURATION, default=current_data.get(CONF_SLEEP_DURATION, DEFAULT_SLEEP_DURATION)): int,
                Required(CONF_AWAKE_STATES, default=current_data.get(CONF_AWAKE_STATES, DEFAULT_AWAKE_STATES)): cv.multi_select(AVAILABLE_STATES),
                Required(CONF_SLEEP_STATES, default=current_data.get(CONF_SLEEP_STATES, DEFAULT_SLEEP_STATES)): cv.multi_select(AVAILABLE_STATES),
                Optional(CONF_NOTIFY_TARGET, default=notify_target): vol.In(list(notify_targets.keys())),  
            }
        )