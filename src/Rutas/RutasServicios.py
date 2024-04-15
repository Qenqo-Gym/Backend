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

@main.route("/<int:id_serv>")
def get_servicio_by_id(id_serv):
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        servicio = ServicioServicios.get_servicio_by_id(id_serv)
        
        if servicio is not None:
            return jsonify({"servicio": servicio, "message": "SUCCESS"})
        else:
            return jsonify({"message":"No existe ese Usuario"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401

@main.route("/crear", methods=['GET','POST'])
def crear_servicio():
    nombre = request.json['nombre']
    descripcion_serv = request.json['descripcion_serv']
    flg_activo = False

    #que los campos no sean nulos se puede manejar con el front (required o en formwtf)
    # Verificamos que el correo no exista en la base de datos
    servicio = [nombre,descripcion_serv,flg_activo]
    busqueda_servicio = ServicioServicios.verif_servicio_unico(nombre)
    if busqueda_servicio == True:
        ServicioServicios.crear_servicio(servicio)
        return jsonify({"message":"Se ha registrado correctamente."}),201
    else:
        return jsonify({"message":"El correo ya existe en nuestros registros."}), 500

@main.route("/actualizar/<int:id_serv>", methods=['GET','PUT'])
def actualizar_datos(id_serv):
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
        servicio = [id_serv,nombre,apellido,edad,peso,altura,sexo,direc,telefono]
        servicio = ServicioServicios.update_servicio(servicio)
        if servicio == True:
            return jsonify({"message": "Usuario ha sido actualizado exitosamente"})
        else:
            return jsonify({"message":"No existe el servicio que se desea actualizar"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401