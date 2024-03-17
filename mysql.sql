DROP TABLE IF EXISTS Usuarios;
DROP TABLE IF EXISTS Membresias;
DROP TABLE IF EXISTS Pagos;
DROP TABLE IF EXISTS Transacciones;
DROP TABLE IF EXISTS Reportes;
DROP TABLE IF EXISTS Entrenadores;
DROP TABLE IF EXISTS Horarios;
--DROP TABLE IF EXISTS Equipos;
--DROP TABLE IF EXISTS Servicios;
--DROP TABLE IF EXISTS Mercancia;

--CREACION DE TABLAS --

CREATE TABLE Usuarios (
    usr_id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER NOT NULL,
    peso INTEGER NOT NULL,
    altura REAL NOT NULL,
    sexo TEXT NOT NULL,
    direc TEXT NOT NULL,
    telefono INTEGER NOT NULL,
    contraseña TEXT NOT NULL,
    email TEXT NOT NULL,
    id_paquete TEXT,
    fecha_inicio TEXT,
    FOREIGN KEY (id_paquete) REFERENCES Membresias (id_paquete)
);

CREATE TABLE Membresias (
    id_paquete TEXT PRIMARY KEY,
    nombre_membresia TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    status INTEGER NOT NULL,
    precio REAL NOT NULL,
    duracion_meses INTEGER NOT NULL,
    fecha_cobro TEXT NOT NULL,
);

CREATE TABLE Pagos (
    id_pago TEXT PRIMARY KEY,
    usr_id TEXT,
    id_paquete TEXT,
    fecha TEXT NOT NULL,
    monto REAL NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES Usuarios (usr_id),
    FOREIGN KEY (id_paquete) REFERENCES Membresias (id_paquete)
);

CREATE TABLE Entrenadores (
    entrenador_id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    celular INTEGER NOT NULL,
    id_horario TEXT,
    especializacion TEXT NOT NULL,
    fecha_incorporado TEXT NOT NULL,
    email TEXT NOT NULL,
    contraseña TEXT NOT NULL,
    FOREIGN KEY (id_horario) REFERENCES Horarios (id_horario)
);

CREATE TABLE Turnos(
    turno_id TEXT PRIMARY KEY,
    --darle una pensada
);

CREATE TABLE Horarios (
    id_horario TEXT PRIMARY KEY,
    usr_id TEXT,
    entrenador_id TEXT,
    sesion TEXT,
    fecha TEXT NOT NULL,
    tiempo_inicio TEXT NOT NULL,
    tiempo_fin TEXT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES Usuarios (usr_id),
    FOREIGN KEY (entrenador_id) REFERENCES Entrenadores (entrenador_id)
);

CREATE TABLE Transacciones (
    id_trans TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    usr_id TEXT,
    flg_mora INTEGER NOT NULL,
    monto TEXT NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (usr_id) REFERENCES Usuarios (usr_id)
);

CREATE TABLE Servicios (
    id_serv TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion_serv TEXT NOT NULL,
    flg_activo INTEGER NOT NULL
);