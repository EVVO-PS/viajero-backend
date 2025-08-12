import sys
import os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine

def test_connection():
    """Probar la conexión a la base de datos Neon"""
    try:
        print("Probando conexión a Neon...")
        print(f"URL de conexión: {engine.url}")
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"Versión: {version}")
            
            # Probar si hay tablas existentes
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = result.fetchall()
            
            if tables:
                print(f"Tablas existentes: {[table[0] for table in tables]}")
            else:
                print("No hay tablas en la base de datos.")
        
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection()