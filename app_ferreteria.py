"""
API REST para Ferretería - Sistema Completo
Sistema de gestión de productos, categorías y clientes
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import requests
import json
import uuid
from decimal import Decimal

# Configuración de la aplicación
app = Flask(__name__)
CORS(app)

# Configuración de base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "ferreteria.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos
db = SQLAlchemy(app)

# Modelos de datos
class Categoria(db.Model):
    """Modelo para categorías de productos"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    productos = db.relationship('Producto', backref='categoria_rel', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

class Producto(db.Model):
    """Modelo para productos de ferretería"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'categoria_id': self.categoria_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Cliente(db.Model):
    """Modelo para clientes"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

class Sucursal(db.Model):
    """Modelo para sucursales"""
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    activa = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'activa': self.activa
        }

class PedidoSucursal(db.Model):
    """Modelo para pedidos entre sucursales"""
    id = db.Column(db.Integer, primary_key=True)
    sucursal_origen_id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    sucursal_destino_id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    estado = db.Column(db.String(50), default='pendiente')  # pendiente, aprobado, enviado, recibido, cancelado
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    observaciones = db.Column(db.Text)
    
    # Relaciones
    sucursal_origen = db.relationship('Sucursal', foreign_keys=[sucursal_origen_id])
    sucursal_destino = db.relationship('Sucursal', foreign_keys=[sucursal_destino_id])
    items = db.relationship('ItemPedidoSucursal', backref='pedido', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sucursal_origen_id': self.sucursal_origen_id,
            'sucursal_destino_id': self.sucursal_destino_id,
            'estado': self.estado,
            'fecha_pedido': self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'observaciones': self.observaciones,
            'items': [item.to_dict() for item in self.items] if self.items else []
        }

class ItemPedidoSucursal(db.Model):
    """Modelo para items de pedidos entre sucursales"""
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido_sucursal.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad_solicitada = db.Column(db.Integer, nullable=False)
    cantidad_aprobada = db.Column(db.Integer, default=0)
    
    # Relaciones
    producto = db.relationship('Producto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else None,
            'cantidad_solicitada': self.cantidad_solicitada,
            'cantidad_aprobada': self.cantidad_aprobada
        }

class TransaccionPago(db.Model):
    """Modelo para transacciones de pago WebPay"""
    id = db.Column(db.Integer, primary_key=True)
    token_transaccion = db.Column(db.String(200), unique=True, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), default='iniciada')  # iniciada, aprobada, rechazada, anulada
    fecha_transaccion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    detalle = db.Column(db.Text)
    
    # Relación
    cliente = db.relationship('Cliente')
    
    def to_dict(self):
        return {
            'id': self.id,
            'token_transaccion': self.token_transaccion,
            'monto': self.monto,
            'estado': self.estado,
            'fecha_transaccion': self.fecha_transaccion.isoformat() if self.fecha_transaccion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'cliente_id': self.cliente_id,
            'detalle': self.detalle
        }

class ConversionMoneda(db.Model):
    """Modelo para conversiones de moneda"""
    id = db.Column(db.Integer, primary_key=True)
    moneda_origen = db.Column(db.String(3), nullable=False)  # CLP, USD, EUR
    moneda_destino = db.Column(db.String(3), nullable=False)
    tasa_cambio = db.Column(db.Float, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)
    activa = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'moneda_origen': self.moneda_origen,
            'moneda_destino': self.moneda_destino,
            'tasa_cambio': self.tasa_cambio,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'activa': self.activa
        }

