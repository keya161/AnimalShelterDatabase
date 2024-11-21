from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from typing import List, Optional


router = APIRouter(prefix="/food_inventory", tags=["Food Inventory"])

@router.post("/", response_model=schemas.FoodInventoryInDB)
def create_food_inventory_endpoint(food_inventory: schemas.FoodInventoryCreate, db: Session = Depends(get_db)):
    return crud.create_food_inventory(db=db, food_inventory=food_inventory)

@router.get("/{food_id}", response_model=schemas.FoodInventoryInDB)
def get_food_inventory_endpoint(food_id: str, db: Session = Depends(get_db)):
    db_food_inventory = crud.get_food_inventory(db=db, food_id=food_id)
    if db_food_inventory is None:
        raise HTTPException(status_code=404, detail="Food inventory not found")
    return db_food_inventory

@router.get("/", response_model=List[schemas.FoodInventoryInDB])
def get_food_inventories_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_food_inventories = crud.get_food_inventories(db=db, skip=skip, limit=limit)
    return db_food_inventories

@router.put("/{food_id}", response_model=schemas.FoodInventoryInDB)
def update_food_inventory(food_id: int, food_inventory: schemas.FoodInventoryUpdate, db: Session = Depends(get_db)):
    # If stock is provided, only update stock, otherwise leave other fields unchanged
    if food_inventory.stock is None:
        raise HTTPException(status_code=400, detail="Stock must be provided to update.")

    updated_inventory = crud.update_food_inventory(db, food_id, food_inventory.stock)
    
    # Check if the record was deleted due to the trigger
    if not updated_inventory:
        raise HTTPException(status_code=404, detail="Food inventory item not found or deleted.")

    return updated_inventory

@router.delete("/{food_id}", response_model=schemas.FoodInventoryInDB)
def delete_food_inventory_endpoint(food_id: str, db: Session = Depends(get_db)):
    db_food_inventory = crud.delete_food_inventory(db=db, food_id=food_id)
    if db_food_inventory is None:
        raise HTTPException(status_code=404, detail="Food inventory not found")
    return db_food_inventory
