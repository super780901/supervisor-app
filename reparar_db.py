from app import app, db
from sqlalchemy import text

print("--- INICIANDO REPARACIÓN DE CONTROL ESCOLAR ---")

with app.app_context():
    # 1. BORRADO FORZOSO
    # Usamos SQL directo para que no le importe si el modelo coincide o no.
    # Simplemente destruye la tabla 'control_escolar'.
    try:
        print("1. Destruyendo tabla antigua 'control_escolar'...")
        db.session.execute(text('DROP TABLE IF EXISTS control_escolar'))
        db.session.commit()
        print("   -> Tabla eliminada correctamente.")
    except Exception as e:
        print(f"   -> Error al intentar borrar: {e}")

    # 2. RECREACIÓN
    # Ahora le pedimos a SQLAlchemy que cree todo lo que falte.
    # Como borramos control_escolar, la creará de nuevo basándose en tu app.py actual.
    print("2. Creando tabla nueva basada en tu código actual...")
    db.create_all()
    print("   -> ¡Base de datos regenerada!")
    print("--- PROCESO TERMINADO ---")