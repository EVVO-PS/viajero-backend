from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import get_db
from typing import List
from auth.token import get_current_user

router = APIRouter(
    prefix="/api/trips",
    tags=["trips"],
    responses={404: {"description": "Trip not found"}}
)

@router.post("/", response_model=schemas.Trip)
def create_trip(
    trip: schemas.TripCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_trip(db, trip, current_user.id)

@router.get("/", response_model=List[schemas.Trip])
def read_trips(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    trips = crud.get_trips(db, current_user.id)
    return trips

@router.get("/{trip_id}", response_model=schemas.Trip)
def read_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    trip = crud.get_trip(db, trip_id)
    if trip is None or trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.put("/{trip_id}", response_model=schemas.Trip)
def update_trip(
    trip_id: int, 
    trip: schemas.TripUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_trip = crud.update_trip(db, trip_id, trip, current_user.id)
    if updated_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return updated_trip

@router.delete("/{trip_id}", response_model=schemas.Trip)
def delete_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted_trip = crud.delete_trip(db, trip_id, current_user.id)
    if deleted_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return deleted_trip
