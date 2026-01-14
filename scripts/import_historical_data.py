#!/usr/bin/env python3
"""
Migration script to import all historical data from Oryx using oryx-wat-scraper.
This script will import all available historical data regardless of what's already in the database.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.services.equipments_service import EquipmentsService
from app.services.systems_service import SystemsService


def import_historical_data():
    """Import all historical data from Oryx scraper."""
    print("=" * 60)
    print("Starting historical data import from Oryx...")
    print("=" * 60)

    db = SessionLocal()
    try:
        equipments_service = EquipmentsService(db)
        systems_service = SystemsService(db)

        # Import all equipment data (import_all=True)
        print("\n[1/4] Importing historical equipment data...")
        equipments_service.import_equipments(import_all=True)

        # Import all equipment totals
        print("\n[2/4] Importing historical equipment totals...")
        equipments_service.import_all_equipments()

        # Import all system data (import_all=True)
        print("\n[3/4] Importing historical system data...")
        systems_service.import_systems(import_all=True)

        # Import all system totals
        print("\n[4/4] Importing historical system totals...")
        systems_service.import_all_systems()

        print("\n" + "=" * 60)
        print("✓ Historical data import completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during historical data import: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        import_historical_data()
    except Exception as e:
        print(f"\n✗ Failed to import historical data: {e}")
        sys.exit(1)
