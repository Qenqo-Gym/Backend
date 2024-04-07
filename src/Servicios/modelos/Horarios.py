class Horarios():

    def  __init__(self, id_horario, usr_id, sesion, fecha, tiempo_inicio, tiempo_fin) -> None:
        self.id_horario=id_horario
        self.usr_id=usr_id
        self.sesion=sesion
        self.fecha=fecha
        self.tiempo_inicio=tiempo_inicio
        self.tiempo_fin=tiempo_fin
    
    def to_json(self):
        return {
            'id_horario': self.id_horario,
            'usr_id': self.usr_id,
            'sesion': self.sesion,
            'fecha': self.fecha,
            'tiempo_inicio': self.tiempo_inicio,
            'tiempo_fin': self.tiempo_fin
        }
