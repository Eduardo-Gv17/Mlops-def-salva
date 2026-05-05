from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre      = Column(String(200), nullable=False, unique=True, index=True)
    dominio     = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo      = Column(Boolean, default=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    features = relationship("Feature", back_populates="dataset", cascade="all, delete-orphan")
