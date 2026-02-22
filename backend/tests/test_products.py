"""Tests for product endpoints and services."""
import json
from io import BytesIO
from fastapi.testclient import TestClient

def test_create_product(client):
    """Test creating a new product."""
    data = {
        "nombre": "Asado",
        "descripcion": "Asado premium con chimichurri",
        "precio": "25.50",
        "stock": "10",
        "stock_minimo": "2"
    }
    
    response = client.post("/productos", data=data)
    assert response.status_code == 200
    product = response.json()
    assert product["nombre"] == "Asado"
    assert product["precio"] == 25.50
    assert product["stock"] == 10

def test_create_product_with_image(client):
    """Test creating a product with an image."""
    # Create a dummy image file
    image_content = b"fake image data"
    
    data = {
        "nombre": "Chorizo",
        "descripcion": "Chorizo argentino",
        "precio": "5.99",
        "stock": "20",
        "stock_minimo": "5"
    }
    
    files = {"imagen": ("test.jpg", BytesIO(image_content), "image/jpeg")}
    
    response = client.post("/productos", data=data, files=files)
    assert response.status_code == 200
    product = response.json()
    assert product["nombre"] == "Chorizo"
    assert product["imagen_path"] is not None

def test_get_products(client):
    """Test getting all products."""
    # Create a product first
    data = {
        "nombre": "Milanesa",
        "descripcion": "Milanesa de ternera",
        "precio": "12.00",
        "stock": "15",
        "stock_minimo": "3"
    }
    client.post("/productos", data=data)
    
    response = client.get("/productos")
    assert response.status_code == 200
    products = response.json()
    assert len(products) > 0
    assert products[0]["nombre"] == "Milanesa"

def test_get_product_by_id(client):
    """Test getting a specific product."""
    # Create a product first
    data = {
        "nombre": "Pollo",
        "descripcion": "Pollo al horno",
        "precio": "8.50",
        "stock": "20",
        "stock_minimo": "4"
    }
    created = client.post("/productos", data=data).json()
    product_id = created["id"]
    
    response = client.get(f"/productos/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert product["id"] == product_id
    assert product["nombre"] == "Pollo"

def test_update_product(client):
    """Test updating a product."""
    # Create a product first
    data = {
        "nombre": "Milanesa",
        "descripcion": "Original",
        "precio": "10.00",
        "stock": "10",
        "stock_minimo": "2"
    }
    created = client.post("/productos", data=data).json()
    product_id = created["id"]
    
    # Update it
    update_data = {
        "nombre": "Milanesa Premium",
        "descripcion": "Actualizada",
        "precio": "15.00",
        "stock": "15",
        "stock_minimo": "3"
    }
    response = client.put(f"/productos/{product_id}", data=update_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["nombre"] == "Milanesa Premium"
    assert updated["precio"] == 15.00

def test_delete_product(client):
    """Test deleting a product."""
    # Create a product first
    data = {
        "nombre": "Temporal",
        "descripcion": "Para borrar",
        "precio": "1.00",
        "stock": "1",
        "stock_minimo": "1"
    }
    created = client.post("/productos", data=data).json()
    product_id = created["id"]
    
    # Delete it
    response = client.delete(f"/productos/{product_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    response = client.get(f"/productos/{product_id}")
    assert response.status_code == 404

def test_stock_critico_endpoint(client):
    """Test getting products with critical stock."""
    # Create a product with normal stock
    data1 = {
        "nombre": "Normal Stock",
        "descripcion": "Buen stock",
        "precio": "10.00",
        "stock": "50",
        "stock_minimo": "5"
    }
    client.post("/productos", data=data1)
    
    # Create a product with critical stock
    data2 = {
        "nombre": "Critical Stock",
        "descripcion": "Poco stock",
        "precio": "10.00",
        "stock": "2",
        "stock_minimo": "5"
    }
    client.post("/productos", data=data2)
    
    response = client.get("/productos/stock-critico")
    assert response.status_code == 200
    critical = response.json()
    
    # Should only return the critical stock product
    assert len(critical) == 1
    assert critical[0]["nombre"] == "Critical Stock"
    assert critical[0]["stock"] <= critical[0]["stock_minimo"]

def test_invalid_product_creation(client):
    """Test validation in product creation."""
    # Missing required field
    data = {
        "nombre": "Incompleto",
        # Missing descripcion, precio, stock, stock_minimo
    }
    
    response = client.post("/productos", data=data)
    assert response.status_code == 422  # Validation error

def test_negative_stock_validation(client):
    """Test that negative stock is not allowed."""
    data = {
        "nombre": "Invalid",
        "descripcion": "Stock negativo",
        "precio": "10.00",
        "stock": "-5",  # Invalid
        "stock_minimo": "2"
    }
    
    response = client.post("/productos", data=data)
    # Should fail validation (stock must be >= 0)
    assert response.status_code == 422
