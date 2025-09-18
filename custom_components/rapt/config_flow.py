"""Config flow for RAPT integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RaptApiClient, RaptApiError
from .const import CONF_API_SECRET, CONF_USERNAME, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_API_SECRET): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    api_client = RaptApiClient(
        username=data[CONF_USERNAME],
        api_secret=data[CONF_API_SECRET],
        session=session,
    )

    try:
        await api_client.authenticate()
        # Try to fetch some data to verify the connection works
        await api_client.get_temperature_controllers()
    except aiohttp.ClientError as err:
        _LOGGER.error("Network error connecting to RAPT API: %s", err)
        raise CannotConnect from err
    except RaptApiError as err:
        _LOGGER.error("RAPT API error: %s", err)
        if "Authentication failed" in str(err):
            raise InvalidAuth from err
        else:
            raise CannotConnect from err
    except Exception as err:
        _LOGGER.error("Unexpected error connecting to RAPT API: %s", err)
        raise CannotConnect from err

    return {"title": "RAPT Devices"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for RAPT."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception during setup: %s", err)
                errors["base"] = "unknown"
            else:
                # Check if already configured by trying to find existing entries with same username
                existing_entry = None
                for entry in self._async_current_entries():
                    if entry.data.get(CONF_USERNAME) == user_input[CONF_USERNAME]:
                        existing_entry = entry
                        break
                
                if existing_entry:
                    return self.async_abort(reason="already_configured")
                
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""