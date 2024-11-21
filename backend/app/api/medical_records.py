# app/routers/medical_records.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import MedicalRecords as MedicalRecordModel
from app.schemas import MedicalRecordCreate, MedicalRecordResponse
from app.crud import create_medical_record, get_medical_records

router = APIRouter(prefix="/medical-records", tags=["Medical Records"])

@router.post("/create", response_model=MedicalRecordResponse)
def api_create_medical_record(record: MedicalRecordCreate, db: Session = Depends(get_db)):
    return create_medical_record(db=db, record=record)

@router.get("/medical-records", response_model=List[MedicalRecordResponse])
def api_get_medical_records(animal_id: Optional[str] = None, db: Session = Depends(get_db)):
    return get_medical_records(db=db, animal_id=animal_id)