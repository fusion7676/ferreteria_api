"""
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
        assert 'id' in data

class TestSucursalesEndpoints:
    """Pruebas para endpoints de sucursales"""
    
    def test_crear_sucursal_valida(self, client):
        """Probar crear sucursal válida"""
        sucursal_data = {
            'nombre': 'Sucursal Test',
            'direccion': 'Calle Test 123',
            'telefono': '22-123-4567',
            'email': 'test@ferreteria.cl'
        }
        
        response = client.post('/sucursales',
                             data=json.dumps(sucursal_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['nombre'] == sucursal_data['nombre']
        assert data['direccion'] == sucursal_data['direccion']
        assert 'id' in data
    
    def test_listar_sucursales(self, client):
        """Probar listar sucursales"""
        response = client.get('/sucursales')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)

class TestPedidosSucursalEndpoints:
    """Pruebas para endpoints de pedidos entre sucursales"""
    
    def test_crear_pedido_sucursal_valido(self, client):
        """Probar crear pedido entre sucursales válido"""
        # Primero crear sucursales
        sucursal1_data = {'nombre': 'Sucursal 1', 'direccion': 'Dir 1'}
        sucursal2_data = {'nombre': 'Sucursal 2', 'direccion': 'Dir 2'}
        
        response1 = client.post('/sucursales', data=json.dumps(sucursal1_data), content_type='application/json')
        response2 = client.post('/sucursales', data=json.dumps(sucursal2_data), content_type='application/json')
        
        sucursal1 = json.loads(response1.data)
        sucursal2 = json.loads(response2.data)
        
        # Crear producto
        producto_data = {'nombre': 'Producto Test', 'precio': 10.0, 'stock': 100}
        response_prod = client.post('/productos', data=json.dumps(producto_data), content_type='application/json')
        producto = json.loads(response_prod.data)
        
        # Crear pedido
        pedido_data = {
            'sucursal_origen_id': sucursal1['id'],
            'sucursal_destino_id': sucursal2['id'],
            'items': [
                {'producto_id': producto['id'], 'cantidad_solicitada': 5}
            ],
            'observaciones': 'Pedido de prueba'
        }
        
        response = client.post('/pedidos-sucursal',
                             data=json.dumps(pedido_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['sucursal_origen_id'] == sucursal1['id']
        assert data['sucursal_destino_id'] == sucursal2['id']
        assert len(data['items']) == 1

class TestWebPayEndpoints:
    """Pruebas para endpoints de WebPay"""
    
    def test_iniciar_transaccion_webpay(self, client):
        """Probar iniciar transacción WebPay"""
        transaccion_data = {
            'monto': 50000,
            'detalle': 'Compra de herramientas'
        }
        
        response = client.post('/webpay/iniciar',
                             data=json.dumps(transaccion_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['monto'] == transaccion_data['monto']
        assert 'token' in data
        assert 'url_pago' in data
        assert data['estado'] == 'iniciada'
    
    def test_confirmar_transaccion_webpay(self, client):
        """Probar confirmar transacción WebPay"""
        # Primero iniciar transacción
        transaccion_data = {'monto': 25000}
        response_init = client.post('/webpay/iniciar',
                                  data=json.dumps(transaccion_data),
                                  content_type='application/json')
        
        init_data = json.loads(response_init.data)
        token = init_data['token']
        
        # Confirmar transacción
        confirmacion_data = {
            'token': token,
            'estado': 'aprobada'
        }
        
        response = client.post('/webpay/confirmar',
                             data=json.dumps(confirmacion_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['token_transaccion'] == token
        assert data['estado'] == 'aprobada'
    
    def test_listar_transacciones_webpay(self, client):
        """Probar listar transacciones WebPay"""
        response = client.get('/webpay/transacciones')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)

class TestDivisasEndpoints:
    """Pruebas para endpoints de cambio de divisas"""
    
    def test_convertir_divisas(self, client):
        """Probar conversión de divisas"""
        conversion_data = {
            'monto': 1000,
            'moneda_origen': 'CLP',
            'moneda_destino': 'USD'
   