from flask import Flask

# Routes
from .Rutas import AuthRutas
from .Rutas import RutasUsuarios

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRutas.main, url_prefix='/auth')
    app.register_blueprint(RutasUsuarios.main, url_prefix='/usuarios')

    return app