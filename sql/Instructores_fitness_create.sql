-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2025-03-12 16:19:42.285

-- tables
-- Table: Cliente
CREATE TABLE Cliente (
    id int  NOT NULL AUTO_INCREMENT,
    nombres varchar(100)  NOT NULL,
    celular int  NOT NULL,
    email varchar(150)  NOT NULL,
    contrasenia varchar(100)  NOT NULL,
    direccion varchar(150)  NOT NULL,
    tipo_cliente varchar(100)  NOT NULL,
    status int  NOT NULL,
    apellidos varchar(100)  NOT NULL,
    imagen varchar(255)  NOT NULL,
    fecha_pago date  NULL,
    CONSTRAINT Cliente_pk PRIMARY KEY (id)
);

-- Table: Cliente_Instructor
CREATE TABLE Cliente_Instructor (
    id int  NOT NULL AUTO_INCREMENT,
    Cliente_id int  NOT NULL,
    Instructor_id int  NOT NULL,
    CONSTRAINT Cliente_Instructor_pk PRIMARY KEY (id)
);

-- Table: Discipline
CREATE TABLE Discipline (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    descripcion text  NOT NULL,
    CONSTRAINT Discipline_pk PRIMARY KEY (id)
);

-- Table: Discipline_Cliente
CREATE TABLE Discipline_Cliente (
    id int  NOT NULL AUTO_INCREMENT,
    Discipline_id int  NOT NULL,
    Cliente_id int  NOT NULL,
    CONSTRAINT Discipline_Cliente_pk PRIMARY KEY (id)
);

-- Table: Discipline_Instructor
CREATE TABLE Discipline_Instructor (
    id int  NOT NULL AUTO_INCREMENT,
    Discipline_id int  NOT NULL,
    Instructor_id int  NOT NULL,
    CONSTRAINT Discipline_Instructor_pk PRIMARY KEY (id)
);

-- Table: Instructor
CREATE TABLE Instructor (
    id int  NOT NULL AUTO_INCREMENT,
    nombres varchar(100)  NOT NULL,
    celular int  NOT NULL,
    email varchar(150)  NOT NULL,
    contrasenia varchar(100)  NOT NULL,
    status int  NOT NULL,
    apellidos varchar(100)  NOT NULL,
    imagen varchar(255)  NOT NULL,
    CONSTRAINT Instructor_pk PRIMARY KEY (id)
);

-- Table: Instructor_Products
CREATE TABLE Instructor_Products (
    id int  NOT NULL AUTO_INCREMENT,
    Instructor_id int  NOT NULL,
    Product_id int  NOT NULL,
    CONSTRAINT Instructor_Products_pk PRIMARY KEY (id)
);

-- Table: Product
CREATE TABLE Product (
    id int  NOT NULL AUTO_INCREMENT,
    title varchar(255)  NULL,
    category int  NULL,
    description text  NULL,
    marca varchar(100)  NOT NULL,
    purchase_price double(10,2)  NULL,
    price double(10,2)  NULL,
    descuento double(10,2)  NULL,
    previous_price double(10,2)  NULL,
    date date  NULL,
    user_id int  NULL,
    status int  NOT NULL DEFAULT 1,
    relevant int  NOT NULL DEFAULT 0,
    additional varchar(200)  NULL,
    outstanding int  NOT NULL DEFAULT 1,
    palabras_claves text  NOT NULL,
    fecha_inicio date  NULL,
    fecha_fin date  NULL,
    profesor varchar(100)  NOT NULL,
    profesor_foto varchar(100)  NOT NULL,
    CONSTRAINT Product_pk PRIMARY KEY (id)
);

