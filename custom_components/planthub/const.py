"""Konstanten für PlantHub Integration."""
from __future__ import annotations

from typing import Final

# Domain
DOMAIN: Final = "planthub"

# Konfiguration
CONF_API_TOKEN: Final = "api_token"
CONF_NAME: Final = "name"
CONF_PLANT_ID: Final = "plant_id"

# Standardwerte
DEFAULT_NAME: Final = "PlantHub"
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 Minuten

# Webhook-Konfiguration
WEBHOOK_BASE_URL: Final = "http://govegan.local:5678/webhook/v1"
WEBHOOK_ENDPOINT: Final = "/planthub"
WEBHOOK_TIMEOUT: Final = 30  # Sekunden

# Attribute
ATTR_PLANT_NAME: Final = "plant_name"
ATTR_PLANT_ID: Final = "plant_id"
ATTR_SOIL_MOISTURE: Final = "soil_moisture"
ATTR_AIR_TEMPERATURE: Final = "air_temperature"
ATTR_AIR_HUMIDITY: Final = "air_humidity"
ATTR_LIGHT: Final = "light"
ATTR_LAST_UPDATE: Final = "last_update"

# Status
STATUS_HEALTHY: Final = "healthy"
STATUS_WARNING: Final = "warning"
STATUS_CRITICAL: Final = "critical"
STATUS_UNKNOWN: Final = "unknown"

# Device Registry
DEVICE_MODEL: Final = "PlantHub Sensor"
DEVICE_MANUFACTURER: Final = "PlantHub"
DEVICE_SW_VERSION: Final = "1.0.0"

# HTTP Status Codes
HTTP_OK: Final = 200
HTTP_UNAUTHORIZED: Final = 401
HTTP_FORBIDDEN: Final = 403
HTTP_NOT_FOUND: Final = 404
HTTP_TOO_MANY_REQUESTS: Final = 429
HTTP_INTERNAL_SERVER_ERROR: Final = 500

# Sensor Thresholds
SOIL_MOISTURE_CRITICAL_THRESHOLD: Final = 30
SOIL_MOISTURE_WARNING_THRESHOLD: Final = 50

# Validation Ranges
MIN_SOIL_MOISTURE: Final = 0
MAX_SOIL_MOISTURE: Final = 100
MIN_AIR_HUMIDITY: Final = 0
MAX_AIR_HUMIDITY: Final = 100
MIN_AIR_TEMPERATURE: Final = -50
MAX_AIR_TEMPERATURE: Final = 100
MIN_LIGHT: Final = 0
