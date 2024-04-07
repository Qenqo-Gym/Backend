from decouple import config
from src.Utils.Errores.ExcepcionPersonalizada import ExcepcionPersonalizada
import pymysql


def get_connection():
    try:
        return pymysql.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            db=config('MYSQL_DB')
        )
    except ExcepcionPersonalizada as ex:
        raise ExcepcionPersonalizada(ex)
