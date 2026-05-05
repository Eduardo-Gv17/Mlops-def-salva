import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PREDLOGS_URL = os.getenv("PREDLOGS_SERVICE_URL", "http://ms3-predlogs:8003")

async def save_predlog(payload: dict) -> dict:
    """Guarda un log de predicción en Ms3."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{PREDLOGS_URL}/api/predlogs", json=payload)
        r.raise_for_status()
        return r.json()

async def check_health() -> dict:
    """Verifica salud de Ms3."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{PREDLOGS_URL}/health")
        r.raise_for_status()
        return r.json()
