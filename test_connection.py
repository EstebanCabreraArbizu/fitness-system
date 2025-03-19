from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.engine.connect()
        print("¡Conexión exitosa a la base de datos!")
    except Exception as e:
        print("Error al conectar a la base de datos:")
        print(e) 