from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioUsuarios import ServicioUsuarios
# Models
from src.Servicios.modelos.Usuarios import Usuarios
#timezone
import datetime
#pytz
import pytz
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
            return jsonify({"message":"No existe ese Usuario"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401

@main.route("/tipo_usuario/<int:tipo_usr>")
def get_usuario_tipo_id(tipo_usr):
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        usuarios = ServicioUsuarios.get_usuario_tipo_id(tipo_usr)
        
        if (len(usuarios) > 0):
            return jsonify({"usuarios": usuarios, "message": "SUCCESS"})
        else:
            return jsonify({"message":"No existe ese tipo de usuario"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401

@main.route("/crear", methods=['GET','POST'])
def crear_usuario():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    email = request.json['email']
    contraseña = request.json['contraseña']
    contraseña_conf = request.json['contraseña_conf']

    #que los campos no sean nulos se puede manejar con el front (required o en formwtf)
    if contraseña != contraseña_conf:
        return jsonify({"message":"Las contraseñas no coinciden","timezone":datetime.datetime.now(tz=pytz.timezone('America/Lima')).isoformat()})
    else:
        # Verificamos que el correo no exista en la base de datos
        usuario = [nombre,apellido,contraseña,email]
        busqueda_usuario = ServicioUsuarios.verif_usuario_unico(email)
        if busqueda_usuario == True:
            ServicioUsuarios.crear_usuario(usuario,datetime.datetime.now(tz=pytz.timezone('America/Lima')).isoformat())
            return jsonify({"message":"Se ha registrado correctamente."}),201
        else:
            return jsonify({"message":"El correo ya existe en nuestros registros."}), 500

@main.route("/actualizar/<int:usr_id>", methods=['GET','PUT'])
def actualizar_datos(usr_id):
    has_access = Security.verify_token(request.headers)
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    edad = request.json['edad']
    peso = request.json['peso']
    altura = request.json['altura']
    sexo = request.json['sexo']
    direc  = request.json['direc']
    telefono = request.json['telefono']

    if has_access:
        usuario = [usr_id,nombre,apellido,edad,peso,altura,sexo,direc,telefono]
        usuario = ServicioUsuarios.update_usuario(usuario)
        if usuario == True:
            return jsonify({"message": "Usuario ha sido actualizado exitosamente"})
        else:
            return jsonify({"message":"No existe el usuario que se desea actualizar"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401