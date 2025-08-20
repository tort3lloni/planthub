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

    # Device Registry Listener sind in Home Assistant 2025 nicht verfügbar
    # await _register_device_registry_listener(hass, entry)
    
    # Registriere Entity Registry Listener für automatische Synchronisation
    await _register_entity_registry_listener(hass, entry)

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
        # Device Registry Listener sind in Home Assistant 2025 nicht verfügbar
        # await _unregister_device_registry_listener(hass, entry)
        
        # Entferne Entity Registry Listener
        await _unregister_entity_registry_listener(hass, entry)
        
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
            # Verwende den Namen aus der Konfiguration, aber erlaube Umbenennung über UI
            device_registry.async_get_or_create(
                config_entry_id=entry.entry_id,
                identifiers={(DOMAIN, plant_id)},
                name=plant_name,  # Standardname, kann über UI geändert werden
                manufacturer=DEVICE_MANUFACTURER,
                model=DEVICE_MODEL,
                sw_version=DEVICE_SW_VERSION,
                # Keine festen Namen setzen - erlaube Umbenennung über UI
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


async def _register_device_registry_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Registriere Device Registry Listener für automatische Synchronisation."""
    # Device Registry Listener sind in Home Assistant 2025 nicht verfügbar
    # Wir verwenden nur Entity Registry Listener für die Synchronisation
    _LOGGER.debug("Device Registry Listener nicht verfügbar in Home Assistant 2025")


async def _unregister_device_registry_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Entferne Device Registry Listener."""
    # Device Registry Listener sind in Home Assistant 2025 nicht verfügbar
    pass


async def _register_entity_registry_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Registriere Entity Registry Listener für automatische Synchronisation."""
    try:
        from homeassistant.helpers import entity_registry as er
        entity_registry = er.async_get(hass)
        
        # Speichere den Listener in hass.data für späteres Entfernen
        if "entity_listeners" not in hass.data[DOMAIN]:
            hass.data[DOMAIN]["entity_listeners"] = {}
        
        def _entity_removed(entity_id: str) -> None:
            """Callback wenn eine Entität entfernt wird."""
            _LOGGER.info("Entität entfernt über UI: %s", entity_id)
            
            # Aktualisiere die Konfiguration, falls die Entität eine Pflanze war
            _update_plant_config_from_entity(hass, entry, entity_id)
        
        # Registriere den Listener
        unsub = entity_registry.async_listen_removed(_entity_removed)
        
        # Speichere den Unsubscribe-Callback
        hass.data[DOMAIN]["entity_listeners"][entry.entry_id] = unsub
        
        _LOGGER.debug("Entity Registry Listener für Integration %s registriert", entry.entry_id)
        
    except Exception as e:
        _LOGGER.error("Fehler beim Registrieren des Entity Registry Listeners: %s", e)


async def _unregister_entity_registry_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Entferne Entity Registry Listener."""
    try:
        if "entity_listeners" in hass.data.get(DOMAIN, {}):
            if entry.entry_id in hass.data[DOMAIN]["entity_listeners"]:
                # Entferne den Listener
                unsub = hass.data[DOMAIN]["entity_listeners"].pop(entry.entry_id)
                unsub()
                _LOGGER.debug("Entity Registry Listener für Integration %s entfernt", entry.entry_id)
                
    except Exception as e:
        _LOGGER.error("Fehler beim Entfernen des Entity Registry Listeners: %s", e)


def _remove_plant_from_config(hass: HomeAssistant, entry: ConfigEntry, device_id: str) -> None:
    """Entferne eine Pflanze aus der Konfiguration basierend auf der Device ID."""
    try:
        # Finde das Gerät anhand der Device ID
        device_registry = dr.async_get(hass)
        device = device_registry.async_get(device_id)
        
        if not device:
            _LOGGER.warning("Gerät %s nicht im Device Registry gefunden", device_id)
            return
        
        # Finde die plant_id aus den Identifiers
        plant_id = None
        for identifier in device.identifiers:
            if identifier[0] == DOMAIN:
                plant_id = identifier[1]
                break
        
        if not plant_id:
            _LOGGER.warning("Keine plant_id für Gerät %s gefunden", device_id)
            return
        
        _LOGGER.info("Entferne Pflanze %s aus der Konfiguration (Gerät über UI entfernt)", plant_id)
        
        # Aktualisiere die Konfiguration
        new_data = entry.data.copy()
        if "plants" in new_data:
            # Entferne die Pflanze aus der Pflanzenliste
            new_data["plants"] = [p for p in new_data["plants"] if p["plant_id"] != plant_id]
            
            # Aktualisiere den Konfigurationseintrag
            hass.config_entries.async_update_entry(entry, data=new_data)
            
            _LOGGER.info("Pflanze %s erfolgreich aus der Konfiguration entfernt", plant_id)
            
            # Aktualisiere den Coordinator
            if entry.entry_id in hass.data.get(DOMAIN, {}):
                coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
                if coordinator:
                    coordinator.plants = new_data.get("plants", [])
                    _LOGGER.debug("Coordinator für Integration %s aktualisiert", entry.entry_id)
        
    except Exception as e:
        _LOGGER.error("Fehler beim Entfernen der Pflanze %s aus der Konfiguration: %s", plant_id, e)


async def _update_plant_config_from_entity(hass: HomeAssistant, entry: ConfigEntry, entity_id: str) -> None:
    """Aktualisiere die PlantHub-Konfiguration basierend auf einer entfernten Entität."""
    try:
        from homeassistant.helpers import entity_registry as er
        entity_registry = er.async_get(hass)
        entity = entity_registry.async_get(entity_id)
        
        if not entity or entity.config_entry_id != entry.entry_id:
            return
        
        # Entferne die Entität aus der Konfiguration
        new_data = entry.data.copy()
        if "plants" in new_data:
            # Entferne die Entität aus der Pflanzenliste
            new_data["plants"] = [p for p in new_data["plants"] if p["plant_id"] != entity.unique_id]
            
            # Aktualisiere den Konfigurationseintrag
            hass.config_entries.async_update_entry(entry, data=new_data)
            
            _LOGGER.info("Entität %s entfernt, Pflanze %s aus Konfiguration entfernt", entity_id, entity.unique_id)
            
            # Aktualisiere den Coordinator
            if entry.entry_id in hass.data.get(DOMAIN, {}):
                coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
                if coordinator:
                    coordinator.plants = new_data.get("plants", [])
                    _LOGGER.debug("Coordinator für Integration %s aktualisiert", entry.entry_id)
        
    except Exception as e:
        _LOGGER.error("Fehler beim Aktualisieren der Konfiguration nach Entitätsentfernung: %s", e)
