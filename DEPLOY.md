# GUÍA DE DESPLIEGUE - Rotisería MVP

## Ambiente Local

### 1. Setup (primera vez)

**Backend:**
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
cp ../.env.example .env
# Editar .env con valores locales si es necesario
```

**Frontend:**
```bash
cd frontend
npm install
cp ../.env.example .env.local
```

### 2. Ejecutar localmente (SQLite - desarrollo rápido)

```bash
# Terminal 1 - Backend
cd backend
.venv\Scripts\Activate.ps1  # o 'source .venv/bin/activate'
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Accede a `http://localhost:5173` (frontend) y `http://localhost:8000/docs` (API docs).

---

## Producción con Docker + PostgreSQL

### 1. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con valores de producción:
# - DATABASE_URL=postgresql://user:pass@db:5432/rotiseria
# - DEBUG=False
# - SECRET_KEY= (generar con: python -c "import secrets; print(secrets.token_urlsafe(32))")
# - BACKEND_CORS_ORIGINS=https://yourdomain.com
# - VITE_API_URL=https://api.yourdomain.com
Deploy Render (backend):

- Create a new Web Service in Render and connect your repo or use `render.yaml` present in repo.
- Set the following environment variables in Render:
	- `DATABASE_URL` (Postgres)
	- `SECRET_KEY` (strong random)
	- `OPENAI_KEY` (optional)
- The service will build the Docker image using `backend/Dockerfile` and run `/app/entrypoint.sh`.

Deploy Vercel (frontend):

- Configure project in Vercel, set `Build Command` to `npm run build` and `Output Directory` to `dist`.
- Add environment variable `VITE_API_URL` or similar pointing to backend URL.
```

### 2. Levantar con Docker Compose

```bash
docker-compose up --build
```

Esto levantará:
- **db**: PostgreSQL en puerto 5432
- **backend**: FastAPI en puerto 8000
- **frontend**: Vite dev server en puerto 5173

Las migraciones se ejecutan automáticamente al startup (`alembic upgrade head`).

### 3. Crear superuser (opcional, si implementas admin panel)

```bash
docker-compose exec backend python -c "
from app.core.db import SessionLocal
# Aquí puedes agregar lógica de creación de usuario admin
"
```

---

## Migraciones de Base de Datos

### Generar nueva migración

```bash
cd backend
# Con app corriendo localmente:
alembic revision --autogenerate -m "descripcion de cambios"
# Luego revisar archivo generado en migrations/versions/
```

### Aplicar migraciones

**Local:**
```bash
alembic upgrade head
```

**Docker:**
```bash
docker-compose exec backend alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1  # una versión atrás
alembic downgrade base  # volver al inicio
```

---

## Migrar datos de SQLite a PostgreSQL

Si ya tienes datos en SQLite local, exporta e importa:

```bash
# 1. Exportar datos desde SQLite (local dev)
python export_data.py  # genero este script si lo necesitas

# 2. Con DB en docker ya corriendo, importa
python import_data.py
```

---

## Configuración de Nginx + Let's Encrypt (producción)

Nota: Esto es para despliegue en un servidor VPS/dedicado.

### 1. Docker Compose con Nginx/Traefik

Puedo generar una versión avanzada del `docker-compose.yml` que incluya Nginx + Certbot para HTTPS automático. Pide cuando lo necesites.

### 2. Variables de entorno en producción

```bash
# .env (nunca commitear)
DATABASE_URL=postgresql://user:strongpass@db:5432/rotiseria
DEBUG=False
SECRET_KEY=<random-32-chars>
BACKEND_CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
VITE_API_URL=https://api.yourdomain.com
```

---

## Integración con IA (opcional)

### OpenAI

```bash
# .env
IA_PROVIDER=openai
IA_API_KEY=sk-...
```

Backend automáticamente usará OpenAI cuando esté configurado.

### Anthropic

```bash
# .env
IA_PROVIDER=anthropic
IA_API_KEY=sk-ant-...
```

---

## Alertas por Email (opcional)

Configura SMTP en `.env`:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=app-specific-password
```

Luego, las alertas de stock bajo se enviarán automáticamente.

---

## Alertas por WhatsApp (opcional)

Usa Twilio:
```bash
WHATSAPP_ACCOUNT_SID=ACxxxxxxxx
WHATSAPP_AUTH_TOKEN=xxxxxxxx
WHATSAPP_FROM=+1234567890
```

---

## Logs y Monitoreo

### Ver logs del backend

```bash
# Local
tail -f backend.log

# Docker
docker-compose logs -f backend
```

### Health check

```bash
curl http://localhost:8000/docs
curl http://localhost:5173/
```

---

## Backup de datos

### PostgreSQL

```bash
# Backup
docker-compose exec db pg_dump -U rotiseria rotiseria > backup.sql

# Restore
docker-compose exec -T db psql -U rotiseria rotiseria < backup.sql
```

---

## Problemas comunes

### Puerto 8000 ya en uso
```bash
netstat -aon | findstr :8000  # Windows
kill <PID>
# o cambiar puerto en docker-compose.yml
```

### Migraciones fallando
```bash
alembic current  # ver versión actual
alembic history  # ver historial
alembic downgrade -1  # rollback
```

### Frontend no conecta a API
- Verificar `VITE_API_URL` en `.env.local`
- Verificar CORS en backend: `BACKEND_CORS_ORIGINS`
- Verificar que backend esté corriendo: `curl http://localhost:8000/docs`

---

## Scripts de automatización (para agregar)

Próximamente:
- `deploy.sh` — despliegue automático a VPS
- `backup.sh` — backup automático de BD
- `restore.sh` — restauración desde backup

Pide cuando los necesites.
