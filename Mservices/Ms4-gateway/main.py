from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.inference import router as inference_router

app = FastAPI(
    title="Ms4 — Inference Gateway",
    description=(
        "Orquestador de inferencia MLOps. Recibe predicciones, verifica modelos en **Ms2**, "
        "calcula outputs con función sigmoid y guarda logs en **Ms3**."
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

app.include_router(inference_router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "service": "ms4-gateway", "version": "1.0.0"}

@app.get("/", tags=["Root"])
def root():
    return {
        "service": "Ms4 — Inference Gateway",
        "docs":    "/docs",
        "health":  "/health"
    }
