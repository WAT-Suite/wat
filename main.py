"""
FastAPI application for War Track Dashboard API.
"""

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routers import equipments, import_router, systems
from app.services.equipments_service import EquipmentsService
from app.services.systems_service import SystemsService

# Initialize scheduler
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifetime events for the application."""
    # Startup
    print("Starting War Track Dashboard API...")

    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)

    # Schedule daily imports at 1 PM
    def import_all_data():
        """Import all data from scraper."""
        db = SessionLocal()
        try:
            equipments_service = EquipmentsService(db)
            systems_service = SystemsService(db)

            print("Running scheduled import...")
            equipments_service.import_equipments()
            equipments_service.import_all_equipments()
            systems_service.import_systems()
            systems_service.import_all_systems()
            print("Scheduled import completed")
        except Exception as e:
            print(f"Error during scheduled import: {e}")
        finally:
            db.close()

    # Schedule daily import at 1 PM
    scheduler.add_job(
        import_all_data,
        trigger=CronTrigger(hour=13, minute=0),
        id="daily_import",
        name="Daily data import at 1 PM",
        replace_existing=True,
    )
    scheduler.start()
    print("Scheduler started - daily imports scheduled at 1 PM")

    yield

    # Shutdown
    print("Shutting down War Track Dashboard API...")
    scheduler.shutdown()


app = FastAPI(
    title="War Track Dashboard API",
    description="API for tracking war equipment and systems",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(equipments.router)
app.include_router(systems.router)
app.include_router(import_router.router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint."""
    return {
        "message": "War Track Dashboard API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
