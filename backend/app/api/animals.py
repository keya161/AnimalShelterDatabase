from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animal as AnimalModel  # SQLAlchemy model
from app.schemas import Animal as AnimalSchema, AnimalCreate
from ..crud import create_animal
router = APIRouter()

@router.get("/animals", response_model=list[AnimalSchema])  # Use the Pydantic schema
def read_animals(db: Session = Depends(get_db)):
    return db.query(AnimalModel).all()

# @router.post("/animals", response_model=AnimalSchema)  # Specify the Pydantic response model
@router.post("/animals/", response_model=AnimalSchema)
def api_create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    return create_animal(db=db, animal=animal)



# def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
#     new_animal = AnimalModel(**animal.dict())
#     db.add(new_animal)
#     db.commit()
#     db.refresh(new_animal)
#     return new_animal
