from app import app, db, ControlEscolar

print("--- Iniciando actualización de la tabla Control Escolar ---")

with app.app_context():
    try:
        # 1. Intentamos borrar la tabla vieja (por si tiene menos columnas)
        ControlEscolar.__table__.drop(db.engine)
        print("Tabla 'ControlEscolar' anterior eliminada correctamente.")
    except:
        print("La tabla no existía o ya estaba borrada. Continuando...")

    # 2. Creamos la nueva tabla con la estructura actualizada (11 indicadores)
    db.create_all()
    print("¡Tabla 'ControlEscolar' creada con éxito!")