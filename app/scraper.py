"""
Scraper service for fetching equipment and system data from Oryx.
Based on implementations from:
- https://github.com/jessicaw9910/oryx
- https://github.com/d-paulus/scrape_oryx_py
"""
import csv
import io
from typing import List, Dict, Any
import httpx
from bs4 import BeautifulSoup


class OryxScraper:
    """Scraper for Oryx equipment loss data."""

    BASE_URL = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"

    def __init__(self):
        self.client = httpx.Client(timeout=30.0)

    def fetch_csv_data(self, url: str) -> List[Dict[str, Any]]:
        """Fetch CSV data from a URL and return as list of dictionaries."""
        try:
            response = self.client.get(url)
            response.raise_for_status()

            # Parse CSV
            csv_data = response.text
            reader = csv.DictReader(io.StringIO(csv_data))
            return list(reader)
        except Exception as e:
            raise Exception(f"Failed to fetch CSV from {url}: {e}")

    def scrape_equipments(self) -> List[Dict[str, Any]]:
        """
        Scrape daily equipment count data.
        Returns data from: https://raw.githubusercontent.com/scarnecchia/oryx_data/main/daily_count.csv
        """
        url = "https://raw.githubusercontent.com/scarnecchia/oryx_data/main/daily_count.csv"
        return self.fetch_csv_data(url)

    def scrape_all_equipments(self) -> List[Dict[str, Any]]:
        """
        Scrape total equipment by type data.
        Returns data from: https://raw.githubusercontent.com/scarnecchia/oryx_data/main/totals_by_type.csv
        """
        url = "https://raw.githubusercontent.com/scarnecchia/oryx_data/main/totals_by_type.csv"
        return self.fetch_csv_data(url)

    def scrape_systems(self) -> List[Dict[str, Any]]:
        """
        Scrape totals by system data.
        Returns data from: https://raw.githubusercontent.com/scarnecchia/oryx_data/main/totals_by_system.csv
        """
        url = "https://raw.githubusercontent.com/scarnecchia/oryx_data/main/totals_by_system.csv"
        return self.fetch_csv_data(url)

    def scrape_all_systems(self) -> List[Dict[str, Any]]:
        """
        Scrape totals by system wide data.
        Returns data from: https://raw.githubusercontent.com/scarnecchia/oryx_data/main/totals_by_system_wide.csv
        """
        url = "https://raw.githubusercontent.com/scarnecchia/oryx_data/main/totals_by_system_wide.csv"
        return self.fetch_csv_data(url)

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
