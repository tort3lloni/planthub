"""PlantHub Sensor für Home Assistant."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_FERTILIZER,
    ATTR_LIGHT,
    ATTR_MOISTURE,
    ATTR_PLANT_NAME,
    ATTR_TEMPERATURE,
    CONF_NAME,
    CONF_PLANT_ID,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setze PlantHub Sensor auf."""
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="planthub",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            PlantHubSensor(coordinator, entry),
            PlantHubMoistureSensor(coordinator, entry),
            PlantHubTemperatureSensor(coordinator, entry),
            PlantHubLightSensor(coordinator, entry),
            PlantHubFertilizerSensor(coordinator, entry),
        ]
    )


async def async_update_data() -> dict[str, Any]:
    """Update data via PlantHub API."""
    # Hier würde normalerweise die API-Abfrage stehen
    # Für Demo-Zwecke geben wir Beispieldaten zurück
    return {
        "plant_name": "Monstera Deliciosa",
        "moisture": 65,
        "temperature": 22.5,
        "light": 800,
        "fertilizer": 45,
    }


class PlantHubSensor(CoordinatorEntity, SensorEntity):
    """Representation eines PlantHub Sensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data[CONF_PLANT_ID]}_status"
        self._attr_name = f"{entry.data[CONF_NAME]} Status"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["gesund", "warnung", "kritisch"]

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        if not data:
            return "unbekannt"
        
        moisture = data.get(ATTR_MOISTURE, 0)
        if moisture < 30:
            return "kritisch"
        elif moisture < 50:
            return "warnung"
        else:
            return "gesund"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        data = self.coordinator.data
        if not data:
            return {}
        
        return {
            ATTR_PLANT_NAME: data.get(ATTR_PLANT_NAME),
            ATTR_MOISTURE: data.get(ATTR_MOISTURE),
            ATTR_TEMPERATURE: data.get(ATTR_TEMPERATURE),
            ATTR_LIGHT: data.get(ATTR_LIGHT),
            ATTR_FERTILIZER: data.get(ATTR_FERTILIZER),
        }


class PlantHubMoistureSensor(CoordinatorEntity, SensorEntity):
    """Representation eines PlantHub Feuchtigkeitssensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data[CONF_PLANT_ID]}_moisture"
        self._attr_name = f"{entry.data[CONF_NAME]} Feuchtigkeit"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        return data.get(ATTR_MOISTURE) if data else None


class PlantHubTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation eines PlantHub Temperatursensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data[CONF_PLANT_ID]}_temperature"
        self._attr_name = f"{entry.data[CONF_NAME]} Temperatur"
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "°C"

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        return data.get(ATTR_TEMPERATURE) if data else None


class PlantHubLightSensor(CoordinatorEntity, SensorEntity):
    """Representation eines PlantHub Lichtsensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data[CONF_PLANT_ID]}_light"
        self._attr_name = f"{entry.data[CONF_NAME]} Licht"
        self._attr_device_class = SensorDeviceClass.ILLUMINANCE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "lux"

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        return data.get(ATTR_LIGHT) if data else None


class PlantHubFertilizerSensor(CoordinatorEntity, SensorEntity):
    """Representation eines PlantHub Düngersensors."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.data[CONF_PLANT_ID]}_fertilizer"
        self._attr_name = f"{entry.data[CONF_NAME]} Dünger"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        data = self.coordinator.data
        return data.get(ATTR_FERTILIZER) if data else None
