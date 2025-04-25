-- Tabla de servicios
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio FLOAT NOT NULL,
    duracion INTEGER NOT NULL,  -- duración en minutos
    capacidad_maxima INTEGER NOT NULL,
    instructor_id INTEGER NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);

-- Tabla de horarios de servicios
CREATE TABLE IF NOT EXISTS horarios_servicio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    servicio_id INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,  -- 0=Lunes, 6=Domingo
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    cupo_maximo INTEGER DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (servicio_id) REFERENCES servicios(id) ON DELETE CASCADE
);

-- Tabla de certificaciones de instructores
CREATE TABLE IF NOT EXISTS certificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_id INTEGER NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    institucion VARCHAR(200) NOT NULL,
    fecha_obtencion DATE,
    descripcion TEXT,
    imagen VARCHAR(255),  -- ruta a la imagen del certificado
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);

-- Tabla de testimonios
CREATE TABLE IF NOT EXISTS testimonios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    contenido TEXT NOT NULL,
    calificacion INTEGER,  -- 1-5 estrellas
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    imagen_antes VARCHAR(255),  -- ruta a la imagen "antes"
    imagen_despues VARCHAR(255),  -- ruta a la imagen "después"
    FOREIGN KEY (instructor_id) REFERENCES instructor(id),
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- Tabla de reservas para los horarios
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    horario_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente',  -- pendiente, confirmada, cancelada, completada
    notas TEXT,
    FOREIGN KEY (horario_id) REFERENCES horarios_servicio(id) ON DELETE CASCADE,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_servicios_instructor ON servicios(instructor_id);
CREATE INDEX idx_horarios_servicio ON horarios_servicio(servicio_id);
CREATE INDEX idx_certificaciones_instructor ON certificaciones(instructor_id);
CREATE INDEX idx_testimonios_instructor ON testimonios(instructor_id);
CREATE INDEX idx_testimonios_cliente ON testimonios(cliente_id);
CREATE INDEX idx_reservas_horario ON reservas(horario_id);
CREATE INDEX idx_reservas_cliente ON reservas(cliente_id);

-- Trigger para actualizar fecha_actualizacion en servicios
CREATE TRIGGER IF NOT EXISTS update_servicios_fecha_actualizacion 
AFTER UPDATE ON servicios
BEGIN
    UPDATE servicios 
    SET fecha_actualizacion = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END; 