from flask import Blueprint, request, jsonify

# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Security
from src.Utils.Security import Security
# Services
from src.Servicios.ServicioMembresias import ServicioMembresias

main = Blueprint('membresia_blueprint', __name__)


@main.route('/')
def get_membresias():
    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            membresias = ServicioMembresias.get_membresias()
            if (len(membresias) > 0):
                return jsonify({'membresias': membresias, 'message': "SUCCESS", 'success': True})
            else:
                return jsonify({'message': "NOTFOUND", 'success': True})
        except ExcepcionPersonalizada:
            return jsonify({'message': "ERROR", 'success': False})
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@main.route("/crear", methods=['GET','POST'])
def crear_membresia():
    nombre_membresia = request.json['nombre_membresia']
    descripcion = request.json['descripcion']
    status_activo = request.json['status_activo']
    precio = request.json['precio']
    duracion_meses = request.json['duracion_meses']
    dia_cobro = request.json['dia_cobro']

    #que los campos no sean nulos se puede manejar con el front (required o en formwtf)
    # Verificamos que el correo no exista en la base de datos
    membresia = [nombre_membresia,descripcion,status_activo,precio,duracion_meses,dia_cobro]
    busqueda_membresia = ServicioMembresias.verif_membresia_unico(nombre_membresia)
    if busqueda_membresia == True:
        ServicioMembresias.crear_membresia(membresia)
        return jsonify({"message":"Se ha registrado correctamente."}),201
    else:
        return jsonify({"message":"El membresia ya existe en nuestros registros."}), 500

@main.route("/actualizar/<int:id_serv>", methods=['GET','PUT'])
def actualizar_datos(id_serv):
    has_access = Security.verify_token(request.headers)
    flg_activo = request.json['flg_activo']

    if has_access:
        membresia = [id_serv,flg_activo]
        membresia = ServicioMembresias.update_membresia(membresia)
        if membresia == True:
            return jsonify({"message": "Servicio ha sido actualizado exitosamente"})
        else:
            return jsonify({"message":"No existe el membresia que se desea actualizar"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401
    
@main.route("/eliminar/<int:id_serv>", methods=['DELETE'])
def eliminar_datos(id_serv):
    has_access = Security.verify_token(request.headers)

    if has_access:
        membresia = ServicioMembresias.delete_membresia(id_serv)
        if membresia == True:
            return jsonify({"message": "Servicio ha sido eliminado exitosamente"})
        else:
            return jsonify({"message":"No existe el membresia que se desea eliminar"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401