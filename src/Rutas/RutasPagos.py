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
    
@main.route("/<int:id>")
def get_pago_by_id(id):
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        pago = ServicioPagos.get_pago_by_id(id)
        
        if pago is not None:
            return jsonify({"pago": pago, "message": "SUCCESS"})
        else:
            return jsonify({"message":"No existe ese Usuario"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401

@main.route("/tipo_pago/<int:tipo_usr>")
def get_pago_tipo_id(tipo_usr):
    has_access = Security.verify_token(request.headers)
    
    if has_access:
        pagos = ServicioPagos.get_pago_tipo_id(tipo_usr)
        
        if (len(pagos) > 0):
            return jsonify({"pagos": pagos, "message": "SUCCESS"})
        else:
            return jsonify({"message":"No existe ese tipo de pago"}), 404
    else:
        return jsonify({"message":"Unauthorized"}), 401

@main.route("/crear", methods=['GET','POST'])
def crear_pago():
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
        pago = [nombre,apellido,contraseña,email]
        busqueda_pago = ServicioPagos.verif_pago_unico(email)
        if busqueda_pago == True:
            ServicioPagos.crear_pago(pago,datetime.datetime.now(tz=pytz.timezone('America/Lima')).isoformat())
            return jsonify({"message":"Se ha registrado correctamente."}),201
        else:
            return jsonify({"message":"El correo ya existe en nuestros registros."}), 500