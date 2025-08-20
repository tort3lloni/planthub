"""Konstanten für PlantHub Integration."""
from __future__ import annotations

from typing import Final

# Domain
DOMAIN: Final = "planthub"

# Konfiguration
CONF_TOKEN: Final = "token"

# Standardwerte
DEFAULT_NAME: Final = "PlantHub"
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 Minuten

# Webhook-Konfiguration
WEBHOOK_BASE_URL: Final = "http://govegan.local:5678"
WEBHOOK_ENDPOINT: Final = "/webhook/v1/planthub"
WEBHOOK_TIMEOUT: Final = 30  # Sekunden

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
MIN_ILLUMINANCE: Final = 0
