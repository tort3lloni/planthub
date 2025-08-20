"""Webhook-Funktionalität für PlantHub Integration."""
from __future__ import annotations

import aiohttp
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import (
    WEBHOOK_BASE_URL,
    WEBHOOK_ENDPOINT,
    WEBHOOK_TIMEOUT,
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    HTTP_FORBIDDEN,
    HTTP_NOT_FOUND,
    HTTP_TOO_MANY_REQUESTS,
    HTTP_INTERNAL_SERVER_ERROR,
    MIN_SOIL_MOISTURE,
    MAX_SOIL_MOISTURE,
    MIN_AIR_HUMIDITY,
    MAX_AIR_HUMIDITY,
    MIN_AIR_TEMPERATURE,
    MAX_AIR_TEMPERATURE,
    MIN_LIGHT,
)

_LOGGER = logging.getLogger(__name__)


class PlantHubWebhookError(HomeAssistantError):
    """Base exception for PlantHub webhook errors."""


class PlantHubAuthError(PlantHubWebhookError):
    """Authentication error (invalid token)."""


class PlantHubConnectionError(PlantHubWebhookError):
    """Connection error."""


class PlantHubRateLimitError(PlantHubWebhookError):
    """Rate limit exceeded."""


class PlantHubDataError(PlantHubWebhookError):
    """Data validation or processing error."""


class HttpClientProtocol(Protocol):
    """Protocol for HTTP client operations."""
    
    async def get(self, url: str) -> aiohttp.ClientResponse:
        """Make GET request."""
        ...
    
    async def post(self, url: str, json: Dict[str, Any]) -> aiohttp.ClientResponse:
        """Make POST request with JSON body."""
        ...


