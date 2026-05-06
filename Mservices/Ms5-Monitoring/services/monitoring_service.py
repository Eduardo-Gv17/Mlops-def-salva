"""
Servicio de monitoreo MLOps — 4 queries analíticas via AWS Athena.

Las tablas en Athena son generadas por Glue Crawlers sobre los datos
exportados a S3 (predlogs y modelos).
"""
from aws.athena_client import run_query

# ── Query 1: Data Drift Básico ────────────────────────────────────────────────
QUERY_DATA_DRIFT = """
SELECT
    p.modelo_nombre                                    AS modelo_nombre,
    substr(p.timestamp, 1, 7)                          AS mes,
    AVG(CAST(p.prediccion_output AS DOUBLE))           AS promedio_prediccion,
    COUNT(*)                                           AS total_predicciones
FROM predlogs p
GROUP BY p.modelo_nombre, substr(p.timestamp, 1, 7)
ORDER BY mes DESC, modelo_nombre
LIMIT 100
"""

# ── Query 2: Framework vs Accuracy ───────────────────────────────────────────
QUERY_FRAMEWORK_ACCURACY = """
SELECT
    m.framework,
    COUNT(DISTINCT m.id)              AS total_modelos,
    AVG(CAST(met.valor_metrica AS DOUBLE)) AS promedio_accuracy
FROM modelos m
JOIN metricas met ON m.id = met.modelo_id
WHERE met.tipo_metrica = 'accuracy'
GROUP BY m.framework
ORDER BY promedio_accuracy DESC
"""

# ── Query 3: Predicciones por Dataset ────────────────────────────────────────
QUERY_PREDICTIONS_BY_DATASET = """
SELECT
    p.dataset_origen,
    COUNT(*)                                    AS total_predicciones,
    AVG(CAST(p.prediccion_output AS DOUBLE))    AS promedio_output
FROM predlogs p
GROUP BY p.dataset_origen
ORDER BY total_predicciones DESC
"""

# ── Query 4: Top 5 Modelos última semana ─────────────────────────────────────
QUERY_TOP_MODELS_WEEKLY = """
SELECT
    p.modelo_id,
    p.modelo_nombre,
    COUNT(*)                                    AS total_peticiones,
    AVG(CAST(p.latencia_ms AS DOUBLE))          AS latencia_promedio
FROM predlogs p
WHERE CAST(p.timestamp AS TIMESTAMP) >= date_add('day', -7, current_timestamp)
GROUP BY p.modelo_id, p.modelo_nombre
ORDER BY total_peticiones DESC
LIMIT 5
"""

async def get_data_drift() -> list[dict]:
    return run_query(QUERY_DATA_DRIFT)

async def get_framework_accuracy() -> list[dict]:
    return run_query(QUERY_FRAMEWORK_ACCURACY)

async def get_predictions_by_dataset() -> list[dict]:
    return run_query(QUERY_PREDICTIONS_BY_DATASET)

async def get_top_models_weekly() -> list[dict]:
    return run_query(QUERY_TOP_MODELS_WEEKLY)
