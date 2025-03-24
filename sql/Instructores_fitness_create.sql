-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2025-03-20 14:52:19.535

-- tables
-- Table: Cliente
CREATE TABLE Cliente (
    id int  NOT NULL AUTO_INCREMENT,
    nombres varchar(100)  NOT NULL,
    celular varchar(15)  NOT NULL,
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

-- Table: Comida
CREATE TABLE Comida (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    descripcion varchar(300)  NULL,
    CONSTRAINT Comida_pk PRIMARY KEY (id)
);

-- Table: Dia_comida
CREATE TABLE Dia_comida (
    id int  NOT NULL AUTO_INCREMENT,
    Dia_semanal_id int  NOT NULL,
    Comida_id int  NOT NULL,
    CONSTRAINT Dia_comida_pk PRIMARY KEY (id)
);

-- Table: Dia_semanal
CREATE TABLE Dia_semanal (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    Dieta_id int  NOT NULL,
    CONSTRAINT Dia_semanal_pk PRIMARY KEY (id)
);

-- Table: Dieta
CREATE TABLE Dieta (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    descripcion varchar(300)  NOT NULL,
	meta_calorias int NOT NULL,
    fecha_inicio date  NOT NULL,
    fecha_fin date  NOT NULL,
    Cliente_id int  NOT NULL,
    Instructor_id int  NOT NULL,
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
    celular varchar(15)  NOT NULL,
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

-- Reference: Dia_comida_Comida (table: Dia_comida)
ALTER TABLE Dia_comida ADD CONSTRAINT Dia_comida_Comida FOREIGN KEY Dia_comida_Comida (Comida_id)
    REFERENCES Comida (id);

-- Reference: Dia_comida_Dia_semanal (table: Dia_comida)
ALTER TABLE Dia_comida ADD CONSTRAINT Dia_comida_Dia_semanal FOREIGN KEY Dia_comida_Dia_semanal (Dia_semanal_id)
    REFERENCES Dia_semanal (id);

-- Reference: Dia_semanal_Dieta (table: Dia_semanal)
ALTER TABLE Dia_semanal ADD CONSTRAINT Dia_semanal_Dieta FOREIGN KEY Dia_semanal_Dieta (Dieta_id)
    REFERENCES Dieta (id);

-- Reference: Dieta_Cliente (table: Dieta)
ALTER TABLE Dieta ADD CONSTRAINT Dieta_Cliente FOREIGN KEY Dieta_Cliente (Cliente_id)
    REFERENCES Cliente (id);

-- Reference: Dieta_Instructor (table: Dieta)
ALTER TABLE Dieta ADD CONSTRAINT Dieta_Instructor FOREIGN KEY Dieta_Instructor (Instructor_id)
    REFERENCES Instructor (id);

-- Reference: Dieta_images_Dieta (table: Dieta_images)
ALTER TABLE Dieta_images ADD CONSTRAINT Dieta_images_Dieta FOREIGN KEY Dieta_images_Dieta (Dieta_id)
    REFERENCES Dieta (id);

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

-- End of file.

