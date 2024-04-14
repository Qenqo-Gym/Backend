from flask import Blueprint, request, jsonify

# Models
from src.Servicios.modelos.Usuarios import Usuarios
# Security
from src.Utils.Security import Security
# Servicios
from src.Servicios.ServicioAuth import ServicioAuth

main = Blueprint('auth_blueprint', __name__)


@main.route('/', methods=['POST'])
def login():
    email = request.json['email']
    contraseña = request.json['contraseña']

    _user = Usuarios(None, None,None, None,None, None,None, None,None, contraseña,email,None,None,None,None,None)
    authenticated_user = ServicioAuth.login_user(_user)

    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401