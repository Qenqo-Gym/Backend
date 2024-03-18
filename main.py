from flask import Flask, render_template
from flask_restful  import Api, Resource
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Instancia de Flask
app = Flask(__name__)
api = Api(app)
#Config para que funcione CSRF tokens con WTForms
app.config['SECRET_KEY'] = "My llave secreta :3"

#Clase para pruebas
class NamerForm(FlaskForm):
    name = StringField('Indique su Nombre' , validators=[DataRequired()])
    submit = SubmitField("Submit")
class usuarios(Resource):
    def get(self):
        return {'data': 'Hola Mundo'}
    def post(self):
        return {"message": "Post"}

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
    return render_template("name.html",
                           name = name,
                           form = form)


api.add_resource(usuarios,"/holamundo")
if  __name__ == '__main__':
    app.run(debug=True)    