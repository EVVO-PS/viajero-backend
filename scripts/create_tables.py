import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine
from models import *  

def create_tables():
    """Crear todas las tablas definidas en models.py"""
    try:
        print("Conectando a la base de datos Neon...")
        print(f"URL de conexión: {engine.url}")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        
        print("¡Tablas creadas exitosamente en Neon!")
        
        # Verificar qué tablas se crearon
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tablas creadas: {tables}")
        
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_tables()