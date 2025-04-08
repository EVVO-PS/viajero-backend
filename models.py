from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from database import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_days = Column(Integer)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)

    # Clave foránea hacia User
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relaciones
    user = relationship("User", back_populates="trips")
    destinations = relationship("Destination", back_populates="trip", cascade="all, delete-orphan")  # Añadido esta línea

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    days = Column(Integer)
    fecha_inicio = Column(DateTime)  # Agregado
    fecha_fin = Column(DateTime)  # Agregado
    trip_id = Column(Integer, ForeignKey("trips.id"))

    trip = relationship("Trip", back_populates="destinations")
    tasks = relationship("Task", back_populates="destination", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    completed = Column(Integer, default=0)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    
    # Relación con el destino
    destination = relationship("Destination", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con viajes
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
