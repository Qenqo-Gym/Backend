use qenqo;
DROP TABLE IF EXISTS Usuarios;
DROP TABLE IF EXISTS Membresias;
DROP TABLE IF EXISTS Pagos;
DROP TABLE IF EXISTS Transacciones;
DROP TABLE IF EXISTS Entrenadores;
DROP TABLE IF EXISTS Horarios;
DROP TABLE IF EXISTS Servicios;

-- CREACION DE TABLAS --

CREATE TABLE Usuarios (
    usr_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INT NOT NULL,
    peso INT NOT NULL,
    altura FLOAT NOT NULL,
    sexo VARCHAR(255) NOT NULL,
    direc TEXT NOT NULL,
    telefono INT NOT NULL,
    contraseña TEXT NOT NULL,
    email TEXT NOT NULL,
    id_paquete INT,
    fecha_inicio TEXT,
    FOREIGN KEY (id_paquete) REFERENCES Membresias (id_paquete)
);

CREATE TABLE Membresias (
    id_paquete INT PRIMARY KEY AUTO_INCREMENT,
    nombre_membresia TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    status_activo INT NOT NULL,
    precio FLOAT NOT NULL,
    duracion_meses INT NOT NULL,
    fecha_cobro TEXT NOT NULL
);

CREATE TABLE Pagos (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    usr_id INT,
    id_paquete INT,
    fecha TEXT NOT NULL,
    monto FLOAT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES Usuarios (usr_id),
    FOREIGN KEY (id_paquete) REFERENCES Membresias (id_paquete)
);

CREATE TABLE Entrenadores (
    entrenador_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre TEXT NOT NULL,
    celular INT NOT NULL,
    id_horario INT,
    cod_turno TEXT,
    des_turno TEXT,
    especializacion TEXT NOT NULL,
    fecha_incorporado TEXT NOT NULL,
    email TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    FOREIGN KEY (id_horario) REFERENCES Horarios (id_horario)
);

CREATE TABLE Horarios (
    id_horario INT PRIMARY KEY AUTO_INCREMENT,
    usr_id INT,
    sesion TEXT,
    fecha TEXT NOT NULL,
    tiempo_inicio TEXT NOT NULL,
    tiempo_fin TEXT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES Usuarios (usr_id)
);

CREATE TABLE Transacciones (
    id_trans INT PRIMARY KEY AUTO_INCREMENT,
    nombre TEXT NOT NULL,
    usr_id INT,
    flg_mora INT NOT NULL,
    monto TEXT NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES Usuarios (usr_id)
);

CREATE TABLE Servicios (
    id_serv INT PRIMARY KEY AUTO_INCREMENT,
    nombre TEXT NOT NULL,
    descripcion_serv TEXT NOT NULL,
    flg_activo INT NOT NULL
);


