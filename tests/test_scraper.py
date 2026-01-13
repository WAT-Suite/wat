"""
Tests for scraper service.
"""

from unittest.mock import Mock, patch

import pytest

from app.scraper import OryxScraper


@pytest.mark.unit
def test_scraper_fetch_csv_data():
    """Test fetching CSV data."""
    scraper = OryxScraper()

    # Mock CSV response
    mock_csv = "country,equipment_type,destroyed,abandoned\nukraine,Tanks,10,2"

    with patch.object(scraper.client, "get") as mock_get:
        mock_response = Mock()
        mock_response.text = mock_csv
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        data = scraper.fetch_csv_data("https://example.com/data.csv")

        assert len(data) == 1
        assert data[0]["country"] == "ukraine"
        assert data[0]["equipment_type"] == "Tanks"
        assert data[0]["destroyed"] == "10"

    scraper.close()


@pytest.mark.unit
def test_scraper_fetch_csv_data_error():
    """Test error handling when fetching CSV data."""
    scraper = OryxScraper()

    with patch.object(scraper.client, "get") as mock_get:
        mock_get.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Failed to fetch CSV"):
            scraper.fetch_csv_data("https://example.com/data.csv")

    scraper.close()


@pytest.mark.unit
def test_scraper_context_manager():
    """Test scraper as context manager."""
    with OryxScraper() as scraper:
        assert scraper is not None
        # Client should be closed after context exits
    # After context, client should be closed


@pytest.mark.unit
@patch("app.scraper.OryxScraper.fetch_csv_data")
def test_scrape_equipments(mock_fetch):
    """Test scraping equipments."""
    mock_fetch.return_value = [
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

    scraper = OryxScraper()
    data = scraper.scrape_equipments()

    assert len(data) == 1
    assert data[0]["country"] == "ukraine"
    mock_fetch.assert_called_once()

    scraper.close()


@pytest.mark.unit
@patch("app.scraper.OryxScraper.fetch_csv_data")
def test_scrape_all_equipments(mock_fetch):
    """Test scraping all equipments."""
    mock_fetch.return_value = [
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

    scraper = OryxScraper()
    data = scraper.scrape_all_equipments()

    assert len(data) == 1
    assert data[0]["country"] == "ukraine"
    mock_fetch.assert_called_once()

    scraper.close()
