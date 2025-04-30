from flask import current_app
from app.db import get_db
import datetime

class Servicio:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, duracion=None, 
                 categoria=None, modalidad=None, nivel=None, imagen=None, 
                 instructor_id=None, estado=None, fecha_creacion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.duracion = duracion  # duracion en minutos
        self.categoria = categoria  # tipo de servicio: entrenamiento, nutrición, etc.
        self.modalidad = modalidad  # presencial, virtual, etc.
        self.nivel = nivel  # principiante, intermedio, avanzado
        self.imagen = imagen
        self.instructor_id = instructor_id
        self.estado = estado  # activo, inactivo
        self.fecha_creacion = fecha_creacion
        self.horarios = []  # lista de horarios disponibles
    
    @staticmethod
    def crear_tablas_si_no_existen():
        """Crea las tablas necesarias si no existen"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Tabla de servicios
            cursor.execute("""
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
            """)
            
            # Tabla de horarios de servicios
            cursor.execute("""
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
            """)
            
            # Tabla de reservas de servicios
            cursor.execute("""
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
            """)
            
            conn.commit()
            current_app.logger.info("Tablas de servicios creadas o verificadas correctamente")
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al crear tablas de servicios: {str(e)}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def obtener_todos_por_instructor(instructor_id):
        """Obtiene todos los servicios de un instructor"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT s.*, 
                       u.nombres as instructor_nombre, 
                       u.apellidos as instructor_apellido,
                       COUNT(DISTINCT sh.id) as total_horarios,
                       COUNT(DISTINCT sr.id) as total_reservas
                FROM Servicio s
                JOIN Usuario u ON s.instructor_id = u.id
                LEFT JOIN Servicio_Horario sh ON s.id = sh.servicio_id
                LEFT JOIN Servicio_Reserva sr ON sh.id = sr.horario_id
                WHERE s.instructor_id = %s
                GROUP BY s.id
                ORDER BY s.fecha_creacion DESC
            """, (instructor_id,))
            
            servicios = cursor.fetchall()
            return servicios
        except Exception as e:
            current_app.logger.error(f"Error al obtener servicios del instructor: {str(e)}")
            return []
        finally:
            cursor.close()
    
    @staticmethod
    def obtener_por_id(servicio_id, instructor_id=None):
        """Obtiene un servicio por su ID, con opción de verificar el instructor"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            current_app.logger.debug(f"Obteniendo servicio con ID: {servicio_id}")
            
            if instructor_id:
                cursor.execute("""
                    SELECT * FROM Servicio 
                    WHERE id = %s AND instructor_id = %s
                """, (servicio_id, instructor_id))
            else:
                cursor.execute("SELECT * FROM Servicio WHERE id = %s", (servicio_id,))
                
            servicio = cursor.fetchone()
            
            if servicio:
                # Obtener horarios del servicio
                cursor.execute("""
                    SELECT sh.id, sh.servicio_id, sh.dia_semana, sh.hora_inicio, sh.hora_fin, 
                           sh.cupos_disponibles, sh.estado
                    FROM Servicio_Horario sh
                    WHERE sh.servicio_id = %s AND sh.estado = 'activo'
                    ORDER BY CASE
                        WHEN sh.dia_semana = 'lunes' THEN 1
                        WHEN sh.dia_semana = 'martes' THEN 2
                        WHEN sh.dia_semana = 'miércoles' THEN 3
                        WHEN sh.dia_semana = 'jueves' THEN 4
                        WHEN sh.dia_semana = 'viernes' THEN 5
                        WHEN sh.dia_semana = 'sábado' THEN 6
                        WHEN sh.dia_semana = 'domingo' THEN 7
                    END, sh.hora_inicio
                """, (servicio_id,))
                
                horarios = cursor.fetchall()
                servicio['horarios'] = horarios
                
                current_app.logger.debug(f"Servicio {servicio_id} tiene {len(horarios)} horarios")
            
            return servicio
        except Exception as e:
            current_app.logger.error(f"Error al obtener servicio: {str(e)}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def crear(servicio_data, horarios_data=None):
        """Crea un nuevo servicio con sus horarios"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Insertar servicio
            cursor.execute("""
                INSERT INTO Servicio (
                    nombre, descripcion, precio, duracion, categoria, 
                    modalidad, nivel, imagen, instructor_id, estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                servicio_data.get('nombre'),
                servicio_data.get('descripcion'),
                servicio_data.get('precio'),
                servicio_data.get('duracion', 60),  # Por defecto 60 minutos
                servicio_data.get('categoria'),
                servicio_data.get('modalidad'),
                servicio_data.get('nivel'),
                servicio_data.get('imagen', 'default-service.png'),
                servicio_data.get('instructor_id'),
                servicio_data.get('estado', 'activo')
            ))
            
            servicio_id = cursor.lastrowid
            
            # Insertar horarios si existen
            if horarios_data:
                for horario in horarios_data:
                    cursor.execute("""
                        INSERT INTO Servicio_Horario (
                            servicio_id, dia_semana, hora_inicio, hora_fin, cupos_disponibles
                        ) VALUES (%s, %s, %s, %s, %s)
                    """, (
                        servicio_id,
                        horario.get('dia_semana'),
                        horario.get('hora_inicio'),
                        horario.get('hora_fin'),
                        horario.get('cupos_disponibles', 1)
                    ))
            
            conn.commit()
            return servicio_id
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al crear servicio: {str(e)}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def actualizar(servicio_id, servicio_data, instructor_id=None):
        """Actualiza un servicio existente"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Verificar que el servicio exista y pertenezca al instructor
            if instructor_id:
                cursor.execute("""
                    SELECT id FROM Servicio 
                    WHERE id = %s AND instructor_id = %s
                """, (servicio_id, instructor_id))
                
                if not cursor.fetchone():
                    return False
            
            # Actualizar servicio
            cursor.execute("""
                UPDATE Servicio SET
                    nombre = %s,
                    descripcion = %s,
                    precio = %s,
                    duracion = %s,
                    categoria = %s,
                    modalidad = %s,
                    nivel = %s,
                    estado = %s
                WHERE id = %s
            """, (
                servicio_data.get('nombre'),
                servicio_data.get('descripcion'),
                servicio_data.get('precio'),
                servicio_data.get('duracion'),
                servicio_data.get('categoria'),
                servicio_data.get('modalidad'),
                servicio_data.get('nivel'),
                servicio_data.get('estado'),
                servicio_id
            ))
            
            # Actualizar imagen si se proporciona
            if 'imagen' in servicio_data and servicio_data['imagen']:
                cursor.execute("""
                    UPDATE Servicio SET imagen = %s WHERE id = %s
                """, (servicio_data['imagen'], servicio_id))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al actualizar servicio: {str(e)}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def eliminar(servicio_id, instructor_id=None):
        """Elimina un servicio y sus horarios"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Verificar que el servicio exista y pertenezca al instructor
            if instructor_id:
                cursor.execute("""
                    SELECT id FROM Servicio 
                    WHERE id = %s AND instructor_id = %s
                """, (servicio_id, instructor_id))
                
                if not cursor.fetchone():
                    return False
            
            # Eliminar el servicio (las tablas con FK ON DELETE CASCADE eliminarán los horarios y reservas)
            cursor.execute("DELETE FROM Servicio WHERE id = %s", (servicio_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al eliminar servicio: {str(e)}")
            return False
        finally:
            cursor.close()
    
    # Métodos para gestionar horarios
    @staticmethod
    def agregar_horario(servicio_id, horario_data, instructor_id=None):
        """Agrega un nuevo horario a un servicio"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Verificar que el servicio exista y pertenezca al instructor
            if instructor_id:
                cursor.execute("""
                    SELECT id FROM Servicio 
                    WHERE id = %s AND instructor_id = %s
                """, (servicio_id, instructor_id))
                
                if not cursor.fetchone():
                    return False
            
            # Verificar que la hora de fin sea posterior a la hora de inicio
            hora_inicio = datetime.datetime.strptime(horario_data.get('hora_inicio'), '%H:%M').time()
            hora_fin = datetime.datetime.strptime(horario_data.get('hora_fin'), '%H:%M').time()
            
            if hora_fin <= hora_inicio:
                return False
            
            # Verificar que la duración no exceda 1 hora
            inicio_dt = datetime.datetime.combine(datetime.date.today(), hora_inicio)
            fin_dt = datetime.datetime.combine(datetime.date.today(), hora_fin)
            duracion_minutos = (fin_dt - inicio_dt).total_seconds() / 60
            
            if duracion_minutos > 60:
                return False
            
            # Insertar horario
            cursor.execute("""
                INSERT INTO Servicio_Horario (
                    servicio_id, dia_semana, hora_inicio, hora_fin, cupos_disponibles
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                servicio_id,
                horario_data.get('dia_semana'),
                horario_data.get('hora_inicio'),
                horario_data.get('hora_fin'),
                horario_data.get('cupos_disponibles', 1)
            ))
            
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al agregar horario: {str(e)}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def eliminar_horario(horario_id, instructor_id=None):
        """Elimina un horario de un servicio"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Verificar que el horario pertenezca a un servicio del instructor
            if instructor_id:
                cursor.execute("""
                    SELECT sh.id
                    FROM Servicio_Horario sh
                    JOIN Servicio s ON sh.servicio_id = s.id
                    WHERE sh.id = %s AND s.instructor_id = %s
                """, (horario_id, instructor_id))
                
                if not cursor.fetchone():
                    return False
            
            # Eliminar horario
            cursor.execute("DELETE FROM Servicio_Horario WHERE id = %s", (horario_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al eliminar horario: {str(e)}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def obtener_horarios_por_servicio(servicio_id):
        """Obtiene todos los horarios de un servicio"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM Servicio_Horario
                WHERE servicio_id = %s AND estado = 'activo'
                ORDER BY CASE
                    WHEN dia_semana = 'lunes' THEN 1
                    WHEN dia_semana = 'martes' THEN 2
                    WHEN dia_semana = 'miércoles' THEN 3
                    WHEN dia_semana = 'jueves' THEN 4
                    WHEN dia_semana = 'viernes' THEN 5
                    WHEN dia_semana = 'sábado' THEN 6
                    WHEN dia_semana = 'domingo' THEN 7
                END, hora_inicio
            """, (servicio_id,))
            
            horarios = cursor.fetchall()
            return horarios
        except Exception as e:
            current_app.logger.error(f"Error al obtener horarios: {str(e)}")
            return []
        finally:
            cursor.close() 