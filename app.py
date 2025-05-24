from flask import Flask, jsonify, request, send_from_directory
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Para permitir peticiones desde frontend

# Crear instancia para sandbox
transaction = Transaction(IntegrationType.TEST)

# Datos de ejemplo para productos
productos = [
    {"id": 1, "nombre": "Martillo", "descripcion": "Martillo de acero", "precio": 12000, "stock": 15},
    {"id": 2, "nombre": "Destornillador", "descripcion": "Destornillador plano", "precio": 8000, "stock": 30},
    {"id": 3, "nombre": "Taladro", "descripcion": "Taladro eléctrico", "precio": 45000, "stock": 5}
]

# Lista para almacenar solicitudes
solicitudes = []

# Tasa simulada USD <-> CLP
TASA_USD_CLP = 800.0  # 1 USD = 800 CLP

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(productos), 200

@app.route('/solicitudes', methods=['POST'])
def crear_solicitud():
    data = request.get_json()
    if not data or "productos" not in data:
        return jsonify({"error": "Falta el campo 'productos' en el cuerpo"}), 400

    productos_solicitados = data["productos"]
    for item in productos_solicitados:
        if "id" not in item or "cantidad" not in item:
            return jsonify({"error": "Cada producto debe tener 'id' y 'cantidad'"}), 400

    solicitud_id = str(uuid.uuid4())
    solicitud = {
        "id": solicitud_id,
        "productos": productos_solicitados
    }
    solicitudes.append(solicitud)

    return jsonify({
        "mensaje": "Solicitud creada correctamente",
        "solicitud": solicitud
    }), 201

@app.route('/convertir', methods=['GET'])
def convertir_divisa():
    try:
        monto = float(request.args.get('monto', ''))
        moneda_origen = request.args.get('moneda_origen', '').upper()
        moneda_destino = request.args.get('moneda_destino', '').upper()
    except (ValueError, TypeError):
        return jsonify({"error": "Parámetros inválidos o faltantes"}), 400

    if not monto or not moneda_origen or not moneda_destino:
        return jsonify({"error": "Faltan parámetros requeridos"}), 400

    if moneda_origen == moneda_destino:
        return jsonify({
            "monto_original": monto,
            "monto_convertido": monto,
            "moneda_origen": moneda_origen,
            "moneda_destino": moneda_destino
        })

    if moneda_origen == 'USD' and moneda_destino == 'CLP':
        monto_convertido = monto * TASA_USD_CLP
    elif moneda_origen == 'CLP' and moneda_destino == 'USD':
        monto_convertido = monto / TASA_USD_CLP
    else:
        return jsonify({"error": "Moneda no soportada"}), 400

    return jsonify({
        "monto_original": monto,
        "monto_convertido": round(monto_convertido, 2),
        "moneda_origen": moneda_origen,
        "moneda_destino": moneda_destino
    })

# WebPay endpoints

@app.route('/pago/iniciar', methods=['POST'])
def iniciar_pago():
    data = request.get_json()
    if not data or "monto_total" not in data:
        return jsonify({"error": "Falta el campo 'monto_total'"}), 400

    monto = data["monto_total"]
    buy_order = uuid.uuid4().hex[:26]  # Acortado a 26 caracteres
    session_id = str(uuid.uuid4())
    return_url = request.host_url + 'pago/confirmar'

    try:
        response = transaction.create(
            buy_order=buy_order,
            session_id=session_id,
            amount=monto,
            return_url=return_url
        )
        return jsonify({
            "token": response.token,
            "url": response.url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pago/confirmar', methods=['GET'])
def confirmar_pago():
    token = request.args.get('token_ws')
    if not token:
        return "Token no recibido", 400

    try:
        result = transaction.commit(token)
        return jsonify({
            "status": "pago confirmado",
            "buy_order": result.buy_order,
            "session_id": result.session_id,
            "amount": result.amount,
            "card_detail": result.card_detail,
            "authorization_code": result.authorization_code,
            "payment_type_code": result.payment_type_code,
            "response_code": result.response_code
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)