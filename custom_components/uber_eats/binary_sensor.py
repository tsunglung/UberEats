"""Upload Uber Eats New Order binary sensor instances."""
import logging

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import (
    CONF_ACCOUNT,
    DEFAULT_NAME,
    DOMAIN,
    UBER_EATS_DATA,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_devices):
    """Set up the binary sensors from a config entry."""

    if config.data.get(CONF_ACCOUNT, None):
        account = config.data[CONF_ACCOUNT]
    else:
        account = config.options[CONF_ACCOUNT]

    data = hass.data[DOMAIN][config.entry_id][UBER_EATS_DATA]
    device = UberEatsBinarySensor(hass, data, account)

    async_add_devices([device], update_before_add=True)

class UberEatsBinarySensor(BinarySensorEntity):
    """Represent a binary sensor."""

    def __init__(self, hass, data, account):
        """Set initializing values."""
        super().__init__()
        self._name = "{} {}".format(DEFAULT_NAME, account)
        self._attributes = {}
        self._state = False
        self._account = account
        self._data = data
        self._https_result = None
        self.hass = hass

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_new_order"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} New Order"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._data.new_order

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._account)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }
