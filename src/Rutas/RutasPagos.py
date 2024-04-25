from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioPagos import ServicioPagos
#timezone
import datetime
#pytz
import pytz
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

@main.route("/crear/<int:usr_id>", methods=['GET','POST'])
def crear_pago(usr_id):
    has_access = Security.verify_token(request.headers)
    monto = request.json['monto']
    fecha = datetime.datetime.now(tz=pytz.timezone('America/Lima')).isoformat()
    pago = [usr_id,fecha,monto]
    if has_access:
        try:
            pagos = ServicioPagos.crear_pago_unico(pago)
            if pagos == True:
                return jsonify({'pagos': pagos, 'message': "Se registró el pago correctamente", 'success': True})
            else:
                return jsonify({'message': "El usuario no fue encontrado", 'success': True})
        except ExcepcionPersonalizada:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401