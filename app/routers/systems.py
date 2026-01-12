from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import (
    SystemsRequest,
    TotalSystemsRequest,
    SystemResponse,
    AllSystemResponse,
)
from app.enums import Countries
from app.services.systems_service import SystemsService

router = APIRouter(prefix="/api/stats", tags=["Systems"])


@router.post(
    "/systems/{country}",
    response_model=List[SystemResponse],
    summary="Get system data by country",
)
def get_systems(
    country: Countries = Path(..., description="Country filter"),
    request: SystemsRequest = None,
    db: Session = Depends(get_db),
):
    """Get system data filtered by country, systems, status, and date range."""
    if country not in Countries:
        raise HTTPException(
            status_code=400,
            detail="Please provide ukraine or russia in parameter",
        )

    service = SystemsService(db)
    try:
        return service.get_systems(
            country=country,
            systems=request.systems if request else None,
            status=request.status if request else None,
            date=request.date if request else None,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/systems",
    response_model=List[AllSystemResponse],
    summary="Get total system data",
)
def get_total_systems(
    request: TotalSystemsRequest = None,
    db: Session = Depends(get_db),
):
    """Get total system data with optional filters."""
    service = SystemsService(db)
    return service.get_total_systems(
        country=request.country if request else None,
        systems=request.systems if request else None,
    )


@router.get(
    "/system-types",
    response_model=List[dict],
    summary="Get system types",
)
def get_system_types(db: Session = Depends(get_db)):
    """Get distinct system types."""
    service = SystemsService(db)
    return service.get_system_types()
