from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class VentaCreate(BaseModel):
    producto_id: int
    cantidad: int


class VentaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    producto_id: int
    cantidad: int
    fecha: Optional[datetime]
    total: float
