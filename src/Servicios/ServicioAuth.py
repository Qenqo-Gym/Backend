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
                cursor.execute('call sp_verifyIdentity(%s, %s)', (user.email, user.contraseña))
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = Usuarios(None, None,None, None,None, None,None, None,None,row[2],row[1],None,None,None,None,None)
            connection.close()
            return authenticated_user
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)