from sqlalchemy.orm import Session
from ..models.venta import Venta
from ..models.product import Producto
from ..schemas.venta import VentaCreate
from typing import List, Dict


def create_venta(db: Session, venta_in: VentaCreate, business_id: str | None = None) -> Venta:
    producto = db.query(Producto).filter(Producto.id == venta_in.producto_id).first()
    if not producto:
        raise ValueError("Producto no encontrado")
    # Ensure product belongs to same business (if provided)
    if business_id is not None and producto.business_id is not None and producto.business_id != business_id:
        raise ValueError("Producto no encontrado")
    if venta_in.cantidad <= 0:
        raise ValueError("Cantidad debe ser mayor que 0")
    if producto.stock < venta_in.cantidad:
        raise ValueError("Stock insuficiente")
    total = producto.precio * venta_in.cantidad
    producto.stock -= venta_in.cantidad
    venta = Venta(producto_id=venta_in.producto_id, cantidad=venta_in.cantidad, total=total)
    if business_id is not None:
        venta.business_id = business_id
    db.add(venta)
    db.commit()
    db.refresh(venta)
    db.refresh(producto)
    return venta


def get_ventas(db: Session, business_id: str | None = None) -> List[Venta]:
    q = db.query(Venta).order_by(Venta.fecha.desc())
    if business_id is not None:
        q = q.filter(Venta.business_id == business_id)
    return q.all()


def estadisticas(db: Session, business_id: str | None = None) -> Dict:
    ventas_q = db.query(Venta)
    if business_id is not None:
        ventas_q = ventas_q.filter(Venta.business_id == business_id)
    ventas = ventas_q.all()
    contador = {}
    for v in ventas:
        contador[v.producto_id] = contador.get(v.producto_id, 0) + v.cantidad
    mas_vendido = None
    if contador:
        pid = max(contador, key=lambda k: contador[k])
        producto = db.query(Producto).filter(Producto.id == pid).first()
        mas_vendido = {"producto_id": pid, "nombre": producto.nombre if producto else None, "cantidad": contador[pid]}
    total_ventas = sum(v.total for v in ventas)
    productos_bajo_stock_q = db.query(Producto).filter(Producto.stock <= Producto.stock_minimo)
    if business_id is not None:
        productos_bajo_stock_q = productos_bajo_stock_q.filter(Producto.business_id == business_id)
    productos_bajo_stock = [
        {"id": p.id, "nombre": p.nombre, "stock": p.stock, "stock_minimo": p.stock_minimo}
        for p in productos_bajo_stock_q.all()
    ]
    ventas_por_producto = []
    for k, v in contador.items():
        producto = db.query(Producto).filter(Producto.id == k).first()
        ventas_por_producto.append({"producto_id": k, "nombre": producto.nombre if producto else None, "cantidad": v})
    ventas_por_producto.sort(key=lambda x: x["cantidad"], reverse=True)
    return {
        "total_ventas_dia": total_ventas,
        "producto_mas_vendido": mas_vendido,
        "productos_bajo_stock": productos_bajo_stock,
        "ventas_por_producto": ventas_por_producto,
    }
