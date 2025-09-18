"""DataUpdateCoordinator for RAPT."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RaptApiClient, RaptApiError
from .const import DOMAIN, UPDATE_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class RaptDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching RAPT data from the API."""

    def __init__(self, hass: HomeAssistant, api_client: RaptApiClient) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )
        self.api_client = api_client
        self._devices: list[dict[str, Any]] = []
        self._known_device_ids: set[str] = set()
        self._discovery_callbacks: list[callable] = []

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from RAPT API."""
        try:
            all_devices = await self.api_client.get_all_devices()
            controllers_data = all_devices["controllers"]
            hydrometers_data = all_devices["hydrometers"]
            fermentation_chambers_data = all_devices["fermentation_chambers"]
            brewzillas_data = all_devices["brewzillas"]
            
            self._track_known_devices(controllers_data, hydrometers_data, fermentation_chambers_data, brewzillas_data)
            self._devices = controllers_data + hydrometers_data + fermentation_chambers_data + brewzillas_data
            data = {
                "controllers": controllers_data,
                "hydrometers": hydrometers_data,
                "fermentation_chambers": fermentation_chambers_data,
                "brewzillas": brewzillas_data,
                "devices": self._devices,
                "last_updated": self.last_update_success,
            }
            
            _LOGGER.debug("Updated RAPT data: %s controllers, %s hydrometers, %s fermentation chambers, %s brewzillas", 
                         len(controllers_data), len(hydrometers_data), len(fermentation_chambers_data), len(brewzillas_data))
            
            return data
            
        except RaptApiError as err:
            raise UpdateFailed(f"Error communicating with RAPT API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    @property
    def devices(self) -> list[dict[str, Any]]:
        """Return the list of devices."""
        return self._devices

    def register_discovery_callback(self, callback: callable) -> None:
        """Register a callback for when new devices are discovered."""
        self._discovery_callbacks.append(callback)

    async def async_discover_devices(self) -> None:
        """Manually trigger device discovery."""
        try:
            all_devices = await self.api_client.get_all_devices()
            controllers_data = all_devices["controllers"]
            hydrometers_data = all_devices["hydrometers"]
            fermentation_chambers_data = all_devices["fermentation_chambers"]
            brewzillas_data = all_devices["brewzillas"]
            
            new_devices = []
            current_device_ids = set()
            
            for device in controllers_data + hydrometers_data + fermentation_chambers_data + brewzillas_data:
                device_id = device.get("id")
                if device_id:
                    current_device_ids.add(device_id)
                    if device_id not in self._known_device_ids:
                        new_devices.append(device)
                        self._known_device_ids.add(device_id)
            
            if new_devices:
                _LOGGER.info("Discovered %s new RAPT devices", len(new_devices))
                for callback in self._discovery_callbacks:
                    await callback(new_devices)
            else:
                _LOGGER.info("No new RAPT devices found")
            
            await self.async_request_refresh()
            
        except Exception as err:
            _LOGGER.error("Failed to discover devices: %s", err)

    def _track_known_devices(self, controllers: list[dict[str, Any]], hydrometers: list[dict[str, Any]], fermentation_chambers: list[dict[str, Any]], brewzillas: list[dict[str, Any]]) -> None:
        """Track known device IDs."""
        for device in controllers + hydrometers + fermentation_chambers + brewzillas:
            device_id = device.get("id")
            if device_id:
                self._known_device_ids.add(device_id)