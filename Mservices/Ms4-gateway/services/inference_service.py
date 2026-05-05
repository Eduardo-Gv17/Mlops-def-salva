import math
import time
from clients import models_client, predlogs_client

def sigmoid(x: float) -> float:
    """Función sigmoid: transforma cualquier número real a [0, 1]."""
    return 1.0 / (1.0 + math.exp(-x))

def compute_prediction(input_features: dict) -> tuple[float, str]:
    """
    Calcula una predicción simulada usando sigmoid sobre los features numéricos.
    Retorna (output: float 0-1, label: str).
    """
    numeric_vals = []
    for v in input_features.values():
        if isinstance(v, (int, float)):
            numeric_vals.append(float(v))

    if not numeric_vals:
        raw = 0.0
    else:
        # Normalizar: suma ponderada de los valores estandarizados
        mean_val = sum(numeric_vals) / len(numeric_vals)
        std_val  = math.sqrt(sum((x - mean_val) ** 2 for x in numeric_vals) / len(numeric_vals)) or 1.0
        normalized = [(x - mean_val) / std_val for x in numeric_vals]
        # Pesos decrecientes para darle más peso a los primeros features
        weights = [1 / (i + 1) for i in range(len(normalized))]
        raw = sum(w * v for w, v in zip(weights, normalized))

    output = round(sigmoid(raw), 6)
    label  = "churn" if output >= 0.5 else "no_churn"
    return output, label

async def run_inference(modelo_id: int, input_features: dict) -> dict:
    """
    Pipeline completo de inferencia:
    1. Verificar modelo en Ms2
    2. Calcular predicción
    3. Guardar log en Ms3
    4. Retornar resultado enriquecido
    """
    start_time = time.monotonic()

    # 1. Verificar modelo en Ms2
    modelo = await models_client.get_modelo(modelo_id)
    if modelo is None:
        raise ValueError(f"Modelo {modelo_id} no encontrado en Ms2")
    if not modelo.get("activo", True):
        raise ValueError(f"Modelo {modelo_id} está inactivo")

    # 2. Calcular predicción
    output, label = compute_prediction(input_features)

    latencia_ms = int((time.monotonic() - start_time) * 1000)

    # 3. Guardar log en Ms3
    log_payload = {
        "modelo_id":        modelo_id,
        "modelo_nombre":    modelo.get("nombre", "unknown"),
        "dataset_origen":   "gateway_inference",
        "input_features":   input_features,
        "prediccion_output": output,
        "prediccion_label": label,
        "latencia_ms":      latencia_ms,
        "estado":           "success"
    }
    saved_log = await predlogs_client.save_predlog(log_payload)

    return {
        "modelo": {
            "id":        modelo.get("id"),
            "nombre":    modelo.get("nombre"),
            "framework": modelo.get("framework"),
            "version":   modelo.get("version")
        },
        "prediccion": {
            "output": output,
            "label":  label
        },
        "latencia_ms": latencia_ms,
        "log_id":      str(saved_log.get("_id", ""))
    }

async def run_batch_inference(modelo_id: int, inputs: list[dict]) -> list[dict]:
    """Inferencia en batch: aplica run_inference a cada set de features."""
    results = []
    for features in inputs:
        try:
            result = await run_inference(modelo_id, features)
            results.append({"status": "success", "result": result})
        except Exception as e:
            results.append({"status": "error", "error": str(e), "input": features})
    return results
