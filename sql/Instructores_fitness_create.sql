-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2025-04-29 13:40:37.807

-- tables
-- Table: Cliente_Instructor
CREATE TABLE Cliente_Instructor (
    id int  NOT NULL AUTO_INCREMENT,
    Usuario_id int  NOT NULL,
    Usuario_2_id int  NOT NULL,
    CONSTRAINT Cliente_Instructor_pk PRIMARY KEY (id)
);

-- Table: Cliente_datos
CREATE TABLE Cliente_datos (
    id int  NOT NULL AUTO_INCREMENT,
    nivel_actividad varchar(50)  NOT NULL,
    direccion varchar(200)  NOT NULL,
    tipo_cliente varchar(50)  NOT NULL,
    Usuario_id int  NOT NULL,
    CONSTRAINT Cliente_datos_pk PRIMARY KEY (id)
);

-- Table: Comida
CREATE TABLE Comida (
    id int  NOT NULL AUTO_INCREMENT,
    tipo_comida varchar(100)  NOT NULL,
    dia_dieta varchar(100)  NOT NULL,
    hora varchar(100)  NOT NULL,
    nombre varchar(100)  NOT NULL,
    descripcion text  NULL,
    calorias int  NOT NULL,
    proteinas float  NOT NULL,
    carbohidratos float  NOT NULL,
    grasas float  NOT NULL,
    recomendacion varchar(100)  NOT NULL,
    image_name varchar(100)  NOT NULL,
    status int  NOT NULL,
    Dieta_id int  NOT NULL,
    CONSTRAINT Comida_pk PRIMARY KEY (id)
);

-- Table: Dieta
CREATE TABLE Dieta (
    id int  NOT NULL AUTO_INCREMENT,
    tipo_dieta varchar(100)  NOT NULL,
    nombre varchar(100)  NOT NULL,
    descripcion varchar(300)  NOT NULL,
    fecha_inicio date  NOT NULL,
    fecha_fin date  NOT NULL,
    duracion_dieta varchar(100)  NOT NULL,
    fecha_registro datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    edad varchar(100)  NOT NULL,
    alergias varchar(100)  NOT NULL,
    enfermedad_cronica varchar(100)  NOT NULL,
    alergia_medicamento varchar(100)  NOT NULL,
    dias_semana varchar(100)  NOT NULL,
    meta_calorias int(100)  NOT NULL,
    status int  NOT NULL,
    Discipline_id int  NOT NULL,
    Usuario_id int  NOT NULL,
    CONSTRAINT Dieta_pk PRIMARY KEY (id)
);

-- Table: Dieta_images
CREATE TABLE Dieta_images (
    id int  NOT NULL AUTO_INCREMENT,
    image_name text  NOT NULL,
    Dieta_id int  NOT NULL,
    CONSTRAINT Dieta_images_pk PRIMARY KEY (id)
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
    Usuario_id int  NOT NULL,
    CONSTRAINT Discipline_Cliente_pk PRIMARY KEY (id)
);

-- Table: Discipline_Instructor
CREATE TABLE Discipline_Instructor (
    id int  NOT NULL AUTO_INCREMENT,
    Discipline_id int  NOT NULL,
    Usuario_id int  NOT NULL,
    CONSTRAINT Discipline_Instructor_pk PRIMARY KEY (id)
);

-- Table: Ejercicio
CREATE TABLE Ejercicio (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    descripcion text  NOT NULL,
    series int  NOT NULL,
    repeticiones int  NOT NULL,
    tiempo_descanso int  NOT NULL,
    CONSTRAINT Ejercicio_pk PRIMARY KEY (id)
);

-- Table: Ejercicio_Rutina
CREATE TABLE Ejercicio_Rutina (
    id int  NOT NULL AUTO_INCREMENT,
    orden int  NOT NULL,
    Ejercicio_id int  NOT NULL,
    Rutina_id int  NOT NULL,
    CONSTRAINT Ejercicio_Rutina_pk PRIMARY KEY (id)
);

