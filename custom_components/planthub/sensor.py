"""Sensor-Plattform für PlantHub Integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
    LIGHT_LUX,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    CONF_TOKEN,
    DEFAULT_NAME,
    DOMAIN,
    STATUS_CRITICAL,
    STATUS_HEALTHY,
    STATUS_UNKNOWN,
    STATUS_WARNING,
    SOIL_MOISTURE_CRITICAL_THRESHOLD,
    SOIL_MOISTURE_WARNING_THRESHOLD,
)

_LOGGER = logging.getLogger(__name__)

# Vollständige Sensor-Beschreibungen für moderne Home Assistant 2025 Standards
SENSOR_DESCRIPTIONS = {
    "status": SensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:flower",
        device_class=None,
        state_class=None,
        native_unit_of_measurement=None,
        entity_registry_visible_default=True,
    ),
    "soil_moisture": SensorEntityDescription(
        key="soil_moisture",
        name="Bodenfeuchtigkeit",
        icon="mdi:water-percent",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_registry_visible_default=True,
    ),
    "air_temperature": SensorEntityDescription(
        key="air_temperature",
        name="Lufttemperatur",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        entity_registry_visible_default=True,
    ),
    "air_humidity": SensorEntityDescription(
        key="air_humidity",
        name="Luftfeuchtigkeit",
        icon="mdi:air-humidifier",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        entity_registry_visible_default=True,
    ),
    "illuminance": SensorEntityDescription(
        key="illuminance",
        name="Helligkeit",
        icon="mdi:brightness-6",
        device_class=SensorDeviceClass.ILLUMINANCE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=LIGHT_LUX,
        entity_registry_visible_default=True,
    ),
    "plant_id": SensorEntityDescription(
        key="plant_id",
        name="Pflanzen-ID",
        icon="mdi:identifier",
        device_class=None,
        state_class=None,
        native_unit_of_measurement=None,
        entity_registry_visible_default=False,
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setze die PlantHub Sensor-Entitäten auf."""
    coordinator: PlantHubDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]
    
    # Erstelle Sensor-Entitäten für alle konfigurierten Pflanzen
    entities = []
    
    for plant_config in coordinator.plants:
        plant_id = plant_config["plant_id"]
        plant_name = plant_config["name"]
        
        # Status-Sensor
        entities.append(PlantHubStatusSensor(coordinator, plant_id, plant_name))
        
        # Bodenfeuchtigkeit-Sensor
        entities.append(PlantHubSoilMoistureSensor(coordinator, plant_id, plant_name))
        
        # Lufttemperatur-Sensor
        entities.append(PlantHubAirTemperatureSensor(coordinator, plant_id, plant_name))
        
        # Luftfeuchtigkeit-Sensor
        entities.append(PlantHubAirHumiditySensor(coordinator, plant_id, plant_name))
        
        # Helligkeit-Sensor
        entities.append(PlantHubIlluminanceSensor(coordinator, plant_id, plant_name))
        
        # Versteckte plant_id Entität (nur für interne Zwecke)
        entities.append(PlantHubPlantIdSensor(coordinator, plant_id, plant_name))
    
    async_add_entities(entities)
    
    # Verstecke plant_id Entitäten
    await _hide_plant_id_entities(hass, [p["plant_id"] for p in coordinator.plants])


class PlantHubDataUpdateCoordinator(DataUpdateCoordinator):
    """Koordinierer für PlantHub Daten-Updates."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        # Hole scan_interval aus der Konfiguration und konvertiere zu timedelta
        scan_interval_seconds = config_entry.data.get("scan_interval", 300)
        update_interval = timedelta(seconds=scan_interval_seconds)
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{config_entry.data.get('name', DEFAULT_NAME)}",
            update_interval=update_interval,
        )
        
        self.config_entry = config_entry
        self.hass = hass
        # Hole den Token aus hass.data statt aus config_entry
        self.token = hass.data[DOMAIN][CONF_TOKEN]
        self.plants = config_entry.data.get("plants", [])  # Liste aller Pflanzen

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data from PlantHub API."""
        try:
            from .webhook import PlantHubWebhook
            
            all_plants_data = {}
            
            async with PlantHubWebhook(self.hass, self.token) as webhook:
                # Hole Daten für alle konfigurierten Pflanzen
                for plant_config in self.plants:
                    plant_id = plant_config["plant_id"]
                    try:
                        plant_data = await webhook.fetch_plant_data(plant_id)
                        all_plants_data[plant_id] = plant_data
                    except Exception as e:
                        _LOGGER.error("Fehler beim Laden der Daten für Pflanze %s: %s", plant_id, e)
                        all_plants_data[plant_id] = None
                
                return {
                    "plants": all_plants_data,
                    "last_update": datetime.now().isoformat(),
                }
                
        except Exception as e:
            _LOGGER.error("Fehler beim Aktualisieren der PlantHub-Daten: %s", e)
            return {
                "plants": {},
                "last_update": datetime.now().isoformat(),
                "error": str(e),
            }

    def get_plant_data(self, plant_id: str) -> Optional[Dict[str, Any]]:
        """Hole Daten für eine spezifische Pflanze."""
        if not self.data or "plants" not in self.data:
            return None
            
        return self.data["plants"].get(plant_id)


