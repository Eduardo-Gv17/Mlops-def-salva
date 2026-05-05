#!/bin/bash
# ════════════════════════════════════════════════════
#  setup-ec2-db.sh — MV3 (mlops-db-mv3)
#  Instala Docker y levanta las 3 bases de datos
#  Uso: bash setup-ec2-db.sh
# ════════════════════════════════════════════════════

set -e
echo "═══════════════════════════════════════"
echo "  MLOps — Setup MV Bases de Datos (MV3)"
echo "═══════════════════════════════════════"

# 1. Actualizar sistema
echo "[1/5] Actualizando paquetes..."
sudo apt-get update -y && sudo apt-get upgrade -y

# 2. Instalar Docker
echo "[2/5] Instalando Docker..."
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER

# 3. Clonar repositorio
echo "[3/5] Clonando repositorio..."
cd ~
git clone https://github.com/<TU_USUARIO>/<TU_REPO>.git mlops
cd mlops/Mservices

# 4. Crear .env
echo "[4/5] Creando .env..."
cp .env.example .env
echo ""
echo "⚠️  Edita el .env con los passwords de las BDs:"
echo "   nano .env"
echo ""
read -p "¿Ya editaste el .env? (s/n): " confirm
if [ "$confirm" != "s" ]; then
    echo "Edita el .env y ejecuta: docker compose -f docker-compose.ec2-db.yml up -d"
    exit 0
fi

# 5. Levantar BDs
echo "[5/5] Levantando bases de datos..."
newgrp docker << EOF
docker compose -f docker-compose.ec2-db.yml up -d
EOF

sleep 15
docker compose -f docker-compose.ec2-db.yml ps

echo ""
echo "✅ Bases de datos disponibles en:"
echo "   PostgreSQL: 172.31.46.140:5432"
echo "   MySQL:      172.31.46.140:3306"
echo "   MongoDB:    172.31.46.140:27017"
