import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .services import async_setup_services  # Import the service setup function

_logger = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the SAAS - Sleep As Android Status component."""
    _logger.info("Starting setup of the SAAS component")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a config entry."""
    _logger.info(f"Starting setup of config entry with ID: {entry.entry_id}")
    hass.data.setdefault(DOMAIN, {})

    if entry.entry_id not in hass.data[DOMAIN] and entry.data:
        hass.data[DOMAIN][entry.entry_id] = entry.data

    _logger.info(f"hass.data[DOMAIN] after adding entry data: {hass.data[DOMAIN]}")

    # Forward the setup to the sensor and button platforms
    for platform in ["sensor", "button"]:
        _logger.info(f"Forwarding setup to {platform} platform")
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    _logger.info(f"hass.data[DOMAIN] before async_setup_services: {hass.data[DOMAIN]}")

    # Setup the services
    _logger.info("Starting setup of services")
    await async_setup_services(hass)
    _logger.info("Finished setup of services")

    _logger.info(f"hass.data[DOMAIN] after setup of services: {hass.data[DOMAIN]}")  # New log

    async def reload_entry():
        _logger.info("Reloading entry")
        await hass.config_entries.async_reload(entry.entry_id)

    async_dispatcher_connect(hass, f"{DOMAIN}_reload_{entry.entry_id}", reload_entry)

    _logger.info("Finished setup of config entry")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _logger.info(f"Starting unload of config entry with ID: {entry.entry_id}")

    # Remove the sensor platform
    _logger.info("Removing sensor platform")
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Ensure hass.data[DOMAIN] is a dictionary before popping
    if isinstance(hass.data.get(DOMAIN, {}), dict):
        hass.data[DOMAIN].pop(entry.entry_id, None)

    _logger.info(f"hass.data[DOMAIN] after removing entry data: {hass.data[DOMAIN]}")
    _logger.info("Finished unload of config entry")
    return True