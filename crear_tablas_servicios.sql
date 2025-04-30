-- Script para crear las tablas del sistema de servicios fitness

-- Tabla de servicios
CREATE TABLE IF NOT EXISTS Servicio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion INT NOT NULL COMMENT 'duración en minutos',
    categoria VARCHAR(50) NOT NULL,
    modalidad VARCHAR(50) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    imagen VARCHAR(255),
    instructor_id INT NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES Usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla de horarios de servicios
CREATE TABLE IF NOT EXISTS Servicio_Horario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    servicio_id INT NOT NULL,
    dia_semana VARCHAR(20) NOT NULL COMMENT 'lunes, martes, etc.',
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    cupos_disponibles INT NOT NULL DEFAULT 1,
    estado VARCHAR(20) NOT NULL DEFAULT 'activo',
    FOREIGN KEY (servicio_id) REFERENCES Servicio(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabla de reservas de servicios
CREATE TABLE IF NOT EXISTS Servicio_Reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horario_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comentarios TEXT,
    FOREIGN KEY (horario_id) REFERENCES Servicio_Horario(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE
) ENGINE=InnoDB; 