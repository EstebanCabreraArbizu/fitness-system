-- Script para insertar datos de prueba en la base de datos del sistema fitness

-- Insertar tipos de usuario
INSERT INTO Tipo_usuario (id, nombre, descripcion) VALUES
(1, 'Cliente', 'Usuario que busca servicios de fitness y nutrición'),
(2, 'Instructor', 'Profesional que ofrece servicios de entrenamiento y nutrición');

-- Insertar usuarios
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
-- Clientes
(1, 'Juan', 'Pérez', '1234567890', 'juan@email.com', '1958e958f5741fd7fd0560fd6eccf1a228d844cc9099ff23931335308fa8d022', 1, 'default_client.png', NOW(), 1),
(2, 'María', 'González', '2345678901', 'maria@email.com', 'b6e5e6e5c2e2e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1', 1, 'default_client.png', NOW(), 1),
(3, 'Carlos', 'Rodríguez', '3456789012', 'carlos@email.com', 'c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7c3e7', 1, 'default_client.png', NOW(), 1),
-- Instructores
(4, 'Ana', 'Martínez', '4567890123', 'ana@email.com', 'a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2', 1, 'default_instructor.png', NOW(), 2),
(5, 'Luis', 'Hernández', '5678901234', 'luis@email.com', 'd4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5', 1, 'default_instructor.png', NOW(), 2),
(6, 'Sofía', 'Díaz', '6789012345', 'sofia@email.com', 'e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6', 1, 'default_instructor.png', NOW(), 2);

-- Insertar datos de clientes
INSERT INTO Cliente_datos (nivel_actividad, direccion, tipo_cliente, Usuario_id) VALUES
('Sedentario', 'Calle Principal 123', 'Principiante', 1),
('Activo', 'Avenida Central 456', 'Intermedio', 2),
('Muy activo', 'Boulevard Norte 789', 'Avanzado', 3);

-- Insertar datos de instructores
INSERT INTO Instructor_datos (certificaciones, estudios, anios_experiencia, especialidad, Usuario_id) VALUES
('Certificado en entrenamiento funcional, Certificado en CrossFit', 'Licenciatura en Educación Física', 5, 'Fitness funcional', 4),
('Certificado en nutrición deportiva, Certificado en levantamiento de pesas', 'Licenciatura en Nutrición', 7, 'Nutrición deportiva', 5),
('Certificado en yoga, Certificado en pilates', 'Diplomado en Rehabilitación Física', 4, 'Yoga y pilates', 6);

-- Insertar historiales de medidas para clientes
INSERT INTO Historial_Medidas (peso, altura, imc, fecha_medicion, Usuario_id) VALUES
(85.5, 1.75, 27.9, NOW() - INTERVAL 30 DAY, 1),
(84.2, 1.75, 27.5, NOW() - INTERVAL 15 DAY, 1),
(83.0, 1.75, 27.1, NOW(), 1),

(65.2, 1.68, 23.1, NOW() - INTERVAL 30 DAY, 2),
(64.5, 1.68, 22.8, NOW() - INTERVAL 15 DAY, 2),
(63.8, 1.68, 22.6, NOW(), 2),

(90.0, 1.82, 27.2, NOW() - INTERVAL 30 DAY, 3),
(88.5, 1.82, 26.7, NOW() - INTERVAL 15 DAY, 3),
(87.2, 1.82, 26.3, NOW(), 3);

-- Asociar clientes con instructores
INSERT INTO Cliente_Instructor (Client_id, Instructor_id) VALUES
(1, 4),
(2, 5),
(3, 6),
(1, 5);

-- Insertar disciplinas
INSERT INTO Discipline (id, nombre, descripcion) VALUES
(1, 'Fitness', 'Actividades físicas para mejorar la condición física general'),
(2, 'Yoga', 'Práctica que conecta el cuerpo, la respiración y la mente'),
(3, 'Crossfit', 'Entrenamiento de alta intensidad y funcional'),
(4, 'Nutrición', 'Planes alimenticios para objetivos específicos');

-- Asociar disciplinas con instructores
INSERT INTO Discipline_Instructor (Discipline_id, Usuario_id) VALUES
(1, 4),
(3, 4),
(4, 5),
(2, 6),
(4, 6);

-- Asociar disciplinas con clientes
INSERT INTO Discipline_Cliente (Discipline_id, Usuario_id) VALUES
(1, 1),
(3, 1),
(4, 2),
(2, 3),
(4, 3);

