-- Inserciones complementarias de dietas y nutrición

-- Inserción de dietas para los alumnos
INSERT INTO Dieta (tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, duracion_dieta, fecha_registro,
            edad, alergias, enfermedad_cronica, alergia_medicamento, dias_semana, meta_calorias, status, Discipline_id, Usuario_id, Usuario_2_id) VALUES
('Déficit calórico', 'Plan pérdida de peso', 'Dieta balanceada con déficit calórico para reducción de peso', 
 DATE_SUB(CURRENT_DATE(), INTERVAL 15 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 45 DAY), '2 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 16 DAY),
 '30-35', 'Ninguna', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 1800, 1, 2, 10, 15),

('Mantenimiento', 'Plan ganancia muscular', 'Dieta con alto aporte proteico para desarrollo muscular', 
 DATE_SUB(CURRENT_DATE(), INTERVAL 10 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 80 DAY), '3 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 11 DAY),
 '25-30', 'Lácteos', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 2500, 1, 1, 11, 15),

('Alta en carbohidratos', 'Plan rendimiento deportivo', 'Dieta enfocada en optimizar el rendimiento cardiovascular', 
 DATE_SUB(CURRENT_DATE(), INTERVAL 20 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 40 DAY), '2 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 21 DAY),
 '30-35', 'Ninguna', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 2800, 1, 3, 12, 15),

('Baja en grasas', 'Plan definición muscular', 'Dieta para reducir grasa corporal y mejorar definición', 
 DATE_SUB(CURRENT_DATE(), INTERVAL 5 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 55 DAY), '2 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 6 DAY),
 '25-30', 'Frutos secos', 'Ninguna', 'Ninguna', 'Lunes-Domingo', 1600, 1, 4, 13, 15),

('Alta en proteínas', 'Plan resistencia', 'Dieta para mejorar resistencia física y rendimiento en carrera', 
 DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY), DATE_ADD(CURRENT_DATE(), INTERVAL 60 DAY), '3 meses', DATE_SUB(CURRENT_DATE(), INTERVAL 31 DAY),
 '35-40', 'Ninguna', 'Ninguna', 'Penicilina', 'Lunes-Domingo', 2200, 1, 2, 14, 15);

-- Inserción de comidas para las dietas (ejemplos para cada cliente)
-- Comidas para Carlos (ID 10)
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, 
                    recomendacion, image_name, status, Dieta_id) VALUES
('Desayuno', 'Lunes', '07:30', 'Tostadas integrales con huevo', 'Dos rebanadas de pan integral con dos huevos revueltos', 
 350, 20, 35, 12, 'Consumir dentro de la primera hora tras despertar', 'desayuno1.jpg', 1, 1),
('Almuerzo', 'Lunes', '13:00', 'Ensalada de pollo', 'Pechuga de pollo a la plancha con ensalada mixta', 
 450, 40, 15, 18, 'Masticar despacio y beber agua entre bocados', 'almuerzo1.jpg', 1, 1),
('Cena', 'Lunes', '20:00', 'Pescado al vapor con verduras', 'Filete de pescado blanco con verduras al vapor', 
 320, 25, 10, 15, 'Cenar al menos 2 horas antes de dormir', 'cena1.jpg', 1, 1);

-- Comidas para Ana (ID 11)
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, 
                    recomendacion, image_name, status, Dieta_id) VALUES
('Desayuno', 'Lunes', '08:00', 'Batido proteico con avena', 'Batido con proteína vegetal, avena y plátano', 
 420, 30, 45, 10, 'Ideal antes del entrenamiento', 'batido1.jpg', 1, 2),
('Almuerzo', 'Lunes', '14:00', 'Bowl de proteínas', 'Arroz integral, lentejas, pollo a la plancha y aguacate', 
 650, 45, 60, 25, 'Consumir dentro de la hora posterior al entrenamiento', 'bowl1.jpg', 1, 2),
('Cena', 'Lunes', '21:00', 'Tortilla de claras con vegetales', 'Tortilla de claras de huevo con espinacas y champiñones', 
 280, 35, 5, 12, 'Incluir proteína de absorción lenta para la noche', 'tortilla1.jpg', 1, 2);

-- Comidas para Miguel (ID 12)
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, 
                    recomendacion, image_name, status, Dieta_id) VALUES
