from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from models.feature import Feature
from models.dataset import Dataset
from schemas.feature import FeatureCreate, FeatureUpdate, FeatureResponse, FeaturePage

router = APIRouter(prefix="/api/features", tags=["Features"])

@router.get("", response_model=FeaturePage, summary="Listar features paginadas")
def list_features(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    tipo_dato: str | None = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Feature)
    if tipo_dato:
        query = query.filter(Feature.tipo_dato == tipo_dato)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}

@router.get("/dataset/{dataset_id}", response_model=FeaturePage, summary="Features de un dataset")
def get_features_by_dataset(
    dataset_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} no encontrado")
    query = db.query(Feature).filter(Feature.dataset_id == dataset_id)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}

@router.get("/{feature_id}", response_model=FeatureResponse, summary="Obtener feature por ID")
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {feature_id} no encontrada")
    return feature

@router.post("", response_model=FeatureResponse, status_code=status.HTTP_201_CREATED, summary="Crear feature")
def create_feature(body: FeatureCreate, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == body.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset {body.dataset_id} no existe")
    feature = Feature(**body.model_dump())
    db.add(feature)
    db.commit()
    db.refresh(feature)
    return feature

@router.put("/{feature_id}", response_model=FeatureResponse, summary="Actualizar feature")
def update_feature(feature_id: int, body: FeatureUpdate, db: Session = Depends(get_db)):
    feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {feature_id} no encontrada")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(feature, field, value)
    db.commit()
    db.refresh(feature)
    return feature

@router.delete("/{feature_id}", summary="Eliminar feature")
def delete_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {feature_id} no encontrada")
    db.delete(feature)
    db.commit()
    return {"message": f"Feature {feature_id} eliminada correctamente"}
