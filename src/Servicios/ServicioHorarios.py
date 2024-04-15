# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Horarios import Horarios


class ServicioHorarios():

    @classmethod
    def get_horarios(cls):
        try:
            connection = get_connection()
            horarios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_listaHorarios()')
                resultset = cursor.fetchall()
                for row in resultset:
                    horario = Horarios(int(row[0]), int(row[1]), row[2], row[3], row[4], row[5])
                    horarios.append(horario.to_json())
            connection.close()
            return horarios
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def verif_horario_unico(cls, correo):
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
    def crear_horario(cls, horario,fecha_ini):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call sp_creacion_horario(%s,%s,%s,%s,%s,%s)'
                                   ,(horario[0],horario[1],horario[2],
                                   horario[3],fecha_ini,4))
            connection.commit()
            connection.close()
            return True
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def get_horario_by_id(cls, id):
        try:
            connection = get_connection()
            horarios = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_Usuario_id(%s)',(id))
                resultset = cursor.fetchall()
                for row in resultset:
                    horario = Horarios(int(row[0]), row[1], row[2], int(row[3]), 
                                        int(row[4]), row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    horarios.append(horario.to_json())
            connection.close()
            if len(horarios)>0:
                return horarios
            else:
                return None
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def update_horario(cls, horario):
        try:
            connection = get_connection()
            flg = False
            with connection.cursor() as cursor:
                cursor.execute('call sp_Usuario_id(%s)',(horario[0]))
                resultset = cursor.fetchall()
                if len(resultset)>0:
                    cursor.execute('call sp_Actualizar_horario(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                                    (horario[0],horario[1], horario[2], int(horario[3]), 
                                    int(horario[4]), float(horario[5]), horario[6], horario[7], 
                                    int(horario[8])))
                    connection.commit()
                    flg=True
            connection.close()
            return flg
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)    