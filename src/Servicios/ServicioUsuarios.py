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
                    usuario = Usuarios(int(row[0]), row[1], row[2], int(row[3]), 
                                        int(row[4]), row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    usuarios.append(usuario.to_json())
            connection.close()
            return usuarios
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def get_usuario_by_id(cls, id):
        try:
            connection = get_connection()
            usuarios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_Usuario_id(%s)',(id))
                resultset = cursor.fetchall()
                for row in resultset:
                    usuario = Usuarios(int(row[0]), row[1], row[2], int(row[3]), 
                                        int(row[4]), row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    usuarios.append(usuario.to_json())
            connection.close()
            return usuarios
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)