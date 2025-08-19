"""Sensor-Plattform für PlantHub Integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    ATTR_DEVICE_CLASS,
    ATTR_ICON,
    ATTR_NAME,
    ATTR_STATE_CLASS,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_NAME,
    PERCENTAGE,
    TEMP_CELSIUS,
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
    ATTR_AIR_HUMIDITY,
    ATTR_AIR_TEMPERATURE,
    ATTR_LIGHT,
    ATTR_PLANT_ID,
    ATTR_PLANT_NAME,
    ATTR_SOIL_MOISTURE,
    ATTR_LAST_UPDATE,
    CONF_API_TOKEN,
    CONF_PLANT_ID,
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


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setze die PlantHub Sensor-Entitäten auf."""
    coordinator: PlantHubDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        "coordinator"
    ]
    
    # Erstelle Sensor-Entitäten für jede Pflanze
    entities = []
    
    for plant_id in coordinator.plant_ids:
        plant_name = coordinator.get_plant_name(plant_id)
        
        # Status-Sensor
        entities.append(PlantHubStatusSensor(coordinator, plant_id, plant_name))
        
        # Bodenfeuchtigkeit-Sensor
        entities.append(PlantHubSoilMoistureSensor(coordinator, plant_id, plant_name))
        
        # Lufttemperatur-Sensor
        entities.append(PlantHubAirTemperatureSensor(coordinator, plant_id, plant_name))
        
        # Luftfeuchtigkeit-Sensor
        entities.append(PlantHubAirHumiditySensor(coordinator, plant_id, plant_name))
        
        # Helligkeit-Sensor
        entities.append(PlantHubLightSensor(coordinator, plant_id, plant_name))
        
        # Versteckte plant_id Entität (nur für interne Zwecke)
        entities.append(PlantHubPlantIdSensor(coordinator, plant_id, plant_name))
    
    async_add_entities(entities)
    
    # Verstecke plant_id Entitäten
    await _hide_plant_id_entities(hass, coordinator.plant_ids)


class PlantHubDataUpdateCoordinator(DataUpdateCoordinator):
    """Koordinierer für PlantHub Daten-Updates."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{config_entry.data[CONF_NAME]}",
            update_interval=config_entry.data.get("scan_interval", 300),
        )
        
        self.config_entry = config_entry
        self.api_token = config_entry.data[CONF_API_TOKEN]
        self.plant_ids = config_entry.data.get(CONF_PLANT_ID, [])
        self._plant_names: Dict[str, str] = {}
        
        # Lade Pflanzennamen aus der Konfiguration
        for plant_config in config_entry.data.get("plants", []):
            if isinstance(plant_config, dict):
                plant_id = plant_config.get(CONF_PLANT_ID)
                plant_name = plant_config.get(CONF_NAME, plant_id)
                if plant_id:
                    self._plant_names[plant_id] = plant_name

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data from PlantHub API."""
        try:
            from .webhook import PlantHubWebhook
            
            async with PlantHubWebhook(self.hass, self.api_token) as webhook:
                # Hole Daten für alle Pflanzen
                all_plants_data = await webhook.fetch_all_plants_data()
                
                # Aktualisiere Pflanzennamen
                for plant_data in all_plants_data:
                    plant_id = plant_data.get(ATTR_PLANT_ID)
                    plant_name = plant_data.get(ATTR_PLANT_NAME, plant_id)
                    if plant_id:
                        self._plant_names[plant_id] = plant_name
                
                return {
                    "plants": all_plants_data,
                    "last_update": datetime.now().isoformat(),
                }
                
        except Exception as e:
            _LOGGER.error("Fehler beim Aktualisieren der PlantHub-Daten: %s", e)
            return {
                "plants": [],
                "last_update": datetime.now().isoformat(),
                "error": str(e),
            }

    def get_plant_data(self, plant_id: str) -> Optional[Dict[str, Any]]:
        """Hole Daten für eine spezifische Pflanze."""
        if not self.data or "plants" not in self.data:
            return None
            
        for plant_data in self.data["plants"]:
            if plant_data.get(ATTR_PLANT_ID) == plant_id:
                return plant_data
        return None

    def get_plant_name(self, plant_id: str) -> str:
        """Hole den Namen einer Pflanze."""
        return self._plant_names.get(plant_id, plant_id)


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
        
        # Erstelle eindeutige Entity-ID
        self._attr_unique_id = f"{plant_id}_{sensor_type}"
        self._attr_name = f"{plant_name} {sensor_type.replace('_', ' ').title()}"
        
        # Verknüpfe mit Device Registry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, plant_id)},
            "name": plant_name,
            "manufacturer": "PlantHub",
            "model": "PlantHub Sensor",
            "sw_version": "1.0.0",
        }

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
            ATTR_PLANT_ID: self.plant_id,
            ATTR_PLANT_NAME: self.plant_name,
            ATTR_LAST_UPDATE: plant_data.get(ATTR_LAST_UPDATE),
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
        self._attr_icon = "mdi:flower"
        self._attr_device_class = None
        self._attr_state_class = None

    @property
    def native_value(self) -> StateType:
        """Return the status of the plant."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return STATUS_UNKNOWN
            
        soil_moisture = plant_data.get(ATTR_SOIL_MOISTURE)
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
                ATTR_SOIL_MOISTURE: plant_data.get(ATTR_SOIL_MOISTURE),
                ATTR_AIR_TEMPERATURE: plant_data.get(ATTR_AIR_TEMPERATURE),
                ATTR_AIR_HUMIDITY: plant_data.get(ATTR_AIR_HUMIDITY),
                ATTR_LIGHT: plant_data.get(ATTR_LIGHT),
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
        self._attr_icon = "mdi:water-percent"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> StateType:
        """Return the soil moisture percentage."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get(ATTR_SOIL_MOISTURE)


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
        self._attr_icon = "mdi:thermometer"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = TEMP_CELSIUS

    @property
    def native_value(self) -> StateType:
        """Return the air temperature in Celsius."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get(ATTR_AIR_TEMPERATURE)


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
        self._attr_icon = "mdi:air-humidifier"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self) -> StateType:
        """Return the air humidity percentage."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get(ATTR_AIR_HUMIDITY)


class PlantHubLightSensor(BasePlantHubSensor):
    """Helligkeit-Sensor für PlantHub Pflanzen."""

    def __init__(
        self,
        coordinator: PlantHubDataUpdateCoordinator,
        plant_id: str,
        plant_name: str,
    ) -> None:
        """Initialize the light sensor."""
        super().__init__(coordinator, plant_id, plant_name, "light")
        self._attr_icon = "mdi:brightness-6"
        self._attr_device_class = SensorDeviceClass.ILLUMINANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = LIGHT_LUX

    @property
    def native_value(self) -> StateType:
        """Return the light level in lux."""
        plant_data = self.coordinator.get_plant_data(self.plant_id)
        if not plant_data:
            return None
        return plant_data.get(ATTR_LIGHT)


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
        self._attr_icon = "mdi:identifier"
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_entity_registry_visible_default = False

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
