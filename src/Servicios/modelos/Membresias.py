class Membresias():
    
    def __init__(self, id_paquete, nombre_membresia, descripcion, status_activo, precio, duracion_meses, fecha_cobro) -> None:
        self.id_paquete = id_paquete
        self.nombre_membresia = nombre_membresia
        self.descripcion = descripcion
        self.status_activo = status_activo
        self.precio = precio
        self.duracion_meses = duracion_meses
        self.fecha_cobro = fecha_cobro
    
    def to_json(self):
        return {
            'id_paquete': self.id_paquete,
            'nombre_membresia': self.nombre_membresia,
            'descripcion': self.descripcion,
            'status_activo': self.status_activo,
            'precio': self.precio,
            'duracion_meses': self.duracion_meses,  
            'fecha_cobro': self.fecha_cobro
        }