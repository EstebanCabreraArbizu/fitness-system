-- Inserciones de usuarios clientes para el sistema de fitness

-- Inserción de tipos de usuario (si no existe)
INSERT INTO Tipo_usuario (id, nombre, descripcion) VALUES 
(1, 'Cliente', 'Usuario que busca servicios de fitness');

-- Inserción de usuarios clientes (con contraseñas en texto plano)
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
(10, 'Carlos', 'Rodríguez', '6641234567', 'carlos@ejemplo.com', 'password123', 1, 'default_user.png', NOW(), 1),
(11, 'Ana', 'Martínez', '6642345678', 'ana@ejemplo.com', 'password123', 1, 'default_user.png', NOW(), 1),
(12, 'Miguel', 'López', '6643456789', 'miguel@ejemplo.com', 'password123', 1, 'default_user.png', NOW(), 1),
(13, 'Laura', 'Sánchez', '6644567890', 'laura@ejemplo.com', 'password123', 1, 'default_user.png', NOW(), 1),
(14, 'Javier', 'González', '6645678901', 'javier@ejemplo.com', 'password123', 1, 'default_user.png', NOW(), 1);

-- Inserción de datos de clientes
INSERT INTO Cliente_datos (nivel_actividad, direccion, tipo_cliente, Usuario_id) VALUES
('Principiante', 'Calle Principal 123', 'regular', 10),
('Intermedio', 'Avenida Central 456', 'premium', 11),
('Avanzado', 'Boulevard Norte 789', 'regular', 12),
('Principiante', 'Calle Sur 321', 'premium', 13),
('Intermedio', 'Avenida Este 654', 'regular', 14);

-- Inserción de historial de medidas para clientes
INSERT INTO Historial_Medidas (peso, altura, imc, fecha_medicion, Usuario_id) VALUES
(85.5, 1.78, 27.0, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 10),
(83.2, 1.78, 26.3, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 10),
(82.0, 1.78, 25.9, CURRENT_DATE(), 10),

(65.3, 1.65, 24.0, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 11),
(64.1, 1.65, 23.5, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 11),
(63.5, 1.65, 23.3, CURRENT_DATE(), 11),

(90.2, 1.82, 27.2, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 12),
(88.5, 1.82, 26.7, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 12),
(86.8, 1.82, 26.2, CURRENT_DATE(), 12),

(58.7, 1.60, 22.9, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 13),
(57.9, 1.60, 22.6, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 13),
(57.2, 1.60, 22.3, CURRENT_DATE(), 13),

(78.4, 1.75, 25.6, DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), 14),
(77.1, 1.75, 25.2, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 14),
(76.3, 1.75, 24.9, CURRENT_DATE(), 14);

-- Inserción de disciplinas
INSERT INTO Discipline (id, nombre, descripcion) VALUES
(1, 'Musculación', 'Entrenamiento enfocado en el desarrollo muscular'),
(2, 'Cardio', 'Entrenamiento cardiovascular'),
(3, 'CrossFit', 'Entrenamiento funcional de alta intensidad'),
(4, 'Yoga', 'Disciplina que combina posturas físicas, ejercicios de respiración y meditación');

-- Asociar disciplinas a clientes
INSERT INTO Discipline_Cliente (Discipline_id, Usuario_id) VALUES
(1, 10), (2, 11), (3, 12), (4, 13), (1, 14);

-- Inserción de metas
INSERT INTO Meta (descripcion, fecha_inicio, fecha_fin, estado, Usuario_id) VALUES
('Perder 5kg en 2 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 45 DAY), 'En progreso', 10),
('Aumentar masa muscular', DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 80 DAY), 'En progreso', 11),
('Mejorar resistencia cardiovascular', DATE_SUB(CURRENT_DATE(), INTERVAL 20 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 40 DAY), 'En progreso', 12),
('Reducir porcentaje de grasa corporal', DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 55 DAY), 'En progreso', 13),
('Preparación para maratón', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 60 DAY), 'En progreso', 14);

