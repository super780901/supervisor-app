from app import app, db
from sqlalchemy import text

print("--- CREANDO TABLA CTE ---")
with app.app_context():
    try:
        db.session.execute(text('DROP TABLE IF EXISTS cte'))
        db.session.commit()
    except:
        pass
    db.create_all()
    print("¡Tabla CTE creada con éxito!")