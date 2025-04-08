from sqlalchemy.orm import Session
import models, schemas
from models import User
from datetime import datetime
import schemas
from passlib.context import CryptContext
from fastapi import HTTPException
from typing import List, Optional

# Configuración de encriptación para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funciones para usuarios
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, name=user.name, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        db.rollback()  # Revertir cambios en caso de error
        raise HTTPException(status_code=500, detail="Error al crear el usuario")
        
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Funciones para viajes
def create_trip(db: Session, trip: schemas.TripCreate, user_id: int):
    # Si no se proporciona fecha de inicio, usamos la fecha actual
    fecha_inicio = trip.fecha_inicio if trip.fecha_inicio else datetime.now()
    fecha_fin = trip.fecha_fin

    # Asegurarse de que las fechas sean objetos datetime
    if isinstance(fecha_inicio, str):
        try:
            fecha_inicio = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
        except ValueError:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                except ValueError:
                    fecha_inicio = datetime.now()

    if isinstance(fecha_fin, str):
        try:
            fecha_fin = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
        except ValueError:
            try:
                fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                try:
                    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
                except ValueError:
                    fecha_fin = None

    # Calcular total_days si no se proporciona pero sí las fechas
    total_days = trip.total_days
    if (total_days is None or total_days == 0) and fecha_inicio and fecha_fin:
        delta = fecha_fin - fecha_inicio
        total_days = delta.days + 1  # Incluimos el día de inicio y fin

    db_trip = models.Trip(
        name=trip.name, 
        total_days=total_days,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        user_id=user_id  # Añadimos el user_id aquí
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

def get_trip(db: Session, trip_id: int):
    return db.query(models.Trip).filter(models.Trip.id == trip_id).first()

def get_trips(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Trip).filter(models.Trip.user_id == user_id).offset(skip).limit(limit).all()

def update_trip(db: Session, trip_id: int, trip: schemas.TripUpdate, user_id: int):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id, models.Trip.user_id == user_id).first()
    if db_trip is None:
        return None
    
    update_data = trip.dict(exclude_unset=True)
    
    # Procesar fechas si están presentes
    if "fecha_inicio" in update_data:
        fecha_inicio = update_data["fecha_inicio"]
        if isinstance(fecha_inicio, str):
            try:
                fecha_inicio = datetime.fromisoformat(fecha_inicio.replace('Z', '+00:00'))
            except ValueError:
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                    except ValueError:
                        fecha_inicio = datetime.now()
        update_data["fecha_inicio"] = fecha_inicio
    
    if "fecha_fin" in update_data:
        fecha_fin = update_data["fecha_fin"]
        if isinstance(fecha_fin, str):
            try:
                fecha_fin = datetime.fromisoformat(fecha_fin.replace('Z', '+00:00'))
            except ValueError:
                try:
                    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M:%S.%f")
                except ValueError:
                    try:
                        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
                    except ValueError:
                        fecha_fin = None
        update_data["fecha_fin"] = fecha_fin
    
    # Calcular total_days si se actualizan las fechas
    if "fecha_inicio" in update_data and "fecha_fin" in update_data:
        fecha_inicio = update_data["fecha_inicio"]
        fecha_fin = update_data["fecha_fin"]
        if fecha_inicio and fecha_fin:
            delta = fecha_fin - fecha_inicio
            update_data["total_days"] = delta.days + 1  # Incluimos el día de inicio y fin
    
    for key, value in update_data.items():
        setattr(db_trip, key, value)
    
    db.commit()
    db.refresh(db_trip)
    return db_trip

def delete_trip(db: Session, trip_id: int, user_id: int):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id, models.Trip.user_id == user_id).first()
    if not trip:
        return None
    
    deleted_trip = schemas.Trip(
        id=trip.id,
        name=trip.name,
        total_days=trip.total_days,
        fecha_inicio=trip.fecha_inicio,  
        fecha_fin=trip.fecha_fin,
        user_id=trip.user_id,
        destinations=[]
    )
    
    db.delete(trip)
    db.commit()
    
    return deleted_trip

# Funciones para destinos
def create_destination(db: Session, destination: schemas.DestinationCreate):
    # Convertir el objeto Pydantic a un diccionario
    destination_data = destination.dict()
    
    # Crear una instancia del modelo SQLAlchemy
    db_destination = models.Destination(**destination_data)
    
    # Añadir a la sesión y commit
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    
    return db_destination

def get_destination(db: Session, destination_id: int):
    return db.query(models.Destination).filter(models.Destination.id == destination_id).first()

def get_destinations(db: Session, trip_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Destination).filter(models.Destination.trip_id == trip_id).offset(skip).limit(limit).all()

def update_destination(db: Session, destination_id: int, destination_update: schemas.DestinationUpdate):
    db_destination = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if db_destination:
        # Actualizar solo los campos que están presentes en la solicitud
        update_data = destination_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_destination, key, value)
        
        db.commit()
        db.refresh(db_destination)
    return db_destination

def delete_destination(db: Session, destination_id: int):
    # Buscar el destino por ID
    destination = db.query(models.Destination).filter(models.Destination.id == destination_id).first()
    if not destination:
        return None  # Si no se encuentra, devolver None

    # Eliminar el destino
    db.delete(destination)
    db.commit()
    return destination

# Función para verificar si un viaje pertenece a un usuario
def verify_trip_owner(db: Session, trip_id: int, user_id: int):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id, models.Trip.user_id == user_id).first()
    return trip is not None
