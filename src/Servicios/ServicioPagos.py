# Database
from src.BaseDeDatos.db_mysql import get_connection
# Errors
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
# Models
from .modelos.Pagos import Pagos


class ServicioPagos():

    @classmethod
    def get_pagos(cls,usr_id,fecha):
        try:
            connection = get_connection()
            pagos = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_listaPagos(%s, %s)',(usr_id,fecha))
                resultset = cursor.fetchall()
                for row in resultset:
                    pago = Pagos(int(row[0]), int(row[1]), int(row[2]), row[3], float(row[4]))
                    pagos.append(pago.to_json())
            connection.close()
            return pagos
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)