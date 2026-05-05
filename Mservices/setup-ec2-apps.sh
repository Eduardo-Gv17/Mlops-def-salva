#!/bin/bash
# ════════════════════════════════════════════════════
#  setup-ec2-apps.sh — MV1 y MV2 (mlops-apps)
#  Instala Docker, clona el repo y levanta los servicios
#  Uso: bash setup-ec2-apps.sh
# ════════════════════════════════════════════════════

set -e
echo "═══════════════════════════════════════"
echo "  MLOps — Setup MV Apps (MV1 / MV2)"
echo "═══════════════════════════════════════"

# 1. Actualizar sistema
echo "[1/6] Actualizando paquetes..."
sudo apt-get update -y && sudo apt-get upgrade -y

# 2. Instalar Docker
echo "[2/6] Instalando Docker..."
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER

# 3. Clonar repositorio
echo "[3/6] Clonando repositorio..."
cd ~
# REEMPLAZA con tu URL de repositorio real
git clone https://github.com/<TU_USUARIO>/<TU_REPO>.git mlops
cd mlops/Mservices

# 4. Crear .env desde .env.example
echo "[4/6] Creando .env..."
cp .env.example .env
echo ""
echo "⚠️  IMPORTANTE: Edita el archivo .env con tus valores reales:"
echo "   nano .env"
echo ""
echo "Valores que debes completar:"
echo "  - IP privada de MV3 (mlops-db-mv3): 172.31.46.140"
echo "  - Passwords de BDs"
echo "  - Credenciales AWS Academy"
echo ""
read -p "¿Ya editaste el .env? (s/n): " confirm
if [ "$confirm" != "s" ]; then
    echo "Por favor edita el .env y vuelve a ejecutar: docker compose -f docker-compose.ec2.yml up -d --build"
    exit 0
fi

# 5. Build y levantar servicios
echo "[5/6] Construyendo y levantando servicios..."
newgrp docker << EOF
docker compose -f docker-compose.ec2.yml up -d --build
EOF

# 6. Verificar
echo "[6/6] Verificando servicios..."
sleep 10
docker compose -f docker-compose.ec2.yml ps

echo ""
echo "✅ Setup completado. Servicios disponibles en:"
echo "   http://$(hostname -I | awk '{print $1}'):8001/docs  (Ms1 Features)"
echo "   http://$(hostname -I | awk '{print $1}'):8002/swagger-ui.html  (Ms2 Models)"
echo "   http://$(hostname -I | awk '{print $1}'):8003/api-docs  (Ms3 PredLogs)"
echo "   http://$(hostname -I | awk '{print $1}'):8004/docs  (Ms4 Gateway)"
echo "   http://$(hostname -I | awk '{print $1}'):8005/docs  (Ms5 Monitoring)"
