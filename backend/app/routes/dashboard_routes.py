from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..services.venta_service import estadisticas
from ..services.product_service import get_products
from ..schemas.dashboard import DashboardResumen
from ..services.pdf_service import generar_pdf_menu
from ..integrations.externals import generar_prompt_ia
from fastapi.responses import StreamingResponse
import io
from pydantic import BaseModel

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/resumen", response_model=DashboardResumen)
def resumen(db: Session = Depends(get_db)):
    stats = estadisticas(db)
    return {
        "total_ventas_dia": stats.get("total_ventas_dia", 0),
        "producto_mas_vendido": stats.get("producto_mas_vendido"),
        "productos_bajo_stock": stats.get("productos_bajo_stock", 0),
        "ventas_por_producto": stats.get("ventas_por_producto", []),
    }


@router.post("/generar-pdf-menu")
def generar_pdf(db: Session = Depends(get_db)):
    productos = get_products(db)
    pdf_bytes = generar_pdf_menu(productos)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=menu.pdf"})


class ProductoIdRequest(BaseModel):
    producto_id: int


@router.post("/generar-contenido-ia")
def generar_contenido_ia(payload: ProductoIdRequest = Body(...), db: Session = Depends(get_db)):
    producto_id = payload.producto_id
    productos = get_products(db)
    producto = next((p for p in productos if p.id == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    contenido = generar_prompt_ia({"nombre": producto.nombre, "descripcion": producto.descripcion, "precio": producto.precio})
    return {"contenido": contenido}
