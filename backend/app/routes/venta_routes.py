from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.venta import VentaCreate, VentaOut
from ..services.venta_service import create_venta, get_ventas
from typing import List
from ..dependencies.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("", response_model=VentaOut)
def registrar_venta(venta: VentaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        v = create_venta(db, venta, business_id=current_user.business_id)
        return v
    except ValueError as e:
        msg = str(e)
        if "Producto no encontrado" in msg:
            raise HTTPException(status_code=404, detail=msg)
        if "Cantidad" in msg or "cantidad" in msg:
            # Input validation error
            raise HTTPException(status_code=422, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


@router.get("", response_model=List[VentaOut])
def listar_ventas(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_ventas(db, business_id=current_user.business_id)
