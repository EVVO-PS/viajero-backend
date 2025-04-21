import os
from database import Base, engine

# Eliminar la base de datos si existe
DB_PATH = os.getenv("DB_PATH", "viajero.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Base de datos {DB_PATH} eliminada con éxito.")

# Crear las tablas
Base.metadata.create_all(bind=engine)
print("Base de datos recreada con éxito.")

