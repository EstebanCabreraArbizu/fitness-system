-- Inserción de tipos de usuario
INSERT INTO Tipo_usuario (id, nombre, descripcion) VALUES 
(1, 'Cliente', 'Usuario que busca servicios de fitness'),
(2, 'Instructor', 'Profesional que ofrece servicios de fitness');

-- Inserción de usuarios (con contraseñas hasheadas usando SHA2)
INSERT INTO Usuario (id, nombres, apellidos, celular, email, contrasenia, status, imagen, fecha_registro, Tipo_usuario_id) VALUES
(1, 'Cliente', 'Ejemplo', '1234567890', 'cliente@ejemplo.com', SHA2('Cliente123!', 256), 1, 'default_user.png', NOW(), 1),
(2, 'Instructor', 'Ejemplo', '0987654321', 'instructor@ejemplo.com', SHA2('Instructor123!', 256), 1, 'default_user.png', NOW(), 2),
(3, 'Admin', 'Sistema', '5555555555', 'admin@sistema.com', SHA2('Admin123!', 256), 1, 'default_user.png', NOW(), 2);

-- Inserción de datos del cliente
INSERT INTO Cliente_datos (id, nivel_actividad, direccion, tipo_cliente, Usuario_id, fecha_pago) VALUES
(1, 'Moderado', 'Calle Cliente 123', 'regular', 1, DATE_ADD(CURRENT_DATE(), INTERVAL -5 DAY));

-- Inserción de datos del instructor
INSERT INTO Instructor_datos (id, certificaciones, estudios, anios_experiencia, especialidad, Usuario_id) VALUES
(1, 'Certificado de Entrenador Personal', 'Licenciatura en Educación Física', 5, 'Entrenamiento funcional', 2),
(2, 'Certificación en Nutrición Deportiva', 'Maestría en Ciencias del Deporte', 8, 'Nutrición deportiva', 3);

-- Inserción de un registro en Historial_Medidas para el cliente
INSERT INTO Historial_Medidas (id, peso, altura, imc, fecha_medicion, Usuario_id) VALUES
(1, 70.5, 175, 23.0, NOW(), 1);

-- Inserción de disciplinas
INSERT INTO Discipline (id, nombre, descripcion) VALUES
(1, 'Fitness General', 'Entrenamiento general de fitness y acondicionamiento físico'),
(2, 'Nutrición Deportiva', 'Asesoramiento nutricional para deportistas'),
(3, 'Musculación', 'Entrenamiento enfocado en desarrollo muscular');

-- Asociar disciplina con instructores
INSERT INTO Discipline_Instructor (id, Discipline_id, Usuario_id) VALUES
(1, 1, 2),
(2, 2, 2),
(3, 2, 3),
(4, 3, 3);

-- Asociar cliente con instructor
INSERT INTO Cliente_Instructor (id, Usuario_id, Usuario_2_id) VALUES
(1, 1, 2),
(2, 1, 3);

-- Asociar cliente con disciplina
INSERT INTO Discipline_Cliente (id, Discipline_id, Usuario_id) VALUES
(1, 1, 1),
(2, 2, 1);

-- Crear rutina
INSERT INTO Rutina (id, nombre, descripcion, fecha_creacion, Usuario_id) VALUES
(1, 'Rutina inicial', 'Rutina para principiantes con ejercicios básicos', NOW(), 1);

-- Crear ejercicios
INSERT INTO Ejercicio (id, nombre, descripcion, series, repeticiones, tiempo_descanso) VALUES
(1, 'Sentadillas', 'Ejercicio para piernas con peso corporal', 3, 15, 60),
(2, 'Flexiones de pecho', 'Ejercicio para pectorales con peso corporal', 3, 12, 60),
(3, 'Plancha', 'Ejercicio isométrico para core', 3, 30, 45);

-- Asociar ejercicios a rutina
INSERT INTO Ejercicio_Rutina (id, orden, Ejercicio_id, Rutina_id) VALUES
(1, 1, 1, 1),
(2, 2, 2, 1),
(3, 3, 3, 1);

