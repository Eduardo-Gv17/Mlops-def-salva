"""
Seed script: 50 datasets × 400 features = 20,000 registros
Uso: docker compose exec ms1-features python scripts/seed_features.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from faker import Faker
from database import SessionLocal, engine, Base
from models.dataset import Dataset
from models.feature import Feature, TipoDatoEnum

fake = Faker('es_ES')

DOMINIOS = [
    "finanzas", "salud", "retail", "telecomunicaciones", "manufactura",
    "energia", "transporte", "educacion", "seguros", "e-commerce",
    "redes_sociales", "iot", "ciberseguridad", "recursos_humanos", "marketing"
]

TIPO_DATOS = list(TipoDatoEnum)

PREFIJOS_FEATURE = [
    "edad", "ingreso", "saldo", "num_transacciones", "score_credito",
    "dias_cliente", "promedio_compra", "max_compra", "min_compra", "num_productos",
    "tasa_abandono", "frecuencia_login", "num_quejas", "dias_inactivo", "nivel_riesgo",
    "porcentaje_pago", "deuda_total", "limite_credito", "ratio_deuda", "num_cuentas",
    "temperatura", "presion", "humedad", "velocidad", "aceleracion",
    "voltaje", "corriente", "potencia", "consumo", "eficiencia",
    "latencia", "throughput", "error_rate", "uptime", "cpu_usage",
    "mem_usage", "disk_io", "network_io", "req_per_sec", "response_time"
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(Dataset).count()
        if existing > 0:
            print(f"⚠️  Ya existen {existing} datasets. Saltando seed.")
            return

        print("🌱 Iniciando seed de Ms1-features...")

        # Crear 50 datasets
        datasets_creados = []
        for i in range(1, 51):
            dominio = random.choice(DOMINIOS)
            nombre = f"{dominio}_dataset_{i:03d}_{fake.year()}"
            dataset = Dataset(
                nombre=nombre,
                dominio=dominio,
                descripcion=f"Dataset de {dominio} - {fake.bs()}. Contiene datos históricos para modelos predictivos.",
                activo=random.choice([True, True, True, False])  # 75% activos
            )
            db.add(dataset)

        db.flush()
        datasets_creados = db.query(Dataset).all()
        print(f"✅ {len(datasets_creados)} datasets creados")

        # Crear 400 features por dataset = 20,000 total
        total_features = 0
        BATCH_SIZE = 500

        for dataset in datasets_creados:
            features_batch = []
            for j in range(400):
                prefijo = random.choice(PREFIJOS_FEATURE)
                sufijo = fake.word().lower().replace(" ", "_")
                nombre_var = f"{prefijo}_{sufijo}_{j:03d}"
                tipo = random.choice(TIPO_DATOS)
                feature = Feature(
                    nombre_variable=nombre_var,
                    tipo_dato=tipo,
                    descripcion=f"Variable {nombre_var}: {fake.sentence(nb_words=8)}",
                    es_categorica=(tipo == TipoDatoEnum.string or random.random() < 0.2),
                    dataset_id=dataset.id
                )
                features_batch.append(feature)

            db.bulk_save_objects(features_batch)
            total_features += len(features_batch)

            if total_features % 2000 == 0:
                db.commit()
                print(f"  → {total_features} features insertadas...")

        db.commit()
        print(f"\n🎉 Seed completado:")
        print(f"   📦 Datasets:  {len(datasets_creados)}")
        print(f"   🔢 Features:  {total_features}")
        print(f"   Total BD:    {total_features + len(datasets_creados)} registros")

    except Exception as e:
        db.rollback()
        print(f"❌ Error en seed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
