import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

# Cargar variables de entorno (útil para desarrollo local)
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
# Si no existe, usar la URL local como fallback para desarrollo
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://neondb_owner:npg_yh1BSzLewK4T@ep-withered-recipe-ac4iedor-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require")

# Para PostgreSQL en Render, es posible que necesites modificar la URL si usa el prefijo postgres://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Configurar la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()