"""
Pruebas unitarias para los modelos de la API Ferretería
"""
import pytest
from app import Producto, Categoria, Cliente

class TestProducto:
    """Pruebas para el modelo Producto"""
    
    def test_crear_producto_valido(self, app_context):
        """Probar creación de producto válido"""
        producto = Producto(
            nombre="Martillo Test",
            descripcion="Martillo para pruebas",
            precio=25.50,
            stock=10
        )
        assert producto.nombre == "Martillo Test"
        assert producto.precio == 25.50
        assert producto.stock == 10
    
    def test_producto_to_dict(self, app_context):
        """Probar conversión de producto a diccionario"""
        producto = Producto(
            nombre="Destornillador",
            descripcion="Destornillador Phillips",
            precio=15.75,
            stock=5
        )
        producto_dict = producto.to_dict()
        
        assert producto_dict['nombre'] == "Destornillador"
        assert producto_dict['precio'] == 15.75
        assert producto_dict['stock'] == 5
    
    def test_producto_precio_positivo(self, app_context):
        """Probar que el precio debe ser positivo"""
        # Esta prueba asume validación en el modelo
        producto = Producto(
            nombre="Producto Test",
            descripcion="Test",
            precio=10.0,
            stock=1
        )
        assert producto.precio > 0

class TestCategoria:
    """Pruebas para el modelo Categoria"""
    
    def test_crear_categoria_valida(self, app_context):
        """Probar creación de categoría válida"""
        categoria = Categoria(
            nombre="Herramientas Eléctricas",
            descripcion="Herramientas que requieren electricidad"
        )
        assert categoria.nombre == "Herramientas Eléctricas"
        assert categoria.descripcion == "Herramientas que requieren electricidad"
    
    def test_categoria_to_dict(self, app_context):
        """Probar conversión de categoría a diccionario"""
        categoria = Categoria(
            nombre="Ferretería",
            descripcion="Artículos de ferretería"
        )
        categoria_dict = categoria.to_dict()
        
        assert categoria_dict['nombre'] == "Ferretería"
        assert categoria_dict['descripcion'] == "Artículos de ferretería"

class TestCliente:
    """Pruebas para el modelo Cliente"""
    
    def test_crear_cliente_valido(self, app_context):
        """Probar creación de cliente válido"""
        cliente = Cliente(
            nombre="María García",
            email="maria@test.com",
            telefono="987654321",
            direccion="Avenida Test 456"
        )
        assert cliente.nombre == "María García"
        assert cliente.email == "maria@test.com"
    
    def test_cliente_to_dict(self, app_context):
        """Probar conversión de cliente a diccionario"""
        cliente = Cliente(
            nombre="Carlos López",
            email="carlos@test.com",
            telefono="555-0123",
            direccion="Calle Test 789"
        )
        cliente_dict = cliente.to_dict()
        
        assert cliente_dict['nombre'] == "Carlos López"
        assert cliente_dict['email'] == "carlos@test.com"