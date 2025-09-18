"""API client for RAPT."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp

from .const import (
    API_AUTH_URL,
    API_BASE_URL,
    API_CONTROLLERS_ENDPOINT,
    API_HYDROMETERS_ENDPOINT,
    API_FERMENTATION_CHAMBERS_ENDPOINT,
    API_BREWZILLAS_ENDPOINT,
)

_LOGGER = logging.getLogger(__name__)


class RaptApiClient:
    """RAPT API client."""

    def __init__(self, username: str, api_secret: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._username = username
        self._api_secret = api_secret
        self._session = session
        self._bearer_token: str | None = None
        self._token_expires_at: datetime | None = None
        self._rate_limit_lock = asyncio.Lock()
        self._last_request_time: datetime | None = None

    async def authenticate(self) -> None:
        """Authenticate with the RAPT API using OAuth2 password flow."""
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'client_id': 'rapt-user',
            'grant_type': 'password',
            'username': self._username,
            'password': self._api_secret
        }
        
        try:
            async with self._session.post(
                API_AUTH_URL, 
                headers=headers, 
                data=data, 
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 400:
                    error_text = await response.text()
                    _LOGGER.error("Bad request - Invalid credentials or parameters: %s", error_text)
                    raise RaptApiError("Authentication failed: Invalid username or API key")
                elif response.status == 401:
                    error_text = await response.text()
                    _LOGGER.error("Unauthorized - Invalid username or API key: %s", error_text)
                    raise RaptApiError("Authentication failed: Invalid username or API key")
                elif response.status != 200:
                    error_text = await response.text()
                    _LOGGER.error("Authentication failed with status %s: %s", response.status, error_text)
                    raise RaptApiError(f"Authentication failed: HTTP {response.status}")
                
                try:
                    token_data = await response.json()
                except aiohttp.ContentTypeError as err:
                    _LOGGER.error("Invalid JSON response from authentication endpoint: %s", err)
                    raise RaptApiError("Authentication failed: Invalid response format")
                
                if "access_token" not in token_data:
                    _LOGGER.error("No access_token in authentication response: %s", token_data)
                    raise RaptApiError("No access token received from API")
                
                self._bearer_token = token_data["access_token"]
                
                # Use expires_in if provided, otherwise default to 45 minutes
                expires_in_seconds = token_data.get("expires_in", 2700)  # 45 minutes default
                self._token_expires_at = datetime.now() + timedelta(seconds=expires_in_seconds)
                
                _LOGGER.info("Successfully authenticated with RAPT API (expires in %s seconds)", expires_in_seconds)
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error during authentication: %s", err)
            raise RaptApiError(f"Network error: {err}") from err

    async def _ensure_authenticated(self) -> None:
        """Ensure we have a valid authentication token."""
        if (
            self._bearer_token is None
            or self._token_expires_at is None
            or datetime.now() >= self._token_expires_at
        ):
            _LOGGER.info("Token expired or missing, re-authenticating")
            await self.authenticate()

    async def _rate_limited_request(self, method: str, url: str, **kwargs) -> Any:
        """Make a rate-limited request to the API."""
        async with self._rate_limit_lock:
            if self._last_request_time is not None:
                time_since_last = datetime.now() - self._last_request_time
                if time_since_last < timedelta(seconds=15):
                    sleep_time = 15 - time_since_last.total_seconds()
                    _LOGGER.debug("Rate limiting: sleeping for %s seconds", sleep_time)
                    await asyncio.sleep(sleep_time)
            
            self._last_request_time = datetime.now()
            
            await self._ensure_authenticated()
            
            headers = kwargs.get("headers", {})
            headers["Authorization"] = f"Bearer {self._bearer_token}"
            kwargs["headers"] = headers
            
            try:
                # Add timeout to prevent hanging requests
                if "timeout" not in kwargs:
                    kwargs["timeout"] = aiohttp.ClientTimeout(total=30)
                
                async with self._session.request(method, url, **kwargs) as response:
                    if response.status == 401:
                        # Token might be expired, try re-authenticating once
                        _LOGGER.warning("Received 401, attempting re-authentication")
                        await self.authenticate()
                        headers["Authorization"] = f"Bearer {self._bearer_token}"
                        
                        async with self._session.request(method, url, **kwargs) as retry_response:
                            if retry_response.status != 200:
                                error_text = await retry_response.text()
                                raise RaptApiError(f"Request failed after re-auth: {retry_response.status} - {error_text}")
                            
                            try:
                                return await retry_response.json()
                            except aiohttp.ContentTypeError as err:
                                _LOGGER.error("Invalid JSON response after retry: %s", err)
                                raise RaptApiError("Invalid JSON response from API")
                    
                    elif response.status != 200:
                        error_text = await response.text()
                        if response.status == 403:
                            raise RaptApiError(f"Access forbidden: {error_text}")
                        elif response.status == 404:
                            raise RaptApiError(f"API endpoint not found: {error_text}")
                        elif response.status >= 500:
                            raise RaptApiError(f"Server error: {response.status} - {error_text}")
                        else:
                            raise RaptApiError(f"Request failed: {response.status} - {error_text}")
                    
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError as err:
                        _LOGGER.error("Invalid JSON response: %s", err)
                        raise RaptApiError("Invalid JSON response from API")
            
            except aiohttp.ClientError as err:
                _LOGGER.error("Network error during API request: %s", err)
                raise RaptApiError(f"Network error: {err}") from err

    async def get_temperature_controllers(self) -> list[dict[str, Any]]:
        """Get temperature controllers from RAPT API."""
        url = f"{API_BASE_URL}{API_CONTROLLERS_ENDPOINT}"
            
        try:
            data = await self._rate_limited_request("GET", url)
            _LOGGER.debug("Retrieved temperature controllers: %s devices", len(data) if isinstance(data, list) else "unknown")
            
            if isinstance(data, list):
                return data
            else:
                _LOGGER.warning("Unexpected response format: %s", type(data))
                return []
                
        except Exception as err:
            _LOGGER.error("Failed to get temperature controllers: %s", err)
            raise



    async def get_all_controller_data(self) -> list[dict[str, Any]]:
        """Get all temperature controllers data."""
        return await self.get_temperature_controllers()

    async def get_hydrometers(self) -> list[dict[str, Any]]:
        """Get hydrometers from RAPT API."""
        url = f"{API_BASE_URL}{API_HYDROMETERS_ENDPOINT}"
        
        try:
            data = await self._rate_limited_request("GET", url)
            _LOGGER.debug("Retrieved hydrometers: %s devices", len(data) if isinstance(data, list) else "unknown")
            
            if isinstance(data, list):
                return data
            else:
                _LOGGER.warning("Unexpected response format: %s", type(data))
                return []
                
        except Exception as err:
            _LOGGER.error("Failed to get hydrometers: %s", err)
            raise



    async def get_all_hydrometer_data(self) -> list[dict[str, Any]]:
        """Get all hydrometers data."""
        return await self.get_hydrometers()

    async def get_fermentation_chambers(self) -> list[dict[str, Any]]:
        """Get fermentation chambers from RAPT API."""
        url = f"{API_BASE_URL}{API_FERMENTATION_CHAMBERS_ENDPOINT}"
        
        try:
            data = await self._rate_limited_request("GET", url)
            _LOGGER.debug("Retrieved fermentation chambers: %s devices", len(data) if isinstance(data, list) else "unknown")
            
            if isinstance(data, list):
                return data
            else:
                _LOGGER.warning("Unexpected response format: %s", type(data))
                return []
                
        except Exception as err:
            _LOGGER.error("Failed to get fermentation chambers: %s", err)
            raise

    async def get_all_fermentation_chamber_data(self) -> list[dict[str, Any]]:
        """Get all fermentation chambers data."""
        return await self.get_fermentation_chambers()

    async def get_brewzillas(self) -> list[dict[str, Any]]:
        """Get BrewZillas from RAPT API."""
        url = f"{API_BASE_URL}{API_BREWZILLAS_ENDPOINT}"
        
        try:
            data = await self._rate_limited_request("GET", url)
            _LOGGER.debug("Retrieved BrewZillas: %s devices", len(data) if isinstance(data, list) else "unknown")
            
            if isinstance(data, list):
                return data
            else:
                _LOGGER.warning("Unexpected response format: %s", type(data))
                return []
                
        except Exception as err:
            _LOGGER.error("Failed to get BrewZillas: %s", err)
            raise

    async def get_all_brewzilla_data(self) -> list[dict[str, Any]]:
        """Get all BrewZillas data."""
        return await self.get_brewzillas()

    async def get_all_devices(self) -> dict[str, list[dict[str, Any]]]:
        """Get all devices (controllers, hydrometers, fermentation chambers, and BrewZillas)."""
        controllers = await self.get_all_controller_data()
        hydrometers = await self.get_all_hydrometer_data()
        fermentation_chambers = await self.get_all_fermentation_chamber_data()
        brewzillas = await self.get_all_brewzilla_data()
        
        return {
            "controllers": controllers,
            "hydrometers": hydrometers,
            "fermentation_chambers": fermentation_chambers,
            "brewzillas": brewzillas,
        }

    async def get_devices(self) -> list[dict[str, Any]]:
        """Get list of available temperature controller devices."""
        return await self.get_all_controller_data()

    async def validate_connection(self) -> bool:
        """Validate the API connection by attempting to authenticate and fetch data."""
        try:
            await self.authenticate()
            # Try to fetch temperature controllers to verify the connection works
            await self.get_temperature_controllers()
            return True
        except Exception as err:
            _LOGGER.error("Connection validation failed: %s", err)
            return False


class RaptApiError(Exception):
    """Exception raised for RAPT API errors."""