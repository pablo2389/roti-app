from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.product import ProductoCreate, ProductoOut, ProductoUpdate
from ..services.product_service import create_product, get_products, get_product, update_product, delete_product, productos_stock_critico
from ..dependencies.auth import get_current_user
from ..models.user import User
import os
from typing import List

router = APIRouter(prefix="/productos", tags=["productos"])

BASE_STATIC = os.path.join(os.path.dirname(__file__), "..", "static")
IMAGES_DIR = os.path.join(BASE_STATIC, "images")
IMAGES_DIR = os.path.abspath(IMAGES_DIR)
os.makedirs(IMAGES_DIR, exist_ok=True)


@router.post("", response_model=ProductoOut)
def crear_producto(
    nombre: str = Form(...),
    descripcion: str | None = Form(None),
    precio: float = Form(...),
    stock: int = Form(...),
    stock_minimo: int = Form(...),
    imagen: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    imagen_path = None
    if imagen:
        filename = f"{imagen.filename}"
        path = os.path.join(IMAGES_DIR, filename)
        with open(path, "wb") as f:
            f.write(imagen.file.read())
        # store public URL path for the frontend
        imagen_path = f"/static/images/{filename}"
    product = ProductoCreate(
        nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, stock_minimo=stock_minimo
    )
    # Validaciones básicas
    if stock < 0 or stock_minimo < 0:
        raise HTTPException(status_code=422, detail="Stock y stock_minimo deben ser >= 0")
    p = create_product(db, product, imagen_path=imagen_path, business_id=current_user.business_id)
    return p


@router.get("", response_model=List[ProductoOut])
def listar_productos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_products(db, business_id=current_user.business_id)

@router.put("/{product_id}", response_model=ProductoOut)
def editar_producto(
    product_id: int,
    nombre: str = Form(...),
    descripcion: str | None = Form(None),
    precio: float = Form(...),
    stock: int = Form(...),
    stock_minimo: int = Form(...),
    imagen: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    imagen_path = None
    if imagen:
        filename = f"{imagen.filename}"
        path = os.path.join(IMAGES_DIR, filename)
        with open(path, "wb") as f:
            f.write(imagen.file.read())
        imagen_path = f"/static/images/{filename}"
    product = ProductoUpdate(nombre=nombre, descripcion=descripcion, precio=precio, stock=stock, stock_minimo=stock_minimo)
    updated = update_product(db, product_id, product, imagen_path=imagen_path, business_id=current_user.business_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated


@router.delete("/{product_id}")
def borrar_producto(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ok = delete_product(db, product_id, business_id=current_user.business_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"ok": True}

@router.get("/stock-critico", response_model=List[ProductoOut])
def stock_critico(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return productos_stock_critico(db, business_id=current_user.business_id)


@router.get("/{product_id}", response_model=ProductoOut)
def obtener_producto(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    p = get_product(db, product_id, business_id=current_user.business_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p
