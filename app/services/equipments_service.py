from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from app.models import Equipment, AllEquipment
from app.schemas import EquipmentResponse, AllEquipmentResponse
from app.enums import Countries, EquipmentType
from app.scraper import OryxScraper


class EquipmentsService:
    def __init__(self, db: Session):
        self.db = db

    def get_equipments(
        self,
        country: Countries,
        types: Optional[List[EquipmentType]] = None,
        date: Optional[List[str]] = None,
    ) -> List[EquipmentResponse]:
        """Get equipment data with filters."""
        query = self.db.query(Equipment)

        if country != Countries.ALL:
            query = query.filter(Equipment.country.ilike(country.value))

        if types:
            query = query.filter(Equipment.type.in_([t.value for t in types]))

        if date and len(date) == 2:
            start_date = date[0]
            end_date = date[1]
            if start_date > end_date:
                raise ValueError(
                    "Start date should be before end date, please correct"
                )
            query = query.filter(
                and_(Equipment.date >= start_date, Equipment.date <= end_date)
            )

        results = query.all()
        return [EquipmentResponse.model_validate(r) for r in results]

    def get_total_equipments(
        self,
        country: Optional[Countries] = None,
        types: Optional[List[EquipmentType]] = None,
    ) -> List[AllEquipmentResponse]:
        """Get total equipment data with filters."""
        query = self.db.query(AllEquipment)

        if country:
            query = query.filter(AllEquipment.country.ilike(country.value))

        if types:
            query = query.filter(AllEquipment.type.in_([t.value for t in types]))

        results = query.order_by(AllEquipment.country, AllEquipment.type).all()
        return [AllEquipmentResponse.model_validate(r) for r in results]

    def get_equipment_types(self) -> List[dict]:
        """Get distinct equipment types for Ukraine."""
        results = (
            self.db.query(AllEquipment.type)
            .filter(AllEquipment.country.ilike(Countries.UKRAINE.value))
            .distinct()
            .order_by(AllEquipment.type)
            .all()
        )
        return [{"type": r[0]} for r in results]

    def import_equipments(self):
        """Import equipment data from scraper with incremental updates."""
        from sqlalchemy.dialects.postgresql import insert
        from sqlalchemy import text

        with OryxScraper() as scraper:
            data = scraper.scrape_equipments()

        # Use upsert (INSERT ... ON CONFLICT) for incremental updates
        for item in data:
            equipment_data = {
                "country": item.get("country", ""),
                "type": item.get("equipment_type", ""),
                "destroyed": int(item.get("destroyed", 0) or 0),
                "abandoned": int(item.get("abandoned", 0) or 0),
                "captured": int(item.get("captured", 0) or 0),
                "damaged": int(item.get("damaged", 0) or 0),
                "total": int(item.get("type_total", 0) or 0),
                "date": item.get("date_recorded", ""),
            }

            # Use PostgreSQL-specific upsert or fallback to update-or-insert
            stmt = insert(Equipment).values(**equipment_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["country", "type", "date"],
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

    def import_all_equipments(self):
        """Import all equipment totals from scraper with incremental updates."""
        from sqlalchemy.dialects.postgresql import insert

        with OryxScraper() as scraper:
            data = scraper.scrape_all_equipments()

        # Use upsert for incremental updates
        for item in data:
            equipment_data = {
                "country": item.get("country", ""),
                "type": item.get("equipment_type", ""),
                "destroyed": int(item.get("destroyed", 0) or 0),
                "abandoned": int(item.get("abandoned", 0) or 0),
                "captured": int(item.get("captured", 0) or 0),
                "damaged": int(item.get("damaged", 0) or 0),
                "total": int(item.get("type_total", 0) or 0),
            }

            stmt = insert(AllEquipment).values(**equipment_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=["country", "type"],
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
