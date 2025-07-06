"""
Configuración de pytest para las pruebas de la API Ferretería
"""
import pytest
import sys
import os

# Agregar el directorio raíz al path para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Producto, Categoria, Cliente

@pytest.fixture
def client():
    """Cliente de prueba para Flask"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def app_context():
    """Contexto de aplicación para pruebas"""
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def sample_categoria():
    """Categoría de ejemplo para pruebas"""
    return {
        'nombre': 'Herramientas',
        'descripcion': 'Herramientas de construcción'
    }

@pytest.fixture
def sample_producto():
    """Producto de ejemplo para pruebas"""
    return {
        'nombre': 'Martillo',
        'descripcion': 'Martillo de acero',
        'precio': 25.50,
        'stock': 10
    }

@pytest.fixture
def sample_cliente():
    """Cliente de ejemplo para pruebas"""
    return {
        'nombre': 'Juan Pérez',
        'email': 'juan@example.com',
        'telefono': '123456789',
        'direccion': 'Calle 123'
    }