-- Inserción de ejercicios según los IDs que se muestran en el sistema
INSERT INTO Ejercicio (id, nombre, descripcion, series, repeticiones, tiempo_descanso) VALUES
(7, 'Dominadas', 'Ejercicio para espalda y biceps', 3, 10, 90),
(11, 'Curl de biceps', 'Ejercicio de aislamiento para biceps', 3, 12, 60),
(17, 'Curl de isquiotibiales', 'Ejercicio de aislamiento para isquiotibiales', 3, 12, 60),
(18, 'Elevaciones de gemelos', 'Ejercicio para pantorrillas', 4, 20, 45),
(19, 'Burpees', 'Ejercicio cardiovascular de cuerpo completo', 5, 15, 45),
(25, 'Crunch abdominal', 'Ejercicio para abdominales superiores', 3, 20, 30),
(26, 'Elevación de piernas', 'Ejercicio para abdominales inferiores', 3, 15, 30),
(30, 'Clean and jerk', 'Levantamiento olímpico completo', 4, 8, 120),
(31, 'Box jumps', 'Saltos a caja para potencia de piernas', 4, 10, 60),
(32, 'Battle ropes', 'Ejercicio con cuerdas para resistencia y fuerza', 3, 30, 45);

-- Inserción adicional de otros ejercicios
INSERT INTO Ejercicio (nombre, descripcion, series, repeticiones, tiempo_descanso) VALUES
('Sentadillas', 'Ejercicio para piernas y glúteos', 4, 12, 60),
('Press de banca', 'Ejercicio para pecho y tríceps', 4, 10, 90),
('Peso muerto', 'Ejercicio para espalda baja y piernas', 3, 8, 120),
('Flexiones de pecho', 'Ejercicio para pectoral y tríceps con peso corporal', 3, 15, 60),
('Press militar', 'Ejercicio para hombros y tríceps', 4, 10, 90),
('Remo con barra', 'Ejercicio para espalda media', 3, 12, 90),
('Mountain climbers', 'Ejercicio cardiovascular para core y resistencia', 3, 30, 30),
('Jumping jacks', 'Ejercicio cardiovascular básico de calentamiento', 3, 30, 30),
('Saltos de cuerda', 'Ejercicio cardiovascular para coordinación y resistencia', 3, 60, 45),
('Sprint en el sitio', 'Ejercicio de alta intensidad para quemar calorías', 5, 20, 40),
('Plancha', 'Ejercicio isométrico para core', 3, 30, 45),
('Russian twist', 'Ejercicio para oblicuos con rotación', 3, 20, 30),
('Superman', 'Ejercicio para espalda baja y glúteos', 3, 15, 30),
('Kettlebell swing', 'Ejercicio con pesa rusa para glúteos y espalda', 3, 20, 45),
('Medicine ball slam', 'Lanzamiento de balón medicinal para potencia', 3, 15, 45);

-- Inserción de rutinas para los clientes
INSERT INTO Rutina (nombre, descripcion, fecha_creacion, Usuario_id) VALUES
('Rutina de fuerza', 'Enfocada en el desarrollo de fuerza en tren superior e inferior', DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY), 10),
('Rutina de hipertrofia', 'Enfocada en el aumento de masa muscular', DATE_SUB(CURRENT_DATE(), INTERVAL 12 DAY), 11),
('Rutina HIIT', 'Entrenamiento de alta intensidad por intervalos', DATE_SUB(CURRENT_DATE(), INTERVAL 18 DAY), 12),
('Rutina de tonificación', 'Enfocada en definir y tonificar el cuerpo', DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), 13),
('Rutina de resistencia', 'Enfocada en mejorar la resistencia cardiovascular', DATE_SUB(CURRENT_DATE(), INTERVAL 25 DAY), 14);

