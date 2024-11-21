from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AdopterCreate, AdopterUpdate, AdopterBase
from ..crud import create_adopter, get_all_adopters, get_adopter_by_id, update_adopter, delete_adopter

router = APIRouter(prefix="/adopters", tags=["Adopters"])

# Create a new adopter
@router.post("/", response_model=AdopterBase, status_code=status.HTTP_201_CREATED)
def create_adopter_endpoint(adopter_data: AdopterCreate, db: Session = Depends(get_db)):
    return create_adopter(db, adopter_data)

# Get all adopters
@router.get("/", response_model=list[AdopterBase])
def get_all_adopters_endpoint(db: Session = Depends(get_db)):
    return get_all_adopters(db)

# Get adopter by ID
@router.get("/{adopter_id}", response_model=AdopterBase)
def get_adopter_by_id_endpoint(adopter_id: str, db: Session = Depends(get_db)):
    adopter = get_adopter_by_id(db, adopter_id)
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter not found")
    return adopter

# Update adopter
@router.put("/{adopter_id}", response_model=AdopterBase)
def update_adopter_endpoint(adopter_id: str, update_data: AdopterUpdate, db: Session = Depends(get_db)):
    adopter = update_adopter(db, adopter_id, update_data)
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter not found")
    return adopter

# Delete adopter
@router.delete("/{adopter_id}", response_model=AdopterBase)
def delete_adopter_endpoint(adopter_id: str, db: Session = Depends(get_db)):
    adopter = delete_adopter(db, adopter_id)
    if not adopter:
        raise HTTPException(status_code=404, detail="Adopter not found")
    return adopter
