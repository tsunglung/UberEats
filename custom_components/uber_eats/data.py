"""Common Uber Eats Data class used by both sensor and entity."""

import logging
from datetime import datetime
import json
from http import HTTPStatus
import requests
from aiohttp.hdrs import USER_AGENT

from .const import (
    ATTR_HTTPS_RESULT,
    BASE_URL,
    HA_USER_AGENT,
    REQUEST_TIMEOUT,
    UBER_EATS_ORDERS
)

_LOGGER = logging.getLogger(__name__)


class UberEatsData():
    """Class for handling the data retrieval."""

    def __init__(self, hass, account, cookie, localcode):
        """Initialize the data object."""
        self._hass = hass
        self._account = account
        self._cookie = cookie
        self._localcode = localcode
        self.orders = {}
        self.account = None
        self.expired = False
        self.ordered = False
        self.new_order = False
        self.uri = BASE_URL
        self.orders[account] = {}
        self._last_check = datetime.now()

    async def async_update_data(self):
        """Async wrapper for getting the update."""
        return await self._hass.async_add_executor_job(self._update_data)
 
    def get_uber_eats_data(self, site, data):
        """ return data """
        return self._update_data()

    def _parser_data(self, orders):
        """ parser data """
        data = orders['orders']

        return data

    def _update_data(self, **kwargs):
        """Get the latest data for Uber Eats from REST service."""
        headers = {
            USER_AGENT: HA_USER_AGENT,
            "content-type": "application/json",
            "cookie": f"sid={self._cookie}",
            "x-csrf-Token": "x"
        }
        payload = {
            "orderUdid": "null",
            "timezone": "Asis/Taipei"
        }
        params = {
           "localCode": self._localcode
        }
        force_update = False
        now = datetime.now()

        if (int(now.timestamp() - self._last_check.timestamp()) > 300):
            force_update = True
            self._last_check = now

        if not self.expired and (self.ordered or force_update):
            try:
                response = requests.post(
                    self.uri,
                    headers=headers,
                    data=json.dumps(payload),
                    params=params,
                    timeout=REQUEST_TIMEOUT)

            except requests.exceptions.RequestException:
                _LOGGER.error("Failed fetching data for %s", self._account)
                return

            if response.status_code == HTTPStatus.OK:
                self.orders[self._account][UBER_EATS_ORDERS] = self._parser_data(
                    response.json().get('data', {})
                )
                if len(self.orders[self._account]) >= 1:
                    self.orders[self._account][ATTR_HTTPS_RESULT] = HTTPStatus.OK
                else:
                    self.orders[self._account][ATTR_HTTPS_RESULT] = HTTPStatus.NOT_FOUND
                self.expired = False
                if len(self.orders[self._account][UBER_EATS_ORDERS]) >= 1:
                    self.new_order = True
                else:
                    self.new_order = False
                    self.ordered = False
                self.account = self._account
            elif response.status_code == HTTPStatus.NOT_FOUND:
                self.orders[self._account][ATTR_HTTPS_RESULT] = HTTPStatus.NOT_FOUND
                self.expired = True
            else:
                info = ""
                self.orders[self._account][ATTR_HTTPS_RESULT] = response.status_code
                if response.status_code == HTTPStatus.FORBIDDEN:
                    info = " Token or Cookie is expired"
                _LOGGER.error(
                    "Failed fetching data for %s (HTTP Status_code = %d).%s",
                    self._account,
                    response.status_code,
                    info
                )
                self.expired = True
        elif self.expired:
            self.orders[self._account][ATTR_HTTPS_RESULT] = 'sessions_expired'
            _LOGGER.warning(
                "Failed fetching data for %s (Sessions expired)",
                self._account,
            )

        return self
