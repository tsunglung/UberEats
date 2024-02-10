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

    def __init__(self, hass, session, account, cookies, localcode):
        """Initialize the data object."""
        self._hass = hass
        self._session = session
        self._account = account
        self._cookie = None
        self._cookie1 = cookies[0]
        self._cookie2 = cookies[1]
        self._localcode = localcode
        self.orders = {}
        self.account = None
        self.expired = False
        self.ordered = False
        self.new_order = False
        self.uri = BASE_URL
        self.orders[account] = {}
        self._last_check = datetime.now()

    def _parser_data(self, orders):
        """ parser data """
        data = []
        if isinstance(orders, dict):
            data = orders.get('orders', [])

        return data

    async def async_update_data(self):
        """Get the latest data for Uber Eats from REST service."""
        if self._cookie is None:
            self._cookie = self._cookie1

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
                response = await self._session.request(
                    "POST",
                    url=self.uri,
                    data=json.dumps(payload),
                    params=params,
                    headers=headers,
                    timeout=REQUEST_TIMEOUT
                )

            except requests.exceptions.RequestException:
                _LOGGER.error("Failed fetching data for %s", self._account)
                return

            if response.status == HTTPStatus.OK:
                try:
                    res = await response.json()
                except:
                    res = {"data": response.text}
                self.orders[self._account][UBER_EATS_ORDERS] = self._parser_data(
                    res.get('data', {})
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
            elif response.status == HTTPStatus.NOT_FOUND:
                self.orders[self._account][ATTR_HTTPS_RESULT] = HTTPStatus.NOT_FOUND
                self.expired = True
            else:
                info = ""
                self.orders[self._account][ATTR_HTTPS_RESULT] = response.status
                if response.status == HTTPStatus.FORBIDDEN:
                    info = " Token or Cookie is expired"
                _LOGGER.error(
                    "Failed fetching data for %s (HTTP Status Code = %d).%s",
                    self._account,
                    response.status,
                    info
                )
                self.expired = True
        elif self.expired:
            self.orders[self._account][ATTR_HTTPS_RESULT] = 'sessions_expired'
            _LOGGER.warning(
                "Failed fetching data for %s (Sessions expired)",
                self._account,
            )
            if self._cookie == self._cookie1:
                self._cookie = self._cookie2 if len(self._cookie2) >= 1 else self._cookie1
            else:
                self._cookie = self._cookie1
            self.expired = False

        return self
