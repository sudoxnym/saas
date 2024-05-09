import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect

_logger = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the SAAS - Sleep As Android Status component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a config entry."""
    hass.data.setdefault(DOMAIN, {})
    # Use hass.data[DOMAIN][entry.entry_id] instead of entry.options
    if entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.entry_id] = hass.data[DOMAIN][entry.entry_id]
    else:
        hass.data[DOMAIN][entry.entry_id] = entry.data  # Use entry.data instead of entry.options

    # Forward the setup to the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    # Define a coroutine function to reload the entry
    async def reload_entry():
        await hass.config_entries.async_reload(entry.entry_id)

    # Listen for the reload signal and reload the integration when it is received
    async_dispatcher_connect(hass, f"{DOMAIN}_reload_{entry.entry_id}", reload_entry)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Remove the sensor platform
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Ensure hass.data[DOMAIN] is a dictionary before popping
    if isinstance(hass.data.get(DOMAIN, {}), dict):
        if entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id)

    return True