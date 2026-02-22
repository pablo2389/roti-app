"""Tests for sales endpoints and services."""
import pytest
from datetime import datetime

def test_create_venta(client):
    """Test creating a sale."""
    # First create a product
    product_data = {
        "nombre": "Asado",
        "descripcion": "Asado premium",
        "precio": "25.00",
        "stock": "10",
        "stock_minimo": "2"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Create a sale
    venta_data = {
        "producto_id": product["id"],
        "cantidad": "2"
    }
    response = client.post("/ventas", json=venta_data)
    assert response.status_code == 200
    venta = response.json()
    assert venta["cantidad"] == 2
    assert venta["total"] == 50.0  # 25 * 2

def test_venta_reduces_stock(client):
    """Test that creating a sale reduces product stock."""
    # Create a product
    product_data = {
        "nombre": "Chorizo",
        "descripcion": "Chorizo argentino",
        "precio": "5.00",
        "stock": "20",
        "stock_minimo": "2"
    }
    product = client.post("/productos", data=product_data).json()
    initial_stock = product["stock"]
    
    # Create a sale
    venta_data = {
        "producto_id": product["id"],
        "cantidad": "5"
    }
    client.post("/ventas", json=venta_data)
    
    # Check stock was reduced
    updated_product = client.get(f"/productos/{product['id']}").json()
    assert updated_product["stock"] == initial_stock - 5

def test_venta_insufficient_stock(client):
    """Test that creating a sale with insufficient stock fails."""
    # Create a product with low stock
    product_data = {
        "nombre": "Escaso",
        "descripcion": "Producto escaso",
        "precio": "10.00",
        "stock": "2",
        "stock_minimo": "1"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Try to sell more than available
    venta_data = {
        "producto_id": product["id"],
        "cantidad": "5"  # Only 2 available
    }
    response = client.post("/ventas", json=venta_data)
    assert response.status_code == 400  # Bad request

def test_get_ventas(client):
    """Test getting all sales."""
    # Create products and sales
    product_data = {
        "nombre": "Milanesa",
        "descripcion": "Milanesa de ternera",
        "precio": "12.00",
        "stock": "30",
        "stock_minimo": "3"
    }
    product = client.post("/productos", data=product_data).json()
    
    venta_data = {
        "producto_id": product["id"],
        "cantidad": "3"
    }
    client.post("/ventas", json=venta_data)
    
    # Get all sales
    response = client.get("/ventas")
    assert response.status_code == 200
    ventas = response.json()
    assert len(ventas) > 0

def test_venta_nonexistent_product(client):
    """Test creating a sale for a non-existent product."""
    venta_data = {
        "producto_id": 9999,  # Non-existent
        "cantidad": "1"
    }
    response = client.post("/ventas", json=venta_data)
    assert response.status_code == 404

def test_multiple_sales_same_product(client):
    """Test creating multiple sales for the same product."""
    # Create a product
    product_data = {
        "nombre": "Pollo",
        "descripcion": "Pollo al horno",
        "precio": "8.00",
        "stock": "50",
        "stock_minimo": "5"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Create multiple sales
    for i in range(3):
        venta_data = {
            "producto_id": product["id"],
            "cantidad": "5"
        }
        response = client.post("/ventas", json=venta_data)
        assert response.status_code == 200
    
    # Verify stock was reduced correctly
    updated_product = client.get(f"/productos/{product['id']}").json()
    assert updated_product["stock"] == 50 - (5 * 3)

def test_zero_quantity_sale(client):
    """Test that sales with zero or negative quantity fail."""
    # Create a product
    product_data = {
        "nombre": "Producto",
        "descripcion": "Prueba",
        "precio": "10.00",
        "stock": "20",
        "stock_minimo": "2"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Try to create sale with zero quantity
    venta_data = {
        "producto_id": product["id"],
        "cantidad": "0"
    }
    response = client.post("/ventas", json=venta_data)
    assert response.status_code == 422  # Validation error

def test_venta_total_calculation(client):
    """Test that sale total is calculated correctly."""
    # Create a product with specific price
    product_data = {
        "nombre": "Especial",
        "descripcion": "Precio especial",
        "precio": "33.33",
        "stock": "100",
        "stock_minimo": "10"
    }
    product = client.post("/productos", data=product_data).json()
    
    # Create sale
    venta_data = {
        "producto_id": product["id"],
        "cantidad": "3"
    }
    response = client.post("/ventas", json=venta_data)
    venta = response.json()
    
    # Total should be 33.33 * 3 = 99.99
    assert abs(venta["total"] - (33.33 * 3)) < 0.01
