# MLOps Lite — Backend Microservicios

Sistema de monitoreo MLOps con 5 microservicios en Docker, desplegados en AWS EC2 con balanceador de carga.

## Arquitectura

```
Internet → API Gateway (HTTPS) → ALB (mlops-alb, privado)
                                      ├── MV1 (mlops-apps-vm1) → 5 microservicios
                                      └── MV2 (mlops-app-vm2)  → 5 microservicios (réplica)
                                               ↓ (IP privada)
                                          MV3 (mlops-db-mv3)
                                          ├── PostgreSQL :5432
                                          ├── MySQL      :3306
                                          └── MongoDB    :27017
```

## Microservicios

| Servicio | Tecnología | Puerto | BD |
|---|---|---|---|
| Ms1-features | Python + FastAPI | 8001 | PostgreSQL |
| Ms2-models | Java + Spring Boot | 8002 | MySQL |
| Ms3-predlogs | Node.js + Express | 8003 | MongoDB |
| Ms4-gateway | Python + FastAPI | 8004 | — (consume Ms2+Ms3) |
| Ms5-Monitoring | Python + FastAPI | 8005 | — (AWS Athena) |

## Quickstart local

```bash
# 1. Clonar
git clone <URL_REPO>
cd Mlops/Mservices

# 2. Configurar variables
cp .env.example .env
nano .env   # rellenar passwords y credenciales AWS

# 3. Levantar todo (dev local con BDs incluidas)
docker compose up -d --build

# 4. Verificar
docker compose ps   # todos deben ser healthy

# 5. Ejecutar seeds (una sola vez)
docker compose exec ms1-features python scripts/seed_features.py
docker compose exec ms3-predlogs node scripts/seed_predlogs.js
# Ms2 se auto-seedea al arrancar (DataSeeder.java)

# 6. Swagger UIs
# Ms1: http://localhost:8001/docs
# Ms2: http://localhost:8002/swagger-ui.html
# Ms3: http://localhost:8003/api-docs
# Ms4: http://localhost:8004/docs
# Ms5: http://localhost:8005/docs
```

## Deploy en AWS EC2

### MV3 — Bases de datos
```bash
bash setup-ec2-db.sh
# Levantar: docker compose -f docker-compose.ec2-db.yml up -d
```

### MV1 y MV2 — Microservicios
```bash
bash setup-ec2-apps.sh
# El .env debe apuntar a la IP privada de MV3: 172.31.46.140
```

## Variables de entorno clave

| Variable | Descripción |
|---|---|
| `FEATURES_DB_HOST` | IP privada de MV3 |
| `MODELS_DB_HOST` | IP privada de MV3 |
| `PREDLOGS_DB_HOST` | IP privada de MV3 |
| `AWS_ACCESS_KEY_ID` | Credencial AWS Academy |
| `ATHENA_OUTPUT_LOCATION` | `s3://mlops-analytics-oswaldoaqm/athena-results/` |

## Datos de prueba
- **Ms1**: 50 datasets × 400 features = **20,000 features**
- **Ms2**: 500 modelos × 40 métricas = **20,000 métricas** (auto-seed al arrancar)
- **Ms3**: **20,000 prediction logs** (distribuidos en últimos 90 días)
