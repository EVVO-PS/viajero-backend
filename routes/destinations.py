from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import get_db
from typing import List
from auth.token import get_current_user

router = APIRouter(
    prefix="/api",  # Mantenemos el prefijo /api
    tags=["destinations"],
    responses={404: {"description": "Destination not found"}}
)

DESTINATION_NOT_FOUND = "Destination not found"

@router.post("/trips/{trip_id}/destinations/", response_model=schemas.Destination)
def create_destination(
    trip_id: int, 
    destination: schemas.DestinationCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        print(f"Received destination data: {destination}")

        # Verificar que el viaje existe y pertenece al usuario actual
        trip = crud.get_trip(db, trip_id)
        if not trip or trip.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Trip not found")

        # Asociar el destino al viaje
        destination_dict = destination.dict()
        destination_dict["trip_id"] = trip_id
        
        # Crear un nuevo objeto DestinationCreate con trip_id incluido
        destination_with_trip = schemas.DestinationCreate(**destination_dict)
        
        return crud.create_destination(db, destination_with_trip)
    except Exception as e:
        import traceback
        print(f"Error creating destination: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Endpoint para obtener un destino por ID
@router.get("/destinations/{destination_id}", response_model=schemas.Destination)
def read_destination(
    destination_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    destination = crud.get_destination(db, destination_id)
    if destination is None:
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    
    # Verificar que el destino pertenece a un viaje del usuario actual
    trip = crud.get_trip(db, destination.trip_id)
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    
    return destination

# Endpoint para actualizar un destino
@router.put("/destinations/{destination_id}", response_model=schemas.Destination)
def update_destination(
    destination_id: int, 
    destination: schemas.DestinationUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        print(f"Updating destination {destination_id} with data: {destination}")
        
        # Verificar que el destino existe
        db_destination = crud.get_destination(db, destination_id)
        if db_destination is None:
            raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
        
        # Verificar que el destino pertenece a un viaje del usuario actual
        trip = crud.get_trip(db, db_destination.trip_id)
        if trip.user_id != current_user.id:
            raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
        
        updated_destination = crud.update_destination(db, destination_id, destination)
        return updated_destination
    except Exception as e:
        import traceback
        print(f"Error updating destination: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error updating destination: {str(e)}")

# Endpoint para eliminar un destino
@router.delete("/destinations/{destination_id}", response_model=schemas.Destination)
def delete_destination(
    destination_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verificar que el destino existe
    db_destination = crud.get_destination(db, destination_id)
    if db_destination is None:
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    
    # Verificar que el destino pertenece a un viaje del usuario actual
    trip = crud.get_trip(db, db_destination.trip_id)
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    
    deleted_destination = crud.delete_destination(db, destination_id)
    return deleted_destination

# Endpoint para obtener todos los destinos de un viaje
@router.get("/trips/{trip_id}/destinations/", response_model=List[schemas.Destination])
def read_destinations(
    trip_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verificar que el viaje existe y pertenece al usuario actual
    trip = crud.get_trip(db, trip_id)
    if not trip or trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    destinations = crud.get_destinations(db, trip_id, limit=limit)
    return destinations
