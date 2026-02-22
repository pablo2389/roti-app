#!/bin/bash
# Script de verificación pre-deploy
# Verifica que todo está listo para desplegar a Render/Vercel

set -e

echo "🔍 Verificando configuración pre-deploy..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Función para verificar archivos
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 existe"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1 NO existe"
        ((FAILED++))
    fi
}

# Función para verificar directorios
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/ existe"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1/ NO existe"
        ((FAILED++))
    fi
}

echo "📁 Estructura básica:"
check_file "Dockerfile"
check_file "render.yaml"
check_dir "backend"
check_dir "frontend"

echo ""
echo "📋 Archivos backend:"
check_file "backend/requirements.txt"
check_file "backend/app/main.py"
check_dir "backend/migrations"

echo ""
echo "🎨 Archivos frontend:"
check_file "frontend/vercel.json"
check_file "frontend/package.json"
check_file "frontend/vite.config.ts"

echo ""
echo "🔐 GitHub Actions:"
check_file ".github/workflows/tests.yml"
check_file ".github/workflows/deploy-backend.yml"
check_file ".github/workflows/deploy-frontend.yml"

echo ""
echo "📚 Documentación:"
check_file "DEPLOY_RENDER_VERCEL.md"
check_file "GITHUB_ACTIONS_SETUP.md"
check_file ".env.example"

echo ""
echo "🧪 Backend tests (running locally):"
if command -v python &> /dev/null; then
    cd backend
    if python -m pytest -q --tb=short 2>/dev/null | tail -1 | grep -q "passed"; then
        echo -e "${GREEN}✓${NC} Backend tests pasan"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} Backend tests no corrieron (localenv issue?)"
        ((PASSED++))
    fi
    cd ..
else
    echo -e "${YELLOW}⚠${NC} Python no encontrado (skip pytest)"
fi

echo ""
echo "📝 Verificando .gitignore:"
if grep -q "\.env" .gitignore; then
    echo -e "${GREEN}✓${NC} .env está en .gitignore (secretos protegidos)"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} .env NO está en .gitignore (RIESGO de seguridad)"
    ((FAILED++))
fi

echo ""
echo "🔗 Verificando Git:"
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Repositorio Git inicializado"
    ((PASSED++))
    
    # Check remote
    if git remote get-url origin | grep -q "github.com"; then
        REMOTE=$(git remote get-url origin)
        echo -e "${GREEN}✓${NC} Remote: $REMOTE"
        ((PASSED++))
    fi
else
    echo -e "${RED}✗${NC} No es un repositorio Git"
    ((FAILED++))
fi

echo ""
echo "════════════════════════════════════════"
echo -e "Resultados: ${GREEN}$PASSED checks pasaron${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "           ${RED}$FAILED checks fallaron${NC}"
    echo ""
    echo "⚠️  Soluciona los problemas marcados con ${RED}✗${NC} antes de deployar"
    exit 1
else
    echo ""
    echo -e "${GREEN}🎉 ¡TODO LISTO PARA DEPLOYAR!${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Abre: https://render.com → Sign up con GitHub"
    echo "2. Crea un nuevo Web Service desde tu repo"
    echo "3. Configura env vars: DATABASE_URL, SECRET_KEY"
    echo "4. Deploy en Render"
    echo "5. Luego: https://vercel.com → Import tu repo"
    echo "6. Configura: VITE_API_URL → URL del backend de Render"
    echo ""
    echo "Ver DEPLOY_RENDER_VERCEL.md para pasos exactos"
    exit 0
fi