-- Table: Product_images
CREATE TABLE Product_images (
    id int  NOT NULL AUTO_INCREMENT,
    image_name text  NOT NULL,
    color_id int  NOT NULL,
    Product_id int  NOT NULL,
    CONSTRAINT Product_images_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: Cliente_Insturctor_Cliente (table: Cliente_Instructor)
ALTER TABLE Cliente_Instructor ADD CONSTRAINT Cliente_Insturctor_Cliente FOREIGN KEY Cliente_Insturctor_Cliente (Cliente_id)
    REFERENCES Cliente (id);

-- Reference: Cliente_Insturctor_Instructor (table: Cliente_Instructor)
ALTER TABLE Cliente_Instructor ADD CONSTRAINT Cliente_Insturctor_Instructor FOREIGN KEY Cliente_Insturctor_Instructor (Instructor_id)
    REFERENCES Instructor (id);

-- Reference: Discipline_Cliente_Cliente (table: Discipline_Cliente)
ALTER TABLE Discipline_Cliente ADD CONSTRAINT Discipline_Cliente_Cliente FOREIGN KEY Discipline_Cliente_Cliente (Cliente_id)
    REFERENCES Cliente (id);

-- Reference: Discipline_Cliente_Discipline (table: Discipline_Cliente)
ALTER TABLE Discipline_Cliente ADD CONSTRAINT Discipline_Cliente_Discipline FOREIGN KEY Discipline_Cliente_Discipline (Discipline_id)
    REFERENCES Discipline (id);

-- Reference: Discipline_Instructor_Discipline (table: Discipline_Instructor)
ALTER TABLE Discipline_Instructor ADD CONSTRAINT Discipline_Instructor_Discipline FOREIGN KEY Discipline_Instructor_Discipline (Discipline_id)
    REFERENCES Discipline (id);

-- Reference: Discipline_Instructor_Instructor (table: Discipline_Instructor)
ALTER TABLE Discipline_Instructor ADD CONSTRAINT Discipline_Instructor_Instructor FOREIGN KEY Discipline_Instructor_Instructor (Instructor_id)
    REFERENCES Instructor (id);

-- Reference: Instructor_Products_Instructor (table: Instructor_Products)
ALTER TABLE Instructor_Products ADD CONSTRAINT Instructor_Products_Instructor FOREIGN KEY Instructor_Products_Instructor (Instructor_id)
    REFERENCES Instructor (id);

-- Reference: Instructor_Products_Products (table: Instructor_Products)
ALTER TABLE Instructor_Products ADD CONSTRAINT Instructor_Products_Products FOREIGN KEY Instructor_Products_Products (Product_id)
    REFERENCES Product (id);

-- Reference: Product_images_Products (table: Product_images)
ALTER TABLE Product_images ADD CONSTRAINT Product_images_Products FOREIGN KEY Product_images_Products (Product_id)
    REFERENCES Product (id);

-- Insertar disciplinas básicas
INSERT INTO Discipline (nombre, descripcion) VALUES 
('Yoga', 'Práctica que conecta el cuerpo, la respiración y la mente.'),
('Pilates', 'Sistema de entrenamiento físico y mental centrado en la postura y el control.'),
('Crossfit', 'Programa de acondicionamiento físico basado en ejercicios funcionales.'),
('Spinning', 'Entrenamiento de ciclismo indoor con música de alta energía.'),
('Zumba', 'Programa de fitness que combina música latina con baile y ejercicio.');

-- Insertar instructores de ejemplo
INSERT INTO Instructor (nombres, celular, email, contrasenia, status, apellidos, imagen) VALUES
('Juan', '5551234567', 'juan@fittrainer.com', 'password123', 1, 'González', 'instructor1.jpg'),
('María', '5557654321', 'maria@fittrainer.com', 'password123', 1, 'Rodríguez', 'instructor2.jpg'),
('Carlos', '5559876543', 'carlos@fittrainer.com', 'password123', 1, 'Sánchez', 'instructor3.jpg');

-- Asociar instructores con disciplinas
INSERT INTO Discipline_Instructor (Discipline_id, Instructor_id) VALUES
(1, 1), -- Juan - Yoga
(2, 2), -- María - Pilates
(3, 3); -- Carlos - Crossfit

-- End of file.