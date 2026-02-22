# 🚀 GUÍA COMPLETA: Deploy Render + Vercel (Opción 1)

## ⏱️ Tiempo total: ~10-15 minutos (primer deploy)

---

## 🔴 PASO 1: Preparar tu repositorio (YA HECHO ✅)

El código está listo:
- ✅ `Dockerfile` en raíz
- ✅ `render.yaml` configurado
- ✅ `frontend/vercel.json` configurado
- ✅ `requirements.txt` con todas las dependencias
- ✅ Tests verdes (24 passed)

**Todo está pusheado a tu repo: `pablo2389/roti-app`**

---

## 🟢 PASO 2: Crear cuenta en Render (2-3 min)

### 2.1 Ir a Render
1. Abre: https://render.com
2. Clickea **"Sign Up"** (arriba derecha)

### 2.2 Registro (elije una opción):
- ✅ **RECOMENDADO:** "Continue with GitHub" (más fácil, vincula auto el repo)
- O: Email + password

Si clickeaste "GitHub":
- Te abre navegador de GitHub → Autoriza Render
- Luego vuelve a Render dashboard

### 2.3 Primer acceso
- Render te pregunta "Welcome! What's your first step?"
- Clickea: **"Web Service"** (bajo "Create a new service")

---

## 🔵 PASO 3: Desplegar Backend en Render (4-5 min)

### 3.1 Conectar repositorio
En la pantalla "New Web Service":
1. Selecciona: **"Build and deploy from a Git repository"**
2. Clickea: **"Connect a repository"**
3. Busca: `roti-app` (tu repo)
4. Clickea el repo → Render pide "Install" → Autoriza → Done ✅

Vuelves a "New Web Service" y ya aparece `pablo2389/roti-app` seleccionado.

### 3.2 Configurar servicio
Llena los campos:

| Campo | Valor | Explicación |
|-------|-------|-------------|
| **Name** | `rotiseria-backend` | Nombre del servicio |
| **Region** | `Ohio (us-ohio)` o más cercano | Elige la región más cercana a ti |
| **Branch** | `main` | La rama de tu repo |
| **Root Directory** | (dejar vacío) | Usa la raíz |
| **Runtime** | `Docker` | Ya lo detecta automático |
| **Plan** | `Starter` ($7/mes, gratis 750h) | Prueba con Starter |

### 3.3 Agregar Environment Variables
Clickea: **"Advanced"** (debajo del formulario)

En la sección **"Environment"**, addVars:
```
DATABASE_URL = sqlite:///./rotiseria.db
SECRET_KEY = generado-aleatorio-32-chars
PORT = 8000
```

Para `SECRET_KEY`, genera uno con:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Cópialo y pégalo en el campo.

### 3.4 Deploy
Clickea: **"Create Web Service"** (abajo a la derecha, botón azul)

**Qué pasa ahora:**
- Render clona tu repo
- Construye la imagen Docker (~3-4 min)
- Inicia el servicio
- Te muestra logs en tiempo real

**Espera a ver algo como:**
```
✓ Deploy successful
Service live at: https://rotiseria-backend.onrender.com
```

*Nota: Los primeros minutos puede ser lento; Render "duerme" servicios inactivos.*

### 3.5 Verificar Backend
Abre en tu navegador:
```
https://rotiseria-backend.onrender.com/docs
```

Deberías ver SwaggerUI (API docs) ✅

---

## 🟡 PASO 4: Crear cuenta Vercel (1-2 min)

### 4.1 Ir a Vercel
1. Abre: https://vercel.com
2. Clickea **"Sign Up"** (arriba derecha)

### 4.2 Registro
- **RECOMENDADO:** "Continue with GitHub"
- Autoriza Vercel en GitHub

---

## 🟣 PASO 5: Desplegar Frontend en Vercel (3 min)

### 5.1 Importar proyecto
En Vercel Dashboard:
1. Clickea: **"Add New..."** → **"Project"** (arriba)
2. Selecciona: **"Import Git Repository"**
3. Busca: `roti-app` (tu repo)
4. Clickea → "Import"

### 5.2 Configurar Vercel
En la pantalla de configuración:

| Campo | Valor |
|-------|-------|
| **Project Name** | `roti-app` (o similar) |
| **Framework Preset** | `Vite` (detecta automático) |
| **Root Directory** | `./frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `dist` (default) |

### 5.3 Environment Variables
En "Environment Variables", agrega:
```
VITE_API_URL = https://rotiseria-backend.onrender.com
```

*(Reemplaza con la URL exacta de tu backend de Render, del paso 3.5)*

### 5.4 Deploy
Clickea: **"Deploy"** (botón abajo)

**Espera a ver:**
```
✓ Deployment successful
Your site is live at: https://roti-app.vercel.app
```

### 5.5 Verificar Frontend
Abre en tu navegador:
```
https://roti-app.vercel.app
```

Deberías ver tu app React cargada ✅

---

## 🎯 PASO 6: Verificar que todo funciona

### Test de Frontend → Backend
1. En tu app frontend, intenta:
   - Crear un producto
   - Ver lista de productos
   - Registrarse / Login (si está implementado)

2. Si funciona, ¡listo! 🎉

3. Si falla con error de red:
   - Abre inspección del navegador (F12) → Network/Console
   - Verifica que `VITE_API_URL` sea correcta
   - En Vercel, redeploy: Settings → Deployments → Redeploy

---

## 📝 Resumen: URLs finales

| Componente | URL |
|-----------|-----|
| Backend API | `https://rotiseria-backend.onrender.com` |
| API Docs | `https://rotiseria-backend.onrender.com/docs` |
| Frontend | `https://roti-app.vercel.app` |

---

## 🔄 Auto-Deploys (después del primer deploy)

Con esta configuración:
- **Cada push a `main`** en tu repo
- → Render redeploy automático del backend
- → Vercel redeploy automático del frontend
- No necesitas hacer nada más 🚀

---

## 🆘 Troubleshooting

### El backend dice "Port not available"
- Render detectó problema con el puerto
- Solución: En Render Settings → delete el servicio y recrealo

### Frontend no conecta al backend
- Error: "CORS denied" o "Failed to fetch"
- Solución: 
  1. Verifica `VITE_API_URL` en Vercel (Settings → Environment Variables)
  2. Redeploy el frontend
  3. Limpiar cache navegador (Ctrl+Shift+K)

### Build falla en Render
- Verifica `requirements.txt` tiene todas las deps
- Ver logs en Render: servicio → Logs

### Database no persiste (si usas SQLite)
- SQLite en Render es efímero (se borra cuando se reinicia)
- **Solución recomendada:** Usar Postgres
  - Crear Database en Render (free tier disponible)
  - Get connection string
  - Set `DATABASE_URL` en Render backend service

---

## 💡 Siguientes pasos (opcional)

1. **Agregar Postgres** (para datos persistentes)
2. **Configurar GitHub Actions** (CI/CD automático)
3. **Agregar SSL** (HTTPS automático, Render lo hace gratis)
4. **Setup monitoring/logs**

Pide cuando los necesites.

---

## ✅ Checklist Final

- [ ] Repo pusheado a GitHub
- [ ] Backend desplegado en Render
- [ ] Frontend desplegado en Vercel
- [ ] Backend responde en `/docs`
- [ ] Frontend carga en navegador
- [ ] Frontend conecta y consume API

**¿Necesitas ayuda en algún paso? Reporta dónde quedate atascado.** 🚀
