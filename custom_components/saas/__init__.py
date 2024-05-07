"""The SAAS - Sleep As Android Stats integration."""
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the SAAS - Sleep As Android Status component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up SAAS - Sleep As Android Status from a config entry."""
    # Store the configuration data for each entry separately, using the entry's unique ID as a key
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = entry.data

    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Remove the sensor platform
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # Remove the entry from the domain data
    hass.data[DOMAIN].pop(entry.entry_id)

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up SAAS - Sleep As Android Status from a config entry."""
    hass.data[DOMAIN] = entry.data
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True