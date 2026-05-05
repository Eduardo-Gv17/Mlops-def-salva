from fastapi import APIRouter, HTTPException
from services import monitoring_service

router = APIRouter(prefix="/api/monitoring", tags=["Monitoring"])

@router.get(
    "/data-drift",
    summary="Query 1 — Drift de predicciones por mes y modelo"
)
async def data_drift():
    """
    Promedio de predicciones agrupadas por mes y nombre de modelo.
    Detecta si un modelo está derivando su distribución de salidas.
    """
    try:
        return {"query": "data_drift", "results": await monitoring_service.get_data_drift()}
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Athena timeout")
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")

@router.get(
    "/framework-accuracy",
    summary="Query 2 — Frameworks vs accuracy promedio histórico"
)
async def framework_accuracy():
    """
    Frameworks ML más utilizados cruzados con su promedio de accuracy histórico.
    Requiere que Glue haya crawleado las tablas 'modelos' y 'metricas'.
    """
    try:
        return {"query": "framework_accuracy", "results": await monitoring_service.get_framework_accuracy()}
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Athena timeout")
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")

@router.get(
    "/predictions-by-dataset",
    summary="Query 3 — Cantidad de predicciones por dataset de origen"
)
async def predictions_by_dataset():
    """
    Total de predicciones y output promedio agrupado por dataset de origen.
    """
    try:
        return {"query": "predictions_by_dataset", "results": await monitoring_service.get_predictions_by_dataset()}
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Athena timeout")
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")

@router.get(
    "/top-models-weekly",
    summary="Query 4 — Top 5 modelos con más predicciones en los últimos 7 días"
)
async def top_models_weekly():
    """
    Top 5 modelos con mayor volumen de peticiones en la última semana,
    con latencia promedio.
    """
    try:
        return {"query": "top_models_weekly", "results": await monitoring_service.get_top_models_weekly()}
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Athena timeout")
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {e}")
