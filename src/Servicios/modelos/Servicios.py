class Servicios():

    def __init__(self, id_serv, nombre, descripcion_serv, flg_activo) -> None:
        self.id_serv = id_serv
        self.nombre = nombre
        self.descripcion_serv = descripcion_serv
        self.flg_activo = flg_activo


    def to_json(self):
        return {
            'id_serv': self.id_serv,
            'nombre': self.nombre,
            'descripcion_serv': self.descripcion_serv,
            'flg_activo': self.flg_activo
        }