-- Crear ejercicios
INSERT INTO Ejercicio (id, nombre, descripcion, series, repeticiones, tiempo_descanso) VALUES
(1, 'Sentadillas', 'Flexión de rodillas simulando sentarse', 3, 15, 60),
(2, 'Flexiones', 'Apoyo en manos y pies, flexionar codos', 3, 12, 60),
(3, 'Abdominales', 'Contracción de abdominales en suelo', 3, 20, 45),
(4, 'Burpees', 'Combinación de sentadilla, plancha y salto', 4, 10, 90),
(5, 'Plancha', 'Posición estática con apoyo en antebrazos', 3, 30, 60),
(6, 'Zancadas', 'Paso al frente flexionando rodillas', 3, 12, 60),
(7, 'Dominadas', 'Tracción en barra horizontal', 3, 8, 90),
(8, 'Peso muerto', 'Levantamiento de peso desde el suelo', 4, 10, 120);

-- Crear rutinas
INSERT INTO Rutina (id, nombre, descripcion, fecha_creacion, Usuario_id) VALUES
(1, 'Rutina Full Body', 'Entrenamiento completo para todo el cuerpo', NOW() - INTERVAL 10 DAY, 4),
(2, 'Cardio HIIT', 'Entrenamiento de alta intensidad por intervalos', NOW() - INTERVAL 7 DAY, 4),
(3, 'Fuerza y Resistencia', 'Rutina para desarrollo muscular y resistencia', NOW() - INTERVAL 5 DAY, 5),
(4, 'Yoga Flow', 'Secuencia de posturas fluidas de yoga', NOW() - INTERVAL 3 DAY, 6);

-- Asociar ejercicios a rutinas
INSERT INTO Ejercicio_Rutina (orden, Ejercicio_id, Rutina_id) VALUES
-- Rutina Full Body
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 6, 1),
-- Cardio HIIT
(1, 4, 2),
(2, 1, 2),
(3, 3, 2),
-- Fuerza y Resistencia
(1, 7, 3),
(2, 8, 3),
(3, 1, 3),
(4, 6, 3),
-- Yoga Flow
(1, 5, 4);

-- Insertar metas para clientes
INSERT INTO Meta (descripcion, fecha_inicio, fecha_fin, estado, Usuario_id) VALUES
('Perder 5kg', NOW(), DATE_ADD(NOW(), INTERVAL 2 MONTH), 'En progreso', 1),
('Aumentar masa muscular', NOW() - INTERVAL 1 MONTH, DATE_ADD(NOW(), INTERVAL 3 MONTH), 'En progreso', 2),
('Mejorar flexibilidad', NOW() - INTERVAL 15 DAY, DATE_ADD(NOW(), INTERVAL 45 DAY), 'En progreso', 3);

-- Crear productos
INSERT INTO Product (title, category, description, marca, purchase_price, price, descuento, previous_price, date, user_id, status, relevant, additional, outstanding, palabras_claves, fecha_inicio, fecha_fin) VALUES
('Proteína Whey', 1, 'Proteína en polvo para después del entrenamiento', 'FitNutrition', 25.00, 39.99, 0.00, NULL, NOW(), 5, 1, 1, 'Alto contenido proteico', 1, 'proteína, suplemento, recuperación', NULL, NULL),
('Mancuernas ajustables', 2, 'Set de mancuernas con peso ajustable', 'FitGear', 45.00, 89.99, 10.00, 99.99, NOW(), 4, 1, 1, 'Incluye estuche', 1, 'mancuernas, pesas, entrenamiento', NULL, NULL),
('Mat de Yoga', 2, 'Colchoneta antideslizante para yoga', 'ZenFit', 15.00, 29.99, 0.00, NULL, NOW(), 6, 1, 0, 'Material ecológico', 1, 'yoga, mat, colchoneta', NULL, NULL);

-- Asociar productos con instructores
INSERT INTO Instructor_Products (Product_id, Usuario_id) VALUES
(1, 5),
(2, 4),
(3, 6);

-- Crear imágenes para productos
INSERT INTO Product_images (image_name, color_id, Product_id) VALUES
('proteina_whey_1.jpg', 1, 1),
('proteina_whey_2.jpg', 2, 1),
('mancuernas_1.jpg', 1, 2),
('mancuernas_2.jpg', 2, 2),
('mat_yoga_1.jpg', 1, 3),
('mat_yoga_2.jpg', 2, 3);

