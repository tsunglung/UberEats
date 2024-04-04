"""Support for the Uber Eats."""
import logging
from typing import Callable

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.device_tracker.const import SourceType
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.const import CONF_USERNAME

from .const import (
    CONF_ACCOUNT,
    DEFAULT_NAME,
    DOMAIN,
    UBER_EATS_DATA,
    UBER_EATS_ORDERS,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_devices: Callable
) -> None:
    """Set up the Uber Eats tracker from config."""

    if config.data.get(CONF_ACCOUNT, None):
        username = config.data[CONF_ACCOUNT]
    else:
        username = config.options[CONF_ACCOUNT]
    data = hass.data[DOMAIN][config.entry_id][UBER_EATS_DATA]
    device = UberEatsTrackerEntity(username, data)

    async_add_devices([device], update_before_add=True)


class UberEatsTrackerEntity(TrackerEntity):
    """Implementation of a Uber Eats tracker."""

    def __init__(self, username, data):
        """Initialize the tracker."""
        self._state = None
        self._data = data
        self._attributes = {}
        self._attr_value = {}
        self._name = "{} {}".format(DEFAULT_NAME, username)
        self._username = username
        self._attr_latitude = None
        self._attr_longitude = None

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_courier"

    @property
    def name(self):
        """Return the name of the tracker."""
        return f"{self._name} Courier"

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._username)},
            'manufacturer': MANUFACTURER,
            'name': self
            ._name
        }

    @property
    def should_poll(self) -> bool:
        """No polling for entities that have location pushed."""
        return True

    @property
    def source_type(self):
        """Return the source type, eg gps or router, of the device."""
        return SourceType.GPS

    @property
    def latitude(self):
        """Return latitude value of the device."""
        return self._attr_latitude

    @property
    def longitude(self):
        """Return longitude value of the device."""
        return self._attr_longitude

    async def async_update(self):
        """Schedule a custom update via the common entity update service."""
        try:
            if self._username in self._data.orders:
                orders = self._data.orders[self._username].get(UBER_EATS_ORDERS, [])
                self._state = len(orders)
                index = 0
                if len(orders) >= 1:
                    self._attr_latitude = orders[0]['backgroundFeedCards'][0]['mapEntity'][0]['latitude']
                    self._attr_longitude = orders[0]['backgroundFeedCards'][0]['mapEntity'][0]['longitude']

        except Exception as e:
            _LOGGER.error(f"paring orders occured exception {e}")