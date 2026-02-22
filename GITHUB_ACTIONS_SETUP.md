# Configuración de GitHub Actions para Despliegue

Este documento explica cómo configurar GitHub Secrets para despliegues automáticos a Render y Vercel.

## 1. Configurar Secrets en GitHub (SIN pastear claves acá)

Ve a tu repositorio → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.

Añade estos secrets:

### Para Backend (Render):

- **`RENDER_API_KEY`**
  - Obtén de: https://dashboard.render.com/account/api-tokens
  - Crea un nuevo token (cópialo, no lo podrás ver después)
  - Pégalo en GitHub Secret

- **`RENDER_SERVICE_ID`**
  - Obtén de: tu servicio en Render Dashboard (URL: `https://dashboard.render.com/services/web/srv-...`)
  - El ID es la cadena después de `/web/` (ej: `srv-123abc...`)
  - Pégalo en GitHub Secret

### Para Frontend (Vercel):

- **`VERCEL_TOKEN`**
  - Obtén de: https://vercel.com/account/tokens
  - Crea un nuevo token
  - Pégalo en GitHub Secret

- **`VERCEL_ORG_ID`**
  - Obtén de: Vercel Dashboard → Settings → General
  - Busca "Team ID" o "Org ID"
  - Pégalo en GitHub Secret

- **`VERCEL_PROJECT_ID`**
  - Obtén de: tu proyecto en Vercel → Settings → General
  - Busca "Project ID"
  - Pégalo en GitHub Secret

- **`VITE_API_URL`** (opcional)
  - URL del backend en Render (ej: `https://rotiseria-backend.onrender.com`)
  - Usado por el frontend para apuntar a la API

---

## 2. Activar Auto-Deploy en Render (alternativa a GitHub Actions)

Si prefieres que Render maneje el deploy sin necesidad de GitHub Actions:

1. Ve a tu servicio en Render
2. **Settings** → **Auto-Deploy**
3. Conecta tu repositorio de GitHub
4. Render desplegará automáticamente en cada push a `main`

---

## 3. Activar Auto-Deploy en Vercel (alternativa)

Vercel se integra mejor con GitHub:

1. Ve a https://vercel.com/new
2. Importa tu repositorio
3. Vercel desplegará automáticamente en cada push a `main`
4. No necesitas secrets si usas la integración nativa

---

## 4. Workflows Disponibles

Con los secrets configurados, estos workflows se ejecutarán automáticamente:

### **Tests** (`.github/workflows/tests.yml`)
- Se ejecuta en cada push a `main` o PR
- Corre tests del backend y build del frontend
- Verifica que nada se rompa antes de desplegar

### **Deploy Backend** (`.github/workflows/deploy-backend.yml`)
- Se ejecuta cuando hay cambios en `/backend` o `Dockerfile`
- Llama a la API de Render para triggerar deploy
- Requiere: `RENDER_API_KEY` y `RENDER_SERVICE_ID`

### **Deploy Frontend** (`.github/workflows/deploy-frontend.yml`)
- Se ejecuta cuando hay cambios en `/frontend`
- Usa Vercel CLI para desplegar
- Requiere: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`

---

## 5. Flujo de Despliegue Recomendado

```
Haces un push a main
   ↓
GitHub Actions ejecuta tests
   ↓
Si los tests pasan, y hay cambios en backend:
   → Workflow deploy-backend se ejecuta
   → Render recibe la request y despliega
   ↓
Si hay cambios en frontend:
   → Workflow deploy-frontend se ejecuta
   → Vercel recibe la request y despliega
```

---

## 6. Monitoreo

- **GitHub**: Ve a tu repo → **Actions** para ver el estado de los workflows
- **Render**: Ve a tu servicio → **Logs** para ver el deploy progress
- **Vercel**: Ve a tu proyecto → **Deployments** para ver el deploy progress

---

## 7. Troubleshooting

### Workflow falla con "Missing secrets"
- Verifica que hayas añadido todos los secrets en GitHub
- Los nombres deben ser exactos (case-sensitive)

### Render no recibe la referencia de deploy
- Verifica que `RENDER_API_KEY` y `RENDER_SERVICE_ID` sean correctos
- Prueba manualmente desde terminal: `curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" -H "Authorization: Bearer $RENDER_API_KEY"`

### Vercel no acepta el token
- Verifica que el token sea "Personal Access Token" de Vercel
- Algunos tokens antigous pueden no funcionar; crea uno nuevo

---

## 8. Resumen Rápido (Checklist)

- [ ] Crea y copia `RENDER_API_KEY` desde https://dashboard.render.com/account/api-tokens
- [ ] Obtén `RENDER_SERVICE_ID` de tu servicio en Render
- [ ] Añade ambos secrets en GitHub
- [ ] Crea y copia `VERCEL_TOKEN` desde https://vercel.com/account/tokens
- [ ] Obtén `VERCEL_ORG_ID` y `VERCEL_PROJECT_ID` de Vercel
- [ ] Añade los 3 secrets de Vercel en GitHub
- [ ] Haz un push a `main` para probar los workflows
- [ ] Ve a **Actions** para verificar que se ejecutaron

---

¿Preguntas? Ver logs en:
- GitHub Actions: `Settings → Actions → View all workflows → Selecciona uno`
- Render: Tu servicio → **Event Log** o **Logs**
- Vercel: Tu proyecto → **Deployments**
