"""
Pruebas de integración para la API Ferretería
"""
import json

class TestIntegracionCatalogo:
    """Pruebas de integración para el catálogo completo"""
    
    def test_flujo_completo_catalogo(self, client):
        """Probar flujo completo del catálogo con todas las integraciones"""
        # 1. Crear categoría
        categoria_data = {
            'nombre': 'Herramientas Eléctricas',
            'descripcion': 'Herramientas que requieren electricidad'
        }
        response = client.post('/categorias', 
                             data=json.dumps(categoria_data),
                             content_type='application/json')
        assert response.status_code == 201
        categoria = json.loads(response.data)
        
        # 2. Crear productos
        productos_data = [
            {
                'nombre': 'Taladro Profesional',
                'descripcion': 'Taladro de alta potencia',
                'precio': 89900,  # En CLP
                'stock': 15,
                'categoria_id': categoria['id']
            },
            {
                'nombre': 'Sierra Circular',
                'descripcion': 'Sierra circular para madera',
                'precio': 125000,  # En CLP
                'stock': 8,
                'categoria_id': categoria['id']
            }
        ]
        
        productos_creados = []
        for producto_data in productos_data:
            response = client.post('/productos',
                                 data=json.dumps(producto_data),
                                 content_type='application/json')
            assert response.status_code == 201
            productos_creados.append(json.loads(response.data))
        
        # 3. Obtener catálogo en CLP
        response = client.get('/catalogo')
        assert response.status_code == 200
        catalogo_clp = json.loads(response.data)
        
        assert len(catalogo_clp['productos']) >= 2
        assert catalogo_clp['moneda_consulta'] == 'CLP'
        assert len(catalogo_clp['categorias']) >= 1
        
        # 4. Obtener catálogo en USD (integración cambio de divisas)
        response = client.get('/catalogo?moneda=USD')
        assert response.status_code == 200
        catalogo_usd = json.loads(response.data)
        
        assert catalogo_usd['moneda_consulta'] == 'USD'
        
        # 5. Filtrar catálogo por categoría
        response = client.get(f'/catalogo?categoria_id={categoria["id"]}')
        assert response.status_code == 200
        catalogo_filtrado = json.loads(response.data)
        
        assert len(catalogo_filtrado['productos']) == 2
        for producto in catalogo_filtrado['productos']:
            assert producto['categoria_id'] == categoria['id']

class TestIntegracionPedidosSucursal:
    """Pruebas de integración para pedidos entre sucursales"""
    
    def test_flujo_completo_pedidos_sucursal(self, client):
        """Probar flujo completo de pedidos entre sucursales"""
        # 1. Crear sucursales
        sucursales_data = [
            {
                'nombre': 'Sucursal Centro',
                'direccion': 'Av. Principal 123',
                'telefono': '22-123-4567',
                'email': 'centro@ferreteria.cl'
            },
            {
                'nombre': 'Sucursal Las Condes',
                'direccion': 'Av. Apoquindo 456',
                'telefono': '22-234-5678',
                'email': 'lascondes@ferreteria.cl'
            }
        ]
        
        sucursales_creadas = []
        for sucursal_data in sucursales_data:
            response = client.post('/sucursales',
                                 data=json.dumps(sucursal_data),
                                 content_type='application/json')
            assert response.status_code == 201
            sucursales_creadas.append(json.loads(response.data))
        
        # 2. Crear productos
        productos_data = [
            {'nombre': 'Martillo', 'precio': 25000, 'stock': 50},
            {'nombre': 'Destornillador', 'precio': 15000, 'stock': 30}
        ]
        
        productos_creados = []
        for producto_data in productos_data:
            response = client.post('/productos',
                                 data=json.dumps(producto_data),
                                 content_type='application/json')
            assert response.status_code == 201
            productos_creados.append(json.loads(response.data))
        
        # 3. Crear pedido entre sucursales
        pedido_data = {
            'sucursal_origen_id': sucursales_creadas[0]['id'],
            'sucursal_destino_id': sucursales_creadas[1]['id'],
            'items': [
                {
                    'producto_id': productos_creados[0]['id'],
                    'cantidad_solicitada': 10
                },
                {
                    'producto_id': productos_creados[1]['id'],
                    'cantidad_solicitada': 5
                }
            ],
            'observaciones': 'Pedido urgente para reposición'
        }
        
        response = client.post('/pedidos-sucursal',
                             data=json.dumps(pedido_data),
                             content_type='application/json')
        assert response.status_code == 201
        pedido_creado = json.loads(response.data)
        
        assert pedido_creado['estado'] == 'pendiente'
        assert len(pedido_creado['items']) == 2
        
        # 4. Aprobar pedido
        aprobaciones_data = {
            'aprobaciones': [
                {
                    'producto_id': productos_creados[0]['id'],
                    'cantidad_aprobada': 8  # Aprobar menos de lo solicitado
                },
                {
                    'producto_id': productos_creados[1]['id'],
                    'cantidad_aprobada': 5  # Aprobar todo lo solicitado
                }
            ]
        }
        
        response = client.put(f'/pedidos-sucursal/{pedido_creado["id"]}/aprobar',
                            data=json.dumps(aprobaciones_data),
                            content_type='application/json')
        assert response.status_code == 200
        pedido_aprobado = json.loads(response.data)
        
        assert pedido_aprobado['estado'] == 'aprobado'
        
        # 5. Listar pedidos con filtros
        response = client.get(f'/pedidos-sucursal?sucursal_origen={sucursales_creadas[0]["id"]}')
        assert response.status_code == 200
        pedidos_filtrados = json.loads(response.data)
        
        assert len(pedidos_filtrados) == 1
        assert pedidos_filtrados[0]['id'] == pedido_creado['id']

