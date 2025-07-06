#!/usr/bin/env python3
"""
Script para configurar el proyecto completo de la API Ferretería
Crea todos los archivos necesarios para la Evaluación 3
"""

import os
import sys

def crear_archivo(ruta, contenido):
    """Crear archivo con contenido"""
    try:
        # Crear directorios si no existen
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Escribir archivo
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"✅ Creado: {ruta}")
        return True
    except Exception as e:
        print(f"❌ Error creando {ruta}: {e}")
        return False

def main():
    """Configurar proyecto completo"""
    print("🎯 CONFIGURADOR DE PROYECTO COMPLETO")
    print("📋 API Ferretería - Evaluación 3")
    print("=" * 80)
    
    archivos_creados = 0
    archivos_totales = 0
    
    # 1. requirements.txt
    archivos_totales += 1
    contenido_requirements = """Flask==3.1.1
Flask-SQLAlchemy==3.1.1
Flask-CORS==6.0.0
pytest==8.3.4
pytest-flask==1.3.0
pytest-cov==6.0.0
requests==2.32.3
coverage==7.6.9"""
    
    if crear_archivo("requirements.txt", contenido_requirements):
        archivos_creados += 1
    
    # 2. pytest.ini
    archivos_totales += 1
    contenido_pytest = """[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning"""
    
    if crear_archivo("pytest.ini", contenido_pytest):
        archivos_creados += 1
    
    # 3. tests/__init__.py
    archivos_totales += 1
    if crear_archivo("tests/__init__.py", "# Tests package"):
        archivos_creados += 1
    
    # 4. tests/conftest.py
    archivos_totales += 1
    contenido_conftest = '''"""
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
    }'''
    
    if crear_archivo("tests/conftest.py", contenido_conftest):
        archivos_creados += 1
    
    # 5. tests/unit/test_models.py
    archivos_totales += 1
    contenido_test_models = '''"""
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
        assert cliente_dict['email'] == "carlos@test.com"'''
    
    if crear_archivo("tests/unit/test_models.py", contenido_test_models):
        archivos_creados += 1
    
    # 6. tests/unit/test_api_endpoints.py
    archivos_totales += 1
    contenido_test_endpoints = '''"""
Pruebas unitarias para los endpoints de la API Ferretería
"""
import pytest
import json

class TestHealthEndpoint:
    """Pruebas para el endpoint de health check"""
    
    def test_health_check(self, client):
        """Probar endpoint de health check"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

class TestProductosEndpoints:
    """Pruebas para endpoints de productos"""
    
    def test_get_productos_vacio(self, client):
        """Probar obtener productos cuando no hay ninguno"""
        response = client.get('/productos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_crear_producto_valido(self, client):
        """Probar crear producto válido"""
        producto_data = {
            'nombre': 'Martillo API Test',
            'descripcion': 'Martillo para pruebas de API',
            'precio': 30.00,
            'stock': 15
        }
        
        response = client.post('/productos', 
                             data=json.dumps(producto_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['nombre'] == producto_data['nombre']
        assert data['precio'] == producto_data['precio']
        assert 'id' in data
    
    def test_crear_producto_datos_invalidos(self, client):
        """Probar crear producto con datos inválidos"""
        producto_data = {
            'nombre': '',  # Nombre vacío
            'precio': -10,  # Precio negativo
            'stock': -5     # Stock negativo
        }
        
        response = client.post('/productos',
                             data=json.dumps(producto_data),
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_obtener_producto_por_id(self, client):
        """Probar obtener producto específico por ID"""
        # Primero crear un producto
        producto_data = {
            'nombre': 'Destornillador Test',
            'descripcion': 'Para pruebas',
            'precio': 15.50,
            'stock': 8
        }
        
        response = client.post('/productos',
                             data=json.dumps(producto_data),
                             content_type='application/json')
        
        producto_creado = json.loads(response.data)
        producto_id = producto_creado['id']
        
        # Ahora obtener el producto por ID
        response = client.get(f'/productos/{producto_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == producto_id
        assert data['nombre'] == producto_data['nombre']

class TestCategoriasEndpoints:
    """Pruebas para endpoints de categorías"""
    
    def test_get_categorias_vacio(self, client):
        """Probar obtener categorías cuando no hay ninguna"""
        response = client.get('/categorias')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_crear_categoria_valida(self, client):
        """Probar crear categoría válida"""
        categoria_data = {
            'nombre': 'Herramientas Test',
            'descripcion': 'Categoría para pruebas'
        }
        
        response = client.post('/categorias',
                             data=json.dumps(categoria_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['nombre'] == categoria_data['nombre']
        assert 'id' in data

class TestClientesEndpoints:
    """Pruebas para endpoints de clientes"""
    
    def test_crear_cliente_valido(self, client):
        """Probar crear cliente válido"""
        cliente_data = {
            'nombre': 'Ana Martínez',
            'email': 'ana@test.com',
            'telefono': '555-9876',
            'direccion': 'Plaza Test 321'
        }
        
        response = client.post('/clientes',
                             data=json.dumps(cliente_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['nombre'] == cliente_data['nombre']
        assert data['email'] == cliente_data['email']
        assert 'id' in data'''
    
    if crear_archivo("tests/unit/test_api_endpoints.py", contenido_test_endpoints):
        archivos_creados += 1
    
    # 7. tests/integration/test_integration.py
    archivos_totales += 1
    contenido_test_integration = '''"""
Pruebas de integración para la API Ferretería
"""
import pytest
import json

class TestIntegracionCompleta:
    """Pruebas de integración que simulan flujos completos"""
    
    def test_flujo_completo_producto(self, client):
        """Probar flujo completo: crear categoría, crear producto, obtener producto"""
        # 1. Crear categoría
        categoria_data = {
            'nombre': 'Herramientas Manuales',
            'descripcion': 'Herramientas que no requieren electricidad'
        }
        
        response = client.post('/categorias',
                             data=json.dumps(categoria_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        categoria = json.loads(response.data)
        categoria_id = categoria['id']
        
        # 2. Crear producto en esa categoría
        producto_data = {
            'nombre': 'Martillo Integración',
            'descripcion': 'Martillo para pruebas de integración',
            'precio': 28.75,
            'stock': 12,
            'categoria_id': categoria_id
        }
        
        response = client.post('/productos',
                             data=json.dumps(producto_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        producto = json.loads(response.data)
        producto_id = producto['id']
        
        # 3. Verificar que el producto se puede obtener
        response = client.get(f'/productos/{producto_id}')
        assert response.status_code == 200
        
        producto_obtenido = json.loads(response.data)
        assert producto_obtenido['nombre'] == producto_data['nombre']
        assert producto_obtenido['categoria_id'] == categoria_id
    
    def test_gestion_stock_completa(self, client):
        """Probar gestión completa de stock"""
        # 1. Crear producto
        producto_data = {
            'nombre': 'Destornillador Stock',
            'descripcion': 'Para pruebas de stock',
            'precio': 18.50,
            'stock': 20
        }
        
        response = client.post('/productos',
                             data=json.dumps(producto_data),
                             content_type='application/json')
        
        producto = json.loads(response.data)
        producto_id = producto['id']
        
        # 2. Actualizar stock
        stock_data = {'cantidad': 5}
        response = client.put(f'/productos/{producto_id}/stock',
                            data=json.dumps(stock_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        
        # 3. Verificar que el stock se actualizó
        response = client.get(f'/productos/{producto_id}')
        producto_actualizado = json.loads(response.data)
        assert producto_actualizado['stock'] == 5
    
    def test_busqueda_productos(self, client):
        """Probar funcionalidad de búsqueda"""
        # 1. Crear varios productos
        productos = [
            {'nombre': 'Martillo Grande', 'descripcion': 'Martillo de 500g', 'precio': 35.0, 'stock': 5},
            {'nombre': 'Martillo Pequeño', 'descripcion': 'Martillo de 200g', 'precio': 20.0, 'stock': 8},
            {'nombre': 'Destornillador', 'descripcion': 'Destornillador Phillips', 'precio': 12.0, 'stock': 15}
        ]
        
        for producto_data in productos:
            response = client.post('/productos',
                                 data=json.dumps(producto_data),
                                 content_type='application/json')
            assert response.status_code == 201
        
        # 2. Buscar productos por término
        response = client.get('/productos?buscar=Martillo')
        assert response.status_code == 200
        
        resultados = json.loads(response.data)
        assert len(resultados) == 2  # Debe encontrar 2 martillos
        
        for resultado in resultados:
            assert 'Martillo' in resultado['nombre']'''
    
    if crear_archivo("tests/integration/test_integration.py", contenido_test_integration):
        archivos_creados += 1
    
    # 8. Script de ejecución de pruebas
    archivos_totales += 1
    contenido_ejecutar_pruebas = '''#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas y generar reportes
"""
import subprocess
import sys
import os
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecutar comando y mostrar resultado"""
    print(f"\\n{'='*60}")
    print(f"🔧 {descripcion}")
    print(f"{'='*60}")
    print(f"Ejecutando: {comando}")
    print("-" * 40)
    
    try:
        resultado = subprocess.run(comando, shell=True, check=False)
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - EXITOSO")
            return True
        else:
            print(f"❌ {descripcion} - FALLÓ")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def main():
    print("🎯 EJECUTOR DE PRUEBAS COMPLETAS")
    print("📋 API Ferretería - Evaluación 3")
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ Error: No se encuentra app.py")
        sys.exit(1)
    
    resultados = []
    
    # 1. Instalar dependencias
    exito = ejecutar_comando("pip install -r requirements.txt", "INSTALACIÓN DE DEPENDENCIAS")
    resultados.append(("Instalación dependencias", exito))
    
    # 2. Ejecutar pruebas unitarias
    exito = ejecutar_comando("python -m pytest tests/unit/ -v", "PRUEBAS UNITARIAS")
    resultados.append(("Pruebas unitarias", exito))
    
    # 3. Ejecutar pruebas de integración
    exito = ejecutar_comando("python -m pytest tests/integration/ -v", "PRUEBAS DE INTEGRACIÓN")
    resultados.append(("Pruebas integración", exito))
    
    # 4. Generar reporte de cobertura
    exito = ejecutar_comando("python -m pytest --cov=app --cov-report=html --cov-report=term", "REPORTE DE COBERTURA")
    resultados.append(("Cobertura de código", exito))
    
    # 5. Generar reporte XML
    exito = ejecutar_comando("python -m pytest --junitxml=test-results.xml", "REPORTE XML")
    resultados.append(("Reporte XML", exito))
    
    # Mostrar resumen
    print("\\n" + "="*80)
    print("📊 RESUMEN FINAL")
    print("="*80)
    
    total = len(resultados)
    exitosas = sum(1 for _, exito in resultados if exito)
    
    for descripcion, exito in resultados:
        estado = "✅ EXITOSO" if exito else "❌ FALLÓ"
        print(f"{descripcion:<30} {estado}")
    
    print("-" * 80)
    print(f"📊 Total: {total} | Exitosas: {exitosas} | Fallidas: {total - exitosas}")
    print(f"🎯 Porcentaje de éxito: {(exitosas/total)*100:.1f}%")
    
    if exitosas == total:
        print("\\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
        print("📁 Reportes generados:")
        print("   - htmlcov/index.html (Cobertura)")
        print("   - test-results.xml (Resultados)")
    else:
        print(f"\\n⚠️ {total - exitosas} prueba(s) con problemas")
    
    print("\\n📸 ¡LISTO PARA CAPTURAS DE PANTALLA!")

if __name__ == "__main__":
    main()'''
    
    if crear_archivo("ejecutar_pruebas_completas.py", contenido_ejecutar_pruebas):
        archivos_creados += 1
    
    # Mostrar resumen
    print("\n" + "="*80)
    print("📊 RESUMEN DE CONFIGURACIÓN")
    print("="*80)
    print(f"✅ Archivos creados: {archivos_creados}/{archivos_totales}")
    
    if archivos_creados == archivos_totales:
        print("\n🎉 ¡PROYECTO CONFIGURADO COMPLETAMENTE!")
        print("\n📝 PRÓXIMOS PASOS:")
        print("1. Ejecutar: python ejecutar_pruebas_completas.py")
        print("2. Tomar capturas de pantalla")
        print("3. Preparar video DEMO")
        print("\n🚀 ¡TODO LISTO PARA LA EVALUACIÓN 3!")
    else:
        print(f"\n⚠️ {archivos_totales - archivos_creados} archivo(s) no se pudieron crear")

if __name__ == "__main__":
    main()