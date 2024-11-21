from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animal, Type  # SQLAlchemy model
from fastapi import APIRouter, Depends
from sqlalchemy import func
router = APIRouter(prefix="/type_count", tags=["Type Count"])

@router.get("/")
def get_animals_by_breed(db: Session = Depends(get_db)):
    # Aggregate query to get the number of animals by breed (type)
    result = db.query(Type.breed, func.count(Animal.animal_id).label("animal_count")) \
               .join(Animal, Animal.breed_id == Type.type_id) \
               .group_by(Type.breed).all()
    
    # Return the result as a JSON list
    return [{"breed": row.breed, "animal_count": row.animal_count} for row in result]