-- Asociar ejercicios a rutinas (usando los IDs correctos)
INSERT INTO Ejercicio_Rutina (orden, Ejercicio_id, Rutina_id) VALUES
-- Rutina de fuerza (Carlos)
(1, 1, 1),    -- Sentadillas (se asignará el ID correcto)
(2, 2, 1),    -- Press de banca (se asignará el ID correcto)
(3, 3, 1),    -- Peso muerto (se asignará el ID correcto)
(4, 7, 1),    -- Dominadas (ID 7 según la imagen)
(5, 30, 1),   -- Clean and jerk (ID 30 según la imagen)
(6, 32, 1),   -- Battle ropes (ID 32 según la imagen)

-- Rutina de hipertrofia (Ana)
(1, 2, 2),    -- Press de banca
(2, 7, 2),    -- Dominadas (ID 7)
(3, 11, 2),   -- Curl de biceps (ID 11)
(4, 17, 2),   -- Curl de isquiotibiales (ID 17)
(5, 18, 2),   -- Elevaciones de gemelos (ID 18)
(6, 25, 2),   -- Crunch abdominal (ID 25)

-- Rutina HIIT (Miguel)
(1, 19, 3),   -- Burpees (ID 19)
(2, 31, 3),   -- Box jumps (ID 31)
(3, 32, 3),   -- Battle ropes (ID 32)
(4, 30, 3),   -- Clean and jerk (ID 30)
(5, 7, 3),    -- Dominadas (ID 7)
(6, 25, 3),   -- Crunch abdominal (ID 25)

-- Rutina de tonificación (Laura)
(1, 1, 4),    -- Sentadillas
(2, 26, 4),   -- Elevación de piernas (ID 26)
(3, 25, 4),   -- Crunch abdominal (ID 25)
(4, 19, 4),   -- Burpees (ID 19)
(5, 17, 4),   -- Curl de isquiotibiales (ID 17)
(6, 18, 4),   -- Elevaciones de gemelos (ID 18)

-- Rutina de resistencia (Javier)
(1, 19, 5),   -- Burpees (ID 19)
(2, 31, 5),   -- Box jumps (ID 31)
(3, 32, 5),   -- Battle ropes (ID 32)
(4, 7, 5),    -- Dominadas (ID 7)
(5, 3, 5),    -- Peso muerto
(6, 25, 5);   -- Crunch abdominal (ID 25)

-- Consultas para ordenar y mostrar los ejercicios
-- Ordenados por ID
SELECT id, nombre, descripcion, series, repeticiones, tiempo_descanso 
FROM Ejercicio 
ORDER BY id;

-- Ordenados por nombre
SELECT id, nombre, descripcion, series, repeticiones, tiempo_descanso 
FROM Ejercicio 
ORDER BY nombre;

-- Ordenados por tipo de ejercicio (asumiendo que agrupamos por descripción)
SELECT id, nombre, descripcion, series, repeticiones, tiempo_descanso 
FROM Ejercicio 
ORDER BY 
  CASE 
    WHEN descripcion LIKE '%cardiovascular%' THEN 1
    WHEN descripcion LIKE '%core%' THEN 2
    WHEN descripcion LIKE '%aislamiento%' THEN 3
    ELSE 4
  END, 
  nombre;

-- Mostrar rutinas con sus ejercicios ordenados por orden de ejecución
SELECT r.id AS rutina_id, r.nombre AS rutina_nombre, 
       u.nombres AS cliente_nombre, u.apellidos AS cliente_apellidos,
       er.orden, e.id AS ejercicio_id, e.nombre AS ejercicio_nombre, 
       e.series, e.repeticiones, e.tiempo_descanso
FROM Rutina r
JOIN Usuario u ON r.Usuario_id = u.id
JOIN Ejercicio_Rutina er ON r.id = er.Rutina_id
JOIN Ejercicio e ON er.Ejercicio_id = e.id
ORDER BY r.id, er.orden; 