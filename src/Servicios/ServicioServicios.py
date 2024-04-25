# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Servicios import Servicios


class ServicioServicios():

    @classmethod
    def verif_servicio_unico(cls, nombre):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_valida_servicio(%s)' , (nombre))
                result = cursor.fetchone()
            connection.close()
            if result is not None and len(result) > 0:
                return False
            else:
                return True
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)

    @classmethod
    def crear_servicio(cls, servicio):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call sp_creacion_servicio(%s,%s,%s)'
                                   ,(servicio[0],servicio[1],servicio[2]))
            connection.commit()
            if cursor.rowcount>0:
                connection.close()
                return True
            else:
                connection.close()
                return None
            
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
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
    
    @classmethod
    def get_servicio_by_id(cls, id):
        try:
            connection = get_connection()
            servicios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_Servicio_id(%s)',(id))
                resultset = cursor.fetchall()
                for row in resultset:
                    servicio = Servicios(row[0], row[1], row[2],row[3])
                    servicios.append(servicio.to_json())
            connection.close()
            if len(servicios)>0:
                return servicios
            else:
                return None
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def update_servicio(cls, servicio):
        try:
            connection = get_connection()
            flg = False
            with connection.cursor() as cursor:
                cursor.execute('call sp_Servicio_id(%s)',(servicio[0]))
                resultset = cursor.fetchall()
                if len(resultset)>0:
                    cursor.execute('call sp_Actualizar_servicio(%s,%s)',
                                    (servicio[0],servicio[1]))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def delete_servicio(cls, id_serv):
        try:
            connection = get_connection()
            flg = False
            with connection.cursor() as cursor:
                cursor.execute('call sp_Servicio_id(%s)',(id_serv))
                resultset = cursor.fetchall()
                if len(resultset)>0:
                    cursor.execute('call sp_Eliminar_servicio(%s)',
                                    (id_serv))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)