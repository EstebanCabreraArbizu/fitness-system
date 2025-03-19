
    DROP DATABASE IF EXISTS personal_trainer_db2;
    CREATE DATABASE personal_trainer_db2;
    USE personal_trainer_db2;
    
    -- Crear tablas principales
    CREATE TABLE cliente (
        id INT PRIMARY KEY AUTO_INCREMENT,
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
    
    CREATE TABLE discipline (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT NOT NULL
    );
    
    CREATE TABLE instructor (
        id INT PRIMARY KEY AUTO_INCREMENT,
        email VARCHAR(120) NOT NULL UNIQUE,
        contrasenia VARCHAR(255) NOT NULL,
        nombres VARCHAR(100) NOT NULL,
        apellidos VARCHAR(100) NOT NULL,
        telefono VARCHAR(20),
        activo BOOLEAN DEFAULT TRUE,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Resto de las tablas...
    