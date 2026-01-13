from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums import Countries
from app.schemas import (
    AllEquipmentResponse,
    EquipmentResponse,
    EquipmentsRequest,
    TotalEquipmentsRequest,
)
from app.services.equipments_service import EquipmentsService

router = APIRouter(prefix="/api/stats", tags=["Equipments"])


@router.post(
    "/equipments/{country}",
    response_model=list[EquipmentResponse],
    summary="Get equipment data by country",
)
def get_equipments(
    country: Countries = Path(..., description="Country filter"),
    request: EquipmentsRequest = None,
    db: Session = Depends(get_db),
):
    """Get equipment data filtered by country, types, and date range."""
    if country not in Countries:
        raise HTTPException(
            status_code=400,
            detail="Please provide ukraine or russia as parameter",
        )

    service = EquipmentsService(db)
    try:
        return service.get_equipments(
            country=country,
            types=request.types if request else None,
            date=request.date if request else None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/equipments",
    response_model=list[AllEquipmentResponse],
    summary="Get total equipment data",
)
def get_total_equipments(
    request: TotalEquipmentsRequest = None,
    db: Session = Depends(get_db),
):
    """Get total equipment data with optional filters."""
    service = EquipmentsService(db)
    return service.get_total_equipments(
        country=request.country if request else None,
        types=request.types if request else None,
    )


@router.get(
    "/equipment-types",
    response_model=list[dict],
    summary="Get equipment types",
)
def get_equipment_types(db: Session = Depends(get_db)):
    """Get distinct equipment types for Ukraine."""
    service = EquipmentsService(db)
    return service.get_equipment_types()
