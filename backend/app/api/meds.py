from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from typing import List, Optional

router = APIRouter(prefix="/medicine_inventory", tags=["Medicine Inventory"])

@router.post("/", response_model=schemas.MedicineInventoryInDB)
def create_medicine_inventory_endpoint(medicine_inventory: schemas.MedicineInventoryCreate, db: Session = Depends(get_db)):
    return crud.create_medicine_inventory(db=db, medicine_inventory=medicine_inventory)

@router.get("/{medicine_id}", response_model=schemas.MedicineInventoryInDB)
def get_medicine_inventory_endpoint(medicine_id: str, db: Session = Depends(get_db)):
    db_medicine_inventory = crud.get_medicine_inventory(db=db, medicine_id=medicine_id)
    if db_medicine_inventory is None:
        raise HTTPException(status_code=404, detail="Medicine inventory not found")
    return db_medicine_inventory

@router.get("/", response_model=List[schemas.MedicineInventoryInDB])
def get_medicine_inventories_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_medicine_inventories = crud.get_medicine_inventories(db=db, skip=skip, limit=limit)
    return db_medicine_inventories

@router.put("/{medicine_id}", response_model=schemas.MedicineInventoryInDB)
def update_medicine_inventory_endpoint(medicine_id: str, medicine_inventory: schemas.MedicineInventoryUpdate, db: Session = Depends(get_db)):
    db_medicine_inventory = crud.update_medicine_inventory(db=db, medicine_id=medicine_id, medicine_inventory=medicine_inventory)
    if db_medicine_inventory is None:
        raise HTTPException(status_code=404, detail="Medicine inventory not found")
    return db_medicine_inventory

@router.delete("/{medicine_id}", response_model=schemas.MedicineInventoryInDB)
def delete_medicine_inventory_endpoint(medicine_id: str, db: Session = Depends(get_db)):
    db_medicine_inventory = crud.delete_medicine_inventory(db=db, medicine_id=medicine_id)
    if db_medicine_inventory is None:
        raise HTTPException(status_code=404, detail="Medicine inventory not found")
    return db_medicine_inventory
