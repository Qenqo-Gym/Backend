class Usuarios():

    def __init__(self, id, nombre, apellido, edad, 
                 peso,altura, sexo, direc, telefono, 
                 contraseña, email, id_paquete, fecha_inicio, admin) -> None:
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.peso = peso
        self.altura = altura
        self.sexo = sexo
        self.direc = direc
        self.telefono = telefono
        self.contraseña = contraseña
        self.email = email
        self.id_paquete = id_paquete
        self.fecha_inicio = fecha_inicio
        self.admin = admin

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'edad': self.edad,
            'peso': self.peso,
            'altura': self.altura,
            'sexo': self.sexo,
            'direc': self.direc,
            'telefono': self.telefono,
            'contraseña': self.contraseña,
            'email': self.email,
            'id_paquete': self.id_paquete,
            'fecha_inicio': self.fecha_inicio,
            'admin': self.admin
        }