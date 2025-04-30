-- Inserciones de ejemplo para el sistema de fitness

-- Inserción de tipos de usuario (si no existen ya)
INSERT INTO Tipo_usuario (id, nombre, descripcion) VALUES 
(1, 'Cliente', 'Usuario que busca servicios de fitness'),
(2, 'Instructor', 'Profesional que ofrece servicios de fitness');

-- Inserción de disciplinas
INSERT INTO Discipline (id, nombre, descripcion) VALUES
(1, 'Musculación', 'Entrenamiento enfocado en el desarrollo muscular'),
(2, 'Cardio', 'Entrenamiento cardiovascular'),
(3, 'CrossFit', 'Entrenamiento funcional de alta intensidad'),
(4, 'Yoga', 'Disciplina que combina posturas físicas, ejercicios de respiración y meditación');

-- Inserción de usuarios clientes
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
(10, 'Carlos', 'Rodríguez', '6641234567', 'carlos@ejemplo.com', SHA2('password123', 256), 1, 'default_user.png', NOW(), 1),
(11, 'Ana', 'Martínez', '6642345678', 'ana@ejemplo.com', SHA2('password123', 256), 1, 'default_user.png', NOW(), 1),
(12, 'Miguel', 'López', '6643456789', 'miguel@ejemplo.com', SHA2('password123', 256), 1, 'default_user.png', NOW(), 1),
(13, 'Laura', 'Sánchez', '6644567890', 'laura@ejemplo.com', SHA2('password123', 256), 1, 'default_user.png', NOW(), 1),
(14, 'Javier', 'González', '6645678901', 'javier@ejemplo.com', SHA2('password123', 256), 1, 'default_user.png', NOW(), 1);

-- Inserción de usuario instructor
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
(15, 'María', 'Entrenadora', '6646789012', 'maria@instructor.com', SHA2('instructor123', 256), 1, 'default_user.png', NOW(), 2);

-- Inserción de datos de clientes
INSERT INTO Cliente_datos (nivel_actividad, direccion, tipo_cliente, Usuario_id, fecha_pago) VALUES
('Principiante', 'Calle Principal 123', 'regular', 10, DATE_ADD(CURRENT_DATE(), INTERVAL -5 DAY)),
('Intermedio', 'Avenida Central 456', 'premium', 11, DATE_ADD(CURRENT_DATE(), INTERVAL -2 DAY)),
('Avanzado', 'Boulevard Norte 789', 'regular', 12, DATE_ADD(CURRENT_DATE(), INTERVAL -10 DAY)),
('Principiante', 'Calle Sur 321', 'premium', 13, DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY)),
('Intermedio', 'Avenida Este 654', 'regular', 14, DATE_ADD(CURRENT_DATE(), INTERVAL -7 DAY));

-- Inserción de datos de instructor
INSERT INTO Instructor_datos (certificaciones, estudios, anios_experiencia, especialidad, Usuario_id) VALUES
('Certificado en Entrenamiento Personal, Certificado en Nutrición Deportiva', 'Licenciatura en Educación Física', 5, 'Entrenamiento funcional', 15);

-- Asociar disciplinas al instructor
INSERT INTO Discipline_Instructor (Discipline_id, Usuario_id) VALUES
(1, 15), (2, 15), (3, 15);

-- Asociar clientes con instructor
INSERT INTO Cliente_Instructor (Usuario_id, Usuario_2_id) VALUES
(10, 15), (11, 15), (12, 15), (13, 15), (14, 15);

-- Asociar disciplinas a clientes
INSERT INTO Discipline_Cliente (Discipline_id, Usuario_id) VALUES
(1, 10), (2, 11), (3, 12), (4, 13), (1, 14);

-- Inserción de historial de medidas
INSERT INTO Historial_Medidas (peso, altura, imc, fecha_medicion, Usuario_id) VALUES
(85.5, 178, 27.0, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 10),
(83.2, 178, 26.3, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 10),
(82.0, 178, 25.9, CURRENT_DATE(), 10),

(65.3, 165, 24.0, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 11),
(64.1, 165, 23.5, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 11),
(63.5, 165, 23.3, CURRENT_DATE(), 11),

(90.2, 182, 27.2, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 12),
(88.5, 182, 26.7, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 12),
(86.8, 182, 26.2, CURRENT_DATE(), 12),

(58.7, 160, 22.9, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 13),
(57.9, 160, 22.6, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 13),
(57.2, 160, 22.3, CURRENT_DATE(), 13),

(78.4, 175, 25.6, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 14),
(77.1, 175, 25.2, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 14),
(76.3, 175, 24.9, CURRENT_DATE(), 14);

