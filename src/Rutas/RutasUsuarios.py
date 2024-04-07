from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioUsuarios import ServicioUsuarios

main = Blueprint('language_blueprint', __name__)


@main.route('/')
def get_languages():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            usuarios = ServicioUsuarios.get_usuarios()
            if (len(usuarios) > 0):
                return jsonify({'usuarios': usuarios, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except ExcepcionPersonalizada:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401