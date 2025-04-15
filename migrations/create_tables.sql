-- Actualizar tabla de metas si es necesario
ALTER TABLE metas
ADD COLUMN IF NOT EXISTS cliente_id INT NULL AFTER id,
ADD COLUMN IF NOT EXISTS nombre VARCHAR(100) NULL AFTER cliente_id,
ADD COLUMN IF NOT EXISTS valor_actual FLOAT NULL AFTER medida_inicial,
ADD FOREIGN KEY IF NOT EXISTS fk_cliente_id (cliente_id) REFERENCES cliente(id) ON DELETE CASCADE;

-- Crear tabla de seguimientos
CREATE TABLE IF NOT EXISTS seguimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    meta_id INT NOT NULL,
    medida_inicial FLOAT NOT NULL,
    medida_actual FLOAT NOT NULL,
    notas TEXT,
    FOREIGN KEY (meta_id) REFERENCES metas(id) ON DELETE CASCADE,
    INDEX idx_meta_id (meta_id),
    INDEX idx_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 