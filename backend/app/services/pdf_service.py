from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from typing import List
from ..models.product import Producto
import os
import pathlib


def generar_pdf_menu(productos: List[Producto]) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    for p in productos:
        if y < 120:
            c.showPage()
            y = height - 50
        # Imagen: if imagen_path is a public URL (/static/...), convert to FS path
        img_path = None
        if p.imagen_path:
            if isinstance(p.imagen_path, str) and p.imagen_path.startswith('/static'):
                # map to backend app static folder
                base = pathlib.Path(__file__).parent / '..'
                candidate = (base / p.imagen_path.lstrip('/')).resolve()
                if candidate.exists():
                    img_path = str(candidate)
            elif os.path.exists(p.imagen_path):
                img_path = p.imagen_path
        if img_path:
            try:
                img = ImageReader(img_path)
                c.drawImage(img, 50, y - 80, width=80, height=80, preserveAspectRatio=True)
            except Exception:
                pass
        c.setFont("Helvetica-Bold", 12)
        c.drawString(140, y, f"{p.nombre}  - ${p.precio:.2f}")
        c.setFont("Helvetica", 10)
        c.drawString(140, y - 16, (p.descripcion or ""))
        y -= 110
    c.save()
    buffer.seek(0)
    return buffer.read()
