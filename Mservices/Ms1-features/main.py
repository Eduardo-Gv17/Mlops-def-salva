from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import datasets, features

# Crear tablas al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ms1 — Features Service",
    description="Microservicio de gestión de datasets y features para MLOps. Gestiona los datasets de entrenamiento y sus variables (features).",
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

app.include_router(datasets.router)
app.include_router(features.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "ms1-features", "version": "1.0.0"}

@app.get("/", tags=["Root"])
def root():
    return {
        "service": "Ms1 — Features Service",
        "docs": "/docs",
        "health": "/health"
    }
