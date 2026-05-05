import os
import httpx
from dotenv import load_dotenv

load_dotenv()

MODELS_URL = os.getenv("MODELS_SERVICE_URL", "http://ms2-models:8002")

async def get_modelo(modelo_id: int) -> dict | None:
    """Verifica que el modelo existe y está activo en Ms2."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(f"{MODELS_URL}/api/modelos/{modelo_id}")
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()
