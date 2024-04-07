from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timezone
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Clavesecreta123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/51941/Documents/Proyectos/Quenco_Backend/qenqo.db'

db = SQLAlchemy(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(50),nullable = False)
    apellido = db.Column(db.String(100),nullable = False)
    edad = db.Column(db.Integer,nullable = False) 
    peso = db.Column(db.Numeric,nullable = False) 
    altura = db.Column(db.Numeric,nullable = False) 
    sexo = db.Column(db.String(50),nullable = False) 
    direc = db.Column(db.String(200),nullable = False) 
    telefono = db.Column(db.Integer,nullable = False)
    #Consideracion Hash 
    contraseña = db.Column(db.String(200),nullable = False) #con hash
    email = db.Column(db.String(120),nullable = False, unique = True)
    id_paquete = db.Column(db.Integer) #TEXT,
    fecha_inicio = db.Column(db.DateTime,default=datetime.now(timezone.utc))
    admin = db.Column(db.Boolean)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token faltante!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            usuario_actual = Usuarios.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token inválido!'}), 401

        return f(usuario_actual, *args, **kwargs)

    return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(usuario_actual):

    if not usuario_actual.admin:
        return jsonify({'message' : 'Privilegios insuficientees para esa acción!'})

    users = Usuarios.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['nombre'] = user.nombre
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(usuario_actual, public_id):

    if not usuario_actual.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = Usuarios.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['nombre'] = user.nombre
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(usuario_actual):
    if not usuario_actual.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Usuarios(public_id=str(uuid.uuid4()), nombre=data['nombre'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(usuario_actual, public_id):
    if not usuario_actual.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = Usuarios.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(usuario_actual, public_id):
    if not usuario_actual.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = Usuarios.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = Usuarios.query.filter_by(nombre=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


if __name__ == '__main__':
    app.run(debug=True)