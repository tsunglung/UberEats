"""Config flow to configure Uber Eats component."""
import logging
from typing import Optional
import voluptuous as vol

from homeassistant import core, exceptions
from homeassistant.config_entries import (
    CONN_CLASS_CLOUD_POLL,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
    )
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.typing import ConfigType
from .const import (
    DOMAIN,
    CONF_ACCOUNT,
    CONF_COOKIE,
    CONF_LOCALCODE,
    DEFAULT_LOCALCODE,
    LOCALCODES
)
from .data import UberEatsData

_LOGGER = logging.getLogger(__name__)

async def validate_input(hass: core.HomeAssistant, data):
    """Validate that the user input allows us to connect to DataPoint.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    account = data[CONF_ACCOUNT]
    cookie = data[CONF_COOKIE]
    localcode = data[CONF_LOCALCODE]

    uber_eats_data = UberEatsData(hass, account, cookie, localcode)
    uber_eats_data.expired = False
    uber_eats_data.ordered = True
    await uber_eats_data.async_update_data()
    if uber_eats_data.account is None:
        raise CannotConnect()

    return {CONF_ACCOUNT: uber_eats_data.account}

class UberEatsFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Uber Eats config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._account: Optional[str] = None
        self._cookie: Optional[str] = None
        self._localcode: Optional[str] = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self,
        user_input: Optional[ConfigType] = None
    ):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_ACCOUNT]}"
            )
            self._abort_if_unique_id_configured()

            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_NAME] = info[CONF_ACCOUNT]
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ACCOUNT): str,
                vol.Required(CONF_COOKIE): str,
                vol.Required(CONF_LOCALCODE, default=DEFAULT_LOCALCODE): vol.In(
                    list(LOCALCODES.keys())
                ),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @property
    def _name(self):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        return self.context.get(CONF_NAME)

    @_name.setter
    def _name(self, value):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        self.context[CONF_NAME] = value
        self.context["title_placeholders"] = {"name": self._account}


class OptionsFlowHandler(OptionsFlow):
    # pylint: disable=too-few-public-methods
    """Handle options flow changes."""
    _account = None
    _cookie = None
    _localcode = None

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                user_input[CONF_NAME] = info[CONF_ACCOUNT]
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        self._account = self.config_entry.options.get(CONF_ACCOUNT, '')
        self._cookie = self.config_entry.options.get(CONF_COOKIE, '')
        self._localcode = self.config_entry.options.get(CONF_LOCALCODE, '')

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_COOKIE, default=self._cookie): str,
                    vol.Required(CONF_LOCALCODE, default=self._localcode): vol.In(
                        list(LOCALCODES.keys())
                    )
                }
            ),
            errors=errors
        )

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""