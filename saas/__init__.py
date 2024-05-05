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
    hass.data[DOMAIN] = entry.data
    discovery.load_platform(hass, "sensor", DOMAIN, {}, entry.data)
    discovery.load_platform(hass, "binary_sensor", DOMAIN, {}, entry.data)
    return True