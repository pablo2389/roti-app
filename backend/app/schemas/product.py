from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    stock_minimo: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoOut(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    imagen_path: Optional[str] = None
    fecha_creacion: Optional[datetime]
