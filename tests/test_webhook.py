"""Unit tests for PlantHub webhook functionality."""
import pytest
from unittest.mock import AsyncMock, MagicMock
import aiohttp

from custom_components.planthub.webhook import (
    PlantHubWebhook,
    PlantHubWebhookError,
    PlantHubAuthError,
    PlantHubConnectionError,
    PlantHubRateLimitError,
    HttpClientProtocol,
)


class MockHttpClient:
    """Mock HTTP client for testing."""
    
    def __init__(self, status: int = 200, response_data: dict = None):
        self.status = status
        self.response_data = response_data or {}
    
    async def get(self, url: str):
        """Mock GET request."""
        response = MagicMock()
        response.status = self.status
        response.json = AsyncMock(return_value=self.response_data)
        return response


@pytest.fixture
def mock_hass():
    """Mock Home Assistant instance."""
    return MagicMock()


@pytest.fixture
def api_token():
    """Sample API token."""
    return "test_token_12345"


@pytest.mark.asyncio
async def test_webhook_initialization(mock_hass, api_token):
    """Test webhook initialization."""
    webhook = PlantHubWebhook(mock_hass, api_token)
    
    assert webhook.api_token == api_token
    assert webhook.hass == mock_hass
    assert "Authorization" in webhook._headers
    assert f"Bearer {api_token}" in webhook._headers["Authorization"]


@pytest.mark.asyncio
async def test_webhook_context_manager(mock_hass, api_token):
    """Test webhook as async context manager."""
    async with PlantHubWebhook(mock_hass, api_token) as webhook:
        assert webhook.session is not None
        assert isinstance(webhook.session, aiohttp.ClientSession)
    
    # Session should be closed after context exit
    assert webhook.session is None


@pytest.mark.asyncio
async def test_webhook_with_custom_http_client(mock_hass, api_token):
    """Test webhook with injected HTTP client."""
    mock_client = MockHttpClient(200, {"id": "test_plant", "name": "Test Plant"})
    
    webhook = PlantHubWebhook(
        mock_hass, 
        api_token, 
        http_client=mock_client,
        base_url="https://test.api.com",
        timeout=10
    )
    
    assert webhook._http_client == mock_client
    assert webhook._base_url == "https://test.api.com"
    assert webhook._timeout == 10


@pytest.mark.asyncio
async def test_fetch_plant_data_success(mock_hass, api_token):
    """Test successful plant data fetch."""
    mock_client = MockHttpClient(200, {
        "id": "plant_001",
        "name": "Test Plant",
        "soil_moisture": 75.5,
        "air_temperature": 22.3,
        "air_humidity": 65.0,
        "light": 1200.0,
        "last_updated": "2024-01-01T12:00:00Z"
    })
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    result = await webhook.fetch_plant_data("plant_001")
    
    assert result["plant_id"] == "plant_001"
    assert result["plant_name"] == "Test Plant"
    assert result["soil_moisture"] == 75.5
    assert result["air_temperature"] == 22.3
    assert result["air_humidity"] == 65.0
    assert result["light"] == 1200.0


@pytest.mark.asyncio
async def test_fetch_plant_data_unauthorized(mock_hass, api_token):
    """Test unauthorized access handling."""
    mock_client = MockHttpClient(401)
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    with pytest.raises(PlantHubAuthError, match="API-Token ist ungültig oder abgelaufen"):
        await webhook.fetch_plant_data("plant_001")


@pytest.mark.asyncio
async def test_fetch_plant_data_forbidden(mock_hass, api_token):
    """Test forbidden access handling."""
    mock_client = MockHttpClient(403)
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    with pytest.raises(PlantHubAuthError, match="Zugriff verweigert"):
        await webhook.fetch_plant_data("plant_001")


@pytest.mark.asyncio
async def test_fetch_plant_data_not_found(mock_hass, api_token):
    """Test not found handling."""
    mock_client = MockHttpClient(404)
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    with pytest.raises(PlantHubWebhookError, match="Pflanze plant_001 nicht gefunden"):
        await webhook.fetch_plant_data("plant_001")


