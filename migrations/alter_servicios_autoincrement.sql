-- Primero eliminamos todas las restricciones de clave foránea
ALTER TABLE horarios_servicio DROP FOREIGN KEY horarios_servicio_ibfk_1;
ALTER TABLE reservas DROP FOREIGN KEY reservas_ibfk_1;

-- Modificamos la columna id en servicios
ALTER TABLE servicios MODIFY COLUMN id INT AUTO_INCREMENT;

-- Modificamos la columna id en horarios_servicio
ALTER TABLE horarios_servicio MODIFY COLUMN id INT AUTO_INCREMENT;

-- Volvemos a crear las restricciones de clave foránea
ALTER TABLE horarios_servicio 
ADD CONSTRAINT horarios_servicio_ibfk_1 
FOREIGN KEY (servicio_id) REFERENCES servicios(id) 
ON DELETE CASCADE;

ALTER TABLE reservas
ADD CONSTRAINT reservas_ibfk_1
FOREIGN KEY (horario_id) REFERENCES horarios_servicio(id)
ON DELETE CASCADE; 