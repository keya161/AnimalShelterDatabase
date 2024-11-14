from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional

# from app.models import Type 
from app.schemas import BreedDropdownResponse
from app.crud import get_breeds_from_db
router = APIRouter(prefix="/breeds", tags=["Breed"])


@router.get("/breeds-dropdown", response_model=List[BreedDropdownResponse])
def get_breeds_dropdown(db: Session = Depends(get_db)):
    # Call the function to fetch breeds from the database
    return get_breeds_from_db(db)