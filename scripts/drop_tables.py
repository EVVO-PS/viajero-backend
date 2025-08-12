import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine

def drop_tables():
    """CUIDADO: Esto eliminará todas las tablas"""
    response = input("⚠️  ¿Estás seguro de que quieres eliminar TODAS las tablas? (escribe 'SI' para confirmar): ")
    
    if response != "SI":
        print("Operación cancelada.")
        return
    
    try:
        print("Eliminando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Todas las tablas han sido eliminadas.")
        
    except Exception as e:
        print(f"❌ Error al eliminar tablas: {e}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()

if __name__ == "__main__":
    drop_tables()