class PlantHubWebhook:
    """Webhook-Handler für PlantHub API."""

    def __init__(
        self, 
        hass: HomeAssistant, 
        api_token: str,
        http_client: Optional[HttpClientProtocol] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> None:
        """Initialize the webhook handler."""
        self.hass = hass
        self.api_token = api_token
        self._http_client = http_client
        self._base_url = base_url or WEBHOOK_BASE_URL
        self._timeout = timeout or WEBHOOK_TIMEOUT
        self.session: Optional[aiohttp.ClientSession] = None
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "User-Agent": "HomeAssistant/PlantHub/1.0.0",
        }

    async def __aenter__(self) -> PlantHubWebhook:
        """Async context manager entry."""
        if self._http_client is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self._timeout),
                headers=self._headers,
            )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def fetch_plant_data(self, plant_id: str) -> Dict[str, Any]:
        """Hole Daten für eine spezifische Pflanze."""
        if not self.session and self._http_client is None:
            raise PlantHubConnectionError("Webhook-Session nicht initialisiert")

        # URL ohne plant_id - plant_id wird im Body übertragen
        url = f"{self._base_url}{WEBHOOK_ENDPOINT}"
        
        # Request-Body mit plant_id
        request_body = {
            "plant_id": plant_id
        }
        
        # Detailliertes Logging vor dem Request
        _LOGGER.debug("=== PLANT HUB API REQUEST DEBUG ===")
        _LOGGER.debug("Plant ID: %s", plant_id)
        _LOGGER.debug("Base URL: %s", self._base_url)
        _LOGGER.debug("Webhook Endpoint: %s", WEBHOOK_ENDPOINT)
        _LOGGER.debug("Final URL: %s", url)
        _LOGGER.debug("Request Body: %s", request_body)
        _LOGGER.debug("API Token: %s...", self.api_token[:10] + "..." if len(self.api_token) > 10 else "***")
        _LOGGER.debug("Headers: %s", {k: v for k, v in self._headers.items() if k != "Authorization"})
        _LOGGER.debug("Authorization: Bearer %s...", self.api_token[:10] + "..." if len(self.api_token) > 10 else "***")
        _LOGGER.debug("Timeout: %d Sekunden", self._timeout)
        _LOGGER.debug("==================================")
        
        try:
            _LOGGER.debug("Rufe PlantHub API für Pflanze %s auf: %s mit Body: %s", plant_id, url, request_body)
            
            if self._http_client:
                # Für Mock-Tests - POST mit Body
                response = await self._http_client.post(url, json=request_body)
                # Mock-Response verarbeiten
                data = response.json() if hasattr(response, 'json') else response
                _LOGGER.debug("Mock-API-Antwort für Pflanze %s: %s", plant_id, data)
                
                # Extrahiere das erste Element aus der Liste, falls es eine Liste ist
                if isinstance(data, list) and len(data) > 0:
                    plant_data = data[0]
                    _LOGGER.debug("Extrahiertes Pflanzendaten aus Liste: %s", plant_data)
                elif isinstance(data, dict):
                    plant_data = data
                    _LOGGER.debug("Pflanzendaten als Dictionary: %s", plant_data)
                else:
                    _LOGGER.error("Unerwartetes Datenformat: %s (Typ: %s)", data, type(data))
                    raise PlantHubWebhookError(f"Unerwartetes Datenformat: {type(data)}")
                
                normalized_data = self._normalize_plant_data(plant_data, plant_id)
                return normalized_data
            else:
                # POST-Request mit plant_id im Body
                async with self.session.post(url, json=request_body) as response:
                    # Response-Logging
                    _LOGGER.debug("=== PLANT HUB API RESPONSE DEBUG ===")
                    _LOGGER.debug("Plant ID: %s", plant_id)
                    _LOGGER.debug("HTTP Status: %d", response.status)
                    _LOGGER.debug("Response Headers: %s", dict(response.headers))
                    _LOGGER.debug("=====================================")
                    
                    await self._handle_response_status(response, plant_id)
                    data = await response.json()
                    _LOGGER.debug("API-Antwort für Pflanze %s: %s", plant_id, data)
                    
                    # Extrahiere das erste Element aus der Liste, falls es eine Liste ist
                    if isinstance(data, list) and len(data) > 0:
                        plant_data = data[0]
                        _LOGGER.debug("Extrahiertes Pflanzendaten aus Liste: %s", plant_data)
                    elif isinstance(data, dict):
                        plant_data = data
                        _LOGGER.debug("Pflanzendaten als Dictionary: %s", plant_data)
                    else:
                        _LOGGER.error("Unerwartetes Datenformat: %s (Typ: %s)", data, type(data))
                        raise PlantHubWebhookError(f"Unerwartetes Datenformat: {type(data)}")
                    
                    normalized_data = self._normalize_plant_data(plant_data, plant_id)
                    return normalized_data
                
        except asyncio.TimeoutError:
            _LOGGER.error("=== PLANT HUB API TIMEOUT ERROR ===")
            _LOGGER.error("Plant ID: %s", plant_id)
            _LOGGER.error("URL: %s", url)
            _LOGGER.error("Timeout nach %d Sekunden", self._timeout)
            _LOGGER.error("=====================================")
            raise PlantHubConnectionError(f"Timeout für Pflanze {plant_id} nach {self._timeout} Sekunden")
            
        except aiohttp.ClientError as e:
            _LOGGER.error("=== PLANT HUB API CLIENT ERROR ===")
            _LOGGER.error("Plant ID: %s", plant_id)
            _LOGGER.error("URL: %s", url)
            _LOGGER.error("Client Error: %s", e)
            _LOGGER.error("===================================")
            raise PlantHubConnectionError(f"Verbindungsfehler für Pflanze {plant_id}: {e}")
            
        except Exception as e:
            _LOGGER.error("=== PLANT HUB API UNEXPECTED ERROR ===")
            _LOGGER.error("Plant ID: %s", plant_id)
            _LOGGER.error("URL: %s", url)
            _LOGGER.error("Unexpected Error: %s", e)
            _LOGGER.error("======================================")
            raise PlantHubWebhookError(f"Unerwarteter Fehler für Pflanze {plant_id}: {e}")

    async def _handle_response_status(self, response: aiohttp.ClientResponse, context: str) -> None:
        """Behandle HTTP-Status-Codes und werfe entsprechende Exceptions."""
        if response.status == HTTP_OK:
            return
            
        elif response.status == HTTP_UNAUTHORIZED:
            _LOGGER.error("API-Token ungültig für %s (Status: %d)", context, response.status)
            raise PlantHubAuthError("API-Token ist ungültig oder abgelaufen")
            
        elif response.status == HTTP_FORBIDDEN:
            _LOGGER.error("Zugriff verweigert für %s (Status: %d)", context, response.status)
            raise PlantHubAuthError("Zugriff verweigert - Token hat keine ausreichenden Berechtigungen")
            
        elif response.status == HTTP_NOT_FOUND:
            _LOGGER.error("Pflanze nicht gefunden: %s (Status: %d)", context, response.status)
            raise PlantHubWebhookError(f"Pflanze {context} nicht gefunden")
            
        elif response.status == HTTP_TOO_MANY_REQUESTS:
            _LOGGER.warning("Rate Limit überschritten für %s (Status: %d)", context, response.status)
            raise PlantHubRateLimitError("API-Rate Limit überschritten")
            
        elif response.status >= HTTP_INTERNAL_SERVER_ERROR:
            _LOGGER.error("Server-Fehler für %s (Status: %d)", context, response.status)
            raise PlantHubConnectionError(f"Server-Fehler: {response.status}")
            
        else:
            _LOGGER.error("Unerwarteter HTTP-Status für %s: %d", context, response.status)
            raise PlantHubWebhookError(f"Unerwarteter HTTP-Status: {response.status}")

    def _normalize_plant_data(self, raw_data: Dict[str, Any], plant_id: str) -> Dict[str, Any]:
        """Normalisiere die rohen API-Daten in das erwartete Format."""
        try:
            # Extrahiere und normalisiere die Daten
            normalized_data = {
                "plant_id": plant_id,
                "plant_name": raw_data.get("name", plant_id),
                "soil_moisture": self._extract_numeric_value(raw_data, "soil_moisture", "moisture"),
                "air_temperature": self._extract_numeric_value(raw_data, "air_temperature", "temperature"),
                "air_humidity": self._extract_numeric_value(raw_data, "air_humidity", "humidity"),
                "light": self._extract_numeric_value(raw_data, "light", "illuminance"),
                "last_update": raw_data.get("last_updated", datetime.now().isoformat()),
            }
            
            # Validiere die Daten
            self._validate_plant_data(normalized_data)
            
            return normalized_data
            
        except Exception as e:
            _LOGGER.error("Fehler beim Normalisieren der Daten für Pflanze %s: %s", plant_id, e)
            # Fallback-Daten zurückgeben
            return self._get_fallback_data(plant_id)

    def _extract_numeric_value(self, data: Dict[str, Any], *keys: str) -> Optional[float]:
        """Extrahiere einen numerischen Wert aus verschiedenen möglichen Schlüsseln."""
        for key in keys:
            value = data.get(key)
            if value is not None:
                try:
                    return float(value)
                except (ValueError, TypeError):
                    continue
        return None

    def _validate_plant_data(self, data: Dict[str, Any]) -> None:
        """Validiere die normalisierten Pflanzendaten."""
        # Überprüfe ob alle erforderlichen Felder vorhanden sind
        required_fields = ["plant_id", "plant_name"]
        for field in required_fields:
            if not data.get(field):
                _LOGGER.warning("Erforderliches Feld fehlt: %s", field)
        
        # Überprüfe numerische Werte auf Plausibilität
        self._validate_numeric_range(
            data.get("soil_moisture"), 
            "Bodenfeuchtigkeit", 
            MIN_SOIL_MOISTURE, 
            MAX_SOIL_MOISTURE
        )
        
        self._validate_numeric_range(
            data.get("air_humidity"), 
            "Luftfeuchtigkeit", 
            MIN_AIR_HUMIDITY, 
            MAX_AIR_HUMIDITY
        )
        
        self._validate_numeric_range(
            data.get("air_temperature"), 
            "Lufttemperatur", 
            MIN_AIR_TEMPERATURE, 
            MAX_AIR_TEMPERATURE
        )
        
        if data.get("light") is not None and data["light"] < MIN_LIGHT:
            _LOGGER.warning("Helligkeit negativ: %s", data["light"])

    def _validate_numeric_range(
        self, 
        value: Optional[float], 
        field_name: str, 
        min_val: float, 
        max_val: float
    ) -> None:
        """Validiere einen numerischen Wert auf einen Bereich."""
        if value is not None and not min_val <= value <= max_val:
            _LOGGER.warning(
                "%s außerhalb des gültigen Bereichs [%s, %s]: %s", 
                field_name, min_val, max_val, value
            )

    def _get_fallback_data(self, plant_id: str) -> Dict[str, Any]:
        """Fallback-Daten bei Fehlern."""
        return {
            "plant_id": plant_id,
            "plant_name": plant_id,
            "soil_moisture": None,
            "air_temperature": None,
            "air_humidity": None,
            "light": None,
            "last_update": datetime.now().isoformat(),
        }
