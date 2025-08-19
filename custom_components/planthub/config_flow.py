"""Config Flow für PlantHub Integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_API_TOKEN,
    CONF_NAME,
    CONF_PLANT_ID,
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
                        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                        vol.Required(CONF_API_TOKEN): str,
                    }
                ),
                description_placeholders={
                    "name": DEFAULT_NAME,
                },
            )

        # Validiere den API-Token
        try:
            await self._validate_token(user_input[CONF_API_TOKEN])
        except Exception as ex:
            _LOGGER.error("Token-Validierung fehlgeschlagen: %s", ex)
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                        vol.Required(CONF_API_TOKEN): str,
                    }
                ),
                errors={"base": "invalid_token"},
                description_placeholders={
                    "name": user_input[CONF_NAME],
                },
            )

        # Speichere die Konfigurationsdaten für den nächsten Schritt
        self._config_data = user_input.copy()
        
        # Gehe zum nächsten Schritt: Pflanzen hinzufügen
        return await self.async_step_add_plants()

    async def async_step_add_plants(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle adding plants step."""
        if user_input is None:
            return self.async_show_form(
                step_id="add_plants",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_PLANT_ID): str,
                        vol.Optional(CONF_NAME): str,
                    }
                ),
                description_placeholders={
                    "name": self._config_data[CONF_NAME],
                },
            )

        # Füge die Pflanze zur Konfiguration hinzu
        plant_config = {
            CONF_PLANT_ID: user_input[CONF_PLANT_ID],
            CONF_NAME: user_input.get(CONF_NAME, user_input[CONF_PLANT_ID]),
        }

        if "plants" not in self._config_data:
            self._config_data["plants"] = []
        
        self._config_data["plants"].append(plant_config)

        # Zeige Bestätigung und frage nach weiteren Pflanzen
        return self.async_show_form(
            step_id="confirm_plants",
            data_schema=vol.Schema(
                {
                    vol.Optional("add_another", default=False): bool,
                }
            ),
            description_placeholders={
                "plant_name": plant_config[CONF_NAME],
                "plant_id": plant_config[CONF_PLANT_ID],
                "total_plants": len(self._config_data["plants"]),
            },
        )

    async def async_step_confirm_plants(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle plant confirmation step."""
        if user_input is None:
            return self.async_show_form(
                step_id="confirm_plants",
                data_schema=vol.Schema(
                    {
                        vol.Optional("add_another", default=False): bool,
                    }
                ),
                description_placeholders={
                    "plant_name": self._config_data["plants"][-1][CONF_NAME],
                    "plant_id": self._config_data["plants"][-1][CONF_PLANT_ID],
                    "total_plants": len(self._config_data["plants"]),
                },
            )

        if user_input.get("add_another", False):
            # Weitere Pflanze hinzufügen
            return await self.async_step_add_plants()
        else:
            # Konfiguration abschließen
            return await self.async_step_final()

    async def async_step_final(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle final configuration step."""
        # Erstelle den Konfigurationseintrag
        title = self._config_data[CONF_NAME]
        
        # Füge scan_interval hinzu (Standard: 5 Minuten)
        self._config_data["scan_interval"] = 300
        
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
                        ): cv.positive_int,
                    }
                ),
            )

        # Aktualisiere die Konfiguration
        new_data = self.config_entry.data.copy()
        new_data["scan_interval"] = user_input["scan_interval"]

        # Aktualisiere den Konfigurationseintrag
        self.hass.config_entries.async_update_entry(
            self.config_entry, data=new_data
        )

        return self.async_create_entry(title="", data={})
