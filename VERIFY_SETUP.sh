#!/bin/bash
# verify_setup.sh - Verificar que todo está configurado correctamente

echo "🔍 Verificando instalación del proyecto Rotisería..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar archivos
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 existe"
        return 0
    else
        echo -e "${RED}✗${NC} $1 NO existe"
        return 1
    fi
}

# Función para verificar directorios
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/ existe"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ NO existe"
        return 1
    fi
}

echo "📁 Verificando estructura de carpetas..."
check_dir "backend"
check_dir "frontend"
check_dir ".github/workflows"

echo ""
echo "📄 Verificando archivos de configuración..."
check_file ".env.example"
check_file "docker-compose.yml"
check_file "README.md"
check_file "DEPLOY.md"

echo ""
echo "⚙️  Verificando backend..."
check_dir "backend/app"
check_dir "backend/migrations"
check_dir "backend/tests"
check_file "backend/requirements.txt"
check_file "backend/Dockerfile"
check_file "backend/alembic.ini"

echo ""
echo "⚙️  Verificando frontend..."
check_dir "frontend/src"
check_dir "frontend/public"
check_file "frontend/package.json"
check_file "frontend/vite.config.js"
check_file "frontend/Dockerfile"

echo ""
echo "🔄 Verificando CI/CD..."
check_file ".github/workflows/tests.yml"
check_file ".github/workflows/deploy.yml"

echo ""
echo "📝 Documentación..."
check_file "README.md"
check_file "DEPLOY.md"
check_file "PROJECT_STATUS.md"

echo ""
echo "✅ Verificación completada!"
echo ""
echo "🚀 Para iniciar:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  python -m venv .venv"
echo "  .venv\\Scripts\\Activate.ps1  # Windows"
echo "  pip install -r requirements.txt"
echo "  alembic upgrade head"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Frontend:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "Docker:"
echo "  docker-compose up -d"
echo "  docker-compose exec backend alembic upgrade head"
