from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.enums import Countries, EquipmentType
from app.models import AllEquipment, Equipment
from app.schemas import AllEquipmentResponse, EquipmentResponse
from app.scraper import OryxScraper


class EquipmentsService:
    def __init__(self, db: Session):
        self.db = db

    def get_equipments(
        self,
        country: Countries,
        types: list[EquipmentType] | None = None,
        date: list[str] | None = None,
    ) -> list[EquipmentResponse]:
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
                raise ValueError("Start date should be before end date, please correct")
            query = query.filter(and_(Equipment.date >= start_date, Equipment.date <= end_date))

        results = query.all()
        return [EquipmentResponse.model_validate(r) for r in results]

    def get_total_equipments(
        self,
        country: Countries | None = None,
        types: list[EquipmentType] | None = None,
    ) -> list[AllEquipmentResponse]:
        """Get total equipment data with filters."""
        query = self.db.query(AllEquipment)

        if country:
            query = query.filter(AllEquipment.country.ilike(country.value))

        if types:
            query = query.filter(AllEquipment.type.in_([t.value for t in types]))

        results = query.order_by(AllEquipment.country, AllEquipment.type).all()
        return [AllEquipmentResponse.model_validate(r) for r in results]

    def get_equipment_types(self) -> list[dict]:
        """Get distinct equipment types for all countries."""
        results = self.db.query(AllEquipment.type).distinct().order_by(AllEquipment.type).all()
        return [{"type": r[0]} for r in results]

    def import_equipments(self, import_all: bool = False):
        """
        Import equipment data from scraper with incremental updates.
        Only imports data for dates that don't exist in the database.

        Args:
            import_all: If True, import all data regardless of existing dates.
                       If False, only import new dates (default).
        """
        from app.utils import upsert_equipment

        # Get existing dates from database
        existing_dates = set()
        if not import_all:
            existing_records = self.db.query(Equipment.date).distinct().all()
            existing_dates = {record[0] for record in existing_records}

        with OryxScraper() as scraper:
            data = scraper.scrape_equipments()

        # Filter out dates we already have (unless import_all is True)
        new_data = []
        if import_all:
            new_data = data
        else:
            for item in data:
                date_recorded = item.get("date_recorded", "")
                if date_recorded and date_recorded not in existing_dates:
                    new_data.append(item)

        if not new_data:
            print(f"No new equipment data to import (existing dates: {len(existing_dates)})")
            return

        print(f"Importing {len(new_data)} new equipment records...")

        # Use upsert for incremental updates
        for item in new_data:
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

            upsert_equipment(self.db, equipment_data, Equipment)

        self.db.commit()
        print(f"✓ Successfully imported {len(new_data)} equipment records")

    def import_all_equipments(self):
        """Import all equipment totals from scraper with incremental updates."""
        from app.utils import upsert_all_equipment

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

            upsert_all_equipment(self.db, equipment_data, AllEquipment)

        self.db.commit()
