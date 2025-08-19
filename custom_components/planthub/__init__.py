"""PlantHub Integration für Home Assistant."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_API_TOKEN,
    CONF_PLANT_ID,
    DEFAULT_NAME,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    DEVICE_SW_VERSION,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the PlantHub component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PlantHub from a config entry."""
    _LOGGER.info("Initialisiere PlantHub Integration: %s", entry.data.get("name", DEFAULT_NAME))

    # Erstelle den Data Update Coordinator
    from .sensor import PlantHubDataUpdateCoordinator
    
    coordinator = PlantHubDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Speichere den Coordinator
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }

    # Erstelle Device Registry Einträge für alle Pflanzen
    await _create_device_registry_entries(hass, entry, coordinator)

    # Setze die Plattformen auf
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Listener für das Entfernen der Integration
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    _LOGGER.info("PlantHub Integration erfolgreich initialisiert")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Entlade PlantHub Integration: %s", entry.data.get("name", DEFAULT_NAME))

    # Entferne alle Plattformen
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Entferne Device Registry Einträge
        await _remove_device_registry_entries(hass, entry)
        
        # Entferne den Coordinator
        hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.info("PlantHub Integration erfolgreich entladen")
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    _LOGGER.info("Lade PlantHub Integration neu: %s", entry.data.get("name", DEFAULT_NAME))
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def _create_device_registry_entries(
    hass: HomeAssistant, entry: ConfigEntry, coordinator: Any
) -> None:
    """Erstelle Device Registry Einträge für alle Pflanzen."""
    try:
        device_registry = dr.async_get(hass)
        
        for plant_id in coordinator.plant_ids:
            plant_name = coordinator.get_plant_name(plant_id)
            
            # Erstelle oder aktualisiere den Device Registry Eintrag
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, plant_id)},
                name=plant_name,
                manufacturer=DEVICE_MANUFACTURER,
                model=DEVICE_MODEL,
                sw_version=DEVICE_SW_VERSION,
                via_device=(DOMAIN, entry.entry_id),
            )
            
            _LOGGER.debug("Device Registry Eintrag erstellt/aktualisiert für Pflanze: %s", plant_id)
            
    except Exception as e:
        _LOGGER.error("Fehler beim Erstellen der Device Registry Einträge: %s", e)


async def _remove_device_registry_entries(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Entferne Device Registry Einträge für alle Pflanzen."""
    try:
        device_registry = dr.async_get(hass)
        
        # Finde alle Geräte, die zu dieser Integration gehören
        devices = dr.async_entries_for_config_entry(device_registry, entry.entry_id)
        
        for device in devices:
            # Entferne das Gerät
            device_registry.async_remove_device(device.id)
            _LOGGER.debug("Device Registry Eintrag entfernt: %s", device.id)
            
    except Exception as e:
        _LOGGER.error("Fehler beim Entfernen der Device Registry Einträge: %s", e)
