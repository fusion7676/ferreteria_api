# API Ferretería - Sistema Completo de Gestión

## Descripción

API REST completa para la gestión de una ferretería que incluye 4 integraciones principales:

1. **Catálogo de Productos** - Gestión completa de productos y categorías
2. **Pedidos entre Sucursales** - Sistema de transferencias entre sucursales
3. **Pagos WebPay** - Integración simulada de pagos
4. **Cambio de Divisas** - Conversión de monedas en tiempo real

## Características Principales

- ✅ **4 Integraciones Completas**: Catálogo, Pedidos Sucursal, WebPay, Divisas
- ✅ **Funcionalidades Adyacentes**: Gestión de clientes, stock, categorías
- ✅ **Tests Unitarios Completos**: Cobertura de endpoints y servicios
- ✅ **Tests de Integración**: Flujos completos de negocio
- ✅ **Base de Datos SQLite**: Persistencia de datos
- ✅ **API REST**: Endpoints bien documentados
- ✅ **Manejo de Errores**: Respuestas HTTP apropiadas
- ✅ **CORS Habilitado**: Para desarrollo frontend

## Tecnologías Utilizadas

- **Python 3.8+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos
- **pytest** - Framework de testing
- **Flask-CORS** - Manejo de CORS

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd ferreteria_api
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python app_ferreteria.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Ejecución de Tests

### Tests Unitarios
```bash
# Ejecutar todos los tests unitarios
pytest tests/unit/ -v

# Ejecutar tests específicos
pytest tests/unit/test_api_endpoints.py -v
pytest tests/unit/test_services.py -v
```

### Tests de Integración
```bash
# Ejecutar todos los tests de integración
pytest tests/integration/ -v

# Ejecutar test específico
pytest tests/integration/test_integration.py -v
```

### Ejecutar Todos los Tests
```bash
# Ejecutar toda la suite de tests
pytest -v

# Con reporte de cobertura
pytest --cov=app_ferreteria tests/ -v
```

## Endpoints de la API

### 🏥 Health Check
- `GET /health` - Estado de la API

### 📦 Productos
- `GET /productos` - Listar productos (con filtros opcionales)
- `POST /productos` - Crear producto
- `GET /productos/{id}` - Obtener producto específico
- `PUT /productos/{id}/stock` - Actualizar stock

### 🏷️ Categorías
- `GET /categorias` - Listar categorías
- `POST /categorias` - Crear categoría

### 👥 Clientes
- `GET /clientes` - Listar clientes
- `POST /clientes` - Crear cliente

### 🏢 Sucursales
- `GET /sucursales` - Listar sucursales
- `POST /sucursales` - Crear sucursal

### 📋 Pedidos entre Sucursales
- `GET /pedidos-sucursal` - Listar pedidos (con filtros)
- `POST /pedidos-sucursal` - Crear pedido
- `PUT /pedidos-sucursal/{id}/aprobar` - Aprobar pedido

### 💳 WebPay (Pagos)
- `POST /webpay/iniciar` - Iniciar transacción
- `POST /webpay/confirmar` - Confirmar transacción
- `GET /webpay/transacciones` - Listar transacciones (con filtros)

### 💱 Cambio de Divisas
- `GET /divisas/tasas` - Obtener tasas de cambio
- `POST /divisas/convertir` - Convertir monto
- `POST /divisas/actualizar-tasas` - Actualizar tasas

### 📚 Catálogo Completo
- `GET /catalogo` - Catálogo completo con conversión de moneda

## Ejemplos de Uso

### 1. Crear un Producto
```bash
curl -X POST http://localhost:5000/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Martillo Profesional",
    "descripcion": "Martillo de acero forjado",
    "precio": 25000,
    "stock": 15
  }'
```

### 2. Obtener Catálogo en USD
```bash
curl "http://localhost:5000/catalogo?moneda=USD"
```

### 3. Crear Pedido entre Sucursales
```bash
curl -X POST http://localhost:5000/pedidos-sucursal \
  -H "Content-Type: application/json" \
  -d '{
    "sucursal_origen_id": 1,
    "sucursal_destino_id": 2,
    "items": [
      {
        "producto_id": 1,
        "cantidad_solicitada": 10
      }
    ],
    "observaciones": "Pedido urgente"
  }'
```

### 4. Iniciar Pago WebPay
```bash
curl -X POST http://localhost:5000/webpay/iniciar \
  -H "Content-Type: application/json" \
  -d '{
    "monto": 50000,
    "cliente_id": 1,
    "detalle": "Compra de herramientas"
  }'
```

### 5. Convertir Moneda
```bash
curl -X POST http://localhost:5000/divisas/convertir \
  -H "Content-Type: application/json" \
  -d '{
    "monto": 100000,
    "moneda_origen": "CLP",
    "moneda_destino": "USD"
  }'
```

## Estructura del Proyecto

```
ferreteria_api/
├── app_ferreteria.py          # Aplicación principal
├── requirements.txt           # Dependencias
├── README.md                 # Este archivo
├── ferreteria.db            # Base de datos SQLite (se crea automáticamente)
└── tests/
    ├── conftest.py          # Configuración de tests
    ├── unit/
    │   ├── test_api_endpoints.py  # Tests de endpoints
    │   └── test_services.py       # Tests de servicios
    └── integration/
        └── test_integration.py    # Tests de integración
```

## Datos de Prueba

Al ejecutar la aplicación por primera vez, se crean automáticamente:

- **3 Categorías** de productos
- **6 Productos** de ejemplo
- **2 Clientes** de prueba
- **2 Sucursales** de ejemplo
- **Tasas de cambio** iniciales (CLP, USD, EUR)

## Funcionalidades Destacadas

### 🔄 Integración Catálogo
- Listado completo de productos con categorías
- Filtrado por categoría, precio, stock
- Búsqueda por nombre/descripción
- Conversión automática de precios según moneda

### 🏢 Integración Pedidos Sucursal
- Creación de pedidos entre sucursales
- Gestión de estados (pendiente, aprobado, rechazado)
- Aprobación parcial de items
- Filtrado por sucursal y estado

### 💳 Integración WebPay
- Simulación completa del flujo de pago
- Generación de tokens únicos
- Estados de transacción (iniciada, aprobada, rechazada)
- Historial de transacciones por cliente

### 💱 Integración Cambio Divisas
- Soporte para CLP, USD, EUR
- Tasas de cambio simuladas pero realistas
- Actualización de tasas
- Conversión en tiempo real

## Consideraciones de Desarrollo

- **Base de Datos**: SQLite para simplicidad, fácil migración a PostgreSQL/MySQL
- **Autenticación**: No implementada (fuera del scope del examen)
- **Logging**: Básico, se puede extender
- **Validaciones**: Implementadas en servicios y endpoints
- **Error Handling**: Manejo apropiado de errores HTTP

## Comandos Útiles

```bash
# Ejecutar aplicación
python app_ferreteria.py

# Ejecutar todos los tests
pytest -v

# Ver cobertura de tests
pytest --cov=app_ferreteria tests/ -v

# Ejecutar solo tests unitarios
pytest tests/unit/ -v

# Ejecutar solo tests de integración
pytest tests/integration/ -v

# Limpiar base de datos (eliminar archivo)
rm ferreteria.db
```

## Estado del Proyecto

✅ **COMPLETO** - Proyecto funcional con:
- 4 integraciones robustas
- Funcionalidades adyacentes implementadas
- Suite completa de tests unitarios e integración
- Documentación completa de ejecución
- Datos de prueba incluidos
