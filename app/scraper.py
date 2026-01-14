"""
Scraper service for fetching equipment and system data from Oryx.
Uses the oryx-wat-scraper library for scraping.
"""

from oryx_wat_scraper import OryxScraper as OryxScraperLib


class OryxScraperWrapper:
    """Wrapper for OryxScraper to maintain compatibility with existing code."""

    def __init__(self):
        self.scraper = OryxScraperLib()

    def scrape_equipments(self) -> list[dict]:
        """
        Scrape daily equipment count data.
        Returns data in the format expected by the service.
        """
        daily_counts = self.scraper.get_daily_counts(countries=["russia", "ukraine"])

        # Convert to expected format
        result = []
        for item in daily_counts:
            result.append(
                {
                    "country": item["country"],
                    "equipment_type": item["equipment_type"],
                    "destroyed": item["destroyed"],
                    "abandoned": item["abandoned"],
                    "captured": item["captured"],
                    "damaged": item["damaged"],
                    "type_total": item["type_total"],
                    "date_recorded": item["date_recorded"],
                }
            )
        return result

    def scrape_all_equipments(self) -> list[dict]:
        """
        Scrape total equipment by type data.
        Returns data in the format expected by the service.
        """
        totals = self.scraper.get_totals_by_type(countries=["russia", "ukraine"])

        # Convert to expected format
        result = []
        for item in totals:
            result.append(
                {
                    "country": item["country"],
                    "equipment_type": item["type"],
                    "destroyed": item["destroyed"],
                    "abandoned": item["abandoned"],
                    "captured": item["captured"],
                    "damaged": item["damaged"],
                    "type_total": item["total"],
                }
            )
        return result

    def scrape_systems(self) -> list[dict]:
        """
        Scrape system data (individual entries).
        Note: oryx_wat_scraper doesn't have system-level scraping yet,
        so this returns empty list for now.
        """
        # TODO: Implement system scraping when oryx_wat_scraper supports it
        return []

    def scrape_all_systems(self) -> list[dict]:
        """
        Scrape totals by system wide data.
        Note: oryx_wat_scraper doesn't have system-level scraping yet,
        so this returns empty list for now.
        """
        # TODO: Implement system scraping when oryx_wat_scraper supports it
        return []

    def close(self):
        """Close the scraper."""
        self.scraper.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Alias for backward compatibility
OryxScraper = OryxScraperWrapper
