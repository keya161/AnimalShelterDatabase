from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animal

router = APIRouter()

@router.get("/animals")
def read_animals(db: Session = Depends(get_db)):
    return db.query(Animal).all()
