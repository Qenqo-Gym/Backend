--Usuarios
DELIMITER //
CREATE PROCEDURE sp_listaUsuarios()
BEGIN
	SELECT
		usu.usr_id, usu.nombre, usu.apellido, usu.edad, usu.peso, usu.altura, 
        usu.sexo, usu.direc, usu.telefono, usu.contraseña, usu.email, 
        usu.id_paquete, usu.fecha_inicio, usu.flg_admin 
    FROM usuarios usu 
    ORDER BY usu.fecha_inicio DESC;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_verifyIdentity(IN pEmail VARCHAR(20), IN pContraseña VARCHAR(20))
BEGIN
	SELECT USER.usr_id, USER.email, USER.nombre, USER.apellido 
	FROM usuarios USER 
    WHERE 1 = 1 
    AND USER.email = pEmail 
	AND USER.contraseña = pContraseña;
END //
DELIMITER ;

-- Servicios
DELIMITER //
CREATE PROCEDURE sp_listaServicios()
BEGIN
	SELECT SERV.id_serv, SERV.nombre, SERV.descripcion_serv, SERV.flg_activo 
    FROM servicios SERV 
    ORDER BY SERV.id_serv DESC;
END //
DELIMITER ;

--Horarios
DELIMITER //
CREATE PROCEDURE sp_listaHorarios()
BEGIN
	SELECT H.id_horario, H.usr_id, H.sesion, H.fecha, H.tiempo_inicio, H.tiempo_fin
    FROM horarios H 
    ORDER BY H.id_horario DESC;
END //
DELIMITER ;

--Pagos
DELIMITER //
CREATE PROCEDURE sp_listaPagos(IN pUsr_id INT, IN pFecha_inirango TEXT)
BEGIN
	SELECT P.id_pago, P.usr_id, P.id_paquete, P.fecha, P.monto
    FROM pagos P
    LEFT JOIN usuarios U ON P.usr_id = U.usr_id
    WHERE 1=1
		AND P.usr_id = pUsr_id
        AND P.fecha >= pFecha_inirango
    ORDER BY P.fecha DESC;
END //
DELIMITER ;