class TestIntegracionWebPay:
    """Pruebas de integración para WebPay"""
    
    def test_flujo_completo_webpay(self, client):
        """Probar flujo completo de pago con WebPay"""
        # 1. Crear cliente
        cliente_data = {
            'nombre': 'Juan Pérez',
            'email': 'juan.perez@email.com',
            'telefono': '9-8765-4321',
            'direccion': 'Calle Falsa 123'
        }
        
        response = client.post('/clientes',
                             data=json.dumps(cliente_data),
                             content_type='application/json')
        assert response.status_code == 201
        cliente_creado = json.loads(response.data)
        
        # 2. Iniciar transacción WebPay
        transaccion_data = {
            'monto': 75000,
            'cliente_id': cliente_creado['id'],
            'detalle': 'Compra de herramientas - Martillo y Destornillador'
        }
        
        response = client.post('/webpay/iniciar',
                             data=json.dumps(transaccion_data),
                             content_type='application/json')
        assert response.status_code == 201
        transaccion_iniciada = json.loads(response.data)
        
        assert transaccion_iniciada['monto'] == 75000
        assert 'token' in transaccion_iniciada
        assert 'url_pago' in transaccion_iniciada
        assert transaccion_iniciada['estado'] == 'iniciada'
        
        # 3. Simular proceso de pago y confirmar
        confirmacion_data = {
            'token': transaccion_iniciada['token'],
            'estado': 'aprobada'
        }
        
        response = client.post('/webpay/confirmar',
                             data=json.dumps(confirmacion_data),
                             content_type='application/json')
        assert response.status_code == 200
        transaccion_confirmada = json.loads(response.data)
        
        assert transaccion_confirmada['estado'] == 'aprobada'
        assert transaccion_confirmada['cliente_id'] == cliente_creado['id']
        
        # 4. Listar transacciones del cliente
        response = client.get(f'/webpay/transacciones?cliente_id={cliente_creado["id"]}')
        assert response.status_code == 200
        transacciones_cliente = json.loads(response.data)
        
        assert len(transacciones_cliente) == 1
        assert transacciones_cliente[0]['id'] == transaccion_confirmada['id']

