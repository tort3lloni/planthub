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

        url = f"{self._base_url}{WEBHOOK_ENDPOINT}/{plant_id}"
        
        try:
            _LOGGER.debug("Rufe PlantHub API auf: %s", url)
            
            if self._http_client:
                response = await self._http_client.get(url)
            else:
                async with self.session.get(url) as response:
                    await self._handle_response_status(response, plant_id)
                    data = await response.json()
                    _LOGGER.debug("API-Antwort für Pflanze %s: %s", plant_id, data)
                    return self._normalize_plant_data(data, plant_id)
                
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout beim API-Aufruf für Pflanze %s", plant_id)
            raise PlantHubConnectionError(f"Timeout für Pflanze {plant_id}")
            
        except aiohttp.ClientError as e:
            _LOGGER.error("Client-Fehler beim API-Aufruf für Pflanze %s: %s", plant_id, e)
            raise PlantHubConnectionError(f"Verbindungsfehler für Pflanze {plant_id}: {e}")
            
        except Exception as e:
            _LOGGER.error("Unerwarteter Fehler beim API-Aufruf für Pflanze %s: %s", plant_id, e)
            raise PlantHubWebhookError(f"Unerwarteter Fehler für Pflanze {plant_id}: {e}")

    async def fetch_all_plants_data(self) -> List[Dict[str, Any]]:
        """Hole Daten für alle Pflanzen."""
        if not self.session and self._http_client is None:
            raise PlantHubConnectionError("Webhook-Session nicht initialisiert")

        url = f"{self._base_url}{WEBHOOK_ENDPOINT}"
        
        try:
            _LOGGER.debug("Rufe PlantHub API für alle Pflanzen auf: %s", url)
            
            if self._http_client:
                response = await self._http_client.get(url)
            else:
                async with self.session.get(url) as response:
                    await self._handle_response_status(response, "all_plants")
                    data = await response.json()
                    _LOGGER.debug("API-Antwort für alle Pflanzen: %s", data)
                    
                    plants_data = []
                    for plant in data.get("plants", []):
                        normalized_data = self._normalize_plant_data(plant, plant.get("id", "unknown"))
                        plants_data.append(normalized_data)
                    
                    return plants_data
                
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout beim API-Aufruf für alle Pflanzen")
            raise PlantHubConnectionError("Timeout für alle Pflanzen")
            
        except aiohttp.ClientError as e:
            _LOGGER.error("Client-Fehler beim API-Aufruf für alle Pflanzen: %s", e)
            raise PlantHubConnectionError(f"Verbindungsfehler für alle Pflanzen: {e}")
            
        except Exception as e:
            _LOGGER.error("Unerwarteter Fehler beim API-Aufruf für alle Pflanzen: %s", e)
            raise PlantHubWebhookError(f"Unerwarteter Fehler für alle Pflanzen: {e}")

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
