"""
Tests for import endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.unit
@patch("app.routers.import_router.OryxScraper")
def test_import_equipments(mock_scraper_class, client, db_session):
    """Test importing equipments."""
    # Mock scraper
    mock_scraper = MagicMock()
    mock_scraper.scrape_equipments.return_value = [
        {
            "country": "ukraine",
            "equipment_type": "Tanks",
            "destroyed": "10",
            "abandoned": "2",
            "captured": "5",
            "damaged": "3",
            "type_total": "20",
            "date_recorded": "2023-01-01",
        }
    ]
    mock_scraper_class.return_value.__enter__.return_value = mock_scraper

    response = client.post("/api/import/equipments")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"].lower()


@pytest.mark.unit
@patch("app.routers.import_router.OryxScraper")
def test_import_all_equipments(mock_scraper_class, client, db_session):
    """Test importing all equipments."""
    # Mock scraper
    mock_scraper = MagicMock()
    mock_scraper.scrape_all_equipments.return_value = [
        {
            "country": "ukraine",
            "equipment_type": "Tanks",
            "destroyed": "100",
            "abandoned": "20",
            "captured": "50",
            "damaged": "30",
            "type_total": "200",
        }
    ]
    mock_scraper_class.return_value.__enter__.return_value = mock_scraper

    response = client.post("/api/import/all-equipments")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.unit
@patch("app.routers.import_router.OryxScraper")
def test_import_systems(mock_scraper_class, client, db_session):
    """Test importing systems."""
    # Mock scraper
    mock_scraper = MagicMock()
    mock_scraper.scrape_systems.return_value = [
        {
            "country": "ukraine",
            "origin": "USA",
            "system": "M1 Abrams",
            "status": "destroyed",
            "url": "https://example.com",
            "date_recorded": "2023-01-01",
        }
    ]
    mock_scraper_class.return_value.__enter__.return_value = mock_scraper

    response = client.post("/api/import/systems")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.unit
@patch("app.routers.import_router.OryxScraper")
def test_import_all_systems(mock_scraper_class, client, db_session):
    """Test importing all systems."""
    # Mock scraper
    mock_scraper = MagicMock()
    mock_scraper.scrape_all_systems.return_value = [
        {
            "country": "ukraine",
            "system": "M1 Abrams",
            "destroyed": "5",
            "abandoned": "1",
            "captured": "2",
            "damaged": "1",
            "total": "9",
        }
    ]
    mock_scraper_class.return_value.__enter__.return_value = mock_scraper

    response = client.post("/api/import/all-systems")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.unit
@patch("app.routers.import_router.OryxScraper")
def test_import_all(mock_scraper_class, client, db_session):
    """Test importing all data."""
    # Mock scraper
    mock_scraper = MagicMock()
    mock_scraper.scrape_equipments.return_value = []
    mock_scraper.scrape_all_equipments.return_value = []
    mock_scraper.scrape_systems.return_value = []
    mock_scraper.scrape_all_systems.return_value = []
    mock_scraper_class.return_value.__enter__.return_value = mock_scraper

    response = client.post("/api/import/all")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"].lower()


@pytest.mark.unit
@patch("app.routers.import_router.OryxScraper")
def test_import_equipments_error(mock_scraper_class, client, db_session):
    """Test import error handling."""
    # Mock scraper to raise an error
    mock_scraper = MagicMock()
    mock_scraper.scrape_equipments.side_effect = Exception("Scraper error")
    mock_scraper_class.return_value.__enter__.return_value = mock_scraper

    response = client.post("/api/import/equipments")
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data
    assert "error" in data["detail"].lower() or "failed" in data["detail"].lower()
