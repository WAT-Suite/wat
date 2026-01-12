#!/usr/bin/env python3
"""
Migration runner script that executes SQL migrations in order.
"""
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from app.database import settings

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def get_migration_files():
    """Get all migration files sorted by version."""
    migrations_dir = Path(__file__).parent.parent / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))
    return migration_files


def get_applied_migrations(engine):
    """Get list of already applied migrations."""
    with engine.connect() as conn:
        # Create migrations table if it doesn't exist
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
            )
        )
        conn.commit()

        # Get applied migrations
        result = conn.execute(text("SELECT version FROM schema_migrations"))
        return {row[0] for row in result}


def apply_migration(engine, migration_file):
    """Apply a single migration file."""
    version = migration_file.stem
    print(f"Applying migration: {version}")

    with open(migration_file, "r") as f:
        migration_sql = f.read()

    with engine.begin() as conn:
        # Execute migration
        conn.execute(text(migration_sql))

        # Record migration
        conn.execute(
            text(
                "INSERT INTO schema_migrations (version) VALUES (:version) "
                "ON CONFLICT (version) DO NOTHING"
            ),
            {"version": version},
        )

    print(f"✓ Migration {version} applied successfully")


def run_migrations():
    """Run all pending migrations."""
    import time

    print("Starting database migrations...")
    print(f"Database URL: {settings.db_url.replace(settings.postgres_password, '***')}")

    # Retry connection with exponential backoff
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            engine = create_engine(settings.db_url, pool_pre_ping=True)

            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Database connection successful")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"✗ Failed to connect to database after {max_retries} attempts")
                raise

    try:
        applied_migrations = get_applied_migrations(engine)
        migration_files = get_migration_files()

        pending_migrations = [
            f
            for f in migration_files
            if f.stem not in applied_migrations
        ]

        if not pending_migrations:
            print("✓ No pending migrations")
            return

        print(f"Found {len(pending_migrations)} pending migration(s)")

        for migration_file in pending_migrations:
            apply_migration(engine, migration_file)

        print("✓ All migrations completed successfully")

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_migrations()
