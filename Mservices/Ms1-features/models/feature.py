from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class TipoDatoEnum(str, enum.Enum):
    float64  = "float64"
    int64    = "int64"
    string   = "string"
    bool     = "bool"
    datetime = "datetime"

class Feature(Base):
    __tablename__ = "features"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_variable = Column(String(200), nullable=False, index=True)
    tipo_dato     = Column(Enum(TipoDatoEnum), nullable=False)
    descripcion   = Column(Text, nullable=True)
    es_categorica = Column(Boolean, default=False)
    dataset_id    = Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    dataset = relationship("Dataset", back_populates="features")