class BasePlantHubSensor(CoordinatorEntity, SensorEntity):
    """Basis-Klasse für alle PlantHub Sensoren."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
        sensor_type: str,
    ) -> None:
        """Initialize the base sensor."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.plant_id = plant_id
        self.plant_name = plant_name
        self.sensor_type = sensor_type
        
        # Verwende vollständige SensorEntityDescription
        self.entity_description = SENSOR_DESCRIPTIONS[sensor_type]
        
        # Erstelle eindeutige Entity-ID basierend auf plant_id und description.key
        self._attr_unique_id = f"{plant_id}_{self.entity_description.key}"
        
        # Wichtig: has_entity_name=True für UI-Umbenennung
        self._attr_has_entity_name = True
        
        # Verknüpfe mit Device Registry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, plant_id)},
            "name": plant_name,  # Standardname, kann über Device Registry UI geändert werden
            "manufacturer": "PlantHub",
            "model": "PlantHub Sensor",
            "sw_version": "1.0.0",
        }

    @property
    def name(self) -> str | None:
        """Return the name of the entity."""
        # Für has_entity_name=True wird der Name aus der Entity Registry gelesen
        # Der Benutzer kann den Namen über die Home Assistant UI ändern
        return None  # None = verwende den Namen aus der Entity Registry

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and "plants" in self.coordinator.data
        )

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return {}
            
        return {
            "plant_id": self.plant_id,
            "plant_name": self.plant_name,
            "last_update": plant_data.get("last_update"),
        }


class PlantHubStatusSensor(BasePlantHubSensor):
    """Status-Sensor für PlantHub Pflanzen."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the status sensor."""
        super().__init__(coordinator, plant_id, plant_name, "status")

    @property
    def native_value(self) -> StateType:
        """Return the status of the plant."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return STATUS_UNKNOWN
            
        soil_moisture = plant_data.get("soil_moisture")
        if soil_moisture is None:
            return STATUS_UNKNOWN
            
        if soil_moisture <= SOIL_MOISTURE_CRITICAL_THRESHOLD:
            return STATUS_CRITICAL
        elif soil_moisture <= SOIL_MOISTURE_WARNING_THRESHOLD:
            return STATUS_WARNING
        else:
            return STATUS_HEALTHY

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        attrs = super().extra_state_attributes
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if plant_data:
            attrs.update({
                "soil_moisture": plant_data.get("soil_moisture"),
                "air_temperature": plant_data.get("air_temperature"),
                "air_humidity": plant_data.get("air_humidity"),
                "illuminance": plant_data.get("illuminance"),
            })
        return attrs


class PlantHubSoilMoistureSensor(BasePlantHubSensor):
    """Bodenfeuchtigkeit-Sensor für PlantHub Pflanzen."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the soil moisture sensor."""
        super().__init__(coordinator, plant_id, plant_name, "soil_moisture")

    @property
    def native_value(self) -> StateType:
        """Return the soil moisture percentage."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get("soil_moisture")


class PlantHubAirTemperatureSensor(BasePlantHubSensor):
    """Lufttemperatur-Sensor für PlantHub Pflanzen."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the air temperature sensor."""
        super().__init__(coordinator, plant_id, plant_name, "air_temperature")

    @property
    def native_value(self) -> StateType:
        """Return the air temperature in Celsius."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get("air_temperature")


class PlantHubAirHumiditySensor(BasePlantHubSensor):
    """Luftfeuchtigkeit-Sensor für PlantHub Pflanzen."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the air humidity sensor."""
        super().__init__(coordinator, plant_id, plant_name, "air_humidity")

    @property
    def native_value(self) -> StateType:
        """Return the air humidity percentage."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get("air_humidity")


class PlantHubIlluminanceSensor(BasePlantHubSensor):
    """Helligkeit-Sensor für PlantHub Pflanzen."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the light sensor."""
        super().__init__(coordinator, plant_id, plant_name, "illuminance")

    @property
    def native_value(self) -> StateType:
        """Return the light level in lux."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get("illuminance")


class PlantHubPlantIdSensor(BasePlantHubSensor):
    """Versteckte plant_id Entität für interne Zwecke."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the plant ID sensor."""
        super().__init__(coordinator, plant_id, plant_name, "plant_id")

    @property
    def native_value(self) -> StateType:
        """Return the plant ID."""
        return self.plant_id


async def _hide_plant_id_entities(hass: HomeAssistant, plant_ids: list) -> None:
    """Verstecke plant_id Entitäten im Entity Registry."""
    try:
        from homeassistant.helpers import entity_registry as er
        
        entity_registry = er.async_get(hass)
        
        for plant_id in plant_ids:
            entity_id = f"sensor.{plant_id}_plant_id"
            if entity_registry.async_get(entity_id):
                entity_registry.async_update_entity(
                    entity_id, hidden_by=er.RegistryEntryHider.INTEGRATION
                )
                _LOGGER.debug("Plant ID Entität versteckt: %s", entity_id)
                
    except Exception as e:
        _LOGGER.warning("Fehler beim Verstecken der Plant ID Entitäten: %s", e)
