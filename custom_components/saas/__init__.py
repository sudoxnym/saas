import asyncio
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .services import async_setup_services  # Import the service setup function

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the SAAS - Sleep As Android Status component."""
    _LOGGER.info("Starting setup of the SAAS component")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    _LOGGER.info(f"Starting setup of config entry with ID: {entry.entry_id}")

    # ensure we have a dict for this integration
    hass.data.setdefault(DOMAIN, {})

    # merge original data + any saved options so runtime sees edits
    merged = {**entry.data, **entry.options}
    hass.data[DOMAIN][entry.entry_id] = merged
    _LOGGER.debug(
        "Merged entry.data and entry.options for %s: %s",
        entry.entry_id,
        hass.data[DOMAIN][entry.entry_id],
    )

    # forward setup to sensor and button platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "button"])

    # set up any custom services
    _LOGGER.info("Starting setup of services")
    await async_setup_services(hass)
    _LOGGER.info("Finished setup of services")

    _LOGGER.info("Finished setup of config entry")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info(f"Starting unload of config entry with ID: {entry.entry_id}")

    # unload sensor and button platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "button"])
    if not unload_ok:
        _LOGGER.error("Failed to unload platforms for saas")
        return False

    # clean up our stored data
    hass.data[DOMAIN].pop(entry.entry_id, None)

    _LOGGER.info(f"hass.data[{DOMAIN}] after unload: {hass.data.get(DOMAIN)}")
    _LOGGER.info("Finished unload of config entry")
    return True
