import logging
import voluptuous as vol
from .const import (
    DOMAIN,
    CONF_NAME,
    CONF_TOPIC,
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
from voluptuous import Schema, Required, Optional, In
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)


class MyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial config flow for SAAS."""
    VERSION = 2
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Initial setup step."""
        errors = {}

        # discover available mobile_app notify services
        notify_services = self.hass.services.async_services().get("notify", {})
        notify_targets = {
            svc.replace("mobile_app_", "")
               .replace("_", " ")
               .lower(): svc
            for svc in notify_services
            if svc.startswith("mobile_app_")
        }

        if user_input is not None:
            # map chosen label back to service name, or remove if invalid
            nt_label = user_input.get(CONF_NOTIFY_TARGET)
            if nt_label in notify_targets:
                user_input[CONF_NOTIFY_TARGET] = notify_targets[nt_label]
            else:
                user_input.pop(CONF_NOTIFY_TARGET, None)

            # basic validation
            if not user_input.get(CONF_NAME):
                errors[CONF_NAME] = "required"

            if not errors:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input
                )

        # build initial form schema
        schema = {
            Required(CONF_NAME): str,
            Required(CONF_TOPIC): str,
            Required(CONF_AWAKE_DURATION, default=DEFAULT_AWAKE_DURATION): int,
            Required(CONF_SLEEP_DURATION, default=DEFAULT_SLEEP_DURATION): int,
            Required(
                CONF_AWAKE_STATES, default=DEFAULT_AWAKE_STATES
            ): cv.multi_select(AVAILABLE_STATES),
            Required(
                CONF_SLEEP_STATES, default=DEFAULT_SLEEP_STATES
            ): cv.multi_select(AVAILABLE_STATES),
        }
        if notify_targets:
            # truly optional, only real targets, no blank choice
            schema[Optional(CONF_NOTIFY_TARGET)] = In(list(notify_targets.keys()))

        return self.async_show_form(
            step_id="user",
            data_schema=Schema(schema),
            errors=errors,
        )

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(entry):
        """Return options flow handler."""
        return OptionsFlowHandler(entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle SAAS options editing."""

    def __init__(self, entry):
        super().__init__()
        self._config_entry = entry

    async def async_step_init(self, user_input=None):
        """Manage the options form (edit)."""
        current = dict(self._config_entry.data)

        # discover mobile_app notify services again
        notify_services = self.hass.services.async_services().get("notify", {})
        notify_targets = {
            svc.replace("mobile_app_", "")
               .replace("_", " ")
               .lower(): svc
            for svc in notify_services
            if svc.startswith("mobile_app_")
        }
        # reverse map for defaults
        reverse_map = {v: k for k, v in notify_targets.items()}

        if user_input is not None:
            new_data = current.copy()

            # standard fields
            for key in (
                CONF_NAME,
                CONF_TOPIC,
                CONF_AWAKE_DURATION,
                CONF_SLEEP_DURATION,
                CONF_AWAKE_STATES,
                CONF_SLEEP_STATES,
            ):
                if key in user_input:
                    new_data[key] = user_input[key]

            # handle notify_target with "no mobile" option
            sel = user_input.get(CONF_NOTIFY_TARGET)
            if sel == "no mobile":
                new_data.pop(CONF_NOTIFY_TARGET, None)
            elif sel in notify_targets:
                new_data[CONF_NOTIFY_TARGET] = notify_targets[sel]

            # persist back into entry.data and reload
            self.hass.config_entries.async_update_entry(
                self._config_entry,
                data=new_data,
            )
            await self.hass.config_entries.async_reload(self._config_entry.entry_id)

            return self.async_create_entry(title="", data=None)

        # build edit form schema with defaults
        schema = {
            Required(
                CONF_NAME, default=current.get(CONF_NAME, "")
            ): str,
            Required(
                CONF_TOPIC, default=current.get(CONF_TOPIC, "")
            ): str,
            Required(
                CONF_AWAKE_DURATION,
                default=current.get(CONF_AWAKE_DURATION, DEFAULT_AWAKE_DURATION),
            ): int,
            Required(
                CONF_SLEEP_DURATION,
                default=current.get(CONF_SLEEP_DURATION, DEFAULT_SLEEP_DURATION),
            ): int,
            Required(
                CONF_AWAKE_STATES,
                default=current.get(CONF_AWAKE_STATES, DEFAULT_AWAKE_STATES),
            ): cv.multi_select(AVAILABLE_STATES),
            Required(
                CONF_SLEEP_STATES,
                default=current.get(CONF_SLEEP_STATES, DEFAULT_SLEEP_STATES),
            ): cv.multi_select(AVAILABLE_STATES),
        }

        if notify_targets:
            # prepend "no mobile", then all real targets, all lowercase with spaces
            labels = ["no mobile"] + list(notify_targets.keys())
            default_label = reverse_map.get(
                current.get(CONF_NOTIFY_TARGET), "no mobile"
            )
            schema[Optional(CONF_NOTIFY_TARGET, default=default_label)] = In(labels)

        return self.async_show_form(
            step_id="init",
            data_schema=Schema(schema),
            errors={},
        )
