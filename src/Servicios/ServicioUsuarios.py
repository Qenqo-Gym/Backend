# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Usuarios import Usuarios



class ServicioUsuarios():

    @classmethod
    def verif_usuario_unico(cls, correo):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_valida_registro(%s)' , (correo))
                result = cursor.fetchone()
            connection.close()
            if result == None:
                return True
            else:
                return False
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)

    @classmethod
    def crear_usuario(cls, usuario,fecha_ini):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call sp_creacion_usuario(%s,%s,%s,%s,%s,%s)'
                                   ,(usuario[0],usuario[1],usuario[2],
                                   usuario[3],fecha_ini,4))
            connection.commit()
            connection.close()
            return True
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def get_usuarios(cls):
        try:
            connection = get_connection()
            usuarios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_listaUsuarios()')
                resultset = cursor.fetchall()
                for row in resultset:
                    usuario = Usuarios(row[0], row[1], row[2], row[3], 
                                        row[4], row[5], row[6], row[7], row[8],
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
                    usuario = Usuarios(row[0], row[1], row[2], row[3], 
                                        row[4], row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    usuarios.append(usuario.to_json())
            connection.close()
            if len(usuarios)>0:
                return usuarios
            else:
                return None
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def get_usuario_tipo_id(cls, tipo_usr):
        try:
            connection = get_connection()
            usuarios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_Usuario_tipo(%s)',(tipo_usr))
                resultset = cursor.fetchall()
                for row in resultset:
                    usuario = Usuarios(row[0], row[1], row[2], row[3], 
                                        row[4], row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    usuarios.append(usuario.to_json())
            connection.close()
            return usuarios
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def update_usuario(cls, usuario):
        try:
            connection = get_connection()
            flg = False
            with connection.cursor() as cursor:
                cursor.execute('call sp_Usuario_id(%s)',(usuario[0]))
                resultset = cursor.fetchall()
                if len(resultset)>0:
                    cursor.execute('call sp_Actualizar_usuario(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    (usuario[0],usuario[1], usuario[2], int(usuario[3]), 
                                    int(usuario[4]), float(usuario[5]), usuario[6], usuario[7], 
                                    int(usuario[8])))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    