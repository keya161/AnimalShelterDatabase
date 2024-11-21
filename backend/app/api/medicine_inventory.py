from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import MedicalRecords as MedicalRecordModel
from app.schemas import MedicineInventoryCreate, MedicineInventoryUpdate
from app.crud import create_medicine, update_medicine_stock, delete_medicine, get_medicine

router = APIRouter(
    prefix="/medicines",  # This is the base path for the medicine routes
    tags=["Medicines"],  # This will group the routes under "Medicines" in the docs
)



# Endpoint to create a new medicine
@router.post("/", response_model=MedicineInventoryCreate)
def create_medicine_endpoint(medicine: MedicineInventoryCreate, db: Session = Depends(get_db)):
    return create_medicine(db=db, medicine=medicine)

# Endpoint to get a medicine by medicine_id
@router.get("/{medicine_id}", response_model=MedicineInventoryCreate)
def get_medicine_endpoint(medicine_id: str, db: Session = Depends(get_db)):
    medicine = get_medicine(db=db, medicine_id=medicine_id)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

# Endpoint to update the stock of a medicine
@router.put("/{medicine_id}", response_model=MedicineInventoryCreate)
def update_medicine_stock_endpoint(medicine_id: str, stock: int, db: Session = Depends(get_db)):
    medicine = update_medicine_stock(db=db, medicine_id=medicine_id, new_stock=stock)
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

# Endpoint to delete a medicine
@router.delete("/{medicine_id}")
def delete_medicine_endpoint(medicine_id: str, db: Session = Depends(get_db)):
    result = delete_medicine(db=db, medicine_id=medicine_id)
    if not result:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"message": "Medicine deleted successfully"}