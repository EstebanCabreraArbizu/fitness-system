from app import create_app, db
from app.models import Cliente, Discipline, Instructor, Product, ProductImage, Rutina, EjercicioRutina
import os
import pymysql

app = create_app()

def setup_database():
    """
    Configura la base de datos: primero la crea con MySQL raw y luego
    configura las tablas mediante SQLAlchemy para que Flask-Migrate
    pueda rastrear los cambios posteriormente.
    """
    # Crear la base de datos si no existe
    mysql_password = input("Ingresa tu contraseña de MySQL: ")
    
    # Conectar a MySQL para crear la base de datos
    connection = None
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=mysql_password
        )
        
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS personal_trainer_db2")
            cursor.execute("CREATE DATABASE personal_trainer_db2")
            print("Base de datos creada exitosamente.")
        
        connection.commit()
    except Exception as e:
        print(f"Error al crear base de datos: {str(e)}")
        return
    finally:
        if connection:
            connection.close()
    
    # Actualizar la configuración con la contraseña proporcionada
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{mysql_password}@localhost/personal_trainer_db2'
    
    # Crear las tablas con SQLAlchemy
    with app.app_context():
        try:
            db.create_all()
            print("Tablas creadas correctamente mediante SQLAlchemy.")
        except Exception as e:
            print(f"Error al crear tablas con SQLAlchemy: {str(e)}")

if __name__ == "__main__":
    setup_database() 