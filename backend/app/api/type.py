from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List, Optional

# from app.models import Type 
from app.schemas import TypeUpdate, TypeCreate, TypeResponse, BreedDropdownResponse
from app.crud import create_type, update_type, delete_type, get_type, get_breeds_from_db
router = APIRouter(prefix="/types", tags=["Types"])

@router.post("/", response_model=TypeResponse)
def create_type_endpoint(type_data: TypeCreate, db: Session = Depends(get_db)):
    return create_type(db, type_data)

@router.get("/{type_id}", response_model=TypeResponse)
def get_type_endpoint(type_id: str, db: Session = Depends(get_db)):
    return get_type(db, type_id)

@router.put("/{type_id}", response_model=TypeResponse)
def update_type_endpoint(type_id: str, type_data: TypeUpdate, db: Session = Depends(get_db)):
    return update_type(db, type_id, type_data)

@router.delete("/{type_id}")
def delete_type_endpoint(type_id: str, db: Session = Depends(get_db)):
    return delete_type(db, type_id)
