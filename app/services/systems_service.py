from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

from app.models import System, AllSystem
from app.schemas import SystemResponse, AllSystemResponse
from app.enums import Countries, Status
from app.scraper import OryxScraper


class SystemsService:
    def __init__(self, db: Session):
        self.db = db

    def get_systems(
        self,
        country: Countries,
        systems: Optional[List[str]] = None,
        status: Optional[List[Status]] = None,
        date: Optional[List[str]] = None,
    ) -> List[SystemResponse]:
        """Get system data with filters."""
        query = self.db.query(System).filter(
            System.country.ilike(country.value)
        )

        if systems:
            query = query.filter(System.system.in_(systems))

        if status:
            query = query.filter(System.status.in_([s.value for s in status]))

        if date and len(date) == 2:
            start_date = date[0]
            end_date = date[1]
            if start_date > end_date:
                raise ValueError(
                    "Start date should be before end date, please correct"
                )
            query = query.filter(
                and_(System.date >= start_date, System.date <= end_date)
            )

        results = query.all()
        return [SystemResponse.model_validate(r) for r in results]

    def get_total_systems(
        self,
        country: Optional[Countries] = None,
        systems: Optional[List[str]] = None,
    ) -> List[AllSystemResponse]:
        """Get total system data with filters."""
        query = self.db.query(AllSystem)

        if country:
            query = query.filter(AllSystem.country.ilike(country.value))

        if systems:
            query = query.filter(AllSystem.system.in_(systems))

        results = query.all()
        return [AllSystemResponse.model_validate(r) for r in results]

    def get_system_types(self) -> List[dict]:
        """Get distinct system types."""
        results = (
            self.db.query(AllSystem.system)
            .distinct()
            .all()
        )
        return [{"system": r[0]} for r in results]

    def import_systems(self):
        """Import system data from scraper with incremental updates."""
        from sqlalchemy.dialects.postgresql import insert

        with OryxScraper() as scraper:
            data = scraper.scrape_systems()

        # Use upsert for incremental updates
        for item in data:
            system_data = {
                "country": item.get("country", ""),
                "origin": item.get("origin", ""),
                "system": item.get("system", ""),
                "status": item.get("status", ""),
                "url": item.get("url", ""),
                "date": item.get("date_recorded", ""),
            }

            stmt = insert(System).values(**system_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["country", "system", "url", "date"],
                set_={
                    "origin": stmt.excluded.origin,
                    "status": stmt.excluded.status,
                },
            )
            self.db.execute(stmt)

        self.db.commit()

    def import_all_systems(self):
        """Import all system totals from scraper with incremental updates."""
        from sqlalchemy.dialects.postgresql import insert

        with OryxScraper() as scraper:
            data = scraper.scrape_all_systems()

        # Use upsert for incremental updates
        for item in data:
            system_data = {
                "country": item.get("country", ""),
                "system": item.get("system", ""),
                "destroyed": int(item.get("destroyed", 0) or 0),
                "abandoned": int(item.get("abandoned", 0) or 0),
                "captured": int(item.get("captured", 0) or 0),
                "damaged": int(item.get("damaged", 0) or 0),
                "total": int(item.get("total", 0) or 0),
            }

            stmt = insert(AllSystem).values(**system_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["country", "system"],
                set_={
                    "destroyed": stmt.excluded.destroyed,
                    "abandoned": stmt.excluded.abandoned,
                    "captured": stmt.excluded.captured,
                    "damaged": stmt.excluded.damaged,
                    "total": stmt.excluded.total,
                },
            )
            self.db.execute(stmt)

        self.db.commit()
