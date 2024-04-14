from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioHorarios import ServicioHorarios

main = Blueprint('horario_blueprint', __name__)


@main.route('/')
def get_horarios():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            horarios = ServicioHorarios.get_horarios()
            if (len(horarios) > 0):
                return jsonify({'horarios': horarios, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except ExcepcionPersonalizada:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401