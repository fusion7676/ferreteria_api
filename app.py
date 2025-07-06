"""
API REST para Ferretería - Sistema Completo
Sistema de gestión de productos, categorías y clientes
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

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
         

if __name__ == '__main__':
    app.run(debug=True)