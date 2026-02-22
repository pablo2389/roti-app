from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..services.pdf_service import generar_pdf_menu
from ..services.venta_service import estadisticas
from ..integrations.externals import generar_prompt_ia
from ..services.product_service import get_products
from fastapi.responses import StreamingResponse
import io

router = APIRouter(tags=["misc"])


@router.post("/generar-pdf-menu")
def generar_pdf(db: Session = Depends(get_db)):
    productos = get_products(db)
    pdf_bytes = generar_pdf_menu(productos)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=menu.pdf"})


@router.post("/generar-contenido-ia")
def generar_contenido(body: dict, db: Session = Depends(get_db)):
    producto_id = body.get('producto_id')
    if producto_id is None:
        raise HTTPException(status_code=400, detail="producto_id requerido")
    productos = get_products(db)
    producto = next((p for p in productos if p.id == int(producto_id)), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    prompt = generar_prompt_ia({"nombre": producto.nombre, "descripcion": producto.descripcion, "precio": producto.precio})
    return {"prompt": prompt}
