-- Alterar tabla cliente para agregar la relación con mediciones
ALTER TABLE cliente
ADD COLUMN IF NOT EXISTS imagen VARCHAR(255),
ADD COLUMN IF NOT EXISTS fecha_pago DATE;

-- Crear tabla mediciones
CREATE TABLE IF NOT EXISTS mediciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha DATETIME NOT NULL,
    peso FLOAT,
    altura FLOAT,
    imc FLOAT,
    cintura FLOAT,
    cadera FLOAT,
    pecho FLOAT,
    brazo FLOAT,
    muslo FLOAT,
    pantorrilla FLOAT,
    porcentaje_grasa FLOAT,
    masa_muscular FLOAT,
    masa_grasa FLOAT,
    notas TEXT,
    FOREIGN KEY (cliente_id) REFERENCES cliente(id) ON DELETE CASCADE
); 