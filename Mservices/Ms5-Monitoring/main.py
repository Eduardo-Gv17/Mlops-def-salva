from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.monitoring import router as monitoring_router
from aws.athena_client import check_connectivity

app = FastAPI(
    title="Ms5 — Monitoring Service",
    description=(
        "Microservicio analítico MLOps. Ejecuta **4 queries** sobre AWS Athena para monitorear "
        "el rendimiento de los modelos: drift de predicciones, accuracy por framework, "
        "predicciones por dataset y top modelos semanales."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(monitoring_router)

@app.get("/health", tags=["Health"])
def health():
    athena_ok = check_connectivity()
    return {
        "status":  "ok" if athena_ok else "degraded",
        "service": "ms5-monitoring",
        "version": "1.0.0",
        "athena":  "connected" if athena_ok else "unreachable"
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "service":   "Ms5 — Monitoring Service",
        "docs":      "/docs",
        "health":    "/health",
        "endpoints": [
            "/api/monitoring/data-drift",
            "/api/monitoring/framework-accuracy",
            "/api/monitoring/predictions-by-dataset",
            "/api/monitoring/top-models-weekly"
        ]
    }
