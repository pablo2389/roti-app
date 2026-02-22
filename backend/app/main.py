from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core import db
from .core.config import settings
from .routes import product_routes, venta_routes, dashboard_routes
import os

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db.Base.metadata.create_all(bind=db.engine)


app.include_router(product_routes.router)
app.include_router(venta_routes.router)
app.include_router(dashboard_routes.router)
from .routes import misc_routes
app.include_router(misc_routes.router)
from .routes import auth_routes
app.include_router(auth_routes.router)

# Mount static files (images, icons)
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount('/static', StaticFiles(directory=static_dir), name='static')
