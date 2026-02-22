from sqlalchemy.orm import Session
from ..models.product import Producto
from ..schemas.product import ProductoCreate, ProductoUpdate
from typing import List
import os


def create_product(db: Session, product: ProductoCreate, imagen_path: str | None = None, business_id: str | None = None) -> Producto:
    payload = product.model_dump()
    db_product = Producto(**payload)
    if imagen_path:
        db_product.imagen_path = imagen_path
    if business_id:
        db_product.business_id = business_id
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, business_id: str | None = None) -> List[Producto]:
    q = db.query(Producto)
    if business_id is not None:
        q = q.filter(Producto.business_id == business_id)
    return q.all()


def get_product(db: Session, product_id: int, business_id: str | None = None) -> Producto | None:
    q = db.query(Producto).filter(Producto.id == product_id)
    if business_id is not None:
        q = q.filter(Producto.business_id == business_id)
    return q.first()


def update_product(db: Session, product_id: int, data: ProductoUpdate, imagen_path: str | None = None, business_id: str | None = None) -> Producto:
    q = db.query(Producto).filter(Producto.id == product_id)
    if business_id is not None:
        q = q.filter(Producto.business_id == business_id)
    db_product = q.first()
    if not db_product:
        return None
    payload = data.model_dump()
    for k, v in payload.items():
        setattr(db_product, k, v)
    if imagen_path:
        db_product.imagen_path = imagen_path
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int, business_id: str | None = None) -> bool:
    q = db.query(Producto).filter(Producto.id == product_id)
    if business_id is not None:
        q = q.filter(Producto.business_id == business_id)
    db_product = q.first()
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


def productos_stock_critico(db: Session, business_id: str | None = None) -> List[Producto]:
    q = db.query(Producto).filter(Producto.stock <= Producto.stock_minimo)
    if business_id is not None:
        q = q.filter(Producto.business_id == business_id)
    return q.all()


def is_stock_critico(product: Producto) -> bool:
    return product.stock <= product.stock_minimo
