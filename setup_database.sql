-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS fitness_trainer3;
USE fitness_trainer3;

-- Tabla Cliente
CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    celular INT NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasenia VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    tipo_cliente VARCHAR(100) NOT NULL,
    status INT NOT NULL,
    imagen VARCHAR(255),
    fecha_pago DATE
);

-- Tabla Instructor
CREATE TABLE instructor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    contrasenia VARCHAR(255) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Discipline
CREATE TABLE discipline (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL
);

-- Tablas de asociación
CREATE TABLE discipline_cliente (
    discipline_id INT,
    cliente_id INT,
    PRIMARY KEY (discipline_id, cliente_id),
    FOREIGN KEY (discipline_id) REFERENCES discipline(id),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

CREATE TABLE cliente_instructor (
    cliente_id INT,
    instructor_id INT,
    PRIMARY KEY (cliente_id, instructor_id),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);

CREATE TABLE discipline_instructor (
    discipline_id INT,
    instructor_id INT,
    PRIMARY KEY (discipline_id, instructor_id),
    FOREIGN KEY (discipline_id) REFERENCES discipline(id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);

-- Tabla Product
CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    category INT,
    description TEXT,
    marca VARCHAR(100) NOT NULL,
    purchase_price DECIMAL(10,2),
    price DECIMAL(10,2),
    descuento DECIMAL(10,2),
    previous_price DECIMAL(10,2),
    date DATE,
    user_id INT,
    status INT NOT NULL DEFAULT 1,
    relevant INT NOT NULL DEFAULT 0,
    additional VARCHAR(200),
    outstanding INT NOT NULL DEFAULT 1,
    palabras_claves TEXT NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    profesor VARCHAR(100) NOT NULL,
    profesor_foto VARCHAR(100) NOT NULL
);

-- Tabla ProductImage
CREATE TABLE product_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_name TEXT NOT NULL,
    color_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Tabla Rutinas
CREATE TABLE rutinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    instructor_id INT NOT NULL,
    discipline_id INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    status INT NOT NULL DEFAULT 1,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(id),
    FOREIGN KEY (discipline_id) REFERENCES discipline(id)
);

-- Tabla EjerciciosRutina
CREATE TABLE ejercicios_rutina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rutina_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    series INT NOT NULL,
    repeticiones INT NOT NULL,
    descanso INT NOT NULL,
    dia_semana INT NOT NULL,
    orden INT NOT NULL,
    notas TEXT,
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id) ON DELETE CASCADE
);

-- Tabla Ejercicios
CREATE TABLE ejercicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    video_url VARCHAR(255),
    imagen_url VARCHAR(255),
    categoria VARCHAR(50),
    equipamiento VARCHAR(100),
    musculos_trabajados VARCHAR(200),
    nivel_dificultad VARCHAR(20)
);

-- Tabla Metas
CREATE TABLE metas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rutina_id INT NOT NULL,
    tipo_medida VARCHAR(50) NOT NULL,
    medida_inicial FLOAT NOT NULL,
    medida_objetivo FLOAT NOT NULL,
    unidad VARCHAR(20) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_logro DATETIME,
    logrado BOOLEAN DEFAULT FALSE,
    notas TEXT,
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id) ON DELETE CASCADE
);

-- Tabla HistorialMedidas
CREATE TABLE historial_medidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    peso FLOAT,
    altura FLOAT,
    imc FLOAT,
    fecha_medicion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha DATE NOT NULL,
    cintura FLOAT,
    cadera FLOAT,
    pecho FLOAT,
    brazos FLOAT,
    piernas FLOAT,
    grasa_corporal FLOAT,
    masa_muscular FLOAT,
    notas TEXT,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- Tabla Dietas
CREATE TABLE dietas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    calorias_diarias INT,
    proteinas FLOAT,
    carbohidratos FLOAT,
    grasas FLOAT,
    notas TEXT,
    cliente_id INT NOT NULL,
    instructor_id INT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);

-- Tabla Comidas
CREATE TABLE comidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    calorias INT,
    proteinas FLOAT,
    carbohidratos FLOAT,
    grasas FLOAT,
    tipo VARCHAR(50)
);

