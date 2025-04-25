-- Insertar un instructor de ejemplo si no existe
INSERT INTO instructor (email, contrasenia, nombres, apellidos, telefono, activo)
SELECT 'instructor1@example.com', 
       '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/IiG', -- password: 'password123'
       'Instructor', 'Ejemplo', '1234567890', TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM instructor WHERE email = 'instructor1@example.com'
); 