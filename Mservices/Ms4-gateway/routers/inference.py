from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any
from services import inference_service
from clients import models_client, predlogs_client
import httpx

router = APIRouter(prefix="/api/inference", tags=["Inference"])

class PredictRequest(BaseModel):
    modelo_id:     int  = Field(..., example=1, description="ID del modelo en Ms2")
    input_features: dict[str, Any] = Field(
        ...,
        example={
            "edad": 25,
            "ingreso_mensual": 1500.50,
            "num_transacciones": 12,
            "saldo_promedio": 3200.00
        }
    )

class BatchPredictRequest(BaseModel):
    modelo_id: int = Field(..., example=1)
    inputs:    list[dict[str, Any]] = Field(..., min_length=1, max_length=50)

@router.post("/predict", summary="Realizar una predicción con un modelo ML")
async def predict(body: PredictRequest):
    """
    Pipeline completo:
    1. Verifica el modelo en **Ms2**
    2. Calcula la predicción con función sigmoid
    3. Guarda el log en **Ms3**
    4. Retorna el resultado enriquecido
    """
    try:
        result = await inference_service.run_inference(
            modelo_id=body.modelo_id,
            input_features=body.input_features
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Error comunicándose con microservicio: {e}")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="No se puede conectar a Ms2 o Ms3")

@router.post("/batch", summary="Inferencia en batch (hasta 50 predicciones)")
async def batch_predict(body: BatchPredictRequest):
    """
    Ejecuta múltiples predicciones en secuencia para el mismo modelo.
    """
    try:
        results = await inference_service.run_batch_inference(
            modelo_id=body.modelo_id,
            inputs=body.inputs
        )
        total    = len(results)
        exitosos = sum(1 for r in results if r["status"] == "success")
        return {
            "modelo_id": body.modelo_id,
            "total":     total,
            "exitosos":  exitosos,
            "errores":   total - exitosos,
            "results":   results
        }
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="No se puede conectar a Ms2 o Ms3")

@router.get("/health", summary="Health check del gateway y sus dependencias")
async def gateway_health():
    """Verifica el estado del gateway y la conectividad con Ms2 y Ms3."""
    ms2_status = "unknown"
    ms3_status = "unknown"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{__import__('os').getenv('MODELS_SERVICE_URL','http://ms2-models:8002')}/actuator/health")
            ms2_status = "ok" if r.status_code == 200 else "degraded"
    except Exception:
        ms2_status = "unreachable"

    try:
        health = await predlogs_client.check_health()
        ms3_status = health.get("status", "unknown")
    except Exception:
        ms3_status = "unreachable"

    overall = "ok" if ms2_status == "ok" and ms3_status == "ok" else "degraded"
    return {
        "status":    overall,
        "service":   "ms4-gateway",
        "version":   "1.0.0",
        "upstream": {
            "ms2-models":  ms2_status,
            "ms3-predlogs": ms3_status
        }
    }
