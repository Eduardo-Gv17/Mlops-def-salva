from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.feature import TipoDatoEnum

class FeatureBase(BaseModel):
    nombre_variable: str = Field(..., min_length=1, max_length=200, example="edad_cliente")
    tipo_dato: TipoDatoEnum = Field(..., example="float64")
    descripcion: Optional[str] = Field(None, example="Edad del cliente en años")
    es_categorica: bool = False
    dataset_id: int = Field(..., example=1)

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(BaseModel):
    nombre_variable: Optional[str] = None
    tipo_dato: Optional[TipoDatoEnum] = None
    descripcion: Optional[str] = None
    es_categorica: Optional[bool] = None

class FeatureResponse(FeatureBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FeaturePage(BaseModel):
    total: int
    page: int
    size: int
    items: list[FeatureResponse]
