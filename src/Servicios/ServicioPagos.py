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
    
    @classmethod
    def crear_pago(cls, pago,fecha_ini):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                    cursor.execute('call sp_creacion_pago(%s,%s,%s,%s,%s,%s)'
                                   ,(pago[0],pago[1],pago[2],
                                   pago[3],fecha_ini,4))
            connection.commit()
            connection.close()
            return True
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def get_pago_by_id(cls, id):
        try:
            connection = get_connection()
            pagos = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_Pago_id(%s)',(id))
                resultset = cursor.fetchall()
                for row in resultset:
                    pago = Pagos(int(row[0]), row[1], row[2], int(row[3]), 
                                        int(row[4]), row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    pagos.append(pago.to_json())
            connection.close()
            if len(pagos)>0:
                return pagos
            else:
                return None
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)
    
    @classmethod
    def get_pago_tipo_id(cls, tipo_usr):
        try:
            connection = get_connection()
            pagos = []
            with connection.cursor() as cursor:
                cursor.execute('call sp_Pago_tipo(%s)',(tipo_usr))
                resultset = cursor.fetchall()
                for row in resultset:
                    pago = Pagos(int(row[0]), row[1], row[2], int(row[3]), 
                                        int(row[4]), row[5], row[6], row[7], row[8],
                                        row[9], row[10], row[11], row[12], row[13],row[14],row[15])
                    pagos.append(pago.to_json())
            connection.close()
            return pagos
        except ExcepcionPersonalizada as ex:
            raise ExcepcionPersonalizada(ex)