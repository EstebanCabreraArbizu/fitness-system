import os
import click
from flask.cli import with_appcontext
from app import create_app, db
from app.models import Cliente, Discipline, Instructor, Product, ProductImage, Rutina, EjercicioRutina
from flask_migrate import Migrate, init, migrate, upgrade

app = create_app()

# Configurar opciones correctas para la migración
with app.app_context():
    migrate_instance = Migrate(app, db)
    
    # Configurar Alembic para ignorar tablas del sistema
    @migrate_instance.configure
    def configure_alembic(config):
        # Incluir solo las tablas que nos interesan
        config.include_schemas = False
        config.include_object = lambda obj, name, type_, reflected, compare_to: (
            # Solo incluir nuestras tablas de modelos
            type_ == "table" and 
            name in db.metadata.tables and
            # Excluir esquemas del sistema
            not name.startswith(('mysql.', 'information_schema.', 'performance_schema.', 'sys.'))
        )
        return config

@click.command('reset-migrate')
@click.option('--force', is_flag=True, help='Forzar la recreación de las migraciones')
def reset_migration():
    """Restablece el sistema de migraciones y crea una nueva migración limpia."""
    import shutil
    
    # Eliminar carpeta migrations si existe y el usuario fuerza
    if os.path.exists('migrations') and click.confirm('¿Eliminar carpeta de migraciones existente?'):
        shutil.rmtree('migrations')
        click.echo('Carpeta de migraciones eliminada.')
    
    # Inicializar migraciones
    with app.app_context():
        init()
        click.echo('Sistema de migraciones inicializado.')
        
        # Crear migración inicial
        migrate(message='tablas_iniciales')
        click.echo('Migración inicial creada.')

@click.command('migrate-init')
def migrate_init():
    """Crea una nueva migración sin modificar la estructura existente."""
    with app.app_context():
        try:
            migrate(message='tablas_iniciales')
            click.echo('Migración creada exitosamente.')
        except Exception as e:
            click.echo(f'Error al crear migración: {str(e)}')

@click.command('apply-migration')
def apply_migration():
    """Aplica las migraciones pendientes."""
    with app.app_context():
        try:
            upgrade()
            click.echo('Migraciones aplicadas correctamente.')
        except Exception as e:
            click.echo(f'Error al aplicar migraciones: {str(e)}')
            click.echo('Detalles del error:')
            import traceback
            click.echo(traceback.format_exc())

@click.command('create-tables')
def create_tables():
    """Crea todas las tablas directamente con SQLAlchemy sin usar migraciones."""
    with app.app_context():
        try:
            db.create_all()
            click.echo('Tablas creadas exitosamente.')
        except Exception as e:
            click.echo(f'Error al crear tablas: {str(e)}')

# Registrar los comandos con la aplicación
app.cli.add_command(reset_migration)
app.cli.add_command(migrate_init)
app.cli.add_command(apply_migration)
app.cli.add_command(create_tables)

if __name__ == '__main__':
    print("===== Sistema de Migración de Base de Datos =====")
    print("Seleccione una opción:")
    print("1. Reiniciar sistema de migraciones")
    print("2. Crear nueva migración")
    print("3. Aplicar migraciones pendientes")
    print("4. Crear tablas directamente (sin migraciones)")
    
    opcion = input("Opción: ")
    
    if opcion == '1':
        reset_migration()
    elif opcion == '2':
        migrate_init()
    elif opcion == '3':
        apply_migration()
    elif opcion == '4':
        create_tables()
    else:
        print("Opción no válida") 