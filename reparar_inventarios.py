from app import app, db
from sqlalchemy import text

print("--- ACTUALIZANDO TABLA INVENTARIOS ---")

with app.app_context():
    # 1. Borramos la tabla vieja si existe
    try:
        db.session.execute(text('DROP TABLE IF EXISTS inventarios'))
        db.session.commit()
        print("Tabla anterior eliminada.")
    except Exception as e:
        print(f"Nota: {e}")

    # 2. Creamos la tabla nueva
    db.create_all()
    print("¡Tabla INVENTARIOS creada correctamente!")