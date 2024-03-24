from flask import Flask, render_template, flash, request
from flask_restful  import Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField,PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_swagger_ui import get_swaggerui_blueprint

#Instancia de Flask
app = Flask(__name__)
#La vieja DB SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Nueva BD con MySQL 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Chicharron@localhost/qenqo' 
#Config para que funcione CSRF tokens con WTForms
app.config['SECRET_KEY'] = "My llave secreta :3"

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://petstore.swagger.io/v2/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

#Inicializando la DB
db = SQLAlchemy(app)

class Usuarios(db.Model): #Creamos tabla usuarios
    usr_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200),nullable = False)# TEXT NOT NULL,
    apellido = db.Column(db.String(200),nullable = False)#TEXT NOT NULL,
    edad = db.Column(db.Integer,nullable = False) #INTEGER NOT NULL,
    peso = db.Column(db.Numeric,nullable = False) #INTEGER NOT NULL,
    altura = db.Column(db.Numeric,nullable = False) #REAL NOT NULL,
    sexo = db.Column(db.String(255),nullable = False) #TEXT NOT NULL,
    direc = db.Column(db.String(200),nullable = False) #TEXT NOT NULL,
    telefono = db.Column(db.Integer,nullable = False) #INTEGER NOT NULL,
    contraseña = db.Column(db.String(200),nullable = False) #TEXT NOT NULL,
    email = db.Column(db.String(120),nullable = False, unique = True) #TEXT NOT NULL,
    id_paquete = db.Column(db.Integer) #TEXT,
    fecha_inicio = db.Column(db.DateTime,default=datetime.now(timezone.utc)) #TEXT,

    def __repr__(self):
        return '<Name %r>' % self.nombre

#Clase para pruebas
class NamerForm(FlaskForm):
    name = StringField('Indique su Nombre' , validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField('Nombre' , validators=[DataRequired()])
    lastname =  StringField('Apellido', validators=[DataRequired()])
    age = IntegerField('Edad', validators=[DataRequired()])
    weight = DecimalField('Peso', validators=[DataRequired()])
    height = DecimalField('Altura', validators=[DataRequired()])
    sex = StringField('Sexo', validators=[DataRequired()])
    address = StringField('Direccion', validators=[DataRequired()])
    phone = IntegerField('Telefono', validators=[DataRequired()])
    password = PasswordField('Contraseña',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(email = form.email.data).first()
        if user is None:
            user = Usuarios(nombre = form.name.data,
                            apellido = form.lastname.data,
                            edad = form.age.data,
                            peso = form.weight.data,
                            altura = form.height.data,
                            sexo = form.sex.data,
                            direc = form.address.data,
                            telefono = form.phone.data,
                            contraseña = form.password.data,
                            email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.lastname.data = ''
        form.age.data = ''
        form.weight.data = ''
        form.height.data = ''
        form.sex.data = ''
        form.address.data = ''
        form.phone.data = ''
        form.password.data = ''
        flash("Usuario añadido correctamente")
    our_users = Usuarios.query.order_by(Usuarios.fecha_inicio)
    return render_template("add_user.html", form = form,name = name, our_users = our_users) #el parametro our_users y toda su lógica es olo para mostrarlo en vivo

#Actualizar Users
@app.route('/update_users/<int:id>',methods=['GET','POST'])
def update_users(id):
    form = UserForm()
    name_to_update = Usuarios.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("Usuario actualizado de maner exitosa")
            return render_template("update_users.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash("Error al actualizar campos...Intentar otra vez")
            return render_template("update_users.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template('update_users.html',
                               form = form,
                               name_to_update = name_to_update)

#Decorador de ruta
@app.route('/')
def index():
    first_name = "Juan"
    stuff = "this is bold text"
    return render_template('index.html',
                           first_name = first_name,
                           stuff = stuff)

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name) 

#Custom Error Pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

#Name page
@app.route("/name",methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #Validando Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted Succesfully!")
    return render_template("name.html",
                           name = name,
                           form = form)


#api.add_resource(usuarios,"/holamundo")
if  __name__ == '__main__':
    app.run(debug=True)    