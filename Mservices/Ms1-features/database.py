import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("FEATURES_DB_HOST", "localhost")
DB_PORT = os.getenv("FEATURES_DB_PORT", "5432")
DB_USER = os.getenv("FEATURES_DB_USER", "mlops_user")
DB_PASSWORD = os.getenv("FEATURES_DB_PASSWORD", "mlops_pass")
DB_NAME = os.getenv("FEATURES_DB_NAME", "features_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_engine_with_retry(url: str, retries: int = 10, delay: int = 3):
    for attempt in range(retries):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✅ Conexión a PostgreSQL exitosa")
            return engine
        except Exception as e:
            logger.warning(f"⏳ Intento {attempt+1}/{retries} fallido: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    raise RuntimeError("❌ No se pudo conectar a PostgreSQL tras múltiples intentos")

engine = create_engine_with_retry(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
