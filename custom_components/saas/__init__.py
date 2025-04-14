import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from .const import DOMAIN
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .services import async_setup_services  # Import the service setup function

try:
    import homeassistant
    import logging
    logging.getLogger(__name__).info("SAAS init loaded successfully")
except Exception as e:
    import traceback
    logging.getLogger(__name__).error(f"SAAS init failed: {e}\n{traceback.format_exc()}")
    raise




_logger = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the SAAS - Sleep As Android Status component."""
    _logger.info("Starting setup of the SAAS component")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a config entry."""
    _logger.info(f"Starting setup of config entry with ID: {entry.entry_id}")

    if "mqtt" not in hass.config.components:
        _logger.warning("MQTT not yet available. Retrying later...")
        raise ConfigEntryNotReady("MQTT integration is not ready")

    hass.data.setdefault(DOMAIN, {})

    if entry.entry_id not in hass.data[DOMAIN] and entry.data:
        hass.data[DOMAIN][entry.entry_id] = entry.data

    _logger.info(f"hass.data[DOMAIN] after adding entry data: {hass.data[DOMAIN]}")

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "button"])

    _logger.info(f"hass.data[DOMAIN] before async_setup_services: {hass.data[DOMAIN]}")

    _logger.info("Starting setup of services")
    await async_setup_services(hass)
    _logger.info("Finished setup of services")

    _logger.info(f"hass.data[DOMAIN] after setup of services: {hass.data[DOMAIN]}")

    async def reload_entry():
        _logger.info("Reloading entry")
        await hass.config_entries.async_reload(entry.entry_id)

    async_dispatcher_connect(hass, f"{DOMAIN}_reload_{entry.entry_id}", reload_entry)

    _logger.info("Finished setup of config entry")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _logger.info(f"Starting unload of config entry with ID: {entry.entry_id}")

    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    if isinstance(hass.data.get(DOMAIN, {}), dict):
        hass.data[DOMAIN].pop(entry.entry_id, None)

    _logger.info(f"hass.data[DOMAIN] after removing entry data: {hass.data[DOMAIN]}")
    _logger.info("Finished unload of config entry")
    return True
