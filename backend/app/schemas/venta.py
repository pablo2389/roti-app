from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VentaCreate(BaseModel):
    producto_id: int
    cantidad: int


class VentaOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    fecha: Optional[datetime]
    total: float

    class Config:
        orm_mode = True
