"""The RAPT integration."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import RaptDataUpdateCoordinator

if TYPE_CHECKING:
    from .api import RaptApiClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up RAPT from a config entry."""
    from .api import RaptApiClient

    api_client = RaptApiClient(
        username=entry.data["username"],
        api_secret=entry.data["api_secret"],
        session=async_get_clientsession(hass),
    )

    try:
        await api_client.authenticate()
    except Exception as err:
        _LOGGER.error("Failed to connect to RAPT API: %s", err)
        raise ConfigEntryNotReady from err

    coordinator = RaptDataUpdateCoordinator(hass, api_client)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_discover_devices(call):
        """Service to re-discover RAPT devices."""
        _LOGGER.info("Manual device discovery triggered")
        await coordinator.async_discover_devices()

    hass.services.async_register(
        DOMAIN,
        "discover_devices",
        async_discover_devices,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, "discover_devices")

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)