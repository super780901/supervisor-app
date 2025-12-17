from app import app, db
from sqlalchemy import text

print("--- ACTUALIZANDO TABLA PIPCE ---")

with app.app_context():
    # 1. Borramos la tabla vieja si existe (para evitar conflictos)
    try:
        db.session.execute(text('DROP TABLE IF EXISTS pipce'))
        db.session.commit()
        print("Tabla anterior eliminada.")
    except Exception as e:
        print(f"Nota: {e}")

    # 2. Creamos la tabla nueva con las columnas ind_5_1... ind_5_11
    db.create_all()
    print("¡Tabla PIPCE creada correctamente con los 11 indicadores!")