('Desayuno', 'Lunes', '07:00', 'Porridge de avena con frutas', 'Avena cocida con leche, plátano y frutos rojos', 
 380, 15, 60, 8, 'Consumir 90 minutos antes del entrenamiento', 'porridge1.jpg', 1, 3),
('Almuerzo', 'Lunes', '13:30', 'Pasta integral con pollo', 'Pasta integral con pechuga de pollo y salsa de tomate natural', 
 580, 35, 70, 12, 'Importante para reponer glucógeno', 'pasta1.jpg', 1, 3),
('Merienda', 'Lunes', '17:00', 'Batido de recuperación', 'Batido con proteína, plátano y avena', 
 350, 25, 40, 5, 'Consumir justo después del entrenamiento', 'batido2.jpg', 1, 3),
('Cena', 'Lunes', '20:30', 'Salmón con arroz y verduras', 'Filete de salmón al horno con arroz integral y verduras salteadas', 
 450, 30, 40, 18, 'Incluir ácidos grasos omega-3 para recuperación', 'salmon1.jpg', 1, 3);

-- Comidas para Laura (ID 13)
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, 
                    recomendacion, image_name, status, Dieta_id) VALUES
('Desayuno', 'Lunes', '08:30', 'Yogur griego con frutas', 'Yogur griego natural con frutas del bosque y semillas de chía', 
 250, 20, 25, 8, 'Usar yogur sin azúcares añadidos', 'yogur1.jpg', 1, 4),
('Media mañana', 'Lunes', '11:00', 'Manzana con proteína', 'Una manzana con una porción de proteína en polvo', 
 150, 15, 20, 1, 'Ideal para mantener niveles de energía', 'manzana1.jpg', 1, 4),
('Almuerzo', 'Lunes', '14:00', 'Pavo a la plancha con quinoa', 'Filete de pavo a la plancha con quinoa y verduras asadas', 
 380, 35, 30, 10, 'Cocinar con mínimo aceite', 'pavo1.jpg', 1, 4),
('Cena', 'Lunes', '20:00', 'Ensalada proteica', 'Ensalada verde con atún, huevo duro y aceite de oliva', 
 320, 30, 5, 18, 'Limitar carbohidratos por la noche', 'ensalada1.jpg', 1, 4);

-- Comidas para Javier (ID 14)
INSERT INTO Comida (tipo_comida, dia_dieta, hora, nombre, descripcion, calorias, proteinas, carbohidratos, grasas, 
                    recomendacion, image_name, status, Dieta_id) VALUES
('Desayuno', 'Lunes', '06:30', 'Batido energético', 'Batido con plátano, avena, proteína y café', 
 350, 25, 45, 6, 'Consumir 45 minutos antes de entrenar', 'batido3.jpg', 1, 5),
('Media mañana', 'Lunes', '10:00', 'Sándwich integral', 'Sándwich de pan integral con pavo y queso bajo en grasa', 
 320, 20, 30, 12, 'Para mantener energía en entrenamientos largos', 'sandwich1.jpg', 1, 5),
('Almuerzo', 'Lunes', '13:30', 'Bowl de carbohidratos', 'Arroz, pollo, aguacate y vegetales', 
 580, 35, 60, 20, 'Importante para la recuperación muscular', 'bowl2.jpg', 1, 5),
('Merienda', 'Lunes', '17:00', 'Smoothie proteico', 'Batido con frutas, proteína y leche de almendras', 
 280, 20, 35, 5, 'Para recuperación post-entrenamiento', 'smoothie1.jpg', 1, 5),
('Cena', 'Lunes', '20:00', 'Tortilla de patatas ligera', 'Tortilla con más claras que yemas y patatas al horno', 
 350, 25, 30, 15, 'Preparar con mínimo aceite', 'tortilla2.jpg', 1, 5);

-- Imágenes para las dietas
INSERT INTO Dieta_images (image_name, Dieta_id) VALUES
('dieta_carlos1.jpg', 1),
('dieta_carlos2.jpg', 1),
('dieta_ana1.jpg', 2),
('dieta_ana2.jpg', 2),
('dieta_miguel1.jpg', 3),
('dieta_miguel2.jpg', 3),
('dieta_laura1.jpg', 4),
('dieta_laura2.jpg', 4),
('dieta_javier1.jpg', 5),
('dieta_javier2.jpg', 5); 