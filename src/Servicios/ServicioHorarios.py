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