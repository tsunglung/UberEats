"""Support for the Uber Eats."""
import logging
from typing import Callable
from http import HTTPStatus

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION
)

from .const import (
    ATTRIBUTION,
    ATTR_ETA,
    ATTR_RESTAURANT_NAME,
    ATTR_COURIER_NAME,
    ATTR_COURIER_PHONE,
    ATTR_COURIER_DESCRIPTION,
    ATTR_TITLE_SUMMARY,
    ATTR_SUBTITLE_SUMMARY,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    ATTR_HTTPS_RESULT,
    ATTR_LIST,
    BASE_URL,
    CONF_ACCOUNT,
    DEFAULT_NAME,
    DOMAIN,
    UBER_EATS_DATA,
    UBER_EATS_COORDINATOR,
    UBER_EATS_ORDERS,
    MANUFACTURER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config: ConfigEntry, async_add_devices: Callable
) -> None:
    """Set up the Uber Eats Sensor from config."""

    if config.data.get(CONF_ACCOUNT, None):
        account = config.data[CONF_ACCOUNT]
    else:
        account = config.options[CONF_ACCOUNT]

    data = hass.data[DOMAIN][config.entry_id][UBER_EATS_DATA]
    data.expired = False
    data.ordered = False
    coordinator = hass.data[DOMAIN][config.entry_id][UBER_EATS_COORDINATOR]
    device = UberEatsSensor(account, data, coordinator)

    async_add_devices([device], update_before_add=True)


class UberEatsSensor(SensorEntity):
    """Implementation of a Uber Eats sensor."""

    def __init__(self, account, data, coordinator):
        """Initialize the sensor."""
        self._state = None
        self._data = data
        self._coordinator = coordinator
        self._attributes = {}
        self._attr_value = {}
        self._name = "{} {}".format(DEFAULT_NAME, account)
        self._account = account

        self.uri = BASE_URL

    @property
    def unique_id(self):
        """Return an unique ID."""
        uid = self._name.replace(" ", "_")
        return f"{uid}_orders"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Orders"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:food-variant"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return None

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        self._attributes = {}
        self._attributes[ATTR_ATTRIBUTION] = ATTRIBUTION
        for k, _ in self._attr_value.items():
            self._attributes[k] = self._attr_value[k]
        return self._attributes

    @property
    def device_info(self):
        return {
            'identifiers': {(DOMAIN, self._account)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }

    async def async_added_to_hass(self) -> None:
        """Set up a listener and load data."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self._update_callback)
        )
        self._update_callback()

    @callback
    def _update_callback(self) -> None:
        """Load data from integration."""
        self.async_write_ha_state()

    async def async_update(self):
        """Schedule a custom update via the common entity update service."""
        await self._coordinator.async_request_refresh()

        for i in ATTR_LIST:
            self._attr_value[i] = ''
        try:
            if self._account in self._data.orders:
                orders = self._data.orders[self._account].get(UBER_EATS_ORDERS, [])
                self._state = len(orders)
                index = 0
                if len(orders) >= 1:
                    for order in orders:
                        if index == 0:
                            for feed in order.get("feedCards", []):
                                if feed['type'] == 'status':
                                    self._attr_value[ATTR_ETA] = feed['status']['title']
                                    self._attr_value[ATTR_TITLE_SUMMARY] = feed['status']['titleSummary']['summary']['text']
                                    self._attr_value[ATTR_SUBTITLE_SUMMARY] = feed['status']['subtitleSummary']['summary']['text']
                                if feed['type'] == 'courier':
                                    self._attr_value[ATTR_COURIER_DESCRIPTION] = feed['courier'][0]['title']

                            self._attr_value[ATTR_RESTAURANT_NAME] = order['activeOrderOverview']['title']
                            for contact in order.get("contacts", []):
                                if contact['type'] == 'COURIER':
                                    self._attr_value[ATTR_COURIER_NAME] = contact['title']
                                    self._attr_value[ATTR_COURIER_PHONE] = contact['phoneNumber']
                            for bgfeedcard in order.get("backgroundFeedCards", []):
                                self._attr_value[ATTR_LATITUDE] = str(bgfeedcard['mapEntity'][0]['latitude'])
                                self._attr_value[ATTR_LONGITUDE] = str(bgfeedcard['mapEntity'][0]['longitude'])
                        if index >= 1:
                            for feed in order.get("feedCards", []):
                                if feed['type'] == 'status':
                                    self._attr_value[f"{ATTR_ETA}_{index + 1}"] = feed['status']['title']
                                    self._attr_value[f"{ATTR_TITLE_SUMMARY}_{index + 1}"] = feed['status']['titleSummary']['summary']['text']
                                    self._attr_value[f"{ATTR_SUBTITLE_SUMMARY}_{index + 1}"] = feed['status']['subtitleSummary']['summary']['text']
                                if feed['type'] == 'courier':
                                    self._attr_value[f"{ATTR_COURIER_DESCRIPTION}_{index + 1}"] = feed['courier'][0]['title']

                            self._attr_value[f"{ATTR_RESTAURANT_NAME}_{index + 1}"] = order['activeOrderOverview']['title']
                            for contact in order.get("contacts", []):
                                if contact['type'] == 'COURIER':
                                    self._attr_value[f"{ATTR_COURIER_NAME}_{index + 1}"] = contact['title']
                                    self._attr_value[f"{ATTR_COURIER_PHONE}_{index + 1}"] = contact['phoneNumber']
                            for bgfeedcard in order.get("backgroundFeedCards", []):
                                self._attr_value[f"{ATTR_LATITUDE}_{index + 1}"] = str(bgfeedcard['mapEntity'][0]['latitude'])
                                self._attr_value[f"{ATTR_LONGITUDE}_{index + 1}"] = str(bgfeedcard['mapEntity'][0]['longitude'])
                        index = index + 1


        except Exception as e:
            _LOGGER.error(f"paring orders occured exception {e}")
            self._state = 0

        self._attr_value[ATTR_HTTPS_RESULT] = self._data.orders[self._account].get(
            ATTR_HTTPS_RESULT, 'Unknown')
        if self._attr_value[ATTR_HTTPS_RESULT] == HTTPStatus.FORBIDDEN:
            self._state = None

        return