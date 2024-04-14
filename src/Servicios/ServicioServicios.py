# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Servicios import Servicios


class ServicioServicios():

    @classmethod
    def get_servicios(cls):
        try:
            connection = get_connection()
            servicios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_listaServicios()')
                resultset = cursor.fetchall()
                for row in resultset:
                    servicio = Servicios(int(row[0]), row[1], row[2], int(row[3]))
                    servicios.append(servicio.to_json())
            connection.close()
            return servicios
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)