-- Inserción de metas
INSERT INTO Meta (descripcion, fecha_inicio, fecha_fin, estado, Usuario_id) VALUES
('Perder 5kg en 2 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 45 DAY), 'En progreso', 10),
('Aumentar masa muscular', DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 80 DAY), 'En progreso', 11),
('Mejorar resistencia cardiovascular', DATE_SUB(CURRENT_DATE(), INTERVAL 20 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 40 DAY), 'En progreso', 12),
('Reducir porcentaje de grasa corporal', DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 55 DAY), 'En progreso', 13),
('Preparación para maratón', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 60 DAY), 'En progreso', 14);

-- Inserción de rutinas
INSERT INTO Rutina (nombre, descripcion, fecha_creacion, Usuario_id) VALUES
('Rutina de fuerza', 'Enfocada en el desarrollo de fuerza en tren superior e inferior', DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY), 10),
('Rutina de hipertrofia', 'Enfocada en el aumento de masa muscular', DATE_SUB(CURRENT_DATE(), INTERVAL 12 DAY), 11),
('Rutina HIIT', 'Entrenamiento de alta intensidad por intervalos', DATE_SUB(CURRENT_DATE(), INTERVAL 18 DAY), 12),
('Rutina de tonificación', 'Enfocada en definir y tonificar el cuerpo', DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), 13),
('Rutina de resistencia', 'Enfocada en mejorar la resistencia cardiovascular', DATE_SUB(CURRENT_DATE(), INTERVAL 25 DAY), 14);

-- Inserción de ejercicios
INSERT INTO Ejercicio (nombre, descripcion, series, repeticiones, tiempo_descanso) VALUES
('Sentadillas', 'Ejercicio para piernas y glúteos', 4, 12, 60),
('Press de banca', 'Ejercicio para pecho y tríceps', 4, 10, 90),
('Peso muerto', 'Ejercicio para espalda baja y piernas', 3, 8, 120),
('Dominadas', 'Ejercicio para espalda y bíceps', 3, 10, 90),
('Burpees', 'Ejercicio cardiovascular de cuerpo completo', 5, 15, 45);

-- Asociar ejercicios a rutinas
INSERT INTO Ejercicio_Rutina (orden, Ejercicio_id, Rutina_id) VALUES
(1, 1, 1), (2, 2, 1), (3, 3, 1),
(1, 2, 2), (2, 4, 2), (3, 3, 2),
(1, 5, 3), (2, 1, 3), (3, 4, 3),
(1, 1, 4), (2, 5, 4), (3, 2, 4),
(1, 5, 5), (2, 3, 5), (3, 4, 5);

-- Inserción de seguimientos de progreso
INSERT INTO Seguimiento_Progreso (
    Usuario_id, fecha_seguimiento, Rutina_id, Meta_id, 
    peso_actual, imc_actual, nivel_esfuerzo, rendimiento, ejercicios_completados,
    adherencia_dieta, sensacion_hambre, energia_diaria, 
    dificultades, logros, observaciones, calificacion_instructor, instructor_id
) VALUES
(10, DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY), 1, 1, 
 83.2, 26.3, 8, 7, 85, 
 75, 6, 7, 
 'Dificultad con el peso muerto', 'Mejoró técnica de sentadillas', 'Progresando bien en general', 7, 15),
 
(10, CURRENT_DATE(), 1, 1, 
 82.0, 25.9, 9, 8, 90, 
 80, 5, 8, 
 'Algo de fatiga al final de la semana', 'Aumentó peso en press de banca', 'Excelente progreso, muy comprometido', 8, 15),
 
(11, DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY), 2, 2, 
 64.1, 23.5, 7, 8, 80, 
 85, 4, 8, 
 'Molestias leves en rodilla derecha', 'Aumentó repeticiones en dominadas', 'Buena adherencia al plan', 8, 15),
 
(12, DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), 3, 3, 
 88.5, 26.7, 9, 7, 95, 
 70, 7, 6, 
 'Fatiga en sesiones HIIT', 'Mejoró tiempo en circuito', 'Necesita mejorar hidratación', 7, 15),
 
(13, DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY), 4, 4, 
 57.9, 22.6, 8, 9, 90, 
 90, 3, 9, 
 'Ninguna relevante', 'Excelente técnica en todos los ejercicios', 'Progreso constante y disciplina ejemplar', 9, 15),
 
(14, DATE_SUB(CURRENT_DATE(), INTERVAL 12 DAY), 5, 5, 
 77.1, 25.2, 6, 6, 75, 
 65, 8, 5, 
 'Falta de tiempo para completar rutinas', 'Mejoró resistencia en carrera', 'Necesita ajustar horarios de entrenamiento', 6, 15); 