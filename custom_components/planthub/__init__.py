"""PlantHub Integration für Home Assistant."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_TOKEN,
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
    if DOMAIN not in config:
        return True
    
    # Lade den Token aus der configuration.yaml
    token = config[DOMAIN].get(CONF_TOKEN)
    if not token:
        _LOGGER.error("PlantHub Token nicht in configuration.yaml gefunden")
        return False
    
    # Speichere den Token in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][CONF_TOKEN] = token
    
    _LOGGER.info("PlantHub Token aus configuration.yaml geladen")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PlantHub from a config entry."""
    _LOGGER.info("Initialisiere PlantHub Integration: %s", entry.data.get("name", DEFAULT_NAME))

    # Prüfe, ob der Token verfügbar ist
    if CONF_TOKEN not in hass.data.get(DOMAIN, {}):
        _LOGGER.error("PlantHub Token nicht verfügbar. Bitte konfiguriere den Token in configuration.yaml")
        return False

    # Erstelle den Data Update Coordinator
    from .sensor import PlantHubDataUpdateCoordinator
    
    coordinator = PlantHubDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    # Speichere den Coordinator
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
    }

    # Erstelle Device Registry Einträge für alle konfigurierten Pflanzen
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
    """Erstelle Device Registry Einträge für alle konfigurierten Pflanzen."""
    try:
        device_registry = dr.async_get(hass)
        
        for plant_config in coordinator.plants:
            plant_id = plant_config["plant_id"]
            plant_name = plant_config["name"]
            
            # Erstelle oder aktualisiere den Device Registry Eintrag
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, plant_id)},
                name=plant_name,
                manufacturer=DEVICE_MANUFACTURER,
                model=DEVICE_MODEL,
                sw_version=DEVICE_SW_VERSION,
            )
            
            _LOGGER.debug("Device Registry Eintrag erstellt/aktualisiert für Pflanze: %s", plant_id)
        
    except Exception as e:
        _LOGGER.error("Fehler beim Erstellen der Device Registry Einträge: %s", e)


async def _remove_device_registry_entries(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Entferne Device Registry Eintrag für die konfigurierte Pflanze."""
    try:
        device_registry = dr.async_get(hass)
        
        # Finde alle Geräte, die zu dieser Integration gehören
        devices = dr.async_entries_for_config_entry(device_registry, entry.entry_id)
        
        for device in devices:
            # Entferne das Gerät
            device_registry.async_remove_device(device.id)
            _LOGGER.debug("Device Registry Eintrag entfernt: %s", device.id)
            
    except Exception as e:
        _LOGGER.error("Fehler beim Entfernen des Device Registry Eintrags: %s", e)