-- Table: Historial_Medidas
CREATE TABLE Historial_Medidas (
    id int  NOT NULL AUTO_INCREMENT,
    peso float  NOT NULL,
    altura float  NOT NULL,
    imc float  NOT NULL,
    fecha_medicion datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Usuario_id int  NOT NULL,
    CONSTRAINT Historial_Medidas_pk PRIMARY KEY (id)
);

-- Table: Instructor_Products
CREATE TABLE Instructor_Products (
    id int  NOT NULL AUTO_INCREMENT,
    Product_id int  NOT NULL,
    Usuario_id int  NOT NULL,
    CONSTRAINT Instructor_Products_pk PRIMARY KEY (id)
);

-- Table: Instructor_datos
CREATE TABLE Instructor_datos (
    id int  NOT NULL AUTO_INCREMENT,
    certificaciones text  NOT NULL,
    estudios text  NOT NULL,
    anios_experiencia int  NOT NULL,
    especialidad varchar(100)  NOT NULL,
    Usuario_id int  NOT NULL,
    CONSTRAINT Instructor_datos_pk PRIMARY KEY (id)
);

-- Table: Meta
CREATE TABLE Meta (
    id int  NOT NULL AUTO_INCREMENT,
    descripcion text  NOT NULL,
    fecha_inicio date  NOT NULL,
    fecha_fin date  NOT NULL,
    estado varchar(50)  NOT NULL,
    Usuario_id int  NOT NULL,
    CONSTRAINT Meta_pk PRIMARY KEY (id)
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

-- Table: Rutina
CREATE TABLE Rutina (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    descripcion text  NOT NULL,
    fecha_creacion datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Usuario_id int  NOT NULL,
    CONSTRAINT Rutina_pk PRIMARY KEY (id)
);

-- Table: Tipo_usuario
CREATE TABLE Tipo_usuario (
    id int  NOT NULL AUTO_INCREMENT,
    nombre int  NOT NULL,
    descripcion int  NOT NULL,
    CONSTRAINT Tipo_usuario_pk PRIMARY KEY (id)
);

-- Table: Usuario
CREATE TABLE Usuario (
    id int  NOT NULL AUTO_INCREMENT,
    nombres varchar(100)  NOT NULL,
    apellidos varchar(100)  NOT NULL,
    celular varchar(15)  NOT NULL,
    email varchar(150)  NOT NULL,
    contrasenia varchar(100)  NOT NULL,
    status int  NOT NULL,
    imagen varchar(255)  NOT NULL,
    fecha_registro datetime  NOT NULL,
    Tipo_usuario_id int  NOT NULL,
    CONSTRAINT Usuario_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: Cliente_Instructor_Usuario (table: Cliente_Instructor)
ALTER TABLE Cliente_Instructor ADD CONSTRAINT Cliente_Instructor_Usuario FOREIGN KEY Cliente_Instructor_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Cliente_Instructor_Usuario_2 (table: Cliente_Instructor)
ALTER TABLE Cliente_Instructor ADD CONSTRAINT Cliente_Instructor_Usuario_2 FOREIGN KEY Cliente_Instructor_Usuario_2 (Usuario_2_id)
    REFERENCES Usuario (id);

-- Reference: Cliente_datos_Usuario (table: Cliente_datos)
ALTER TABLE Cliente_datos ADD CONSTRAINT Cliente_datos_Usuario FOREIGN KEY Cliente_datos_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Comida_Dieta (table: Comida)
ALTER TABLE Comida ADD CONSTRAINT Comida_Dieta FOREIGN KEY Comida_Dieta (Dieta_id)
    REFERENCES Dieta (id);

-- Reference: Dieta_Discipline (table: Dieta)
ALTER TABLE Dieta ADD CONSTRAINT Dieta_Discipline FOREIGN KEY Dieta_Discipline (Discipline_id)
    REFERENCES Discipline (id);

-- Reference: Dieta_Usuario (table: Dieta)
ALTER TABLE Dieta ADD CONSTRAINT Dieta_Usuario FOREIGN KEY Dieta_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Dieta_images_Dieta (table: Dieta_images)
ALTER TABLE Dieta_images ADD CONSTRAINT Dieta_images_Dieta FOREIGN KEY Dieta_images_Dieta (Dieta_id)
    REFERENCES Dieta (id);

-- Reference: Discipline_Cliente_Discipline (table: Discipline_Cliente)
ALTER TABLE Discipline_Cliente ADD CONSTRAINT Discipline_Cliente_Discipline FOREIGN KEY Discipline_Cliente_Discipline (Discipline_id)
    REFERENCES Discipline (id);

-- Reference: Discipline_Cliente_Usuario (table: Discipline_Cliente)
ALTER TABLE Discipline_Cliente ADD CONSTRAINT Discipline_Cliente_Usuario FOREIGN KEY Discipline_Cliente_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Discipline_Instructor_Discipline (table: Discipline_Instructor)
ALTER TABLE Discipline_Instructor ADD CONSTRAINT Discipline_Instructor_Discipline FOREIGN KEY Discipline_Instructor_Discipline (Discipline_id)
    REFERENCES Discipline (id);

-- Reference: Discipline_Instructor_Usuario (table: Discipline_Instructor)
ALTER TABLE Discipline_Instructor ADD CONSTRAINT Discipline_Instructor_Usuario FOREIGN KEY Discipline_Instructor_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Ejercicio_Rutina_Ejercicio (table: Ejercicio_Rutina)
ALTER TABLE Ejercicio_Rutina ADD CONSTRAINT Ejercicio_Rutina_Ejercicio FOREIGN KEY Ejercicio_Rutina_Ejercicio (Ejercicio_id)
    REFERENCES Ejercicio (id);

-- Reference: Ejercicio_Rutina_Rutina (table: Ejercicio_Rutina)
ALTER TABLE Ejercicio_Rutina ADD CONSTRAINT Ejercicio_Rutina_Rutina FOREIGN KEY Ejercicio_Rutina_Rutina (Rutina_id)
    REFERENCES Rutina (id);

-- Reference: Historial_Medidas_Usuario (table: Historial_Medidas)
ALTER TABLE Historial_Medidas ADD CONSTRAINT Historial_Medidas_Usuario FOREIGN KEY Historial_Medidas_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Instructor_Products_Products (table: Instructor_Products)
ALTER TABLE Instructor_Products ADD CONSTRAINT Instructor_Products_Products FOREIGN KEY Instructor_Products_Products (Product_id)
    REFERENCES Product (id);

-- Reference: Instructor_Products_Usuario (table: Instructor_Products)
ALTER TABLE Instructor_Products ADD CONSTRAINT Instructor_Products_Usuario FOREIGN KEY Instructor_Products_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Instructor_datos_Usuario (table: Instructor_datos)
ALTER TABLE Instructor_datos ADD CONSTRAINT Instructor_datos_Usuario FOREIGN KEY Instructor_datos_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Meta_Usuario (table: Meta)
ALTER TABLE Meta ADD CONSTRAINT Meta_Usuario FOREIGN KEY Meta_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Product_images_Products (table: Product_images)
ALTER TABLE Product_images ADD CONSTRAINT Product_images_Products FOREIGN KEY Product_images_Products (Product_id)
    REFERENCES Product (id);

-- Reference: Rutina_Usuario (table: Rutina)
ALTER TABLE Rutina ADD CONSTRAINT Rutina_Usuario FOREIGN KEY Rutina_Usuario (Usuario_id)
    REFERENCES Usuario (id);

-- Reference: Usuario_Tipo_usuario (table: Usuario)
ALTER TABLE Usuario ADD CONSTRAINT Usuario_Tipo_usuario FOREIGN KEY Usuario_Tipo_usuario (Tipo_usuario_id)
    REFERENCES Tipo_usuario (id);

-- End of file.

