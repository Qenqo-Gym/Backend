# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Membresias import Membresias


class ServicioMembresias():

    @classmethod
    def verif_membresia_unico(cls, nombre):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('call sp_valida_membresia(%s)' , (nombre))
                result = cursor.fetchone()
            connection.close()
            if result is not None and len(result) > 0:
                return False
            else:
                return True
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)

    @classmethod
    def crear_membresia(cls, membresia):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call sp_creacion_membresia(%s,%s,%s)'
                                   ,(membresia[0],membresia[1],membresia[2]))
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
    def get_membresias(cls):
        try:
            connection = get_connection()
            membresias = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_listaMembresias()')
                resultset = cursor.fetchall()
                for row in resultset:
                    membresia = Membresias(int(row[0]), row[1], row[2], int(row[3]))
                    membresias.append(membresia.to_json())
            connection.close()
            return membresias
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def update_membresia(cls, membresia):
        try:
            connection = get_connection()
            flg = False
            with connection.cursor() as cursor:
                cursor.execute('call sp_Servicio_id(%s)',(membresia[0]))
                resultset = cursor.fetchall()
                if len(resultset)>0:
                    cursor.execute('call sp_Actualizar_membresia(%s,%s)',
                                    (membresia[0],membresia[1]))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def delete_membresia(cls, id_serv):
        try:
            connection = get_connection()
            flg = False
            with connection.cursor() as cursor:
                cursor.execute('call sp_Servicio_id(%s)',(id_serv))
                resultset = cursor.fetchall()
                if len(resultset)>0:
                    cursor.execute('call sp_Eliminar_membresia(%s)',
                                    (id_serv))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)