-- Tabla de asociación Comida-Dieta
CREATE TABLE comida_dieta (
    comida_id INT,
    dieta_id INT,
    PRIMARY KEY (comida_id, dieta_id),
    FOREIGN KEY (comida_id) REFERENCES comidas(id),
    FOREIGN KEY (dieta_id) REFERENCES dietas(id) ON DELETE CASCADE
);

-- Tabla ComidaDieta (detalles específicos de cada comida en una dieta)
CREATE TABLE comidas_dieta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dieta_id INT NOT NULL,
    tipo_comida VARCHAR(50) NOT NULL,
    hora TIME NOT NULL,
    descripcion TEXT NOT NULL,
    calorias INT,
    proteinas FLOAT,
    carbohidratos FLOAT,
    grasas FLOAT,
    lunes BOOLEAN DEFAULT TRUE,
    martes BOOLEAN DEFAULT TRUE,
    miercoles BOOLEAN DEFAULT TRUE,
    jueves BOOLEAN DEFAULT TRUE,
    viernes BOOLEAN DEFAULT TRUE,
    sabado BOOLEAN DEFAULT TRUE,
    domingo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (dieta_id) REFERENCES dietas(id) ON DELETE CASCADE
);

-- Tabla HistorialMedidasMetas
CREATE TABLE historial_medidas_metas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    meta_id INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    medida FLOAT NOT NULL,
    notas TEXT,
    FOREIGN KEY (meta_id) REFERENCES metas(id) ON DELETE CASCADE
);

-- Tabla de asociación entre ejercicios y rutinas
CREATE TABLE ejercicio_rutina (
    ejercicio_id INT,
    rutina_id INT,
    PRIMARY KEY (ejercicio_id, rutina_id),
    FOREIGN KEY (ejercicio_id) REFERENCES ejercicios(id),
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id)
);

