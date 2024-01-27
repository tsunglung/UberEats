"""Upload Uber Eats Button instances."""
import logging

from homeassistant.components.button import ButtonEntity

from .const import (
    BASE_URL,
    CONF_ACCOUNT,
    DEFAULT_NAME,
    DOMAIN,
    UBER_EATS_DATA,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_devices):
    """Set up the binary sensors from a config entry."""

    cookie = None
    if config.data.get(CONF_ACCOUNT, None):
        account = config.data[CONF_ACCOUNT]
    else:
        account = config.options[CONF_ACCOUNT]

    data = hass.data[DOMAIN][config.entry_id][UBER_EATS_DATA]
    device = UberEatsButton(hass, data, account)

    async_add_devices([device], update_before_add=True)

class UberEatsButton(ButtonEntity):
    """Represent a binary sensor."""

    def __init__(self, hass, data, account):
        """Set initializing values."""
        super().__init__()
        self._name = "{} {}".format(DEFAULT_NAME, account)
        self._attributes = {}
        self._account = account
        self._data = data
        self.hass = hass
        self.uri = BASE_URL

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_order"

    @property
    def name(self):
        """Return the name of the button."""
        return f"{self._name} Order"

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._account)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }

    async def async_press(self) -> None:
        """Press the button."""
        self._data.ordered = True