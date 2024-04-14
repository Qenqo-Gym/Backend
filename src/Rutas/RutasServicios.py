from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioServicios import ServicioServicios

main = Blueprint('servicio_blueprint', __name__)


@main.route('/')
def get_servicios():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            servicios = ServicioServicios.get_servicios()
            if (len(servicios) > 0):
                return jsonify({'servicios': servicios, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except ExcepcionPersonalizada:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401