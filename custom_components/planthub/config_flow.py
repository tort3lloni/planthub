"""Config Flow für PlantHub Integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DEFAULT_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class PlantHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PlantHub."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        super().__init__()
        self._config_data: Dict[str, Any] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("name", default=DEFAULT_NAME): str,
                        vol.Required("api_token"): str,
                        vol.Required("plant_id"): str,
                        vol.Optional("plant_name"): str,
                    }
                ),
                description_placeholders={
                    "name": DEFAULT_NAME,
                },
            )

        # Validiere den API-Token
        try:
            await self._validate_token(user_input["api_token"])
        except Exception as ex:
            _LOGGER.error("Token-Validierung fehlgeschlagen: %s", ex)
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("name", default=user_input["name"]): str,
                        vol.Required("api_token"): str,
                        vol.Required("plant_id", default=user_input["plant_id"]): str,
                        vol.Optional("plant_name", default=user_input.get("plant_name", "")): str,
                    }
                ),
                errors={"base": "invalid_token"},
                description_placeholders={
                    "name": user_input["name"],
                },
            )

        # Speichere die Konfigurationsdaten
        self._config_data = {
            "name": user_input["name"],
            "api_token": user_input["api_token"],
            "plant_id": user_input["plant_id"],
            "plant_name": user_input.get("plant_name", user_input["plant_id"]),
            "scan_interval": 300,  # Standard: 5 Minuten
        }
        
        # Konfiguration direkt abschließen
        return await self.async_step_final()

    async def async_step_final(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle final configuration step."""
        # Erstelle den Konfigurationseintrag
        title = f"{self._config_data['name']} - {self._config_data['plant_name']}"
        
        return self.async_create_entry(
            title=title,
            data=self._config_data,
        )

    async def _validate_token(self, token: str) -> None:
        """Validiere den API-Token."""
        # Hier könnte eine echte API-Validierung implementiert werden
        # Für jetzt prüfen wir nur, dass der Token nicht leer ist
        if not token or len(token.strip()) < 10:
            raise ValueError("Token zu kurz oder leer")

        _LOGGER.info("API-Token validiert")

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> PlantHubOptionsFlow:
        """Get the options flow for this handler."""
        return PlantHubOptionsFlow(config_entry)


class PlantHubOptionsFlow(config_entries.OptionsFlow):
    """Handle PlantHub options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {
                        vol.Optional(
                            "scan_interval",
                            default=self.config_entry.data.get("scan_interval", 300),
                        ): int,
                    }
                ),
            )

        # Aktualisiere die Konfiguration
        new_data = self.config_entry.data.copy()
        new_data["scan_interval"] = user_input["scan_interval"]
        
        self.hass.config_entries.async_update_entry(
            self.config_entry, data=new_data
        )
        
        return self.async_create_entry(title="", data={})
