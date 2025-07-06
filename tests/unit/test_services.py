"""
Pruebas unitarias para los servicios de negocio
"""
import pytest
from app_ferreteria import (
    ProductoService, PedidoSucursalService, WebPayService, CambioDivisasService,
    Producto, Sucursal, Cliente, TransaccionPago, ConversionMoneda
)

class TestProductoService:
    """Pruebas para ProductoService"""
    
    def test_crear_producto_valido(self, app):
        """Probar crear producto válido"""
        with app.app_context():
            data = {
                'nombre': 'Martillo Service Test',
                'descripcion': 'Martillo para pruebas de servicio',
                'precio': 25.50,
                'stock': 10
            }
            
            producto = ProductoService.crear_producto(data)
            
            assert producto.nombre == data['nombre']
            assert producto.precio == data['precio']
            assert producto.stock == data['stock']
            assert producto.id is not None
    
    def test_crear_producto_sin_nombre(self, app):
        """Probar crear producto sin nombre"""
        with app.app_context():
            data = {
                'precio': 25.50,
                'stock': 10
            }
            
            with pytest.raises(ValueError, match="El nombre es obligatorio"):
                ProductoService.crear_producto(data)
    
    def test_crear_producto_precio_invalido(self, app):
        """Probar crear producto con precio inválido"""
        with app.app_context():
            data = {
                'nombre': 'Producto Test',
                'precio': -10,
                'stock': 10
            }
            
            with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
                ProductoService.crear_producto(data)

class TestPedidoSucursalService:
    """Pruebas para PedidoSucursalService"""
    
    def test_crear_pedido_valido(self, app):
        """Probar crear pedido válido entre sucursales"""
        with app.app_context():
            # Crear sucursales
            sucursal1 = Sucursal(nombre='Sucursal 1', direccion='Dir 1')
            sucursal2 = Sucursal(nombre='Sucursal 2', direccion='Dir 2')
            
            from app_ferreteria import db
            db.session.add(sucursal1)
            db.session.add(sucursal2)
            db.session.flush()
            
            # Crear producto
            producto = Producto(nombre='Producto Test', precio=10.0, stock=100)
            db.session.add(producto)
            db.session.flush()
            
            # Crear pedido
            data = {
                'sucursal_origen_id': sucursal1.id,
                'sucursal_destino_id': sucursal2.id,
                'items': [
                    {'producto_id': producto.id, 'cantidad_solicitada': 5}
                ],
                'observaciones': 'Pedido de prueba'
            }
            
            pedido = PedidoSucursalService.crear_pedido(data)
            
            assert pedido.sucursal_origen_id == sucursal1.id
            assert pedido.sucursal_destino_id == sucursal2.id
            assert len(pedido.items) == 1
            assert pedido.estado == 'pendiente'
    
    def test_crear_pedido_misma_sucursal(self, app):
        """Probar crear pedido con misma sucursal origen y destino"""
        with app.app_context():
            data = {
                'sucursal_origen_id': 1,
                'sucursal_destino_id': 1,
                'items': [
                    {'producto_id': 1, 'cantidad_solicitada': 5}
                ]
            }
            
            with pytest.raises(ValueError, match="La sucursal origen no puede ser igual a la destino"):
                PedidoSucursalService.crear_pedido(data)

class TestWebPayService:
    """Pruebas para WebPayService"""
    
    def test_iniciar_transaccion_valida(self, app):
        """Probar iniciar transacción válida"""
        with app.app_context():
            resultado = WebPayService.iniciar_transaccion(
                monto=50000,
                detalle='Compra de herramientas'
            )
            
            assert resultado['monto'] == 50000
            assert 'token' in resultado
            assert 'url_pago' in resultado
            assert resultado['estado'] == 'iniciada'
    
    def test_iniciar_transaccion_monto_invalido(self, app):
        """Probar iniciar transacción con monto inválido"""
        with app.app_context():
            with pytest.raises(ValueError, match="El monto debe ser mayor a 0"):
                WebPayService.iniciar_transaccion(monto=-100)
    
    def test_confirmar_transaccion(self, app):
        """Probar confirmar transacción"""
        with app.app_context():
            # Iniciar transacción
            resultado = WebPayService.iniciar_transaccion(monto=25000)
            token = resultado['token']
            
            # Confirmar transacción
            transaccion = WebPayService.confirmar_transaccion(token, 'aprobada')
            
            assert transaccion.token_transaccion == token
            assert transaccion.estado == 'aprobada'

class TestCambioDivisasService:
    """Pruebas para CambioDivisasService"""
    
    def test_obtener_tasa_cambio_misma_moneda(self, app):
        """Probar obtener tasa de cambio para la misma moneda"""
        with app.app_context():
            tasa = CambioDivisasService.obtener_tasa_cambio('CLP', 'CLP')
            assert tasa == 1.0
    
    def test_convertir_monto_valido(self, app):
        """Probar convertir monto válido"""
        with app.app_context():
            resultado = CambioDivisasService.convertir_monto(
                monto=1000,
                moneda_origen='CLP',
                moneda_destino='USD'
            )
            
            assert resultado['monto_original'] == 1000
            assert resultado['moneda_origen'] == 'CLP'
            assert resultado['moneda_destino'] == 'USD'
            assert 'monto_convertido' in resultado
            assert 'tasa_cambio' in resultado
    
    def test_convertir_monto_invalido(self, app):
        """Probar convertir monto inválido"""
        with app.app_context():
            with pytest.raises(ValueError, match="El monto debe ser mayor a 0"):
                CambioDivisasService.convertir_monto(
                    monto=-100,
                    moneda_origen='CLP',
                    moneda_destino='USD'
                )
    
    def test_actualizar_tasas_cambio(self, app):
        """Probar actualizar tasas de cambio"""
        with app.app_context():
            resultado = CambioDivisasService.actualizar_tasas_cambio()
            assert "Se actualizaron" in resultado
            assert "tasas de cambio" in resultado