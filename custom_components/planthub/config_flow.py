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
    CONF_TOKEN,
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
                    }
                ),
                description_placeholders={
                    "name": DEFAULT_NAME,
                },
            )

        # Prüfe, ob der Token in hass.data verfügbar ist
        if CONF_TOKEN not in self.hass.data.get(DOMAIN, {}):
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("name", default=user_input["name"]): str,
                    }
                ),
                errors={"base": "token_not_configured"},
                description_placeholders={
                    "name": user_input["name"],
                },
            )

        # Speichere die Konfigurationsdaten
        self._config_data = {
            "name": user_input["name"],
            "scan_interval": 300,  # Standard: 5 Minuten
        }
        
        # Gehe zum nächsten Schritt: Erste Pflanze hinzufügen
        return await self.async_step_add_first_plant()

    async def async_step_add_first_plant(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle adding the first plant step."""
        if user_input is None:
            return self.async_show_form(
                step_id="add_first_plant",
                data_schema=vol.Schema(
                    {
                        vol.Required("plant_id"): str,
                        vol.Optional("plant_name"): str,
                    }
                ),
                description_placeholders={
                    "name": self._config_data["name"],
                },
            )

        # Füge die erste Pflanze zur Konfiguration hinzu
        plant_config = {
            "plant_id": user_input["plant_id"],
            "name": user_input.get("plant_name", user_input["plant_id"]),
        }

        self._config_data["plants"] = [plant_config]
        
        # Konfiguration abschließen
        return await self.async_step_final()

    async def async_step_final(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle final configuration step."""
        # Erstelle den Konfigurationseintrag
        title = self._config_data["name"]
        
        return self.async_create_entry(
            title=title,
            data=self._config_data,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> PlantHubOptionsFlow:
        """Get the options flow for this handler."""
        return PlantHubOptionsFlow(config_entry)


class PlantHubOptionsFlow(config_entries.OptionsFlow):
    """Handle PlantHub options."""

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is None:
            # Zeige aktuelle Pflanzen an
            current_plants = self.config_entry.data.get("plants", [])
            plant_list = "\n".join([f"• {p['name']} ({p['plant_id']})" for p in current_plants])
            
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Optional("action", default="add"): vol.In({
                        "add": "Pflanze hinzufügen",
                        "remove": "Pflanze entfernen",
                        "settings": "Einstellungen ändern"
                    })
                }),
                description_placeholders={
                    "current_plants": plant_list or "Keine Pflanzen konfiguriert"
                }
            )

        if user_input["action"] == "add":
            return await self.async_step_add_plant()
        elif user_input["action"] == "remove":
            return await self.async_step_remove_plant()
        else:
            return await self.async_step_settings()

    async def async_step_add_plant(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle adding a new plant."""
        if user_input is None:
            return self.async_show_form(
                step_id="add_plant",
                data_schema=vol.Schema({
                    vol.Required("plant_id"): str,
                    vol.Optional("plant_name"): str,
                })
            )

        # Füge die neue Pflanze hinzu
        new_plant = {
            "plant_id": user_input["plant_id"],
            "name": user_input.get("plant_name", user_input["plant_id"]),
        }

        # Aktualisiere die Konfiguration
        new_data = self.config_entry.data.copy()
        if "plants" not in new_data:
            new_data["plants"] = []
        
        # Prüfe, ob die Pflanze bereits existiert
        existing_plant_ids = [p["plant_id"] for p in new_data["plants"]]
        if new_plant["plant_id"] in existing_plant_ids:
            return self.async_show_form(
                step_id="add_plant",
                data_schema=vol.Schema({
                    vol.Required("plant_id", default=user_input["plant_id"]): str,
                    vol.Optional("plant_name", default=user_input.get("plant_name", "")): str,
                }),
                errors={"base": "plant_id_exists"}
            )

        new_data["plants"].append(new_plant)
        
        # Aktualisiere den Konfigurationseintrag
        self.hass.config_entries.async_update_entry(
            self.config_entry, data=new_data
        )
        
        return self.async_create_entry(title="", data={})

    async def async_step_remove_plant(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle removing a plant."""
        current_plants = self.config_entry.data.get("plants", [])
        
        if not current_plants:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Optional("action", default="add"): vol.In({
                        "add": "Pflanze hinzufügen",
                        "remove": "Pflanze entfernen",
                        "settings": "Einstellungen ändern"
                    })
                }),
                errors={"base": "no_plants_to_remove"}
            )

        if user_input is None:
            # Erstelle Auswahl-Liste für Pflanzen
            plant_options = {p["plant_id"]: f"{p['name']} ({p['plant_id']})" for p in current_plants}
            
            return self.async_show_form(
                step_id="remove_plant",
                data_schema=vol.Schema({
                    vol.Required("plant_id_to_remove"): vol.In(plant_options)
                })
            )

        # Entferne die ausgewählte Pflanze
        plant_id_to_remove = user_input["plant_id_to_remove"]
        new_data = self.config_entry.data.copy()
        new_data["plants"] = [p for p in new_data["plants"] if p["plant_id"] != plant_id_to_remove]
        
        # Aktualisiere den Konfigurationseintrag
        self.hass.config_entries.async_update_entry(
            self.config_entry, data=new_data
        )
        
        return self.async_create_entry(title="", data={})

    async def async_step_settings(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle changing settings."""
        if user_input is None:
            return self.async_show_form(
                step_id="settings",
                data_schema=vol.Schema({
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.data.get("scan_interval", 300),
                    ): int,
                })
            )

        # Aktualisiere die Einstellungen
        new_data = self.config_entry.data.copy()
        new_data["scan_interval"] = user_input["scan_interval"]
        
        self.hass.config_entries.async_update_entry(
            self.config_entry, data=new_data
        )
        
        return self.async_create_entry(title="", data={})
