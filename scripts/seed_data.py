import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa tus modelos
from models import User, Trip, Destination  # Ajusta según tus modelos

DATABASE_URL = "postgres://neondb_owner:npg_yh1BSzLewK4T@ep-withered-recipe-ac4iedor-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    """Insertar datos de prueba"""
    db = SessionLocal()
    try:
        print("Insertando datos de prueba...")
        
        # Verificar si ya existen datos
        existing_user = db.query(User).filter(User.email == "test@viajero.com").first()
        if existing_user:
            print("Los datos de prueba ya existen.")
            return
        
        # Crear usuario de prueba
        test_user = User(
            email="test@viajero.com",
            name="Usuario de Prueba",
            # Asegúrate de hashear la contraseña según tu implementación
            hashed_password="$2b$12$ejemplo_hash"  
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"Usuario creado con ID: {test_user.id}")
        
        # Crear viaje de prueba
        test_trip = Trip(
            title="Viaje de Prueba",
            description="Un viaje de ejemplo",
            user_id=test_user.id
        )
        
        db.add(test_trip)
        db.commit()
        
        print("¡Datos de prueba insertados exitosamente!")
        
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
