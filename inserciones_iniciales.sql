-- Inserción de tipos de usuario
INSERT INTO Tipo_usuario (id, nombre, descripcion) VALUES 
(1, 'Cliente', 'Usuario que busca servicios de fitness'),
(2, 'Instructor', 'Profesional que ofrece servicios de fitness');

-- Inserción de usuario cliente (contraseña: Cliente123!)
-- La contraseña está hasheada con SHA-256 (password + salt="fitsystem2025")
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
(1, 'Cliente', 'Ejemplo', '1234567890', 'cliente@ejemplo.com', '0fbf346d7cf6e7dfd79b8b622e9e77d477335a33ca48101172cd97acf558e506', 1, 'default_user.png', NOW(), 1);

-- Inserción de usuario instructor (contraseña: Instructor123!)
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
(2, 'Instructor', 'Ejemplo', '0987654321', 'instructor@ejemplo.com', 'fc9dd241ace73103df45637246ee8b74f0f37ae38be9c1cbecc6dcf8a5a7cdba', 1, 'default_user.png', NOW(), 2);

-- Inserción de datos del cliente
INSERT INTO Cliente_datos (id, nivel_actividad, direccion, tipo_cliente, Usuario_id) VALUES
(1, 'Moderado', 'Calle Cliente 123', 'regular', 1);

-- Inserción de datos del instructor
INSERT INTO Instructor_datos (id, certificaciones, estudios, anios_experiencia, especialidad, Usuario_id) VALUES
(1, 'Certificado de Entrenador Personal', 'Licenciatura en Educación Física', 5, 'Entrenamiento funcional', 2);

-- Inserción de un registro en Historial_Medidas para el cliente
INSERT INTO Historial_Medidas (id, peso, altura, imc, fecha_medicion, Usuario_id) VALUES
(1, 70.5, 1.75, 23.0, NOW(), 1);

-- Inserción de una disciplina
INSERT INTO Discipline (id, nombre, descripcion) VALUES
(1, 'Fitness General', 'Entrenamiento general de fitness y acondicionamiento físico');

-- Asociar disciplina con instructor
INSERT INTO Discipline_Instructor (id, Discipline_id, Usuario_id) VALUES
(1, 1, 2);

-- Asociar cliente con instructor
INSERT INTO Cliente_Instructor (id, Usuario_id, Usuario_2_id) VALUES
(1, 1, 2);

-- Asociar cliente con disciplina
INSERT INTO Discipline_Cliente (id, Discipline_id, Usuario_id) VALUES
(1, 1, 1); 