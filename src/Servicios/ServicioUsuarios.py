# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Usuarios import Usuarios


class ServicioUsuarios():

    @classmethod
    def get_usuarios(cls):
        try:
            connection = get_connection()
            usuarios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_listaUsuarios()')
                resultset = cursor.fetchall()
                for row in resultset:
                    usuarios = Usuarios(int(row[0]), row[1])
                    usuarios.append(usuarios.to_json())
            connection.close()
            return usuarios
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)