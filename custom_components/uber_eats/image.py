"""This component provides basic support for Uber Eats Courier Image."""

import logging
from datetime import datetime

from homeassistant.components.image import ImageEntity
from homeassistant.helpers.typing import UndefinedType

from .const import (
    ATTR_COURIER_NAME,
    CONF_ACCOUNT,
    DEFAULT_NAME,
    DOMAIN,
    UBER_EATS_DATA,
    UBER_EATS_ORDERS,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config, async_add_devices):
    """Add a Image from a config entry."""

    if config.data.get(CONF_ACCOUNT, None):
        account = config.data[CONF_ACCOUNT]
    else:
        account = config.options[CONF_ACCOUNT]

    data = hass.data[DOMAIN][config.entry_id][UBER_EATS_DATA]
    device = UberEatsImage(hass, data, account)

    async_add_devices([device], update_before_add=True)

class UberEatsImage(ImageEntity):
    """An implementation of a Uber Eats Courier Image."""

    def __init__(self, hass, data, account):
        """Set initializing values."""
        super().__init__(hass)
        self._name = "{} {}".format(DEFAULT_NAME, account)
        self._attributes = {}
        self._account = account
        self._data = data
        self._attr_should_poll = True
        self.hass = hass

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_courier_image"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Courier"

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._account)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }

    @property
    def state(self) -> str | None:
        """Return the state."""
        try:
            if self._account in self._data.orders:
                orders = self._data.orders[self._account].get(UBER_EATS_ORDERS, [])
                if len(orders) >= 1:
                    for order in orders:
                        for contact in order.get("contacts", []):
                            if contact['type'] == 'COURIER':
                                return contact['title']
        except:
            return None

    @property
    def image_url(self) -> str | None | UndefinedType:
        """Return URL of image."""
        try:
            if self._account in self._data.orders:
                orders = self._data.orders[self._account].get(UBER_EATS_ORDERS, [])
                for order in orders:
                    for feed in order.get("feedCards", []):
                        if feed['type'] == 'courier':
                            self._attr_image_last_updated = datetime.now()
                            return feed['courier'][0]['iconUrl']
        except:
            pass
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Unknown_person.jpg/217px-Unknown_person.jpg"

