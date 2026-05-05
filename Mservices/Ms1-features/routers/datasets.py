from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from models.dataset import Dataset
from schemas.dataset import DatasetCreate, DatasetUpdate, DatasetResponse, DatasetPage

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])

@router.get("", response_model=DatasetPage, summary="Listar datasets paginados")
def list_datasets(
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Registros por página"),
    activo: bool | None = Query(None, description="Filtrar por activo/inactivo"),
    dominio: str | None = Query(None, description="Filtrar por dominio"),
    db: Session = Depends(get_db)
):
    query = db.query(Dataset)
    if activo is not None:
        query = query.filter(Dataset.activo == activo)
    if dominio:
        query = query.filter(Dataset.dominio.ilike(f"%{dominio}%"))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": items}

@router.get("/{dataset_id}", response_model=DatasetResponse, summary="Obtener dataset por ID")
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} no encontrado")
    return dataset

@router.post("", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED, summary="Crear dataset")
def create_dataset(body: DatasetCreate, db: Session = Depends(get_db)):
    existing = db.query(Dataset).filter(Dataset.nombre == body.nombre).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Ya existe un dataset con nombre '{body.nombre}'")
    dataset = Dataset(**body.model_dump())
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

@router.put("/{dataset_id}", response_model=DatasetResponse, summary="Actualizar dataset")
def update_dataset(dataset_id: int, body: DatasetUpdate, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} no encontrado")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(dataset, field, value)
    db.commit()
    db.refresh(dataset)
    return dataset

@router.delete("/{dataset_id}", summary="Soft delete de dataset")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} no encontrado")
    dataset.activo = False
    db.commit()
    return {"message": f"Dataset {dataset_id} desactivado correctamente"}
