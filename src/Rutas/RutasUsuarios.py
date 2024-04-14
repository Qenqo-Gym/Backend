from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioUsuarios import ServicioUsuarios

main = Blueprint('usuario_blueprint', __name__)


@main.route('/')
def get_usuarios():
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

@main.route("/<int:id>")
def get_usuario_by_id(id):
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        usuario = ServicioUsuarios.get_usuario_by_id(id)
        
        if usuario is not None:
            return jsonify({"usuario": usuario, "message": "SUCCESS"})
        else:
            return jsonify({"message":"NOEXISTE"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401

@main.route("/<int:tipo_usr>")
def get_usuario_tipo_id(tipo_usr):
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        usuarios = ServicioUsuarios.get_usuario_tipo_id(tipo_usr)
        
        if (len(usuarios) > 0):
            return jsonify({"usuarios": usuarios, "message": "SUCCESS"})
        else:
            return jsonify({"message":"NOEXISTE"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401
#@main.route("/crear", methods=['POST'])
#def crear_usuario():
