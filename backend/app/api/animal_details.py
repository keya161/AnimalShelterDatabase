from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animal as AnimalModel  # SQLAlchemy model
from app.schemas import AnimalResponse as AnimalSchema, AnimalCreate, AnimalDetail
from ..crud import create_animal, get_animal_by_name
from fastapi import HTTPException
router = APIRouter()

@router.get("/animaldetails/{name}", response_model=AnimalDetail)
def api_get_animal_details(name:str, db: Session = Depends(get_db)):
    return get_animal_by_name(name=name, db=db)