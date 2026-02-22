"""Tests for dashboard endpoints."""
import json

def test_dashboard_resumen(client):
    """Test dashboard summary endpoint."""
    # Create some products
    products_data = [
        {
            "nombre": "Asado",
            "descripcion": "Premium",
            "precio": "25.00",
            "stock": "10",
            "stock_minimo": "2"
        },
        {
            "nombre": "Chorizo",
            "descripcion": "Argentino",
            "precio": "5.00",
            "stock": "30",
            "stock_minimo": "5"
        },
        {
            "nombre": "Milanesa",
            "descripcion": "Ternera",
            "precio": "12.00",
            "stock": "2",  # Critical stock
            "stock_minimo": "5"
        }
    ]
    
    products = []
    for data in products_data:
        product = client.post("/productos", data=data).json()
        products.append(product)
    
    # Create some sales
    sales_data = [
        {"producto_id": products[0]["id"], "cantidad": "2"},  # Asado x2
        {"producto_id": products[1]["id"], "cantidad": "5"},  # Chorizo x5
        {"producto_id": products[0]["id"], "cantidad": "1"},  # Asado x1
    ]
    
    for data in sales_data:
        client.post("/ventas", json=data)
    
    # Get dashboard summary
    response = client.get("/dashboard/resumen")
    assert response.status_code == 200
    
    summary = response.json()
    assert "total_ventas_dia" in summary
    assert "producto_mas_vendido" in summary
    assert "productos_bajo_stock" in summary
    assert "ventas_por_producto" in summary
    
    # Verify data correctness
    assert summary["total_ventas_dia"] == (25*2 + 5*5 + 25*1)  # 130
    assert summary["producto_mas_vendido"] is not None
    assert len(summary["productos_bajo_stock"]) > 0

def test_dashboard_graph_data(client):
    """Test that dashboard returns correct data for graphs."""
    # Create products
    product_data = {
        "nombre": "Producto Test",
        "descripcion": "Para gráficos",
        "precio": "15.00",
        "stock": "50",
        "stock_minimo": "5"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Create multiple sales
    for _ in range(3):
        venta_data = {
            "producto_id": product["id"],
            "cantidad": "2"
        }
        client.post("/ventas", json=venta_data)
    
    # Get dashboard with graph data
    response = client.get("/dashboard/resumen")
    assert response.status_code == 200
    
    summary = response.json()
    ventas_por_producto = summary.get("ventas_por_producto", [])
    
    # Should have data for our product
    assert len(ventas_por_producto) > 0
    assert any(v["nombre"] == "Producto Test" for v in ventas_por_producto)

def test_dashboard_empty_state(client):
    """Test dashboard with no products or sales."""
    response = client.get("/dashboard/resumen")
    assert response.status_code == 200
    
    summary = response.json()
    assert summary["total_ventas_dia"] == 0
    assert summary["producto_mas_vendido"] is None
    assert len(summary["productos_bajo_stock"]) == 0

def test_dashboard_with_multiple_critical_products(client):
    """Test dashboard correctly identifies multiple products with critical stock."""
    # Create products with critical stock
    for i in range(3):
        product_data = {
            "nombre": f"Crítico {i}",
            "descripcion": "Bajo stock",
            "precio": "10.00",
            "stock": "1",
            "stock_minimo": "5"
        }
        client.post("/productos", data=product_data)
    
    response = client.get("/dashboard/resumen")
    assert response.status_code == 200
    
    summary = response.json()
    critical_products = summary["productos_bajo_stock"]
    
    # Should have 3 products with critical stock
    assert len(critical_products) == 3

def test_pdf_menu_generation(client):
    """Test PDF menu generation endpoint."""
    # Create a product
    product_data = {
        "nombre": "Asado",
        "descripcion": "Asado premium con chimichurri",
        "precio": "25.00",
        "stock": "10",
        "stock_minimo": "2"
    }
    client.post("/productos", data=product_data)
    
    # Generate PDF
    response = client.post("/dashboard/generar-pdf-menu")
    assert response.status_code == 200
    
    # Check response is PDF
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0

def test_ia_content_generation(client):
    """Test IA content generation endpoint."""
    # Create a product
    product_data = {
        "nombre": "Especial Rotisería",
        "descripcion": "Nuestro mejor asado",
        "precio": "30.00",
        "stock": "10",
        "stock_minimo": "2"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Generate IA content
    request_data = {
        "producto_id": product["id"]
    }
    response = client.post("/dashboard/generar-contenido-ia", json=request_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "contenido" in result
    assert len(result["contenido"]) > 0

def test_ia_nonexistent_product(client):
    """Test IA generation with non-existent product."""
    request_data = {
        "producto_id": 9999
    }
    response = client.post("/dashboard/generar-contenido-ia", json=request_data)
    assert response.status_code == 404
