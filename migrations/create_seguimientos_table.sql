-- Crear tabla de seguimientos
CREATE TABLE seguimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    meta_id INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor_actual FLOAT NOT NULL,
    notas TEXT,
    FOREIGN KEY (meta_id) REFERENCES metas(id) ON DELETE CASCADE,
    INDEX idx_meta_id (meta_id),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 