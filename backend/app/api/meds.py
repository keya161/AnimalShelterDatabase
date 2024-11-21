<<<<<<< HEAD
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from app.database import get_db
# from app import models, schemas
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from typing import List, Optional
>>>>>>> 58171ba902c014ed50b31226eddbc05a0bdfc09b

# router = APIRouter(prefix="/medicine_inventory", tags=["Medicine Inventory"])

<<<<<<< HEAD
# # Create a new medicine inventory item
# @router.post("/", response_model=schemas.MedicineInventoryInDB)
# def create_medicine_inventory_endpoint(
#     medicine_inventory: schemas.MedicineInventoryCreate, 
#     db: Session = Depends(get_db)
# ):
#     # Create a new MedicineInventory model instance
#     db_medicine_inventory = models.MedicineInventory(
#         name=medicine_inventory.name,
#         stock=medicine_inventory.stock,
#         expiry=medicine_inventory.expiry,
#         date_of_buying=medicine_inventory.date_of_buying
#     )
#     db.add(db_medicine_inventory)
#     db.commit()
#     db.refresh(db_medicine_inventory)
#     return db_medicine_inventory

# # Retrieve a specific medicine inventory item by ID
# @router.get("/{medicine_id}", response_model=schemas.MedicineInventoryInDB)
# def get_medicine_inventory_endpoint(medicine_id: str, db: Session = Depends(get_db)):
#     db_medicine_inventory = db.query(models.MedicineInventory).filter(
#         models.MedicineInventory.medicine_id == medicine_id
#     ).first()
#     if db_medicine_inventory is None:
#         raise HTTPException(status_code=404, detail="Medicine inventory not found")
#     return db_medicine_inventory

# # Retrieve all medicine inventory items with pagination
# @router.get("/", response_model=List[schemas.MedicineInventoryInDB])
# def get_medicine_inventories_endpoint(
#     skip: int = 0, 
#     limit: int = 100, 
#     db: Session = Depends(get_db)
# ):
#     return db.query(models.MedicineInventory).offset(skip).limit(limit).all()

# # Update an existing medicine inventory item
# @router.put("/{medicine_id}", response_model=schemas.MedicineInventoryInDB)
# def update_medicine_inventory_endpoint(
#     medicine_id: str, 
#     medicine_inventory: schemas.MedicineInventoryUpdate, 
#     db: Session = Depends(get_db)
# ):
#     db_medicine_inventory = db.query(models.MedicineInventory).filter(
#         models.MedicineInventory.medicine_id == medicine_id
#     ).first()
#     if db_medicine_inventory is None:
#         raise HTTPException(status_code=404, detail="Medicine inventory not found")
    
#     # Update fields
#     db_medicine_inventory.name = medicine_inventory.name
#     db_medicine_inventory.stock = medicine_inventory.stock
#     db_medicine_inventory.expiry = medicine_inventory.expiry
#     db_medicine_inventory.date_of_buying = medicine_inventory.date_of_buying
    
#     db.commit()
#     db.refresh(db_medicine_inventory)
#     return db_medicine_inventory

# # Delete a medicine inventory item
# @router.delete("/{medicine_id}", response_model=schemas.MedicineInventoryInDB)
# def delete_medicine_inventory_endpoint(medicine_id: str, db: Session = Depends(get_db)):
#     db_medicine_inventory = db.query(models.MedicineInventory).filter(
#         models.MedicineInventory.medicine_id == medicine_id
#     ).first()
#     if db_medicine_inventory is None:
#         raise HTTPException(status_code=404, detail="Medicine inventory not found")
    
#     db.delete(db_medicine_inventory)
#     db.commit()
#     return db_medicine_inventory
=======
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
>>>>>>> 58171ba902c014ed50b31226eddbc05a0bdfc09b
