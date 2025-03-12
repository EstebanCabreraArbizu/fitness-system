-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2025-03-12 13:57:13.231

-- tables
-- Table: Cliente
CREATE TABLE Cliente (
    id int  NOT NULL AUTO_INCREMENT,
    nombres varchar(100)  NOT NULL,
    celular int  NOT NULL,
    email varchar(150)  NOT NULL,
    direccion varchar(150)  NOT NULL,
    tipo_cliente varchar(100)  NOT NULL,
    status int  NOT NULL,
    apellidos varchar(100)  NOT NULL,
    imagen varchar(255)  NOT NULL,
    fecha_pago date  NULL,
    Discipline_id int  NOT NULL,
    CONSTRAINT Cliente_pk PRIMARY KEY (id)
);

-- Table: Cliente_Insturctor
CREATE TABLE Cliente_Insturctor (
    id int  NOT NULL AUTO_INCREMENT,
    Cliente_id int  NOT NULL,
    Instructor_id int  NOT NULL,
    CONSTRAINT Cliente_Insturctor_pk PRIMARY KEY (id)
);

-- Table: Discipline
CREATE TABLE Discipline (
    id int  NOT NULL AUTO_INCREMENT,
    nombre varchar(100)  NOT NULL,
    descripcion text  NOT NULL,
    CONSTRAINT Discipline_pk PRIMARY KEY (id)
);

-- Table: Instructor
CREATE TABLE Instructor (
    id int  NOT NULL AUTO_INCREMENT,
    nombres varchar(100)  NOT NULL,
    celular int  NOT NULL,
    email varchar(150)  NOT NULL,
    status int  NOT NULL,
    apellidos varchar(100)  NOT NULL,
    imagen varchar(255)  NOT NULL,
    Discipline_id int  NOT NULL,
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
-- Reference: Cliente_Discipline (table: Cliente)
ALTER TABLE Cliente ADD CONSTRAINT Cliente_Discipline FOREIGN KEY Cliente_Discipline (Discipline_id)
    REFERENCES Discipline (id);

-- Reference: Cliente_Insturctor_Cliente (table: Cliente_Insturctor)
ALTER TABLE Cliente_Insturctor ADD CONSTRAINT Cliente_Insturctor_Cliente FOREIGN KEY Cliente_Insturctor_Cliente (Cliente_id)
    REFERENCES Cliente (id);

-- Reference: Cliente_Insturctor_Instructor (table: Cliente_Insturctor)
ALTER TABLE Cliente_Insturctor ADD CONSTRAINT Cliente_Insturctor_Instructor FOREIGN KEY Cliente_Insturctor_Instructor (Instructor_id)
    REFERENCES Instructor (id);

-- Reference: Instructor_Discipline (table: Instructor)
ALTER TABLE Instructor ADD CONSTRAINT Instructor_Discipline FOREIGN KEY Instructor_Discipline (Discipline_id)
    REFERENCES Discipline (id);

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

