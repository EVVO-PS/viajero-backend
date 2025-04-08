import os
from database import Base, engine

# Eliminar la base de datos si existe
if os.path.exists("viajero.db"):
    os.remove("viajero.db")
    print("Base de datos eliminada.")

# Crear las tablas
Base.metadata.create_all(bind=engine)
print("Base de datos recreada con éxito.")

