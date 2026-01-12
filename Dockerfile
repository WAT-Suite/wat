FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "uv run python scripts/run_migrations.py && uv run uvicorn main:app --host 0.0.0.0 --port 8000"]
