from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes import auth, users
from routes import destinations
from routes import trips
import os

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Viajero API")

origins = [
    "https://viajero-backend.onrender.com",  # Reemplaza con tu dominio de Netlify
    "http://localhost:4200"  # Opcional, para desarrollo local
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(destinations.router)
app.include_router(trips.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Viajero"}