-- Tabla de asociación entre instructores y productos
CREATE TABLE instructor_products (
    instructor_id INT,
    product_id INT,
    PRIMARY KEY (instructor_id, product_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(id),
    FOREIGN KEY (product_id) REFERENCES product(id)
);

-- Insertar datos de ejemplo
INSERT INTO cliente (nombres, apellidos, celular, email, contrasenia, direccion, tipo_cliente, status, imagen, fecha_pago)
VALUES 
('Juan', 'Perez', 987654321, 'juan.perez@example.com', 'password123', 'Av. Principal 123', 'Regular', 1, 'imagen1.jpg', '2025-03-31'),
('Maria', 'Lopez', 912345678, 'maria.lopez@example.com', 'password456', 'Av. Secundaria 456', 'VIP', 1, 'imagen2.jpg', '2025-03-25'),
('Carlos', 'Gomez', 923456789, 'carlos.gomez@example.com', 'password789', 'Av. Tercera 789', 'Regular', 0, 'imagen3.jpg', NULL);

INSERT INTO instructor (email, contrasenia, nombres, apellidos, telefono, activo, fecha_registro)
VALUES 
('instructor1@example.com', 'securepassword1', 'Ana', 'Martinez', '987654321', TRUE, CURRENT_TIMESTAMP),
('instructor2@example.com', 'securepassword2', 'Luis', 'Hernandez', '912345678', TRUE, CURRENT_TIMESTAMP),
('instructor3@example.com', 'securepassword3', 'Sofia', 'Ramirez', '923456789', FALSE, CURRENT_TIMESTAMP);

INSERT INTO discipline (nombre, descripcion)
VALUES 
('Yoga', 'Disciplina para mejorar la flexibilidad y reducir el estrés.'),
('CrossFit', 'Entrenamientos intensos para fortalecer músculos y resistencia.'),
('Pilates', 'Técnica para fortalecer el core y mejorar la postura.');

INSERT INTO discipline_cliente (discipline_id, cliente_id)
VALUES 
(1, 1),
(2, 2),
(3, 3);

INSERT INTO cliente_instructor (cliente_id, instructor_id)
VALUES 
(1, 1),
(2, 2),
(3, 3);

INSERT INTO discipline_instructor (discipline_id, instructor_id)
VALUES 
(1, 1),
(2, 2),
(3, 3);

INSERT INTO product (title, category, description, marca, purchase_price, price, descuento, previous_price, date, user_id, status, relevant, additional, outstanding, palabras_claves, fecha_inicio, fecha_fin, profesor, profesor_foto)
VALUES 
('Cuerda de Saltar', 1, 'Ideal para ejercicios aeróbicos.', 'FitnessPro', 10.00, 15.00, 5.00, NULL, '2025-03-15', 1, 1, 0, NULL, 1, 'ejercicio, cuerda, cardio', '2025-03-10', '2025-03-20', 'Ana Martinez', 'ana.jpg'),
('Colchoneta de Yoga', 2, 'Excelente para sesiones de yoga.', 'YogaCo', 20.00, 25.00, 5.00, 22.00, '2025-03-18', 2, 1, 1, 'Color azul', 1, 'yoga, colchoneta, comodidad', '2025-03-15', '2025-03-25', 'Luis Hernandez', 'luis.jpg'),
('Pesas Rusas', 3, 'Fortalece músculos con pesas de alta calidad.', 'MuscleMax', 30.00, 35.00, 5.00, NULL, '2025-03-20', 3, 1, 0, NULL, 1, 'pesas, fuerza, gimnasio', '2025-03-19', '2025-03-29', 'Sofia Ramirez', 'sofia.jpg');

INSERT INTO product_images (image_name, color_id, product_id)
VALUES 
('imagen_producto1.jpg', 1, 1),
('imagen_producto2.jpg', 2, 2),
('imagen_producto3.jpg', 3, 3);

INSERT INTO rutinas (cliente_id, instructor_id, discipline_id, titulo, descripcion, fecha_inicio, fecha_fin, nivel, status)
VALUES 
(1, 1, 1, 'Rutina de Cardio', 'Ejercicios para mejorar la resistencia cardiovascular.', '2025-04-01', '2025-05-01', 'Intermedio', 1),
(2, 2, 2, 'Entrenamiento de Fuerza', 'Rutina para fortalecer músculos principales.', '2025-04-05', '2025-05-05', 'Avanzado', 1),
(3, 3, 3, 'Pilates Básico', 'Ejercicios para mejorar la postura y flexibilidad.', '2025-04-10', '2025-05-10', 'Básico', 1);

INSERT INTO ejercicios_rutina (rutina_id, nombre, series, repeticiones, descanso, dia_semana, orden, notas)
VALUES 
(1, 'Saltos de cuerda', 3, 15, 60, 1, 1, 'Mantén una postura recta.'),
(2, 'Sentadillas', 4, 12, 90, 2, 1, 'No flexiones las rodillas más de 90 grados.'),
(3, 'Estiramientos de espalda', 5, 10, 30, 3, 1, 'Respira profundamente durante el ejercicio.');

INSERT INTO ejercicios (nombre, descripcion, video_url, imagen_url, categoria, equipamiento, musculos_trabajados, nivel_dificultad)
VALUES 
('Flexiones', 'Ejercicio para fortalecer el pecho y los brazos.', 'http://video.com/flexiones', 'http://imagen.com/flexiones.jpg', 'Calistenia', 'Sin equipamiento', 'Pecho, brazos', 'Intermedio'),
('Abdominales', 'Fortalece los músculos del abdomen.', 'http://video.com/abdominales', 'http://imagen.com/abdominales.jpg', 'Calistenia', 'Sin equipamiento', 'Abdomen', 'Básico'),
('Dominadas', 'Trabaja los músculos de la espalda.', 'http://video.com/dominadas', 'http://imagen.com/dominadas.jpg', 'Calistenia', 'Barra de dominadas', 'Espalda, brazos', 'Avanzado');

INSERT INTO metas (rutina_id, tipo_medida, medida_inicial, medida_objetivo, unidad, fecha_registro, fecha_logro, logrado, notas)
VALUES 
(1, 'Peso', 80.0, 75.0, 'kg', CURRENT_TIMESTAMP, NULL, FALSE, 'Objetivo de bajar de peso en 2 meses.'),
(2, 'Tiempo en carrera', 30.0, 25.0, 'minutos', CURRENT_TIMESTAMP, NULL, FALSE, 'Mejorar la resistencia al correr.'),
(3, 'Flexibilidad', 20.0, 30.0, 'cm', CURRENT_TIMESTAMP, NULL, FALSE, 'Incrementar la flexibilidad para yoga.');

INSERT INTO historial_medidas (cliente_id, peso, altura, imc, fecha_medicion, fecha, cintura, cadera, pecho, brazos, piernas, grasa_corporal, masa_muscular, notas)
VALUES 
(1, 80.0, 175.0, 26.1, CURRENT_TIMESTAMP, '2025-03-31', 90.0, 95.0, 100.0, 35.0, 60.0, 20.0, 40.0, 'Medición inicial.'),
(2, 70.0, 168.0, 24.8, CURRENT_TIMESTAMP, '2025-03-31', 85.0, 90.0, 95.0, 30.0, 55.0, 18.0, 35.0, 'Progreso moderado.'),
(3, 65.0, 160.0, 25.4, CURRENT_TIMESTAMP, '2025-03-31', 80.0, 85.0, 90.0, 28.0, 50.0, 22.0, 33.0, 'Buen progreso.');

INSERT INTO dietas (nombre, descripcion, fecha_inicio, fecha_fin, calorias_diarias, proteinas, carbohidratos, grasas, notas, cliente_id, instructor_id)
VALUES 
('Dieta Keto', 'Dieta baja en carbohidratos, alta en grasas.', '2025-04-01', '2025-04-15', 2000, 100.0, 50.0, 150.0, 'Foco en pérdida de peso.', 1, 1),
('Dieta Vegetariana', 'Alimentación basada en vegetales y proteína vegetal.', '2025-04-01', '2025-04-15', 1800, 80.0, 200.0, 50.0, 'Promueve bienestar general.', 2, 2),
('Dieta Deportiva', 'Alta en proteínas y carbohidratos para rendimiento.', '2025-04-01', '2025-04-15', 2500, 150.0, 300.0, 100.0, 'Ideal para atletas.', 3, 3);

INSERT INTO comidas (nombre, descripcion, calorias, proteinas, carbohidratos, grasas, tipo)
VALUES 
('Pollo a la plancha', 'Proteína magra cocida con hierbas.', 200, 40.0, 0.0, 5.0, 'Almuerzo'),
('Ensalada de quinoa', 'Vegetales frescos con quinoa.', 250, 8.0, 40.0, 10.0, 'Cena'),
('Batido de proteína', 'Bebida alta en proteínas con frutas.', 150, 30.0, 15.0, 2.0, 'Desayuno');

INSERT INTO comida_dieta (comida_id, dieta_id)
VALUES 
(1, 1),
(2, 2),
(3, 3);

INSERT INTO comidas_dieta (dieta_id, tipo_comida, hora, descripcion, calorias, proteinas, carbohidratos, grasas)
VALUES 
(1, 'Desayuno', '08:00:00', 'Tostadas integrales con aguacate.', 200, 6.0, 30.0, 8.0),
(2, 'Almuerzo', '13:00:00', 'Ensalada César con pollo.', 350, 25.0, 20.0, 15.0),
(3, 'Cena', '19:00:00', 'Sopa de verduras y pescado.', 250, 20.0, 15.0, 5.0);

INSERT INTO historial_medidas_metas (meta_id, fecha, medida, notas)
VALUES 
(1, '2025-03-15 10:00:00', 78.5, 'Progreso inicial hacia la meta de pérdida de peso.'),
(2, '2025-03-20 09:30:00', 28.0, 'Reducción del tiempo en carrera logrado con buen desempeño.'),
(3, '2025-03-25 11:00:00', 25.0, 'Incremento significativo en flexibilidad con ejercicios constantes.'); 