# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Servicios import Servicios


class ServicioServicios():

    @classmethod
    def verif_servicio_unico(cls, correo):
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
    def crear_servicio(cls, servicio,fecha_ini):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call sp_creacion_servicio(%s,%s,%s,%s,%s,%s)'
                                   ,(servicio[0],servicio[1],servicio[2],
                                   servicio[3],fecha_ini,4))
            connection.commit()
            connection.close()
            return True
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
                    servicio = Servicios(row[0], row[1], row[2])
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
                    cursor.execute('call sp_Actualizar_servicio(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    (servicio[0],servicio[1], servicio[2], int(servicio[3]), 
                                    int(servicio[4]), float(servicio[5]), servicio[6], servicio[7], 
                                    int(servicio[8])))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)