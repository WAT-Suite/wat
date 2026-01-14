# War Assets Tracker API

FastAPI-based API server for tracking war equipment and systems data, with automated data scraping from Oryx.

## Features

- FastAPI with async support
- PostgreSQL database with SQL migrations
- Automated data scraping from Oryx
- Scheduled daily imports (1 PM)
- RESTful API endpoints matching the NestJS version
- Docker Compose setup for easy development

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose

### Installation

1. Install dependencies using uv:
```bash
uv sync
```

2. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update `.env` with your database credentials if needed.

4. Start the database and application:
```bash
docker-compose up -d
```

The application will:
- Run database migrations on startup
- Start the FastAPI server on port 8000
- Schedule daily data imports at 1 PM

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Equipments
- `POST /api/stats/equipments/{country}` - Get equipment data by country
  - Query filters: `types` (array), `date` (array with [start_date, end_date])
- `POST /api/stats/equipments` - Get total equipment data
  - Query filters: `country` (string), `types` (array)
- `GET /api/stats/equipment-types` - Get equipment types

### Systems
- `POST /api/stats/systems/{country}` - Get system data by country
  - Query filters: `systems` (array), `status` (array), `date` (array with [start_date, end_date])
- `POST /api/stats/systems` - Get total system data
  - Query filters: `country` (string), `systems` (array)
- `GET /api/stats/system-types` - Get system types

### Import
- `POST /api/import/equipments` - Manually trigger equipment import (new dates only)
- `POST /api/import/all-equipments` - Manually trigger all equipment totals import
- `POST /api/import/systems` - Manually trigger system import (new dates only)
- `POST /api/import/all-systems` - Manually trigger all system totals import
- `POST /api/import/all` - Import all new data (new dates only)
- `POST /api/import/historical` - Import all historical data (ignores existing dates)

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. Install and set up:

```bash
# Install pre-commit
uv sync --dev

# Install git hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

The hooks will automatically run on `git commit` and check:
- Code formatting (black)
- Linting (ruff)
- Type checking (mypy)
- YAML/JSON/TOML validation
- Trailing whitespace and end-of-file fixes

### Running migrations manually

```bash
python scripts/run_migrations.py
```

### Importing historical data

To import all historical data from Oryx (first-time setup):

```bash
python scripts/import_historical_data.py
```

This script will:
- Import all available historical equipment data
- Import all equipment totals
- Import all available historical system data
- Import all system totals

**Note**: Regular imports (via API or scheduled) only import new dates that don't exist in the database. Use the historical import script for initial data population.

### Running the server locally (without Docker)

```bash
# Activate virtual environment
source .venv/bin/activate  # or `uv run` prefix commands

# Run migrations
python scripts/run_migrations.py

# Start server
uvicorn main:app --reload
```

### Running tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=term-missing

# Run only unit tests
uv run pytest -m "not integration"
```

### Running CI checks locally

```bash
# Format code
uv run black --check .

# Lint code
uv run ruff check .

# Type check
uv run mypy app --ignore-missing-imports

# Run tests
uv run pytest --cov=app --cov-report=xml --cov-report=term-missing -m "not integration"
```

## Project Structure

```
war-assets-tracker/
├── app/
│   ├── __init__.py
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── enums.py             # Enumerations
│   ├── scraper.py           # Oryx scraper service
│   ├── routers/             # API routes
│   │   ├── equipments.py
│   │   ├── systems.py
│   │   └── import.py
│   └── services/            # Business logic
│       ├── equipments_service.py
│       └── systems_service.py
├── migrations/              # SQL migration files
│   └── 001_initial_schema.sql
├── scripts/
│   ├── run_migrations.py         # Migration runner
│   └── import_historical_data.py # Historical data import script
├── main.py                  # FastAPI application
├── pyproject.toml           # Project dependencies
├── docker-compose.yml       # Docker setup
└── Dockerfile              # Application container
```

## Data Updates

The system uses **incremental updates** (upserts) instead of full data replacement:
- ✅ **New records are inserted** when they don't exist
- ✅ **Existing records are updated** based on unique constraints
- ✅ **No data deletion** - only updates changed records
- ✅ **Smart date filtering** - only imports data for dates that don't exist in the database
- ✅ **Live data scraping** - uses `oryx-wat-scraper` library to scrape directly from Oryx blog
- ✅ **Efficient updates** - scheduled imports only process new dates, not existing ones

Unique constraints for upsert operations:
- `Equipment`: (country, type, date) - Updates existing records for same country/type/date
- `AllEquipment`: (country, type) - Updates totals for same country/type
- `System`: (country, system, url, date) - Updates specific system instances
- `AllSystem`: (country, system) - Updates totals for same country/system

## Query Filters

All endpoints support filtering:

### Date Filters
- ✅ **Fully supported** on equipment and system endpoints
- Format: `["YYYY-MM-DD", "YYYY-MM-DD"]` (start date, end date)
- Example: `{"date": ["2023-01-01", "2023-12-31"]}`
- Available on:
  - `POST /api/stats/equipments/{country}` - Filter equipment by date range
  - `POST /api/stats/systems/{country}` - Filter systems by date range
- Validation: Start date must be before or equal to end date

### Other Filters
- **Equipment types**: Filter by equipment type (e.g., "Tanks", "Aircraft")
- **Systems**: Filter by system name
- **Status**: Filter by status (destroyed, abandoned, captured, damaged)
- **Country**: Filter by country (ukraine, russia, all)

## Notes

- Data is automatically imported daily at 1 PM via APScheduler
- Migrations run automatically on container startup
- The scraper uses `oryx-wat-scraper` library to scrape directly from the Oryx blog
- All endpoints match the NestJS API structure for compatibility
- Updates are incremental - only new dates are imported (existing dates are skipped)
- Use `scripts/import_historical_data.py` for initial data population
- Regular imports only fetch new data, making them fast and efficient
