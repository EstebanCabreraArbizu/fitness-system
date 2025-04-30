-- Tabla de seguimiento del progreso de estudiantes
CREATE TABLE IF NOT EXISTS Seguimiento_Progreso (
    id INT NOT NULL AUTO_INCREMENT,
    Usuario_id INT NOT NULL,
    fecha_seguimiento DATE NOT NULL,
    
    -- Relacionar con elementos existentes
    Rutina_id INT NULL,
    Meta_id INT NULL,
    Dieta_id INT NULL,
    
    -- Métricas de desempeño
    peso_actual FLOAT NULL,
    imc_actual FLOAT NULL,
    
    -- Progreso específico de rutina
    nivel_esfuerzo INT NULL COMMENT 'Escala 1-10',
    rendimiento INT NULL COMMENT 'Escala 1-10',
    ejercicios_completados INT NULL COMMENT 'Porcentaje completado',
    
    -- Progreso específico de dieta
    adherencia_dieta INT NULL COMMENT 'Porcentaje de cumplimiento',
    sensacion_hambre INT NULL COMMENT 'Escala 1-10',
    energia_diaria INT NULL COMMENT 'Escala 1-10',
    
    -- Progreso general
    dificultades TEXT NULL,
    logros TEXT NULL,
    observaciones TEXT NULL,
    
    -- Calificación general
    calificacion_instructor INT NULL COMMENT 'Escala 1-10',
    
    -- Usuario que registra (instructor)
    instructor_id INT NOT NULL,
    
    -- Constraints
    PRIMARY KEY (id),
    CONSTRAINT Seguimiento_Usuario FOREIGN KEY (Usuario_id) REFERENCES Usuario(id),
    CONSTRAINT Seguimiento_Rutina FOREIGN KEY (Rutina_id) REFERENCES Rutina(id),
    CONSTRAINT Seguimiento_Meta FOREIGN KEY (Meta_id) REFERENCES Meta(id),
    CONSTRAINT Seguimiento_Dieta FOREIGN KEY (Dieta_id) REFERENCES Dieta(id),
    CONSTRAINT Seguimiento_Instructor FOREIGN KEY (instructor_id) REFERENCES Usuario(id)
) ENGINE=InnoDB;

-- Tabla para imágenes de seguimiento (evidencia visual)
CREATE TABLE IF NOT EXISTS Seguimiento_Imagen (
    id INT NOT NULL AUTO_INCREMENT,
    Seguimiento_Progreso_id INT NOT NULL,
    nombre_imagen VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL COMMENT 'antes, durante, después',
    fecha_carga DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    CONSTRAINT Seguimiento_Imagen_Progreso FOREIGN KEY (Seguimiento_Progreso_id) 
        REFERENCES Seguimiento_Progreso(id) ON DELETE CASCADE
) ENGINE=InnoDB; 