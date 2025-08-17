"""Config Flow für PlantHub Integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_NAME, CONF_PLANT_ID, DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PlantHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow für PlantHub."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                        vol.Required(CONF_PLANT_ID): str,
                    }
                ),
            )

        await self.async_set_unique_id(user_input[CONF_PLANT_ID])
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data=user_input,
        )

    async def async_step_import(self, import_info: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_info)


class InvalidPlantId(HomeAssistantError):
    """Error to indicate we cannot connect."""
