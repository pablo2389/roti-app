# Rotisería - Full Stack Professional Project

Sistema de gestión integral para rotisería con soporte para productos, ventas, análisis de datos y generación de contenido con IA.

## 🎯 Características

### Backend (FastAPI)
- ✅ API RESTful completa con validación Pydantic V2
- ✅ Gestión de productos con imágenes
- ✅ Registro de ventas con control automático de stock
- ✅ Dashboard con estadísticas en tiempo real
- ✅ Generación de PDFs de menú con ReportLab
- ✅ Integración con IA (OpenAI, Anthropic, Cohere)
- ✅ Migraciones de base de datos con Alembic
- ✅ Soporte SQLite (desarrollo) y PostgreSQL (producción)

### Frontend (React + Vite)
- ✅ Interfaz responsive con Tailwind CSS
- ✅ Progressive Web App (PWA)
- ✅ Dashboards visuales con Recharts
- ✅ Carga de imágenes con preview
- ✅ Soporte offline con service worker

### DevOps
- ✅ Docker y docker-compose
- ✅ GitHub Actions CI/CD
- ✅ Tests con pytest
- ✅ Linting y code quality

## 🚀 Quick Start

### Backend (Windows)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## 🧪 Tests
```bash
cd backend
pytest tests/ -v
```

## 📊 API Endpoints

**Productos**
- GET/POST `/productos`
- GET/PUT/DELETE `/productos/{id}`
- GET `/productos/stock-critico`

**Ventas**
- GET/POST `/ventas`

**Dashboard**
- GET `/dashboard/resumen`
- POST `/dashboard/generar-pdf-menu`
- POST `/dashboard/generar-contenido-ia`

## 🔧 Environment

Copy `.env.example` to `.env` and configure:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/rotiseria
OPENAI_API_KEY=sk-...
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
```

## 📁 Project Structure

```
rotiseria/
├── backend/          # FastAPI + SQLAlchemy
├── frontend/         # React + Vite
├── .github/workflows # CI/CD
├── docker-compose.yml
├── .env.example
└── DEPLOY.md        # Production guide
```

## 📝 Deployment

See [DEPLOY.md](DEPLOY.md) for production setup.

## 📞 Support

GitHub Issues for bugs and features.

---
**Version:** 1.0.0 | **Status:** Production Ready