-- Crear dietas
INSERT INTO Dieta (id, tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, duracion_dieta, fecha_registro, edad, alergias, enfermedad_cronica, alergia_medicamento, dias_semana, meta_calorias, status, Discipline_id, Client_id, Instructor_id) VALUES
(1, 'Déficit calórico', 'Plan de pérdida de peso', 'Plan alimenticio para reducción de peso', NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), '30 días', NOW() - INTERVAL 2 DAY, '30-40', 'Ninguna', 'Ninguna', 'Ninguna', 'Lunes-Viernes', 1800, 1, 4, 1, 5),
(2, 'Alto en proteínas', 'Plan de aumento muscular', 'Plan alimenticio para ganancia de masa muscular', NOW(), DATE_ADD(NOW(), INTERVAL 45 DAY), '45 días', NOW() - INTERVAL 1 DAY, '25-35', 'Lactosa', 'Ninguna', 'Ninguna', 'Todos los días', 2500, 1, 4, 2, 5),
(3, 'Equilibrada', 'Plan de mantenimiento', 'Plan alimenticio balanceado', NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), '30 días', NOW(), '40-50', 'Gluten', 'Hipertensión', 'Ninguna', 'Todos los días', 2000, 1, 4, 3, 6);

-- Crear comidas para dietas
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, recomendacion, image_name, status, Dieta_id) VALUES
-- Dieta 1: Plan pérdida de peso
('Desayuno', 'Lunes', '8:00', 'Avena con frutas', 'Avena cocida con manzana y canela', 300, 12, 45, 5, 'Consumir con un vaso de agua', 'avena_frutas.jpg', 1, 1),
('Almuerzo', 'Lunes', '13:00', 'Ensalada de pollo', 'Pechuga de pollo a la plancha con vegetales variados', 450, 40, 25, 10, 'Usar aceite de oliva como aderezo', 'ensalada_pollo.jpg', 1, 1),
('Cena', 'Lunes', '20:00', 'Pescado al horno', 'Filete de pescado al horno con brócoli al vapor', 350, 35, 15, 12, 'Condimentar con limón y especias', 'pescado_horno.jpg', 1, 1),

-- Dieta 2: Plan aumento muscular
('Desayuno', 'Lunes', '7:30', 'Omelette proteico', 'Omelette de claras con espinacas y pavo', 400, 35, 20, 15, 'Acompañar con pan integral', 'omelette_proteico.jpg', 1, 2),
('Almuerzo', 'Lunes', '13:00', 'Arroz con pollo', 'Arroz integral con pollo y vegetales salteados', 650, 45, 65, 15, 'Consumir dentro de los 90 minutos post-entrenamiento', 'arroz_pollo.jpg', 1, 2),
('Merienda', 'Lunes', '16:30', 'Batido proteico', 'Batido de proteínas con plátano y mantequilla de maní', 350, 30, 30, 12, 'Ideal para después del entrenamiento', 'batido_proteico.jpg', 1, 2),
('Cena', 'Lunes', '20:30', 'Salmón con quinoa', 'Filete de salmón con quinoa y espárragos', 550, 40, 40, 20, 'Rica fuente de ácidos grasos omega-3', 'salmon_quinoa.jpg', 1, 2),

-- Dieta 3: Plan mantenimiento
('Desayuno', 'Lunes', '8:00', 'Tostadas con aguacate', 'Tostadas integrales con aguacate y huevo', 400, 20, 35, 20, 'Usar pan sin gluten', 'tostadas_aguacate.jpg', 1, 3),
('Almuerzo', 'Lunes', '13:30', 'Bowl de quinoa', 'Bowl de quinoa con garbanzos y verduras asadas', 500, 25, 60, 15, 'Aliñar con limón y hierbas', 'bowl_quinoa.jpg', 1, 3),
('Cena', 'Lunes', '20:00', 'Pavo al horno', 'Pechuga de pavo al horno con batata asada', 450, 35, 30, 10, 'Bajo en sodio', 'pavo_horno.jpg', 1, 3);

-- Imágenes para dietas
INSERT INTO Dieta_images (image_name, Dieta_id) VALUES
('dieta_perdida_peso.jpg', 1),
('dieta_aumento_muscular.jpg', 2),
('dieta_mantenimiento.jpg', 3);
