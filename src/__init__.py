from flask import Flask

# Routes
from .Rutas import AuthRutas
from .Rutas import RutasUsuarios
from .Rutas import RutasServicios
from .Rutas import RutasHorarios
from .Rutas import RutasPagos

app = Flask(__name__)


def init_app(config):
    # Configuration
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(AuthRutas.main, url_prefix='/auth')
    app.register_blueprint(RutasUsuarios.main, url_prefix='/usuarios')
    app.register_blueprint(RutasServicios.main, url_prefix='/servicios')
    app.register_blueprint(RutasHorarios.main, url_prefix='/horarios')
    app.register_blueprint(RutasPagos.main, url_prefix='/pagos')
    return app