from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from app.models import RoleEnum
# -------------------------
# Animal Schemas
# -------------------------

class AnimalCreate(BaseModel):
    name: str
    dob: date
    gender: str  # Use "M" or "F"
    passive_adopter: Optional[str] = None
    breed_id: str

class AnimalResponse(AnimalCreate):  # Inherit from AnimalCreate
    animal_id: str  # Corrected to match the database model

    class Config:
        from_attributes = True
 
# -------------------------
# Get All details about an animal including reports and adopter
# -------------------------
class AdopterBase(BaseModel):
    adopter_id: str
    name: str
    contribution: float
class MedicalRecordBase(BaseModel):
    record_id: str  # animal_id should be str since it is CHAR(5)
    report: str
    doctor: str
    date: str  # Ensure date is a string in ISO format
    diagnosis: str
    medicine: str
    follow_up: str  # Should also be a string in ISO format
    freq_of_usage: int

class AnimalDetail(BaseModel):
    animal_id: str  # This should match the type in your Animal model
    name: str
    breed: str  # Ensure breed is a string
    passive_adopter: Optional[List[AdopterBase]]  # If it's a string, use Optional
    medical_records: List[MedicalRecordBase]  # List of medical record
        
# -------------------------
# Medical Record Schemas
# -------------------------

class MedicalRecordCreate(BaseModel):
    name: str
    report: Optional[str] = None
    doctor: str
    date: date
    diagnosis: str
    medicine: str
    follow_up: Optional[date] = None
    freq_of_usage: Optional[int] = None

class MedicalRecord(MedicalRecordCreate):
    class Config:
        from_attributes = True

class MedicalRecordResponse(BaseModel):
    record_id: str
    animal_id: str
    name: str
    report: str
    doctor: str
    date: date
    diagnosis: str
    medicine: str
    follow_up: date
    freq_of_usage: int

    class Config:
        from_attributes = True
# -------------------------
# Employee Schemas
# -------------------------

class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    date_of_joining: date
    role: RoleEnum

class Employee(EmployeeCreate):
    class Config:
        from_attributes = True
        
class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    date_of_joining: date
    role: RoleEnum
    class Config:
        from_attributes = True
