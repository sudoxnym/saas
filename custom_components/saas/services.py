import logging
from homeassistant.core import ServiceCall, HomeAssistant
from .const import DOMAIN, DAY_MAPPING

_LOGGER = logging.getLogger(__name__)

class SAASService:
    def __init__(self, hass, name, notify_target):
        self._hass = hass
        self._name = name
        self._notify_target = notify_target
        _LOGGER.debug(f"SAASService initialized with name: {name}, notify_target: {notify_target}")

    async def call_service(self, service_call: ServiceCall):
        """Call the service."""
        service_name = self._notify_target  # Remove the "notify." prefix

        # Extract parameters with default values
        params = ['message', 'day', 'hour', 'minute']
        defaults = ['Default Message', 'monday', 0, 0]
        message, day, hour, minute = (service_call.data.get(param, default) for param, default in zip(params, defaults))

        _LOGGER.debug(f"Extracted parameters from service call: message: {message}, day: {day}, hour: {hour}, minute: {minute}")

        # Convert day name to number
        day_number = DAY_MAPPING.get(day.lower(), day)

        _LOGGER.debug(f"Converted day name to number: {day_number}")

        _LOGGER.info(f"Service called with message: {message}, day: {day_number}, hours: {hour}, minutes: {minute}")

        service_data = {
            "message": "command_activity",
            "data": {
                "intent_action": "android.intent.action.SET_ALARM",
                "intent_extras": f"android.intent.extra.alarm.SKIP_UI:true,android.intent.extra.alarm.MESSAGE:{message},android.intent.extra.alarm.DAYS:{day_number}:ArrayList<Integer>,android.intent.extra.alarm.HOUR:{hour},android.intent.extra.alarm.MINUTES:{minute}"
            },
        }

        _LOGGER.debug(f"Prepared service data: {service_data}")

        try:
            await self._hass.services.async_call(
                "notify",
                service_name,
                service_data,
                blocking=True,
            )
            _LOGGER.info(f"Service call completed")
        except Exception as e:
            _LOGGER.error(f"Error occurred while calling service: {e}")

async def async_setup_services(hass: HomeAssistant) -> bool:
    """Set up services for the SAAS component."""
    _LOGGER.info(f"Setting up services for {DOMAIN}")
    # Register the service for each entry
    for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
        if entry_data:
            name = entry_data.get('name', 'default name')
            notify_target = entry_data.get('notify_target', 'default notify target')
            if notify_target:  # Only register the service if notify_target was chosen
                _LOGGER.debug(f"Found notify_target: {notify_target} for name: {name}. Registering service.")
                saas_service = SAASService(hass, name, notify_target)
                try:
                    hass.services.async_register(DOMAIN, f'saas_{name}_alarm_set', saas_service.call_service)
                    _LOGGER.info(f"Registered service: saas_{name}_alarm_set")
                except Exception as e:
                    _LOGGER.error(f"Error occurred while registering service: {e}")
            else:
                _LOGGER.warning(f"No notify_target found for name: {name}. Skipping service registration.")
        else:
            _LOGGER.warning(f"No entry data found for entry_id: {entry_id}")
    _LOGGER.info(f"Finished setting up services for {DOMAIN}")

    return True