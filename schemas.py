from pydantic import BaseModel, validator, EmailStr
from typing import List, Optional
from datetime import datetime, date

class TaskBase(BaseModel):
    description: str
    completed: Optional[int] = 0
3
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    destination_id: int

    class Config:
        orm_mode = True

class DestinationBase(BaseModel):
    name: str
    country: str
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    days: Optional[int] = None

class DestinationCreate(DestinationBase):
    trip_id: int

class Destination(DestinationBase):
    id: int
    trip_id: int

    class Config:
        orm_mode = True

class TripBase(BaseModel):
    name: str
    total_days: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    name: Optional[str] = None
    total_days: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class Trip(TripBase):
    id: int
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    destinations: List[Destination] = []

    class Config:
        orm_mode = True

class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    days: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    trip_id: Optional[int] = None

# Esquemas para Usuario
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: str
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    name: str
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Actualizado de orm_mode a from_attributes para Pydantic V2

# Esquemas para Autenticación
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
