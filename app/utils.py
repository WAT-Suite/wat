"""
Utility functions for database operations.
"""

from sqlalchemy.orm import Session


def get_dialect_name(db: Session) -> str:
    """Get the database dialect name."""
    return db.bind.dialect.name if hasattr(db, "bind") else "postgresql"


def upsert_equipment(db: Session, equipment_data: dict, model_class):
    """Upsert equipment data (works with both PostgreSQL and SQLite)."""
    dialect = get_dialect_name(db)

    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert

        stmt = insert(model_class).values(**equipment_data)
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
        db.execute(stmt)
    else:
        # SQLite fallback: try to update, if not found, insert
        existing = (
            db.query(model_class)
            .filter(
                model_class.country == equipment_data["country"],
                model_class.type == equipment_data["type"],
                model_class.date == equipment_data["date"],
            )
            .first()
        )

        if existing:
            for key, value in equipment_data.items():
                setattr(existing, key, value)
        else:
            db.add(model_class(**equipment_data))


def upsert_all_equipment(db: Session, equipment_data: dict, model_class):
    """Upsert all equipment data (works with both PostgreSQL and SQLite)."""
    dialect = get_dialect_name(db)

    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert

        stmt = insert(model_class).values(**equipment_data)
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
        db.execute(stmt)
    else:
        # SQLite fallback
        existing = (
            db.query(model_class)
            .filter(
                model_class.country == equipment_data["country"],
                model_class.type == equipment_data["type"],
            )
            .first()
        )

        if existing:
            for key, value in equipment_data.items():
                setattr(existing, key, value)
        else:
            db.add(model_class(**equipment_data))


def upsert_system(db: Session, system_data: dict, model_class):
    """Upsert system data (works with both PostgreSQL and SQLite)."""
    dialect = get_dialect_name(db)

    if dialect == "postgresql":
        from sqlalchemy.dialects.postgresql import insert

        stmt = insert(model_class).values(**system_data)
        if "url" in system_data and "date" in system_data:
            # System model
            stmt = stmt.on_conflict_do_update(
                index_elements=["country", "system", "url", "date"],
                set_={
                    "origin": stmt.excluded.origin,
                    "status": stmt.excluded.status,
                },
            )
        else:
            # AllSystem model
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
        db.execute(stmt)
    else:
        # SQLite fallback
        if "url" in system_data and "date" in system_data:
            # System model
            existing = (
                db.query(model_class)
                .filter(
                    model_class.country == system_data["country"],
                    model_class.system == system_data["system"],
                    model_class.url == system_data["url"],
                    model_class.date == system_data["date"],
                )
                .first()
            )
        else:
            # AllSystem model
            existing = (
                db.query(model_class)
                .filter(
                    model_class.country == system_data["country"],
                    model_class.system == system_data["system"],
                )
                .first()
            )

        if existing:
            for key, value in system_data.items():
                setattr(existing, key, value)
        else:
            db.add(model_class(**system_data))
