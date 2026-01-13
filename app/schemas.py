from pydantic import BaseModel, Field

from app.enums import Countries, EquipmentType, Status


class EquipmentsRequest(BaseModel):
    types: list[EquipmentType] | None = None
    date: list[str] | None = Field(
        None,
        min_length=2,
        max_length=2,
        description="First item is start date, second is end date (YYYY-MM-DD)",
    )


class TotalEquipmentsRequest(BaseModel):
    country: Countries | None = None
    types: list[EquipmentType] | None = None


class SystemsRequest(BaseModel):
    systems: list[str] | None = None
    status: list[Status] | None = None
    date: list[str] | None = Field(
        None,
        min_length=2,
        max_length=2,
        description="First item is start date, second is end date (YYYY-MM-DD)",
    )


class TotalSystemsRequest(BaseModel):
    country: Countries | None = None
    systems: list[str] | None = None


class EquipmentResponse(BaseModel):
    id: int
    country: str
    type: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int
    date: str

    class Config:
        from_attributes = True


class AllEquipmentResponse(BaseModel):
    id: int
    country: str
    type: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int

    class Config:
        from_attributes = True


class SystemResponse(BaseModel):
    id: int
    country: str
    origin: str
    system: str
    status: str
    url: str
    date: str

    class Config:
        from_attributes = True


class AllSystemResponse(BaseModel):
    id: int
    country: str
    system: str
    destroyed: int
    abandoned: int
    captured: int
    damaged: int
    total: int

    class Config:
        from_attributes = True
