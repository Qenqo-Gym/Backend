# Base de datos
from src.BaseDeDatos.db_mysql import get_connection
# Errores
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Usuarios import Usuarios


class ServicioAuth():

    @classmethod
    def login_user(cls, user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute('call sp_verifyIdentity(%s, %s)', (user.username, user.password))
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = Usuarios(int(row[0]), row[1], None, row[2])
            connection.close()
            return authenticated_user
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)