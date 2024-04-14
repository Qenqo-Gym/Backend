class Pagos():

    def __init__(self,id_pago,usr_id,id_paquete,fecha,monto) -> None:
        self.id_pago=id_pago
        self.usr_id=usr_id
        self.id_paquete=id_paquete
        self.fecha=fecha
        self.monto=monto

    def to_json(self):
        return {
            'id_pago': self.id_pago,
            'usr_id': self.usr_id,
            'id_paquete': self.id_paquete,
            'fecha': self.fecha,
            'monto': self.monto
        }