from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/animals", tags=["Animals"])

@router.post("/", response_model=schemas.AnimalResponse)
def create_animal_endpoint(animal_data: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.create_animal(db, animal_data)

@router.get("/{animal_id}", response_model=schemas.AnimalResponse)
def get_animal_endpoint(animal_id: str, db: Session = Depends(get_db)):
    return crud.get_animal(db, animal_id)

@router.put("/{animal_id}", response_model=schemas.AnimalResponse)
def update_animal_endpoint(animal_id: str, animal_data: schemas.AnimalUpdate, db: Session = Depends(get_db)):
    return crud.update_animal(db, animal_id, animal_data)

@router.delete("/{animal_id}")
def delete_animal_endpoint(animal_id: str, db: Session = Depends(get_db)):
    return crud.delete_animal(db, animal_id)