-- Crear una meta para el cliente
INSERT INTO Meta (id, descripcion, fecha_inicio, fecha_fin, estado, Usuario_id) VALUES
(1, 'Perder 5kg en 3 meses', '2023-05-01', '2023-07-31', 'En progreso', 1);

-- Crear una dieta
INSERT INTO Dieta (id, tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, duracion_dieta, fecha_registro, 
                   edad, alergias, enfermedad_cronica, alergia_medicamento, dias_semana, meta_calorias, 
                   status, Discipline_id, Usuario_id, Usuario_2_id) VALUES
(1, 'Pérdida de peso', 'Dieta balanceada baja en calorías', 'Dieta equilibrada para bajar de peso de forma gradual', 
   '2023-05-01', '2023-07-31', '3 meses', NOW(), '30-40', 'Ninguna', 'Ninguna', 'Ninguna', 
   'Lunes-Viernes', 1800, 1, 2, 1, 2);

-- Crear comidas para la dieta
INSERT INTO Comida (id, tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, 
                   grasas, recomendacion, image_name, status, Dieta_id) VALUES
(1, 'Desayuno', 'Lunes', '08:00', 'Desayuno proteico', 'Yogurt con frutas y granola', 
   350, 15, 45, 12, 'Consumir despacio', 'desayuno.jpg', 1, 1),
(2, 'Almuerzo', 'Lunes', '13:00', 'Ensalada de pollo', 'Ensalada verde con pechuga de pollo a la parrilla', 
   450, 35, 20, 15, 'Añadir limón al gusto', 'ensalada.jpg', 1, 1),
(3, 'Cena', 'Lunes', '20:00', 'Cena ligera', 'Sopa de verduras con pescado al horno', 
   380, 25, 25, 12, 'Evitar pan', 'cena.jpg', 1, 1);

-- Crear imágenes para la dieta
INSERT INTO Dieta_images (id, image_name, Dieta_id) VALUES
(1, 'dieta1.jpg', 1),
(2, 'plan_dieta.jpg', 1);

-- Crear productos
INSERT INTO Product (id, title, category, description, marca, purchase_price, price, descuento, 
                    previous_price, date, user_id, status, relevant, outstanding, 
                    palabras_claves, fecha_inicio, fecha_fin) VALUES
(1, 'Proteína Whey', 1, 'Proteína de suero de leche de alta calidad', 
   'FitPro', 25.00, 40.00, 0.00, 45.00, '2023-04-15', 2, 1, 1, 1, 
   'proteina, suplemento, fitness', '2023-04-15', '2023-12-31'),
(2, 'Banda elástica', 2, 'Banda de resistencia para ejercicios', 
   'GymPlus', 8.00, 15.00, 2.00, 17.00, '2023-04-20', 3, 1, 0, 1, 
   'banda, resistencia, ejercicio', '2023-04-20', '2023-12-31');

-- Crear imágenes para productos
INSERT INTO Product_images (id, image_name, color_id, Product_id) VALUES
(1, 'proteina1.jpg', 1, 1),
(2, 'proteina2.jpg', 2, 1),
(3, 'banda1.jpg', 1, 2);

-- Asociar productos con instructores
INSERT INTO Instructor_Products (id, Product_id, Usuario_id) VALUES
(1, 1, 2),
(2, 2, 3);

-- Insertar seguimiento de progreso
INSERT INTO Seguimiento_Progreso (
    Usuario_id, fecha_seguimiento, Rutina_id, Meta_id, 
    peso_actual, imc_actual, nivel_esfuerzo, rendimiento, ejercicios_completados,
    adherencia_dieta, sensacion_hambre, energia_diaria, 
    dificultades, logros, observaciones, calificacion_instructor, instructor_id
) VALUES
(1, DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), 1, 1, 
 72.0, 23.5, 7, 6, 80, 
 75, 6, 7, 
 'Dificultad con las planchas', 'Mejoró técnica de sentadillas', 'Progresando bien en general', 7, 2); 