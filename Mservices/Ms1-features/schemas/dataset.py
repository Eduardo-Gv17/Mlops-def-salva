from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DatasetBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=200, example="customer_churn_2024")
    dominio: str = Field(..., min_length=1, max_length=100, example="finanzas")
    descripcion: Optional[str] = Field(None, example="Dataset de churn bancario 2024")
    activo: bool = True

class DatasetCreate(DatasetBase):
    pass

class DatasetUpdate(BaseModel):
    nombre: Optional[str] = None
    dominio: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class DatasetResponse(DatasetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DatasetPage(BaseModel):
    total: int
    page: int
    size: int
    items: list[DatasetResponse]
