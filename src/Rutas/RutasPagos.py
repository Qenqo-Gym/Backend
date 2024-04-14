from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioPagos import ServicioPagos

main = Blueprint('pago_blueprint', __name__)


@main.route('/')
def get_pagos():
    has_access = Security.verify_token(request.headers)
    usr_id = request.json['usr_id']
    fecha = request.json['fecha']
    if has_access:
        try:
            pagos = ServicioPagos.get_pagos(usr_id,fecha)
            if (len(pagos) > 0):
                return jsonify({'pagos': pagos, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except ExcepcionPersonalizada:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401