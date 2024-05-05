from homeassistant.helpers.entity import Entity
from homeassistant.components.mqtt import async_subscribe
from .const import DOMAIN, CONF_NAME, INTEGRATION_NAME, MODEL

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the SAAS binary sensor platform."""
    name = hass.data[DOMAIN].get(CONF_NAME, "Default Name")
    add_entities([SAASBinarySensor(hass, name)])

class SAASBinarySensor(Entity):
    """Representation of a SAAS - Sleep As Android Stats binary sensor."""
    def __init__(self, hass, name):
        """Initialize the binary sensor."""
        self._state = None
        self._name = name
        self._hass = hass

    @property
    def name(self):
        """Return the name of the binary sensor."""
        return f"SAAS {self._name} Awake"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._state in self._hass.data[DOMAIN]["awake_states"]
    
    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self._name)},
            "name": self._name,
            "manufacturer": INTEGRATION_NAME,
            "model": MODEL,
        }
    
    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        async def message_received(msg):
            """Handle new MQTT messages."""
            self._state = msg.payload
            self.async_schedule_update_ha_state()

        await async_subscribe(self._hass, self._hass.data[DOMAIN]["topic_template"], message_received)