# Servicios de negocio
class ProductoService:
    """Servicio para gestión de productos"""
    
    @staticmethod
    def crear_producto(data):
        """Crear un nuevo producto"""
        # Validaciones
        if not data.get('nombre'):
            raise ValueError("El nombre es obligatorio")
        
        if not data.get('precio') or data.get('precio') <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        
        if data.get('stock', 0) < 0:
            raise ValueError("El stock no puede ser negativo")
        
        # Crear producto
        producto = Producto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=data['precio'],
            stock=data.get('stock', 0),
            categoria_id=data.get('categoria_id')
        )
        
        db.session.add(producto)
        db.session.commit()
        
        return producto
    
    @staticmethod
    def obtener_productos(buscar=None):
        """Obtener lista de productos con búsqueda opcional"""
        query = Producto.query
        
        if buscar:
            query = query.filter(
                Producto.nombre.contains(buscar) | 
                Producto.descripcion.contains(buscar)
            )
        
        return query.all()
    
    @staticmethod
    def obtener_producto_por_id(producto_id):
        """Obtener producto por ID"""
        return Producto.query.get(producto_id)
    
    @staticmethod
    def actualizar_stock(producto_id, cantidad):
        """Actualizar stock de un producto"""
        producto = Producto.query.get(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        
        producto.stock = cantidad
        db.session.commit()
        
        return producto

class PedidoSucursalService:
    """Servicio para gestión de pedidos entre sucursales"""
    
    @staticmethod
    def crear_pedido(data):
        """Crear un nuevo pedido entre sucursales"""
        # Validaciones
        if not data.get('sucursal_origen_id') or not data.get('sucursal_destino_id'):
            raise ValueError("Sucursal origen y destino son obligatorias")
        
        if data.get('sucursal_origen_id') == data.get('sucursal_destino_id'):
            raise ValueError("La sucursal origen no puede ser igual a la destino")
        
        if not data.get('items') or len(data.get('items')) == 0:
            raise ValueError("El pedido debe tener al menos un item")
        
        # Verificar que las sucursales existan
        sucursal_origen = Sucursal.query.get(data['sucursal_origen_id'])
        sucursal_destino = Sucursal.query.get(data['sucursal_destino_id'])
        
        if not sucursal_origen or not sucursal_destino:
            raise ValueError("Una o ambas sucursales no existen")
        
        if not sucursal_origen.activa or not sucursal_destino.activa:
            raise ValueError("Una o ambas sucursales están inactivas")
        
        # Crear pedido
        pedido = PedidoSucursal(
            sucursal_origen_id=data['sucursal_origen_id'],
            sucursal_destino_id=data['sucursal_destino_id'],
            observaciones=data.get('observaciones', '')
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obtener el ID del pedido
        
        # Agregar items
        for item_data in data['items']:
            if not item_data.get('producto_id') or not item_data.get('cantidad_solicitada'):
                raise ValueError("Cada item debe tener producto_id y cantidad_solicitada")
            
            # Verificar que el producto exista
            producto = Producto.query.get(item_data['producto_id'])
            if not producto:
                raise ValueError(f"Producto con ID {item_data['producto_id']} no existe")
            
            item = ItemPedidoSucursal(
                pedido_id=pedido.id,
                producto_id=item_data['producto_id'],
                cantidad_solicitada=item_data['cantidad_solicitada']
            )
            
            db.session.add(item)
        
        db.session.commit()
        return pedido
    
    @staticmethod
    def aprobar_pedido(pedido_id, aprobaciones):
        """Aprobar un pedido con cantidades específicas"""
        pedido = PedidoSucursal.query.get(pedido_id)
        if not pedido:
            raise ValueError("Pedido no encontrado")
        
        if pedido.estado != 'pendiente':
            raise ValueError("Solo se pueden aprobar pedidos pendientes")
        
        # Actualizar cantidades aprobadas
        for aprobacion in aprobaciones:
            item = ItemPedidoSucursal.query.filter_by(
                pedido_id=pedido_id,
                producto_id=aprobacion['producto_id']
            ).first()
            
            if item:
                item.cantidad_aprobada = aprobacion['cantidad_aprobada']
        
        pedido.estado = 'aprobado'
        pedido.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        return pedido

class WebPayService:
    """Servicio para integración con WebPay (simulado)"""
    
    @staticmethod
    def iniciar_transaccion(monto, cliente_id=None, detalle=""):
        """Iniciar una transacción de pago"""
        if not monto or monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        # Generar token único para la transacción
        token = str(uuid.uuid4())
        
        # Crear registro de transacción
        transaccion = TransaccionPago(
            token_transaccion=token,
            monto=monto,
            cliente_id=cliente_id,
            detalle=detalle
        )
        
        db.session.add(transaccion)
        db.session.commit()
        
        # Simular respuesta de WebPay
        return {
            'token': token,
            'url_pago': f'https://webpay-simulator.com/pay/{token}',
            'monto': monto,
            'estado': 'iniciada'
        }
    
    @staticmethod
    def confirmar_transaccion(token, estado_pago="aprobada"):
        """Confirmar el resultado de una transacción"""
        transaccion = TransaccionPago.query.filter_by(token_transaccion=token).first()
        
        if not transaccion:
            raise ValueError("Transacción no encontrada")
        
        if transaccion.estado != 'iniciada':
            raise ValueError("La transacción ya fue procesada")
        
        # Actualizar estado
        transaccion.estado = estado_pago
        transaccion.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        
        return transaccion

class CambioDivisasService:
    """Servicio para cambio de divisas"""
    
    # Tasas de cambio simuladas (en un caso real se obtendría de una API externa)
    TASAS_CAMBIO = {
        'CLP_USD': 0.0011,  # 1 CLP = 0.0011 USD
        'USD_CLP': 900.0,   # 1 USD = 900 CLP
        'CLP_EUR': 0.00095, # 1 CLP = 0.00095 EUR
        'EUR_CLP': 1050.0,  # 1 EUR = 1050 CLP
        'USD_EUR': 0.85,    # 1 USD = 0.85 EUR
        'EUR_USD': 1.18     # 1 EUR = 1.18 USD
    }
    
    @staticmethod
    def obtener_tasa_cambio(moneda_origen, moneda_destino):
        """Obtener tasa de cambio entre dos monedas"""
        if moneda_origen == moneda_destino:
            return 1.0
        
        clave = f"{moneda_origen}_{moneda_destino}"
        
        # Buscar en base de datos primero
        conversion = ConversionMoneda.query.filter_by(
            moneda_origen=moneda_origen,
            moneda_destino=moneda_destino,
            activa=True
        ).first()
        
        if conversion:
            return conversion.tasa_cambio
        
        # Si no está en BD, usar tasas simuladas
        if clave in CambioDivisasService.TASAS_CAMBIO:
            tasa = CambioDivisasService.TASAS_CAMBIO[clave]
            
            # Guardar en BD para futuras consultas
            nueva_conversion = ConversionMoneda(
                moneda_origen=moneda_origen,
                moneda_destino=moneda_destino,
                tasa_cambio=tasa
            )
            db.session.add(nueva_conversion)
            db.session.commit()
            
            return tasa
        
        raise ValueError(f"Conversión no disponible para {moneda_origen} a {moneda_destino}")
    
    @staticmethod
    def convertir_monto(monto, moneda_origen, moneda_destino):
        """Convertir un monto de una moneda a otra"""
        if not monto or monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        tasa = CambioDivisasService.obtener_tasa_cambio(moneda_origen, moneda_destino)
        monto_convertido = round(monto * tasa, 2)
        
        return {
            'monto_original': monto,
            'moneda_origen': moneda_origen,
            'monto_convertido': monto_convertido,
            'moneda_destino': moneda_destino,
            'tasa_cambio': tasa,
            'fecha_conversion': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def actualizar_tasas_cambio():
        """Actualizar tasas de cambio (simulado - en producción consultaría API externa)"""
        import random
        
        actualizadas = 0
        for clave, tasa_base in CambioDivisasService.TASAS_CAMBIO.items():
            moneda_origen, moneda_destino = clave.split('_')
            
            # Simular fluctuación del ±5%
            variacion = random.uniform(-0.05, 0.05)
            nueva_tasa = round(tasa_base * (1 + variacion), 6)
            
            # Buscar conversión existente
            conversion = ConversionMoneda.query.filter_by(
                moneda_origen=moneda_origen,
                moneda_destino=moneda_destino,
                activa=True
            ).first()
            
            if conversion:
                conversion.tasa_cambio = nueva_tasa
                conversion.fecha_actualizacion = datetime.utcnow()
            else:
                nueva_conversion = ConversionMoneda(
                    moneda_origen=moneda_origen,
                    moneda_destino=moneda_destino,
                    tasa_cambio=nueva_tasa
                )
                db.session.add(nueva_conversion)
            
            actualizadas += 1
        
        db.session.commit()
        return f"Se actualizaron {actualizadas} tasas de cambio"

# Endpoints de la API

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/productos', methods=['GET', 'POST'])
def gestionar_productos():
    """Gestionar productos (GET: listar, POST: crear)"""
    
    if request.method == 'GET':
        # Obtener productos con búsqueda opcional
        buscar = request.args.get('buscar')
        productos = ProductoService.obtener_productos(buscar)
        return jsonify([producto.to_dict() for producto in productos])
    
    elif request.method == 'POST':
        # Crear nuevo producto
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos requeridos'}), 400
            
            producto = ProductoService.crear_producto(data)
            return jsonify(producto.to_dict()), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    """Obtener producto específico por ID"""
    producto = ProductoService.obtener_producto_por_id(producto_id)
    
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    return jsonify(producto.to_dict())

@app.route('/productos/<int:producto_id>/stock', methods=['PUT'])
def actualizar_stock_producto(producto_id):
    """Actualizar stock de un producto"""
    try:
        data = request.get_json()
        if not data or 'cantidad' not in data:
            return jsonify({'error': 'Cantidad requerida'}), 400
        
        cantidad = data['cantidad']
        producto = ProductoService.actualizar_stock(producto_id, cantidad)
        
        return jsonify(producto.to_dict())
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/categorias', methods=['GET', 'POST'])
def gestionar_categorias():
    """Gestionar categorías (GET: listar, POST: crear)"""
    
    if request.method == 'GET':
        # Obtener todas las categorías
        categorias = Categoria.query.all()
        return jsonify([categoria.to_dict() for categoria in categorias])
    
    elif request.method == 'POST':
        # Crear nueva categoría
        try:
            data = request.get_json()
            if not data or not data.get('nombre'):
                return jsonify({'error': 'Nombre de categoría requerido'}), 400
            
            categoria = Categoria(
                nombre=data['nombre'],
                descripcion=data.get('descripcion', '')
            )
            
            db.session.add(categoria)
            db.session.commit()
            
            return jsonify(categoria.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/clientes', methods=['GET', 'POST'])
def gestionar_clientes():
    """Gestionar clientes (GET: listar, POST: crear)"""
    
    if request.method == 'GET':
        # Obtener todos los clientes
        clientes = Cliente.query.all()
        return jsonify([cliente.to_dict() for cliente in clientes])
    
    elif request.method == 'POST':
        # Crear nuevo cliente
        try:
            data = request.get_json()
            if not data or not data.get('nombre') or not data.get('email'):
                return jsonify({'error': 'Nombre y email son requeridos'}), 400
            
            # Verificar que el email no exista
            cliente_existente = Cliente.query.filter_by(email=data['email']).first()
            if cliente_existente:
                return jsonify({'error': 'El email ya está registrado'}), 400
            
            cliente = Cliente(
                nombre=data['nombre'],
                email=data['email'],
                telefono=data.get('telefono', ''),
                direccion=data.get('direccion', '')
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            return jsonify(cliente.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

# Endpoints para Sucursales
@app.route('/sucursales', methods=['GET', 'POST'])
def gestionar_sucursales():
    """Gestionar sucursales (GET: listar, POST: crear)"""
    
    if request.method == 'GET':
        # Obtener todas las sucursales
        sucursales = Sucursal.query.all()
        return jsonify([sucursal.to_dict() for sucursal in sucursales])
    
    elif request.method == 'POST':
        # Crear nueva sucursal
        try:
            data = request.get_json()
            if not data or not data.get('nombre') or not data.get('direccion'):
                return jsonify({'error': 'Nombre y dirección son requeridos'}), 400
            
            sucursal = Sucursal(
                nombre=data['nombre'],
                direccion=data['direccion'],
                telefono=data.get('telefono', ''),
                email=data.get('email', '')
            )
            
            db.session.add(sucursal)
            db.session.commit()
            
            return jsonify(sucursal.to_dict()), 201
            
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

# Endpoints para Pedidos entre Sucursales
@app.route('/pedidos-sucursal', methods=['GET', 'POST'])
def gestionar_pedidos_sucursal():
    """Gestionar pedidos entre sucursales"""
    
    if request.method == 'GET':
        # Obtener pedidos con filtros opcionales
        sucursal_origen = request.args.get('sucursal_origen')
        sucursal_destino = request.args.get('sucursal_destino')
        estado = request.args.get('estado')
        
        query = PedidoSucursal.query
        
        if sucursal_origen:
            query = query.filter_by(sucursal_origen_id=sucursal_origen)
        if sucursal_destino:
            query = query.filter_by(sucursal_destino_id=sucursal_destino)
        if estado:
            query = query.filter_by(estado=estado)
        
        pedidos = query.all()
        return jsonify([pedido.to_dict() for pedido in pedidos])
    
    elif request.method == 'POST':
        # Crear nuevo pedido
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Datos requeridos'}), 400
            
            pedido = PedidoSucursalService.crear_pedido(data)
            return jsonify(pedido.to_dict()), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/pedidos-sucursal/<int:pedido_id>/aprobar', methods=['PUT'])
def aprobar_pedido_sucursal(pedido_id):
    """Aprobar un pedido entre sucursales"""
    try:
        data = request.get_json()
        if not data or 'aprobaciones' not in data:
            return jsonify({'error': 'Aprobaciones requeridas'}), 400
        
        pedido = PedidoSucursalService.aprobar_pedido(pedido_id, data['aprobaciones'])
        return jsonify(pedido.to_dict())
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# Endpoints para WebPay
@app.route('/webpay/iniciar', methods=['POST'])
def iniciar_pago_webpay():
    """Iniciar transacción de pago con WebPay"""
    try:
        data = request.get_json()
        if not data or not data.get('monto'):
            return jsonify({'error': 'Monto requerido'}), 400
        
        resultado = WebPayService.iniciar_transaccion(
            monto=data['monto'],
            cliente_id=data.get('cliente_id'),
            detalle=data.get('detalle', '')
        )
        
        return jsonify(resultado), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/webpay/confirmar', methods=['POST'])
def confirmar_pago_webpay():
    """Confirmar resultado de transacción WebPay"""
    try:
        data = request.get_json()
        if not data or not data.get('token'):
            return jsonify({'error': 'Token requerido'}), 400
        
        transaccion = WebPayService.confirmar_transaccion(
            token=data['token'],
            estado_pago=data.get('estado', 'aprobada')
        )
        
        return jsonify(transaccion.to_dict())
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/webpay/transacciones', methods=['GET'])
def listar_transacciones_webpay():
    """Listar transacciones de WebPay"""
    estado = request.args.get('estado')
    cliente_id = request.args.get('cliente_id')
    
    query = TransaccionPago.query
    
    if estado:
        query = query.filter_by(estado=estado)
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    
    transacciones = query.order_by(TransaccionPago.fecha_transaccion.desc()).all()
    return jsonify([transaccion.to_dict() for transaccion in transacciones])

# Endpoints para Cambio de Divisas
@app.route('/divisas/convertir', methods=['POST'])
def convertir_divisas():
    """Convertir monto entre divisas"""
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['monto', 'moneda_origen', 'moneda_destino']):
            return jsonify({'error': 'Monto, moneda_origen y moneda_destino son requeridos'}), 400
        
        resultado = CambioDivisasService.convertir_monto(
            monto=data['monto'],
            moneda_origen=data['moneda_origen'].upper(),
            moneda_destino=data['moneda_destino'].upper()
        )
        
        return jsonify(resultado)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/divisas/tasas', methods=['GET'])
def obtener_tasas_cambio():
    """Obtener todas las tasas de cambio disponibles"""
    tasas = ConversionMoneda.query.filter_by(activa=True).all()
    return jsonify([tasa.to_dict() for tasa in tasas])

@app.route('/divisas/actualizar-tasas', methods=['POST'])
def actualizar_tasas_cambio():
    """Actualizar tasas de cambio"""
    try:
        resultado = CambioDivisasService.actualizar_tasas_cambio()
        return jsonify({'mensaje': resultado})
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# Endpoint de Catálogo Completo (Integración 1)
@app.route('/catalogo', methods=['GET'])
def obtener_catalogo_completo():
    """Obtener catálogo completo con productos, categorías y precios en diferentes monedas"""
    try:
        # Obtener parámetros
        moneda = request.args.get('moneda', 'CLP').upper()
        categoria_id = request.args.get('categoria_id')
        buscar = request.args.get('buscar')
        
        # Obtener productos
        query = Producto.query
        
        if categoria_id:
            query = query.filter_by(categoria_id=categoria_id)
        
        if buscar:
            query = query.filter(
                Producto.nombre.contains(buscar) | 
                Producto.descripcion.contains(buscar)
            )
        
        productos = query.all()
        
        # Convertir precios si es necesario
        catalogo = []
        for producto in productos:
            item = producto.to_dict()
            
            if moneda != 'CLP':
                try:
                    conversion = CambioDivisasService.convertir_monto(
                        producto.precio, 'CLP', moneda
                    )
                    item['precio_original'] = producto.precio
                    item['precio'] = conversion['monto_convertido']
                    item['moneda'] = moneda
                    item['tasa_cambio'] = conversion['tasa_cambio']
                except:
                    item['precio_original'] = producto.precio
                    item['moneda'] = 'CLP'
                    item['error_conversion'] = f'No se pudo convertir a {moneda}'
            else:
                item['moneda'] = 'CLP'
            
            # Agregar información de categoría
            if producto.categoria_rel:
                item['categoria'] = producto.categoria_rel.to_dict()
            
            catalogo.append(item)
        
        # Obtener categorías
        categorias = Categoria.query.all()
        
        return jsonify({
            'productos': catalogo,
            'categorias': [cat.to_dict() for cat in categorias],
            'total_productos': len(catalogo),
            'moneda_consulta': moneda,
            'filtros_aplicados': {
                'categoria_id': categoria_id,
                'buscar': buscar
            }
        })
        
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# Inicialización de la base de datos
def init_db():
    """Inicializar base de datos con datos de ejemplo"""
    with app.app_context():
        db.create_all()
        
        # Crear categorías de ejemplo si no existen
        if Categoria.query.count() == 0:
            categorias_ejemplo = [
                Categoria(nombre='Herramientas Manuales', descripcion='Herramientas que no requieren electricidad'),
                Categoria(nombre='Herramientas Eléctricas', descripcion='Herramientas que requieren electricidad'),
                Categoria(nombre='Materiales de Construcción', descripcion='Materiales para construcción y reparación')
            ]
            
            for categoria in categorias_ejemplo:
                db.session.add(categoria)
            
            db.session.commit()
            print("✅ Categorías de ejemplo creadas")
        
        # Crear productos de ejemplo si no existen
        if Producto.query.count() == 0:
            productos_ejemplo = [
                Producto(nombre='Martillo', descripcion='Martillo de acero 500g', precio=25.50, stock=15, categoria_id=1),
                Producto(nombre='Destornillador Phillips', descripcion='Destornillador Phillips #2', precio=12.75, stock=25, categoria_id=1),
                Producto(nombre='Taladro Eléctrico', descripcion='Taladro eléctrico 600W', precio=89.90, stock=8, categoria_id=2),
                Producto(nombre='Tornillos', descripcion='Tornillos para madera 3x25mm (100 unidades)', precio=8.50, stock=50, categoria_id=3)
            ]
            
            for producto in productos_ejemplo:
                db.session.add(producto)
            
            db.session.commit()
            print("✅ Productos de ejemplo creados")
        
        # Crear sucursales de ejemplo si no existen
        if Sucursal.query.count() == 0:
            sucursales_ejemplo = [
                Sucursal(nombre='Sucursal Centro', direccion='Av. Principal 123, Santiago Centro', telefono='22-123-4567', email='centro@ferreteria.cl'),
                Sucursal(nombre='Sucursal Las Condes', direccion='Av. Apoquindo 456, Las Condes', telefono='22-234-5678', email='lascondes@ferreteria.cl'),
                Sucursal(nombre='Sucursal Maipú', direccion='Av. Pajaritos 789, Maipú', telefono='22-345-6789', email='maipu@ferreteria.cl')
            ]
            
            for sucursal in sucursales_ejemplo:
                db.session.add(sucursal)
            
            db.session.commit()
            print("✅ Sucursales de ejemplo creadas")
        
        # Crear clientes de ejemplo si no existen
        if Cliente.query.count() == 0:
            clientes_ejemplo = [
                Cliente(nombre='Juan Pérez', email='juan.perez@email.com', telefono='9-8765-4321', direccion='Calle Falsa 123'),
                Cliente(nombre='María González', email='maria.gonzalez@email.com', telefono='9-7654-3210', direccion='Av. Siempre Viva 456')
            ]
            
            for cliente in clientes_ejemplo:
                db.session.add(cliente)
            
            db.session.commit()
            print("✅ Clientes de ejemplo creados")
        
        # Inicializar tasas de cambio
        if ConversionMoneda.query.count() == 0:
            resultado = CambioDivisasService.actualizar_tasas_cambio()
            print(f"✅ {resultado}")

if __name__ == '__main__':
    init_db()
    print("🚀 Iniciando API de Ferretería...")
    print("📋 Endpoints disponibles:")
    print("   === BÁSICOS ===")
    print("   GET  /health - Health check")
    print("   GET  /catalogo - Catálogo completo con conversión de monedas")
    print("   === PRODUCTOS ===")
    print("   GET  /productos - Listar productos")
    print("   POST /productos - Crear producto")
    print("   GET  /productos/<id> - Obtener producto")
    print("   PUT  /productos/<id>/stock - Actualizar stock")
    print("   === CATEGORÍAS ===")
    print("   GET  /categorias - Listar categorías")
    print("   POST /categorias - Crear categoría")
    print("   === CLIENTES ===")
    print("   GET  /clientes - Listar clientes")
    print("   POST /clientes - Crear cliente")
    print("   === SUCURSALES ===")
    print("   GET  /sucursales - Listar sucursales")
    print("   POST /sucursales - Crear sucursal")
    print("   === PEDIDOS ENTRE SUCURSALES ===")
    print("   GET  /pedidos-sucursal - Listar pedidos")
    print("   POST /pedidos-sucursal - Crear pedido")
    print("   PUT  /pedidos-sucursal/<id>/aprobar - Aprobar pedido")
    print("   === WEBPAY ===")
    print("   POST /webpay/iniciar - Iniciar transacción")
    print("   POST /webpay/confirmar - Confirmar transacción")
    print("   GET  /webpay/transacciones - Listar transacciones")
    print("   === CAMBIO DE DIVISAS ===")
    print("   POST /divisas/convertir - Convertir montos")
    print("   GET  /divisas/tasas - Obtener tasas de cambio")
    print("   POST /divisas/actualizar-tasas - Actualizar tasas")
    print("🌐 Servidor ejecutándose en: http://127.0.0.1:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)