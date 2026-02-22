from pydantic import BaseModel
from typing import Any, List


class DashboardResumen(BaseModel):
    total_ventas_dia: float
    producto_mas_vendido: Any = None
    productos_bajo_stock: List[Any] = []
    ventas_por_producto: List[Any] = []
