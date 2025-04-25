-- Actualizar la tabla instructor
ALTER TABLE instructor
ADD COLUMN IF NOT EXISTS nombre VARCHAR(100) NOT NULL AFTER id,
ADD COLUMN IF NOT EXISTS apellidos VARCHAR(100) NOT NULL AFTER nombre,
ADD COLUMN IF NOT EXISTS email VARCHAR(120) NOT NULL AFTER apellidos,
ADD COLUMN IF NOT EXISTS password_hash VARCHAR(128) AFTER email,
ADD COLUMN IF NOT EXISTS telefono VARCHAR(20) AFTER password_hash,
ADD COLUMN IF NOT EXISTS especialidad VARCHAR(100) AFTER telefono,
ADD COLUMN IF NOT EXISTS experiencia INTEGER AFTER especialidad,
ADD COLUMN IF NOT EXISTS biografia TEXT AFTER experiencia,
ADD COLUMN IF NOT EXISTS foto_perfil VARCHAR(255) AFTER biografia,
ADD COLUMN IF NOT EXISTS redes_sociales JSON AFTER foto_perfil,
ADD COLUMN IF NOT EXISTS activo BOOLEAN DEFAULT TRUE AFTER redes_sociales,
ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER activo;

-- Agregar índices
CREATE INDEX IF NOT EXISTS idx_instructor_email ON instructor(email);
CREATE INDEX IF NOT EXISTS idx_instructor_activo ON instructor(activo);

-- Insertar un instructor de ejemplo si no existe
INSERT INTO instructor (nombre, apellidos, email, password_hash, telefono, especialidad, experiencia, biografia, activo)
SELECT 'Instructor', 'Ejemplo', 'instructor1@example.com', 
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/IiG', -- password: 'password123'
       '1234567890', 'Entrenamiento Personal', 5, 
       'Instructor certificado con experiencia en entrenamiento personal y grupal.',
       TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM instructor WHERE email = 'instructor1@example.com'
); 