"""
Tests for main application endpoints.
"""

import pytest


@pytest.mark.unit
def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "War Track Dashboard API"
    assert "version" in data
    assert "docs" in data


@pytest.mark.unit
def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.unit
def test_invalid_country_endpoint(client):
    """Test endpoint with invalid country."""
    response = client.post("/api/stats/equipments/invalid")
    assert response.status_code == 422  # Validation error


@pytest.mark.unit
def test_invalid_system_country_endpoint(client):
    """Test system endpoint with invalid country."""
    response = client.post("/api/stats/systems/invalid")
    assert response.status_code == 422  # Validation error
