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
- ✅ Autenticación JWT y multi-tenant ready

### Frontend (React + Vite)
- ✅ Interfaz responsive con Tailwind CSS
- ✅ Progressive Web App (PWA)
- ✅ Dashboards visuales con Recharts
- ✅ Carga de imágenes con preview
- ✅ Soporte offline con service worker
- ✅ Consumidor de API con axios

### DevOps
- ✅ Docker y docker-compose
- ✅ GitHub Actions CI/CD (tests, deploy)
- ✅ Render + Vercel ready
- ✅ Tests con pytest (24✅ passing)
- ✅ Linting y code quality

## 🚀 Deployment Rápido (Opción 1)

**⏱️ 10-15 minutos para estar en producción:**

1. **Backend en Render**: https://render.com → New Web Service → Connect repo → Done
2. **Frontend en Vercel**: https://vercel.com → Import repo → Done

Ver: **[DEPLOY_RENDER_VERCEL.md](DEPLOY_RENDER_VERCEL.md)** para pasos exactos.

Alternativamente, **CLI en local**: [DEPLOY_RENDER_VERCEL.md#opción-3](DEPLOY_RENDER_VERCEL.md)

## 🔧 Quick Start Local

### Backend (Windows)
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Accede a: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Accede a: `http://localhost:5173`

### Docker (completo)
```bash
docker-compose up --build
docker-compose exec backend alembic upgrade head
```

Backend: `http://localhost:8000/docs`
Frontend: `http://localhost:5173`

## 🧪 Tests

```bash
cd backend
pytest tests/ -v
# Todos: 24 ✅ passing
```

## 🔐 Autenticación

Sistema JWT incluido:

```bash
# Registrar
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"secret"}'

# Usar token
curl -X GET http://localhost:8000/productos \
  -H "Authorization: Bearer {token}"
```

## 📊 API Endpoints

Accede a **Interactive Docs**: `http://localhost:8000/docs`

**Autenticación**
- POST `/auth/register` - Crear cuenta
- POST `/auth/login` - Obtener token
- GET `/auth/me` - Perfil actual

**Productos**
- GET/POST `/productos` - Listar/crear
- GET/PUT/DELETE `/productos/{id}` - CRUD
- GET `/productos/stock-critico` - Stock bajo

**Ventas**
- GET/POST `/ventas` - Listar/registrar venta
- GET `/ventas/estadisticas` - Resumen

**Dashboard**
- GET `/dashboard/resumen` - KPIs
- POST `/dashboard/generar-pdf-menu` - PDF menú
- POST `/dashboard/generar-contenido-ia` - Contenido con IA

## 🌍 Environment Variables

Crear `.env` en la raíz (local) o configurar en plataforma de deploy:

```env
# Backend
DATABASE_URL=sqlite:///./rotiseria.db
SECRET_KEY=your-super-secret-key-change-in-prod
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALGORITHM=HS256

# Optional: IA integrations
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...

# Frontend (en Vercel)
VITE_API_URL=http://localhost:8000

# Optional: Email / WhatsApp alerts
SMTP_SERVER=smtp.gmail.com
TWILIO_ACCOUNT_SID=...
```

## 📁 Project Structure

```
roti-app/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy ORM
│   │   ├── schemas/       # Pydantic V2 validation
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── dependencies/  # Auth, DB dependencies
│   │   ├── core/          # Config, security
│   │   └── main.py        # FastAPI app
│   ├── migrations/        # Alembic DB migrations
│   ├── tests/            # pytest fixtures + tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page routes
│   │   ├── utils/         # Helpers, API calls
│   │   └── App.jsx        # Main component
│   ├── public/
│   │   ├── manifest.json  # PWA manifest
│   │   └── service-worker.js
│   ├── package.json
│   └── vercel.json
├── .github/workflows/
│   ├── tests.yml          # Run pytest on push
│   ├── deploy-backend.yml # Deploy to Render
│   └── deploy-frontend.yml # Deploy to Vercel
├── docker-compose.yml
├── .gitignore
├── DEPLOY_RENDER_VERCEL.md  # 📘 LEER PRIMERO
├── GITHUB_ACTIONS_SETUP.md
└── verify-deploy.sh
```

## 📘 Deployment Guide

**⭐ ANTES DE DEPLOYAR:**
```bash
bash verify-deploy.sh  # Verifica todo está OK
```

**Opción 1: Render + Vercel (Recomendado - 10 min)**

Ver: **[DEPLOY_RENDER_VERCEL.md](DEPLOY_RENDER_VERCEL.md)**

Pasos:
1. Render: Connect GitHub → New Web Service → Deploy backend
2. Vercel: Import repo → Deploy frontend
3. Verificar en ~5 minutos

**Opción 2: GitHub Actions (Automático)**

Ver: **[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)**

Configura secretos en GitHub → auto-deploy on push

**Opción 3: Local CLI**

```bash
# Render
npm install -g render
render deploy

# Vercel
npm install -g vercel
vercel
```

## 🛠 Tech Stack

| Layer | Tech | Version |
|-------|------|---------|
| Backend | FastAPI | 0.104.1 |
| ORM | SQLAlchemy | 2.0.23 |
| Validation | Pydantic | 2.5.0 |
| Auth | python-jose | 3.3.0 |
| DB Migrations | Alembic | 1.12.1 |
| PDF | ReportLab | 4.0.7 |
| Frontend | React | 18.2.0 |
| Build | Vite | 5.0.0 |
| Styling | Tailwind CSS | 3.3.0 |
| Charts | Recharts | 2.10.0 |
| HTTP | Axios | 1.6.0 |
| Container | Docker | - |
| Deploy | Render / Vercel | - |
| CI/CD | GitHub Actions | - |

## ❓ FAQ

**P: ¿Cuánto tiempo toma deployar?**
R: ~10-15 minutos siguiendo [DEPLOY_RENDER_VERCEL.md](DEPLOY_RENDER_VERCEL.md)

**P: ¿Qué base de datos usa?**
R: SQLite en dev, PostgreSQL en prod (configurable)

**P: ¿Es multi-tenant?**
R: Sí, cada usuario ve solo sus datos (`business_id`)

**P: ¿Cómo agrego IA?**
R: Configura `OPENAI_API_KEY` en env vars y usa `/dashboard/generar-contenido-ia`

**P: ¿Tests incluidos?**
R: Sí, 24 tests passing (`pytest`). Corre en GitHub Actions automáticamente.

## 📞 Support & Contributing

- 🐛 Bugs: [GitHub Issues](../../issues)
- 📧 Email: Configura en `SMTP_CONFIG`
- 📱 WhatsApp: Configura Twilio en env vars

---

**Versión:** 1.0.0 | **Estado:** Production Ready ✅

