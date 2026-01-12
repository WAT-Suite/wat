from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.equipments_service import EquipmentsService
from app.services.systems_service import SystemsService

router = APIRouter(prefix="/api/import", tags=["Import"])


@router.post("/equipments", summary="Import equipment data")
def import_equipments(
    db: Session = Depends(get_db),
):
    """Trigger import of equipment data from scraper."""
    try:
        service = EquipmentsService(db)
        service.import_equipments()
        return {"message": "Equipment data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.post("/all-equipments", summary="Import all equipment totals")
def import_all_equipments(
    db: Session = Depends(get_db),
):
    """Trigger import of all equipment totals from scraper."""
    try:
        service = EquipmentsService(db)
        service.import_all_equipments()
        return {"message": "All equipment data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.post("/systems", summary="Import system data")
def import_systems(
    db: Session = Depends(get_db),
):
    """Trigger import of system data from scraper."""
    try:
        service = SystemsService(db)
        service.import_systems()
        return {"message": "System data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.post("/all-systems", summary="Import all system totals")
def import_all_systems(
    db: Session = Depends(get_db),
):
    """Trigger import of all system totals from scraper."""
    try:
        service = SystemsService(db)
        service.import_all_systems()
        return {"message": "All system data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.post("/all", summary="Import all data")
def import_all(
    db: Session = Depends(get_db),
):
    """Trigger import of all data from scraper."""
    try:
        equipments_service = EquipmentsService(db)
        systems_service = SystemsService(db)

        equipments_service.import_equipments()
        equipments_service.import_all_equipments()
        systems_service.import_systems()
        systems_service.import_all_systems()

        return {"message": "All data imported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
