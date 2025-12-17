from app import app, db
from sqlalchemy import text

print("--- CREANDO TABLA COOPERATIVA ---")
with app.app_context():
    try:
        db.session.execute(text('DROP TABLE IF EXISTS cooperativa'))
        db.session.commit()
    except:
        pass
    db.create_all()
    print("¡Tabla COOPERATIVA creada con éxito!")