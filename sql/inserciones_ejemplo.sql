-- Inserciones de ejemplo para el sistema de fitness

-- Insertando Tipo de usuario (si no existen ya)
INSERT INTO Tipo_usuario (id, nombre, descripcion) VALUES 
(1, 'Cliente', 'Usuario que busca servicios de fitness'),
(2, 'Instructor', 'Profesional que ofrece servicios de fitness');

-- Insertando Disciplinas
INSERT INTO Discipline (nombre, descripcion) VALUES
('Musculación', 'Entrenamiento enfocado en el desarrollo muscular y fuerza'),
('Crossfit', 'Entrenamiento funcional de alta intensidad'),
('Nutrición Deportiva', 'Alimentación especializada para rendimiento deportivo'),
('Fitness Funcional', 'Entrenamiento enfocado en mejorar la funcionalidad del cuerpo'),
('Pérdida de Peso', 'Programas especializados para reducción de grasa corporal');

-- Insertando Instructores de ejemplo
INSERT INTO Usuario (nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
('Carlos', 'Martínez', '6641234567', 'carlos.martinez@fitsystem.com', SHA2('Inst123!', 256), 1, 'instructor1.jpg', NOW(), 2),
('Ana', 'Gómez', '6642345678', 'ana.gomez@fitsystem.com', SHA2('Inst123!', 256), 1, 'instructor2.jpg', NOW(), 2),
('Roberto', 'Sánchez', '6643456789', 'roberto.sanchez@fitsystem.com', SHA2('Inst123!', 256), 1, 'instructor3.jpg', NOW(), 2);

-- Insertando datos de instructores
INSERT INTO Instructor_datos (certificaciones, estudios, anios_experiencia, especialidad, Usuario_id) VALUES
('Certificado en Entrenamiento Personal NSCA, Certificado en TRX', 'Licenciatura en Educación Física', 5, 'Musculación', LAST_INSERT_ID()-2),
('Certificado CrossFit L2, Nutricionista Deportiva', 'Maestría en Nutrición Deportiva', 7, 'Nutrición y CrossFit', LAST_INSERT_ID()-1),
('Certificado en Personal Training NASM, Especialista en Rehabilitación', 'Fisioterapeuta', 4, 'Fitness Funcional', LAST_INSERT_ID());

-- Asignando disciplinas a instructores
INSERT INTO Discipline_Instructor (Discipline_id, Usuario_id) VALUES
(1, LAST_INSERT_ID()-2), -- Carlos - Musculación
(4, LAST_INSERT_ID()-2), -- Carlos - Fitness Funcional
(2, LAST_INSERT_ID()-1), -- Ana - Crossfit
(3, LAST_INSERT_ID()-1), -- Ana - Nutrición Deportiva
(4, LAST_INSERT_ID()), -- Roberto - Fitness Funcional
(5, LAST_INSERT_ID()); -- Roberto - Pérdida de Peso

-- Insertando Clientes de ejemplo
INSERT INTO Usuario (nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
('Juan', 'Pérez', '6649876543', 'juan.perez@email.com', SHA2('Client123!', 256), 1, 'cliente1.jpg', NOW(), 1),
('María', 'López', '6648765432', 'maria.lopez@email.com', SHA2('Client123!', 256), 1, 'cliente2.jpg', NOW(), 1),
('Pedro', 'García', '6647654321', 'pedro.garcia@email.com', SHA2('Client123!', 256), 1, 'cliente3.jpg', NOW(), 1),
('Laura', 'Rodríguez', '6646543210', 'laura.rodriguez@email.com', SHA2('Client123!', 256), 1, 'cliente4.jpg', NOW(), 1),
('Miguel', 'Fernández', '6645432109', 'miguel.fernandez@email.com', SHA2('Client123!', 256), 1, 'cliente5.jpg', NOW(), 1);

-- Insertando datos de clientes
INSERT INTO Cliente_datos (nivel_actividad, direccion, tipo_cliente, Usuario_id, fecha_pago) VALUES
('Principiante', 'Calle Primera #123', 'regular', LAST_INSERT_ID()-4, DATE_ADD(CURDATE(), INTERVAL -5 DAY)),
('Intermedio', 'Avenida Central #456', 'premium', LAST_INSERT_ID()-3, DATE_ADD(CURDATE(), INTERVAL -2 DAY)),
('Avanzado', 'Boulevard Norte #789', 'regular', LAST_INSERT_ID()-2, DATE_ADD(CURDATE(), INTERVAL -10 DAY)),
('Intermedio', 'Calle Sur #1011', 'premium', LAST_INSERT_ID()-1, DATE_ADD(CURDATE(), INTERVAL -1 DAY)),
('Principiante', 'Avenida Este #1213', 'regular', LAST_INSERT_ID(), DATE_ADD(CURDATE(), INTERVAL -7 DAY));

-- Asignando disciplinas a clientes
INSERT INTO Discipline_Cliente (Discipline_id, Usuario_id) VALUES
(1, LAST_INSERT_ID()-4), -- Juan - Musculación
(5, LAST_INSERT_ID()-3), -- María - Pérdida de Peso
(2, LAST_INSERT_ID()-2), -- Pedro - Crossfit
(4, LAST_INSERT_ID()-1), -- Laura - Fitness Funcional
(3, LAST_INSERT_ID()); -- Miguel - Nutrición Deportiva

-- Asignando clientes a instructores
INSERT INTO Cliente_Instructor (Usuario_id, Usuario_2_id) VALUES
(LAST_INSERT_ID()-4, LAST_INSERT_ID()-7), -- Juan con Carlos
(LAST_INSERT_ID()-3, LAST_INSERT_ID()-6), -- María con Ana
(LAST_INSERT_ID()-2, LAST_INSERT_ID()-6), -- Pedro con Ana
(LAST_INSERT_ID()-1, LAST_INSERT_ID()-5), -- Laura con Roberto
(LAST_INSERT_ID(), LAST_INSERT_ID()-6); -- Miguel con Ana

-- Insertando medidas de clientes
INSERT INTO Historial_Medidas (peso, altura, imc, fecha_medicion, Usuario_id) VALUES
(85.5, 178, 27.0, DATE_ADD(CURDATE(), INTERVAL -60 DAY), LAST_INSERT_ID()-4), -- Juan inicial
(83.2, 178, 26.3, DATE_ADD(CURDATE(), INTERVAL -30 DAY), LAST_INSERT_ID()-4), -- Juan progreso
(80.8, 178, 25.5, CURDATE(), LAST_INSERT_ID()-4), -- Juan actual

(68.5, 165, 25.2, DATE_ADD(CURDATE(), INTERVAL -45 DAY), LAST_INSERT_ID()-3), -- María inicial
(67.0, 165, 24.6, DATE_ADD(CURDATE(), INTERVAL -20 DAY), LAST_INSERT_ID()-3), -- María progreso
(65.7, 165, 24.1, CURDATE(), LAST_INSERT_ID()-3), -- María actual

(78.0, 175, 25.5, DATE_ADD(CURDATE(), INTERVAL -90 DAY), LAST_INSERT_ID()-2), -- Pedro inicial
(79.5, 175, 26.0, DATE_ADD(CURDATE(), INTERVAL -60 DAY), LAST_INSERT_ID()-2), -- Pedro progreso (aumento masa)
(81.0, 175, 26.4, CURDATE(), LAST_INSERT_ID()-2), -- Pedro actual

(62.0, 162, 23.6, DATE_ADD(CURDATE(), INTERVAL -30 DAY), LAST_INSERT_ID()-1), -- Laura inicial
(60.5, 162, 23.1, CURDATE(), LAST_INSERT_ID()-1), -- Laura actual

(90.0, 180, 27.8, DATE_ADD(CURDATE(), INTERVAL -15 DAY), LAST_INSERT_ID()), -- Miguel inicial
(88.5, 180, 27.3, CURDATE(), LAST_INSERT_ID()); -- Miguel actual

-- Insertando metas para clientes
INSERT INTO Meta (descripcion, fecha_inicio, fecha_fin, estado, Usuario_id) VALUES
('Reducir 10kg de peso', DATE_ADD(CURDATE(), INTERVAL -60 DAY), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'En progreso', LAST_INSERT_ID()-4), -- Juan
('Participar en media maratón', DATE_ADD(CURDATE(), INTERVAL -45 DAY), DATE_ADD(CURDATE(), INTERVAL 45 DAY), 'En progreso', LAST_INSERT_ID()-3), -- María
('Aumentar masa muscular 5kg', DATE_ADD(CURDATE(), INTERVAL -90 DAY), DATE_ADD(CURDATE(), INTERVAL 0 DAY), 'Completada', LAST_INSERT_ID()-2), -- Pedro
('Mejorar flexibilidad y postura', DATE_ADD(CURDATE(), INTERVAL -30 DAY), DATE_ADD(CURDATE(), INTERVAL 60 DAY), 'En progreso', LAST_INSERT_ID()-1), -- Laura
('Desarrollar hábitos alimenticios saludables', DATE_ADD(CURDATE(), INTERVAL -15 DAY), DATE_ADD(CURDATE(), INTERVAL 75 DAY), 'En progreso', LAST_INSERT_ID()); -- Miguel

-- Insertando rutinas para clientes
INSERT INTO Rutina (nombre, descripcion, fecha_creacion, Usuario_id) VALUES
('Rutina Pérdida de Peso', 'Rutina enfocada en ejercicios de cardio y quema de grasa', DATE_ADD(CURDATE(), INTERVAL -58 DAY), LAST_INSERT_ID()-4), -- Juan
('Preparación Media Maratón', 'Plan de entrenamiento cardiovascular progresivo', DATE_ADD(CURDATE(), INTERVAL -43 DAY), LAST_INSERT_ID()-3), -- María
('Hipertrofia Muscular', 'Rutina de fuerza e hipertrofia para aumento de masa muscular', DATE_ADD(CURDATE(), INTERVAL -88 DAY), LAST_INSERT_ID()-2), -- Pedro
('Rehabilitación Postural', 'Ejercicios de flexibilidad y fortalecimiento de core', DATE_ADD(CURDATE(), INTERVAL -28 DAY), LAST_INSERT_ID()-1), -- Laura
('Introducción al Fitness', 'Rutina básica para principiantes con enfoque en técnica', DATE_ADD(CURDATE(), INTERVAL -13 DAY), LAST_INSERT_ID()); -- Miguel

-- Insertando ejercicios
INSERT INTO Ejercicio (nombre, descripcion, series, repeticiones, tiempo_descanso) VALUES
('Sentadillas', 'Ejercicio compuesto para piernas y glúteos', 4, 12, 60),
('Press de Banca', 'Ejercicio compuesto para pectoral y tríceps', 4, 10, 90),
('Dominadas', 'Ejercicio para espalda y bíceps', 3, 8, 60),
('Planchas', 'Ejercicio isométrico para core', 3, 30, 45),
('Burpees', 'Ejercicio cardiovascular de alta intensidad', 3, 15, 30),
('Peso Muerto', 'Ejercicio compuesto para espalda baja y piernas', 4, 8, 120),
('Mountain Climbers', 'Ejercicio cardiovascular para core', 3, 20, 30),
('Zancadas', 'Ejercicio unilateral para piernas', 3, 12, 45),
('Fondos', 'Ejercicio para tríceps y hombros', 3, 10, 60),
('Remo con Barra', 'Ejercicio para espalda media', 3, 12, 60);

-- Asignando ejercicios a rutinas
INSERT INTO Ejercicio_Rutina (orden, Ejercicio_id, Rutina_id) VALUES
(1, 1, LAST_INSERT_ID()-4), -- Sentadillas - Rutina Juan
(2, 5, LAST_INSERT_ID()-4), -- Burpees - Rutina Juan
(3, 7, LAST_INSERT_ID()-4), -- Mountain Climbers - Rutina Juan
(4, 8, LAST_INSERT_ID()-4), -- Zancadas - Rutina Juan

(1, 5, LAST_INSERT_ID()-3), -- Burpees - Rutina María
(2, 7, LAST_INSERT_ID()-3), -- Mountain Climbers - Rutina María
(3, 8, LAST_INSERT_ID()-3), -- Zancadas - Rutina María

(1, 2, LAST_INSERT_ID()-2), -- Press de Banca - Rutina Pedro
(2, 3, LAST_INSERT_ID()-2), -- Dominadas - Rutina Pedro
(3, 6, LAST_INSERT_ID()-2), -- Peso Muerto - Rutina Pedro
(4, 10, LAST_INSERT_ID()-2), -- Remo con Barra - Rutina Pedro

(1, 4, LAST_INSERT_ID()-1), -- Planchas - Rutina Laura
(2, 8, LAST_INSERT_ID()-1), -- Zancadas - Rutina Laura
(3, 9, LAST_INSERT_ID()-1), -- Fondos - Rutina Laura

(1, 1, LAST_INSERT_ID()), -- Sentadillas - Rutina Miguel
(2, 2, LAST_INSERT_ID()), -- Press de Banca - Rutina Miguel
(3, 4, LAST_INSERT_ID()); -- Planchas - Rutina Miguel

-- Insertando dietas
INSERT INTO Dieta (tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, duracion_dieta, fecha_registro,
            edad, alergias, enfermedad_cronica, alergia_medicamento, dias_semana, meta_calorias, status, Discipline_id, Usuario_id, Usuario_2_id) VALUES
('Hipocalórica', 'Dieta de definición', 'Plan alimenticio para reducción de grasa corporal', 
 DATE_ADD(CURDATE(), INTERVAL -58 DAY), DATE_ADD(CURDATE(), INTERVAL 32 DAY), '3 meses', DATE_ADD(CURDATE(), INTERVAL -59 DAY),
 '35', 'Ninguna', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 1800, 1, 5, LAST_INSERT_ID()-9, LAST_INSERT_ID()-12), -- Juan con Carlos

('Deportiva', 'Dieta para runner', 'Plan nutricional para corredores de media y larga distancia', 
 DATE_ADD(CURDATE(), INTERVAL -43 DAY), DATE_ADD(CURDATE(), INTERVAL 47 DAY), '3 meses', DATE_ADD(CURDATE(), INTERVAL -44 DAY),
 '28', 'Gluten', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 2200, 1, 3, LAST_INSERT_ID()-8, LAST_INSERT_ID()-11), -- María con Ana

('Hipercalórica', 'Dieta para ganancia muscular', 'Plan alimenticio para aumento de masa muscular', 
 DATE_ADD(CURDATE(), INTERVAL -88 DAY), DATE_ADD(CURDATE(), INTERVAL 2 DAY), '3 meses', DATE_ADD(CURDATE(), INTERVAL -89 DAY),
 '32', 'Lactosa', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 3000, 1, 1, LAST_INSERT_ID()-7, LAST_INSERT_ID()-11), -- Pedro con Ana

('Equilibrada', 'Dieta de salud general', 'Plan nutricional balanceado para salud y bienestar', 
 DATE_ADD(CURDATE(), INTERVAL -28 DAY), DATE_ADD(CURDATE(), INTERVAL 62 DAY), '3 meses', DATE_ADD(CURDATE(), INTERVAL -29 DAY),
 '40', 'Ninguna', 'Hipotiroidismo', 'Ninguna', 'Lunes-Domingo', 1900, 1, 4, LAST_INSERT_ID()-6, LAST_INSERT_ID()-10), -- Laura con Roberto

('Detox', 'Dieta depurativa', 'Plan alimenticio para limpieza y mejora del sistema digestivo', 
 DATE_ADD(CURDATE(), INTERVAL -13 DAY), DATE_ADD(CURDATE(), INTERVAL 77 DAY), '3 meses', DATE_ADD(CURDATE(), INTERVAL -14 DAY),
 '45', 'Frutos secos', 'Hipertensión', 'Ninguna', 'Lunes-Domingo', 2000, 1, 3, LAST_INSERT_ID()-5, LAST_INSERT_ID()-11); -- Miguel con Ana

-- Insertar comidas (solo algunos ejemplos)
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, 
                    recomendacion, image_name, status, Dieta_id) VALUES
('Desayuno', 'Lunes', '08:00', 'Avena con frutas', 'Avena con plátano, fresas y arándanos', 320, 12, 45, 8, 
 'Consumir dentro de la primera hora después de despertar', 'avena.jpg', 1, LAST_INSERT_ID()-4), -- Dieta Juan
 
('Comida', 'Lunes', '14:00', 'Pechuga de pollo con verduras', 'Pechuga a la plancha con ensalada de verduras', 450, 35, 15, 20, 
 'Añadir limón para mejor digestión', 'pollo_verduras.jpg', 1, LAST_INSERT_ID()-4), -- Dieta Juan
 
('Desayuno', 'Lunes', '07:00', 'Batido energético', 'Batido de plátano, frutos rojos y proteína', 350, 25, 40, 5, 
 'Ideal antes del entrenamiento matutino', 'batido.jpg', 1, LAST_INSERT_ID()-3), -- Dieta María
 
('Cena', 'Lunes', '20:00', 'Salmón con quinoa', 'Filete de salmón al horno con guarnición de quinoa', 520, 35, 30, 25, 
 'Rica fuente de omega-3', 'salmon.jpg', 1, LAST_INSERT_ID()-3), -- Dieta María
 
('Desayuno', 'Lunes', '08:00', 'Tortilla proteica', 'Tortilla de claras con espinacas y queso bajo en grasa', 380, 30, 10, 22, 
 'Acompañar con pan integral', 'tortilla.jpg', 1, LAST_INSERT_ID()-2); -- Dieta Pedro

-- Insertar seguimientos de progreso
INSERT INTO Seguimiento_Progreso (
    Usuario_id, fecha_seguimiento, Rutina_id, Meta_id, Dieta_id,
    peso_actual, imc_actual, nivel_esfuerzo, rendimiento, ejercicios_completados,
    adherencia_dieta, sensacion_hambre, energia_diaria, dificultades, logros,
    observaciones, calificacion_instructor, instructor_id
) VALUES
-- Seguimientos Juan
(LAST_INSERT_ID()-9, DATE_ADD(CURDATE(), INTERVAL -45 DAY), LAST_INSERT_ID()-9, LAST_INSERT_ID()-4, LAST_INSERT_ID()-4,
 83.2, 26.3, 7, 6, 85,
 70, 8, 6, 'Dificultad con los burpees por problemas en las rodillas', 'Ha mejorado resistencia en cardio',
 'Necesita trabajar en técnica de sentadillas', 7, LAST_INSERT_ID()-12),
 
(LAST_INSERT_ID()-9, DATE_ADD(CURDATE(), INTERVAL -15 DAY), LAST_INSERT_ID()-9, LAST_INSERT_ID()-4, LAST_INSERT_ID()-4,
 81.5, 25.7, 8, 7, 90,
 75, 6, 7, 'Sigue con molestias en rodillas con alto impacto', 'Notable mejora en capacidad cardiovascular',
 'Se ajustará rutina para reducir impacto en rodillas', 8, LAST_INSERT_ID()-12),

-- Seguimientos María
(LAST_INSERT_ID()-8, DATE_ADD(CURDATE(), INTERVAL -35 DAY), LAST_INSERT_ID()-8, LAST_INSERT_ID()-3, LAST_INSERT_ID()-3,
 67.0, 24.6, 9, 8, 95,
 85, 4, 8, 'Falta de tiempo algunos días por trabajo', 'Excelente progreso en rendimiento de carrera',
 'Preparada para aumentar distancia en próximas semanas', 9, LAST_INSERT_ID()-11),

(LAST_INSERT_ID()-8, DATE_ADD(CURDATE(), INTERVAL -7 DAY), LAST_INSERT_ID()-8, LAST_INSERT_ID()-3, LAST_INSERT_ID()-3,
 65.7, 24.1, 9, 9, 100,
 90, 3, 9, 'Ninguna relevante', 'Ha alcanzado nuevo récord personal en 10K',
 'Excelente adherencia al plan, lista para media maratón', 10, LAST_INSERT_ID()-11),

-- Seguimientos Pedro
(LAST_INSERT_ID()-7, DATE_ADD(CURDATE(), INTERVAL -60 DAY), LAST_INSERT_ID()-7, LAST_INSERT_ID()-2, LAST_INSERT_ID()-2,
 79.5, 26.0, 8, 7, 90,
 80, 5, 7, 'Algunas molestias en hombro con press de banca', 'Aumento de fuerza en ejercicios compuestos',
 'Trabajar en movilidad de hombros', 8, LAST_INSERT_ID()-11),
 
(LAST_INSERT_ID()-7, DATE_ADD(CURDATE(), INTERVAL -30 DAY), LAST_INSERT_ID()-7, LAST_INSERT_ID()-2, LAST_INSERT_ID()-2,
 80.2, 26.2, 9, 8, 95,
 85, 4, 8, 'Ninguna relevante', 'Progreso considerable en todos los ejercicios',
 'Excelente técnica y constancia', 9, LAST_INSERT_ID()-11),

-- Seguimiento Laura
(LAST_INSERT_ID()-6, DATE_ADD(CURDATE(), INTERVAL -15 DAY), LAST_INSERT_ID()-6, LAST_INSERT_ID()-1, LAST_INSERT_ID()-1,
 61.2, 23.3, 7, 7, 80,
 70, 5, 7, 'Dificultad con fondos por falta de fuerza', 'Mejora notable en postura general',
 'Necesita fortalecer brazos y hombros', 7, LAST_INSERT_ID()-10),

-- Seguimiento Miguel
(LAST_INSERT_ID()-5, DATE_ADD(CURDATE(), INTERVAL -7 DAY), LAST_INSERT_ID()-5, LAST_INSERT_ID(), LAST_INSERT_ID(),
 89.0, 27.5, 6, 5, 70,
 65, 7, 6, 'Fatiga rápida con ejercicios básicos', 'Está aprendiendo técnica correcta',
 'Necesita mejorar resistencia general', 6, LAST_INSERT_ID()-11);

-- Insertar imágenes de seguimiento (ejemplos)
INSERT INTO Seguimiento_Imagen (Seguimiento_Progreso_id, nombre_imagen, tipo, fecha_carga) VALUES
(LAST_INSERT_ID()-6, 'juan_antes_1.jpg', 'antes', DATE_ADD(CURDATE(), INTERVAL -45 DAY)),
(LAST_INSERT_ID()-5, 'juan_progreso_1.jpg', 'durante', DATE_ADD(CURDATE(), INTERVAL -15 DAY)),
(LAST_INSERT_ID()-4, 'maria_antes_1.jpg', 'antes', DATE_ADD(CURDATE(), INTERVAL -35 DAY)),
(LAST_INSERT_ID()-3, 'maria_despues_1.jpg', 'despues', DATE_ADD(CURDATE(), INTERVAL -7 DAY)),
(LAST_INSERT_ID()-2, 'pedro_antes_1.jpg', 'antes', DATE_ADD(CURDATE(), INTERVAL -60 DAY)),
(LAST_INSERT_ID()-1, 'pedro_despues_1.jpg', 'despues', DATE_ADD(CURDATE(), INTERVAL -30 DAY)),
(LAST_INSERT_ID(), 'laura_antes_1.jpg', 'antes', DATE_ADD(CURDATE(), INTERVAL -15 DAY)); 