@pytest.mark.asyncio
async def test_fetch_plant_data_rate_limit(mock_hass, api_token):
    """Test rate limit handling."""
    mock_client = MockHttpClient(429)
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    with pytest.raises(PlantHubRateLimitError, match="API-Rate Limit überschritten"):
        await webhook.fetch_plant_data("plant_001")


@pytest.mark.asyncio
async def test_fetch_plant_data_server_error(mock_hass, api_token):
    """Test server error handling."""
    mock_client = MockHttpClient(500)
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    with pytest.raises(PlantHubConnectionError, match="Server-Fehler: 500"):
        await webhook.fetch_plant_data("plant_001")


@pytest.mark.asyncio
async def test_fetch_all_plants_data_success(mock_hass, api_token):
    """Test successful fetch of all plants data."""
    mock_client = MockHttpClient(200, {
        "plants": [
            {
                "id": "plant_001",
                "name": "Plant 1",
                "soil_moisture": 80.0,
                "air_temperature": 20.0,
                "air_humidity": 70.0,
                "light": 1000.0
            },
            {
                "id": "plant_002",
                "name": "Plant 2",
                "soil_moisture": 60.0,
                "air_temperature": 25.0,
                "air_humidity": 60.0,
                "light": 1500.0
            }
        ]
    })
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    result = await webhook.fetch_all_plants_data()
    
    assert len(result) == 2
    assert result[0]["plant_id"] == "plant_001"
    assert result[0]["plant_name"] == "Plant 1"
    assert result[1]["plant_id"] == "plant_002"
    assert result[1]["plant_name"] == "Plant 2"


@pytest.mark.asyncio
async def test_data_normalization_with_fallback(mock_hass, api_token):
    """Test data normalization with fallback for missing data."""
    mock_client = MockHttpClient(200, {
        "id": "plant_001",
        "name": "Test Plant"
        # Missing sensor data
    })
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    result = await webhook.fetch_plant_data("plant_001")
    
    assert result["plant_id"] == "plant_001"
    assert result["plant_name"] == "Test Plant"
    assert result["soil_moisture"] is None
    assert result["air_temperature"] is None
    assert result["air_humidity"] is None
    assert result["light"] is None
    assert "last_update" in result


@pytest.mark.asyncio
async def test_data_validation_ranges(mock_hass, api_token):
    """Test data validation for numeric ranges."""
    mock_client = MockHttpClient(200, {
        "id": "plant_001",
        "name": "Test Plant",
        "soil_moisture": 150.0,  # Invalid: > 100
        "air_humidity": -10.0,   # Invalid: < 0
        "air_temperature": 150.0, # Invalid: > 100
        "light": -500.0          # Invalid: < 0
    })
    
    webhook = PlantHubWebhook(mock_hass, api_token, http_client=mock_client)
    
    # Should not raise exception, but log warnings
    result = await webhook.fetch_plant_data("plant_001")
    
    assert result["plant_id"] == "plant_001"
    # Values should still be returned even if out of range
    assert result["soil_moisture"] == 150.0
    assert result["air_humidity"] == -10.0
    assert result["air_temperature"] == 150.0
    assert result["light"] == -500.0


@pytest.mark.asyncio
async def test_webhook_error_inheritance():
    """Test that webhook errors inherit from HomeAssistantError."""
    from homeassistant.exceptions import HomeAssistantError
    
    assert issubclass(PlantHubWebhookError, HomeAssistantError)
    assert issubclass(PlantHubAuthError, PlantHubWebhookError)
    assert issubclass(PlantHubConnectionError, PlantHubWebhookError)
    assert issubclass(PlantHubRateLimitError, PlantHubWebhookError)


@pytest.mark.asyncio
async def test_http_client_protocol():
    """Test that HttpClientProtocol is properly defined."""
    # This should not raise any errors
    protocol = HttpClientProtocol
    
    # Check that it's a Protocol class
    assert hasattr(protocol, '__protocol_attributes__')
