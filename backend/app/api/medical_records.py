# app/routers/medical_records.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import MedicalRecords as MedicalRecordModel
from app.schemas import MedicalRecord as MedicalRecordSchema, MedicalRecordCreate
from app.crud import create_medical_record, get_medical_records

router = APIRouter()

@router.post("/medical-records", response_model=MedicalRecordSchema)
def api_create_medical_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    return create_medical_record(db=db, record=record)

@router.get("/medical-records", response_model=List[MedicalRecordSchema])  # Adjust response model as needed
def api_get_medical_records(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retrieve medical records for a specific animal or all medical records if no animal_name is provided.
    """
    return get_medical_records(name=name, db=db)