class TestIntegracionCambioDivisas:
    """Pruebas de integración para cambio de divisas"""
    
    def test_flujo_completo_cambio_divisas(self, client):
        """Probar flujo completo de cambio de divisas"""
        # 1. Actualizar tasas de cambio
        response = client.post('/divisas/actualizar-tasas')
        assert response.status_code == 200
        resultado_actualizacion = json.loads(response.data)
        
        assert 'mensaje' in resultado_actualizacion
        assert 'actualizaron' in resultado_actualizacion['mensaje']
        
        # 2. Obtener tasas de cambio disponibles
        response = client.get('/divisas/tasas')
        assert response.status_code == 200
        tasas_disponibles = json.loads(response.data)
        
        assert len(tasas_disponibles) > 0
        
        # 3. Convertir diferentes montos y monedas
        conversiones_test = [
            {'monto': 100000, 'origen': 'CLP', 'destino': 'USD'},
            {'monto': 100, 'origen': 'USD', 'destino': 'CLP'},
            {'monto': 50000, 'origen': 'CLP', 'destino': 'EUR'}
        ]
        
        for conversion_test in conversiones_test:
            conversion_data = {
                'monto': conversion_test['monto'],
                'moneda_origen': conversion_test['origen'],
                'moneda_destino': conversion_test['destino']
            }
            
            response = client.post('/divisas/convertir',
                                 data=json.dumps(conversion_data),
                                 content_type='application/json')
            assert response.status_code == 200
            resultado_conversion = json.loads(response.data)
            
            assert resultado_conversion['monto_original'] == conversion_test['monto']
            assert resultado_conversion['moneda_origen'] == conversion_test['origen']
            assert resultado_conversion['moneda_destino'] == conversion_test['destino']
            assert 'monto_convertido' in resultado_conversion
            assert 'tasa_cambio' in resultado_conversion

class TestIntegracionCompleta:
    """Pruebas de integración que combinan todas las funcionalidades"""
    
    def test_escenario_compra_completa(self, client):
        """Probar escenario completo de compra con todas las integraciones"""
        # 1. Configurar datos base
        # Crear categoría
        categoria_data = {'nombre': 'Herramientas', 'descripcion': 'Herramientas varias'}
        response = client.post('/categorias', data=json.dumps(categoria_data), content_type='application/json')
        categoria = json.loads(response.data)
        
        # Crear productos
        producto_data = {
            'nombre': 'Kit Herramientas Básicas',
            'descripcion': 'Kit completo de herramientas básicas',
            'precio': 45000,  # CLP
            'stock': 20,
            'categoria_id': categoria['id']
        }
        response = client.post('/productos', data=json.dumps(producto_data), content_type='application/json')
        producto = json.loads(response.data)
        
        # Crear cliente
        cliente_data = {
            'nombre': 'María González',
            'email': 'maria.gonzalez@email.com',
            'telefono': '9-7654-3210'
        }
        response = client.post('/clientes', data=json.dumps(cliente_data), content_type='application/json')
        cliente = json.loads(response.data)
        
        # 2. Cliente consulta catálogo en USD
        response = client.get('/catalogo?moneda=USD')
        assert response.status_code == 200
        
        # 3. Cliente decide comprar y se inicia transacción WebPay
        transaccion_data = {
            'monto': producto['precio'],  # En CLP
            'cliente_id': cliente['id'],
            'detalle': f'Compra de {producto["nombre"]}'
        }
        
        response = client.post('/webpay/iniciar', data=json.dumps(transaccion_data), content_type='application/json')
        assert response.status_code == 201
        transaccion = json.loads(response.data)
        
        # 4. Se confirma el pago
        confirmacion_data = {
            'token': transaccion['token'],
            'estado': 'aprobada'
        }
        
        response = client.post('/webpay/confirmar', data=json.dumps(confirmacion_data), content_type='application/json')
        assert response.status_code == 200
        pago_confirmado = json.loads(response.data)
        
        assert pago_confirmado['estado'] == 'aprobada'
        
        # 5. Se actualiza el stock del producto
        nuevo_stock_data = {'cantidad': producto['stock'] - 1}
        response = client.put(f'/productos/{producto["id"]}/stock',
                            data=json.dumps(nuevo_stock_data),
                            content_type='application/json')
        assert response.status_code == 200
        producto_actualizado = json.loads(response.data)
        
        assert producto_actualizado['stock'] == producto['stock'] - 1 